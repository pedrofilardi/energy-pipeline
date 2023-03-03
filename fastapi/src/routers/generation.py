
from fastapi import APIRouter, Query
from app.models.user import CategoriesType, CountryType, FrecuencyType, SourcesType
from app.functions.functions import lista_paises
import json

import psycopg2
import pandas as pd
import json


### DISEÑO DE COMO VA A SER
### CARGAR TODOS LOS PAISES
### PULIR MODELADO

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

def having_construction(countries=None, sources=None):
        condition = "HAVING "
        if countries is not None:
            countries_str =  ", ".join(f"'{w}'" for w in countries)
            condition = condition + f"country.name_es IN ({countries_str})"
        if  sources is not None:
            if countries is not None:
                condition = condition + " AND "
            sources_str =  ", ".join(f"'{w}'" for w in sources)
            condition = condition + f"sc.name IN ({sources_str})"
        if countries is None and sources is None:
            condition = ""
        
        return condition
    

router = APIRouter()

# we split queries in order to avoid dependencies for API docs clarity sake.  
# Frecuency, last or porcentage do not depend on each other, they just add query granularity


#WIDGETS

@router.get("/evolution-sources-total")
async def evolution_sources_total(countries: list[CountryType] | None = Query(default=None, alias="country"),
                            sources: list[SourcesType] | None =  Query(default=None, alias="source"),
                            frequency: FrecuencyType = Query(default="Diario", alias="trunc"),
                            last_value: bool  = Query(default=False, alias="last"),
                            percentage: bool  = Query(default=False)):
    
    frecuency_map={
        "Anual" : "year",
        "Mensual": "month",
        "Semanal": "week",
        "Diario": "day"
    }
    

   

                
        
    
    
    sql = f'''SELECT DATE_TRUNC('{frecuency_map[frequency]}', f.timestamp) AS timestamp, f.countries, f.sources, SUM(generacion)
            FROM 
                (SELECT dt.timestamp, country.name_es AS countries, sc.name AS sources, SUM(fact.generation) generacion
                FROM factgeneration fact JOIN dimensionsources sc
                ON fact.source_id = sc.id
                JOIN dimensioncountry country ON fact.country_id = country.id
                JOIN dimensiondatetime dt ON fact.timestamp_id = dt.id
                GROUP BY dt.timestamp, country.name_es, sc.name
                {having_construction(countries,sources)}) AS f
                GROUP BY DATE_TRUNC('{frecuency_map[frequency]}', f.timestamp), f.countries, f.sources ; '''
        
    conn = connect(param_dic)
    cursor = conn.cursor()
    cursor.execute(sql)
    query = cursor.fetchall()
    
    df = pd.DataFrame(
        query, columns=["Timestamp", "Country", "Type", "Generation"])
    return json.loads(df.to_json(orient='records'))


@router.get("/last-sources-percentage")
async def evolution_sources_total(countries: list[None] = Query(default=None, alias="country"),
                            source: SourcesType | None =  Query(default=None, alias="source"),
                            frequency: FrecuencyType = Query(default="Anual", alias="trunc"),
                            last_value: bool  = Query(default=False, alias="last"),
                            percentage: bool  = Query(default=False),
                            date: str = Query(default="2022-02-02")):
    
    if countries is None:
        if source is not None:
            option = f" WHERE sources = '{source}' AND timestamp = '{date}' "
        else:
            option = ""
    else:
        countries_str=", ".join(f"'{w}'" for w in countries)
        option = f" WHERE sources = '{source}' AND countries IN ({countries_str}) AND timestamp = '{date}' "
    
    
    
    sql =   sql = f'''SELECT * FROM public.generation_percentage_day
                     {option}'''
    conn = connect(param_dic)
    cursor = conn.cursor()
    cursor.execute(sql)
    query = cursor.fetchall()

    df = pd.DataFrame(
        query, columns=["Timestamp", "Country", "Type", "Generation"])
    

    if frequency == "Anual":
        df = df[df["Timestamp"].dt.year == df.Timestamp.max().year]
    if frequency == "Mensual":
        df = df[df["Timestamp"] >= df.Timestamp.max().strftime('%b-%Y')]
    if frequency == "Diario":
        df= df[df["Timestamp"] >= df.Timestamp.max().strftime('%d-%b-%Y')]
        

    return json.loads(df.to_json(orient='records'))


    

@router.get("/evolution-sources-percentage")
async def evolution_sources_total(countries: CountryType | None = Query(default=None, alias="country"),
                            source: SourcesType | None =  Query(default=None, alias="source"),
                            frequency: FrecuencyType = Query(default="Diario", alias="trunc"),
                            last_value: bool  = Query(default=False, alias="last"),
                            percentage: bool  = Query(default=False)):
    
    
    
    sql = f'''SELECT * FROM public.generation_percentage_anual
            WHERE countries = '{countries}';

'''


    conn = connect(param_dic)
    cursor = conn.cursor()
    cursor.execute(sql)
    query = cursor.fetchall()
    
    df = pd.DataFrame(
        query, columns=["Timestamp", "Country", "Type", "Generation"])
    return json.loads(df.to_json(orient='records'))
    
    
    
    
    
    
    

@router.get("/evolution-categories-percentage")
async def queries_generation_category(country: CountryType | None = Query(default=None, alias="country"),
                                    categories: list[CategoriesType] | None  = Query(default=None, alias="category"),
                                    frequency: FrecuencyType = Query(default="Diario",  alias="frecuency"),
                                    last_value: bool  = Query(default=False, alias="last"),
                                    percentage: bool  = Query(default=False)):
    
    sql = f'''SELECT * FROM public.generation_percentage_type_month 
                WHERE countries = '{country}';'''


    conn = connect(param_dic)
    cursor = conn.cursor()
    cursor.execute(sql)
    query = cursor.fetchall()
    
    df = pd.DataFrame(
        query, columns=["Timestamp", "Country", "Type", "Generation"])
    return json.loads(df.to_json(orient='records'))
  

    
@router.get("/lista_paises")
async def query_lista_paises():
    return lista_paises()





@router.get("/evolution-categories-total")
async def queries_generation_category(country: CountryType | None = Query(default=None, alias="country"),
                                    categories: list[CategoriesType] | None  = Query(default=None, alias="category"),
                                    frequency: FrecuencyType = Query(default="Diario",  alias="frecuency"),
                                    last_value: bool  = Query(default=False, alias="last"),
                                    percentage: bool  = Query(default=False)):
    
    sql = f'''SELECT * FROM public.generation_total_category_month 
                WHERE countries = '{country}';'''


    conn = connect(param_dic)
    cursor = conn.cursor()
    cursor.execute(sql)
    query = cursor.fetchall()
    
    df = pd.DataFrame(
        query, columns=["Timestamp", "Country", "Type", "Generation"])
    return json.loads(df.to_json(orient='records'))


