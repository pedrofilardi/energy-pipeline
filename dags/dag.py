from datetime import datetime
from airflow import DAG

from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.python import PythonOperator

import pandas as pd
from entsoe import EntsoePandasClient
import configparser

parser = configparser.ConfigParser()
parser.read("./auth.cfg")

API_KEY = parser.get("entso", "api_key")
COUNTRY_CODES = ["ES", "FR", "DE"]

SOURCES_ID = {
    'Biomass': 1,
    'Fossil Brown coal/Lignite': 2,
    'Fossil Coal-derived gas': 3,
    'Fossil Gas': 4,
    'Fossil Hard coal': 5,
    'Fossil Oil': 6,
    'Fossil Oil shale': 7,
    'Fossil Peat': 8,
    'Geothermal': 9,
    'Hydro Pumped Storage': 10,
    'Hydro Run-of-river and poundage': 11,
    'Hydro Water Reservoir': 12,
    'Marine': 13,
    'Nuclear': 14,
    'Other': 15,
    'Other renewable': 16,
    'Solar': 17,
    'Waste': 18,
    'Wind Onshore': 19,
    'Wind Offshore': 20
}

dag = DAG(
    dag_id="energy", start_date=datetime(2019, 1, 1), schedule_interval=None
)

# utils


def timestamp_to_str(timestamp):
    return timestamp.strftime("%Y%m%d")

# dag_functions


def _retrieve_metadata(country: str, ti) -> None:

    sql = f'''SELECT timestamp, country.id, country.utc from logs_incremental
            JOIN dimensioncountry country ON
            logs_incremental.country_id = country.id
            WHERE last = 1 and country.ISO2 = '{country}';'''

    postgres_hook = PostgresHook(
        postgres_conn_id="postgres_conn", schema="postgres")
    conn = postgres_hook.get_conn()
    cursor = conn.cursor()
    cursor.execute(sql)
    query = cursor.fetchall()

    last_date = '20150101'
    if query:
        last_date = query[0][0]

    ti.xcom_push(key=country, value={"last_date": last_date,
                                     "country_id": query[0][1],
                                     "country_timezone": query[0][2]})


def _download_data(country: str, ti) -> None:

    metadata = ti.xcom_pull(
        key=country, task_ids=f"retrieve_metadata_{country}")
    last_date, tz = metadata["last_date"], metadata["country_timezone"]

    client = EntsoePandasClient(api_key=API_KEY)

    start = pd.Timestamp(last_date, tz=tz)
    end = pd.Timestamp.now(tz=tz)

    df = client.query_generation(country, start=start, end=end)
    df.to_csv(f"./data/raw/df_{country}.csv")


def _transform_data(country: str, ti) -> None:
    df = pd.read_csv(
        f"./data/raw/df_{country}.csv", index_col=0, header=[0, 1])
    df.index = pd.to_datetime(df.index)

    if isinstance(df.columns, pd.MultiIndex):
        if "Actual Consumption" in df.columns.get_level_values(1):
            new_columns = [x[0]
                           for x in df.columns if x[1] == 'Actual Aggregated']
            # eliminamos columna de sources
            df.columns = df.columns.droplevel(0)
            df = df.loc[:, df.columns.isin(['Actual Aggregated'])]
            df.columns = new_columns

    interval = (pd.Series(df.tail(2).index).diff(
    ).dt.total_seconds()/60).values[1]

    if interval == 30:
        # eliminar las entradas incompletas.
        while df.tail(1).index.minute != 30:
            df.drop(df.tail(1).index, inplace=True)

    if interval == 15:
        # eliminar las entradas incompletas.
        while df.tail(1).index.minute != 45:
            df.drop(df.tail(1).index, inplace=True)

    df = df.groupby(pd.Grouper(freq='H', level=0, closed='left')).mean()
    # con closed left toma las filas desde 8:00 hasta las 8:45. Con right desde 8:15 A 9

    df = df.groupby(pd.Grouper(freq='D', level=0)).sum()

    df["date_str"] = df.index.map(lambda x: timestamp_to_str(x))
    df.to_csv(f"./data/curated/df_{country}.csv")

    ti.xcom_push(key=country, value=df.tail(1)["date_str"].values[0])


def _load_data(country: str, ti):

    df = pd.read_csv(
        f"./data/curated/df_{country}.csv", index_col=0, dtype={"date_str": str})
    df.index = pd.to_datetime(df.index)

    # load dates dimension
    postgres_hook = PostgresHook(
        postgres_conn_id="postgres_conn", schema="postgres")
    conn = postgres_hook.get_conn()
    cursor = conn.cursor()
    cursor.execute(
        f'''SELECT id from dimensiondatetime''')
    all = cursor.fetchall()
    set_datetime = set([x[0] for x in all])

    data = []
    for datetime_str, timestamp in zip(df["date_str"], df.index):
        if datetime_str not in set_datetime:
            datetime = timestamp.strftime('%Y-%m-%d')
            year = timestamp.year
            month = timestamp.month
            day = timestamp.day
            data.append([datetime_str, datetime, year, month, day])

    if data:
        sql = '''INSERT INTO dimensionDatetime VALUES(%s,%s,%s,%s,%s);'''
        cursor.executemany(sql, data)
        print("Se han añadido ", len(data), " nuevas fechas")

    last_date = ti.xcom_pull(key=country, task_ids=f"retrieve_metadata_{country}")[
        "last_date"]

    if last_date != '20150101':
        # delete last day
        cursor.execute(
            f"DELETE FROM factgeneration WHERE timestamp_id = '{timestamp}' ")

    # insert new rows
    sql = f'''SELECT id FROM dimensioncountry WHERE ISO2 = '{country}' '''
    cursor.execute(sql)
    query = cursor.fetchall()

    sql = '''INSERT INTO factGeneration(country_id, source_id, timestamp_id, generation) VALUES(%s,%s,%s,%s);'''
    sources = set(df.columns).intersection(set(SOURCES_ID.keys()))
    for column in sources:
        values = [[query[0][0], SOURCES_ID[column], row[1], row[0]]
                  for row in df[[column, "date_str"]].values.tolist()]
        cursor.executemany(sql, values)

    conn.commit()


def _reset_flag(country: str, ti) -> None:

    last_row = ti.xcom_pull(key=country, task_ids=f"transform_data_{country}")

    postgres_hook = PostgresHook(
        postgres_conn_id="postgres_conn", schema="postgres")
    conn = postgres_hook.get_conn()
    cursor = conn.cursor()

    cursor.execute(
        f'''SELECT * FROM dimensionCountry WHERE ISO2 = '{country}' ''')
    query = cursor.fetchall()
    COUNTRY_ID = query[0][0]

    sql = f'''UPDATE logs_incremental SET last = 0 WHERE last = 1 AND country_id = '{COUNTRY_ID}';'''
    cursor.execute(sql)

    # set new flag
    values = [[COUNTRY_ID, last_row, 1]]
    sql = '''INSERT INTO logs_incremental(country_id, timestamp, last) VALUES(%s,%s,%s);'''
    cursor.executemany(sql, values)


# DAG tasks

for country in COUNTRY_CODES:

    t0 = PythonOperator(
        task_id=f"retrieve_metadata_{country}",
        python_callable=_retrieve_metadata,
        op_kwargs={"country": country},
        dag=dag,
    )

    t1 = PythonOperator(
        task_id=f"download_data_{country}",
        python_callable=_download_data,
        op_kwargs={"country": country},
        dag=dag,
    )

    t2 = PythonOperator(
        task_id=f"transform_data_{country}",
        python_callable=_transform_data,
        op_kwargs={"country": country},
        dag=dag,
    )

    t3 = PythonOperator(
        task_id=f"load_data_{country}",
        python_callable=_load_data,
        op_kwargs={"country": country},
        dag=dag,
    )

    t4 = PythonOperator(
        task_id=f"reset_flag_{country}",
        python_callable=_reset_flag,
        op_kwargs={"country": country},
        dag=dag,
    )

    t0 >> t1 >> t2 >> t3 >> t4