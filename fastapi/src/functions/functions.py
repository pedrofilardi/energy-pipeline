
import psycopg2
import pandas as pd
import json




param_dic = {
    "host"      : "localhost",
    "user"      : "postgres",
    "password"  : "admin",
    "port": 5433
}


def connect(params_dic):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        conn = psycopg2.connect(**params_dic)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return conn
    
    
freq = {"Anual": "Y",
        "Mensual": "M",
        "Semanal": "W",
        "Diario": "D"
        }

def query_sql(sql):
    conn = connect(param_dic)
    cursor = conn.cursor()
    cursor.execute(sql)
    query = cursor.fetchall()
    return query
    
    
def query_to_df(query, frecuency: str, porcentual: bool):
    
    df = pd.DataFrame(
        query, columns=["Timestamp", "Country", "Type", "Generation"])

    df["Timestamp"] = pd.to_datetime(df["Timestamp"], utc=True)

    df = (
        df.pivot_table(values=['Generation'], index="Timestamp", columns=[
                       'Type', 'Country'], aggfunc='first')
        .groupby(pd.Grouper(freq=freq[frecuency], level=0, closed='left'))
        .sum()
    )

    df.columns = df.columns.droplevel(0)
    
    if porcentual:
    
        df["total"] = df.sum(axis=1)
        df = (df.iloc[:, :-1]
                .apply(lambda x: x.astype(float)/df["total"]*100, axis=0))

    df = (df.reset_index()
          .melt(id_vars="Timestamp", value_vars=None, var_name=["Type", "Country"],
                value_name='Generation', col_level=None, ignore_index=True)
    )
    
    
    return df





def last(func, frecuency):
    def wrapper(*args, **kargs):
        df = func(*args, **kargs)
        if frecuency == "Anual":
            df = df[df["Timestamp"].dt.year == df.Timestamp.max().year]
        if frecuency == "Mensual":
            df = df[df["Timestamp"] >= df.Timestamp.max().strftime('%b-%Y')]
        if frecuency == "Diario":
            df= df[df["Timestamp"] >= df.Timestamp.max().strftime('%d-%b-%Y')]
        return df
    return wrapper
    
    
    

def sql_constructor(type: str, countries: list, options: list | None, porcentual: bool):
    
    if type == "source":
        opcion_clase = 'sc.name'
    elif type == "category":
        opcion_clase = 'sc.type'
        
    countries = ", ".join(f"'{w}'" for w in countries)
    
    #si devolvemos todo
    if ((porcentual==True) | (options is None)):
        sql = f'''SELECT fact.timestamp_id, country.name_es, {opcion_clase}, SUM(fact.generation)
                    FROM factgeneration fact JOIN dimensionsources sc
                    ON fact.source_id = sc.id
                    JOIN dimensioncountry country ON fact.country_id = country.id
                    GROUP BY fact.timestamp_id, country.name_es, {opcion_clase}
                    HAVING country.name_es IN ({countries})'''

    
    else:
        options_str = ", ".join(f"'{w}'" for w in options)
        sql = f'''SELECT fact.timestamp_id, country.name_es, {opcion_clase}, SUM(fact.generation)
                    FROM factgeneration fact JOIN dimensionsources sc
                    ON fact.source_id = sc.id
                    JOIN dimensioncountry country ON fact.country_id = country.id
                    GROUP BY fact.timestamp_id, country.name_es, {opcion_clase}
                    HAVING country.name_es IN ({countries}) and {opcion_clase} IN ({options_str}) '''
                    
    return sql
    
    
def lista_paises():
    sql='''SELECT DISTINCT(country.name_es)
FROM factgeneration f
JOIN dimensioncountry country
ON f.country_id=country.id'''
    conn = connect(param_dic)
    cursor = conn.cursor()

    cursor.execute(sql)
    query = cursor.fetchall()
    query=[x[0] for x in query]
    
    return {"countries" : query}