
import pandas as pd
import requests
from datetime import datetime


import pandas as pd
import requests


def get_dataframe(func):
    def wrapper(*args, **kwargs) -> pd.DataFrame:
        url = func(*args, **kwargs)
        res = requests.get(url = url)
        df = pd.read_json(res.text, orient='records')
        df["Timestamp"]=pd.to_datetime(df["Timestamp"])
        df=df.sort_values(by=["Timestamp", "Type"])
        return df
    return wrapper



@get_dataframe
def get_line_evolution_sources(source: str, country: str = 'España') -> str:
    url=f"http://127.0.0.1:8000/generation/evolution-sources-total?source={source}&trunc=Mensual&{country}"
    return url


@get_dataframe
def get_percentage_source_day(source: str, date: datetime) -> str:
    url=f"http://127.0.0.1:8000/generation/last-sources-percentage?trunc=Anual&date={date}&source={source}"
    return url


@get_dataframe
def get_line_evolution_countries(country: str, source: str = '') -> str:
    url=f"http://127.0.0.1:8000/generation/evolution-sources-total?country={country}&trunc=Mensual&{source}"
    return url

@get_dataframe
def get_evolution_percentage_sources_countries(country: str, source: str = '') -> str:
    url=f"http://127.0.0.1:8000/generation/evolution-sources-percentage?country={country}&{source}"
    return url

@get_dataframe
def get_bar_evolution_country_type(country: str, source: str = '') -> str:
    url=f"http://127.0.0.1:8000/generation/evolution-categories-percentage?country={country}&{source}"
    return url


@get_dataframe
def get_evolution_total_categories_countries(country: str) -> str:
    url=f"http://127.0.0.1:8000/generation/evolution-categories-total?country={country}"
    return url



