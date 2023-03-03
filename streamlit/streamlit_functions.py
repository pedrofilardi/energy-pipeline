import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

import calendar




percentage_map={
    "Total": "False",
    "Porcentual": "True"
}

def query_list(variable,  lista):
    query=""
    for elem in lista:
        query = query + variable + f"={elem}&"
    return query[:-1]
        


def countries():
    res = requests.get(url = "http://127.0.0.1:8000/generation/lista_paises")
    json_df=json.loads(res.text)
    lista_paises = json_df["countries"]
    return lista_paises



def line_evolution_sources(df):

    
    fig = px.line(df, x="Timestamp", y="Generation", color='Country')
    
   
    fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=30, r=20, t=0, b=20),
            autosize=False,
            width=700,
            height=300,
            title={
                'text': "",
                'y':0.96,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            
            legend=dict(y=0.45),
            legend_title_text = ''
        )
    fig.update_xaxes(title='', visible=True, showticklabels=True)
        
    return fig


def sources_percentage(country, kind):
    if kind == "pie":
        res = requests.get(url = f"http://127.0.0.1:8000/generation/evolution-sources-percentage?country={country}&trunc=Anual")
        df = pd.read_json(res.text, orient='records')
        df["Timestamp"]=pd.to_datetime(df["Timestamp"])
        #coger la ultima solo
        fig = px.pie(df, values='Generation', names='Type' , color_discrete_sequence=px.colors.qualitative.Light24)
        fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=30, r=20, t=0, b=20),
                yaxis=dict(
                title_text="Generación %",
                ticktext=["0%", "20%", "40%", "60%","80%","100%"],
                tickvals=[0, 20, 40, 60, 80, 100],
                tickmode="array",
                titlefont=dict(size=10),    
            ),
            autosize=False,
            width=300,
            height=300,
            title={
                'text': "",
                'y':0.96,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            barmode='stack',
            legend=dict(y=0.45),
            legend_title_text = ''
            )
        fig.update_xaxes(title='', visible=True, showticklabels=True)
        return fig
    else:
            
        

    
        res = requests.get(url = f"http://127.0.0.1:8000/generation/evolution-sources-percentage?country={country}&trunc=Anual")
        df = pd.read_json(res.text, orient='records')
        df["Timestamp"]=pd.to_datetime(df["Timestamp"])
        fig = px.bar(df, x="Timestamp", y="Generation", color="Type",  color_discrete_sequence=px.colors.qualitative.Light24,title="Long-Form Input")
        fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=30, r=20, t=0, b=20),
                yaxis=dict(
                title_text="Generación %",
                ticktext=["0%", "20%", "40%", "60%","80%","100%"],
                tickvals=[0, 20, 40, 60, 80, 100],
                tickmode="array",
                titlefont=dict(size=10),    
            ),
            autosize=False,
            width=300,
            height=300,
            title={
                'text': "",
                'y':0.96,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            barmode='stack',
            legend=dict(y=0.45),
            legend_title_text = ''
            )
        fig.update_xaxes(title='', visible=True, showticklabels=True)
        
    return fig



def last_max_value(country):
    

    url = f"http://127.0.0.1:8000/items/source?frecuency=Anual&last=true&percentage=true&country={country}"
    res = requests.get(url = url)
    df = pd.read_json(res.text, orient='records')
    final = df[df["Generation"]==df.Generation.max()]
    return final.Type.values[0],final.Generation.values[0]



def filter_geojson(geojson, countries: pd.Series):
    return [country for country in geojson if country["properties"]["ISO3"] in countries.values]


def mapa(df, percentage=True,  type=None):
    
    
    map_iso3={  'Austria': 'AUT',
                'Bélgica': 'BEL',
                'Bosnia y Erzegovina': 'BIH',
                'Bulgaria': 'BGR',
                'Croacia': 'HRV',
                'Chipre': 'CYP',
                'República Checa': 'CZE',
                'Dinamarca': 'DNK',
                'Estonia': 'EST',
                'Finlandia': 'FIN',
                'Francia': 'FRA',
                'Alemania': 'DEU',
                'Grecia': 'GRC',
                'Hungría': 'HUN',
                'Irlanda': 'IRL',
                'Italia': 'ITA',
                'Kosovo': 'XXK',
                'Letonia': 'LVA',
                'Lituania': 'LTU',
                'Moldavia': 'MDA',
                'Montenegro': 'MNE',
                'Países Bajos': 'NLD',
                'Noruega': 'NOR',
                'Polonia': 'POL',
                'Portugal': 'PRT',
                'Rumanía': 'ROU',
                'Serbia': 'SRB',
                'Eslovaquia': 'SVK',
                'Eslovenia': 'SVN',
                'España': 'ESP',
                'Suecia': 'SWE',
                'Suiza': 'CHE',
                'Georgia': 'GEO'}
    df["ISO3"]=df.Country.map(map_iso3)


    europe = json.load(open("europe.geojson", 'r'))
    europe_json=europe["features"]

    if percentage==False:
        range_color=(0, df.Generation.max())
    else:
        range_color=(0, 100)


    fig = px.choropleth(df, locations="ISO3", geojson=filter_geojson(europe_json, df.ISO3), featureidkey='properties.ISO3', color="Generation", scope="europe",

                        color_continuous_scale=["yellow", "orange", "red"], range_color=range_color)

    fig.update_layout(width=1000,
                    height=400,
                    dragmode=False,
                    geo=dict(
                        showframe=False,
                        showcoastlines=False,
                        projection={"type": "natural earth"}

                    ),
                    margin=dict(l=0, r=0, t=0, b=10, autoexpand=True),


                    coloraxis_colorbar=dict(
                        len=0.91,
                        x=1,
                        y=0.48,
                        thickness=30,

                    ),


                    )

    return fig




def sources_percentage2(df2):

        
        #coger la ultima solo
        fig = px.bar(df2, y='Generation', x='Country', text_auto='.2s',
            title="Default: various text sizes, positions and angles")
        fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=30, r=20, t=0, b=40),
                yaxis=dict(
                title_text="Generación %",
                ticktext=["0%", "20%", "40%", "60%","80%","100%"],
                tickvals=[0, 20, 40, 60, 80, 100],
                tickmode="array",
                titlefont=dict(size=10),    
            ),
            autosize=False,
            width=260,
            height=300,
            title={
                'text': "",
                'y':0.96,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
           
            legend=dict(y=0.45),
            legend_title_text = ''
            )
        fig.update_xaxes(title='', visible=True, showticklabels=True)
        return fig
    
    
    
    
    
def plot_bar_evolution_country_type(df):
        
    fig = px.bar(df, x="Timestamp", y="Generation", color="Type",  color_discrete_sequence=px.colors.qualitative.Light24,title="Long-Form Input")
    fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=30, r=20, t=0, b=20),
            yaxis=dict(
                title_text="Generación %",
                ticktext=["0%", "20%", "40%", "60%","80%","100%"],
                tickvals=[0, 20, 40, 60, 80, 100],
                tickmode="array",
                titlefont=dict(size=10),    
        ),
        autosize=False,
        width=600,
        height=500,
        title={
            'text': "",
            'y':0.96,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        barmode='stack',
        legend=dict(y=0.45),
        legend_title_text = ''
        )
    fig.update_xaxes(title='', visible=True, showticklabels=True)
        
            
    return fig



    
def plot_line_evolution_country_type(df):
        
    fig = px.line(df, x="Timestamp", y="Generation", color='Type')
    
   
    fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=35, r=0, t=0, b=0),
            autosize=False,
            width=1000,
            height=300,
            title={
                'text': "",
                'y':0.96,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            
            legend=dict(
                orientation="h",
                yanchor="top",
                x=0.5,
                xanchor="center",
           
      
),legend_title_text = ''
        )
    fig.update_xaxes(title='', visible=True, showticklabels=True)
    fig.update_yaxes(title_text='Generación %', title_standoff = 30)
        
    return fig



def plot_polar_category_total(df, year):
    
    


    df=df[(df["Timestamp"].dt.year==year)]
    
    df['Month'] = df['Timestamp'].apply(lambda x: calendar.month_abbr[x.month])
    
    fig = px.bar_polar(df, r="Generation", theta="Month",
                   color="Type", 
                   color_discrete_sequence= px.colors.qualitative.Plotly,)

    fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=20, b=20),
            polar = dict(
            radialaxis = dict(showticklabels=False, ticks=''),
        
    ),
            autosize=False,
            width=300,
            height=300,
            title={
                'text': "",
                'y':0.96,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            barmode='stack',
            showlegend=False
        )
    
    return fig




def plot_percentage_countries_sources_total(df):
    import plotly.graph_objects as go



    fig = go.Figure()
    colors=list(px.colors.qualitative.Plotly) + list(px.colors.qualitative.Set2)
    for column, color in zip(set(df["Type"]),  colors):
        print(column)
        df2=df[df["Type"]==column]


        fig.add_trace(go.Scatter(
            x=df2["Timestamp"], y=df2["Generation"],
            hoverinfo='x+y+name',
            mode='lines',
            line=dict(width=0.5, color=color),
            stackgroup='one',
            # define stack group,
            name=column,
            opacity=1
        ))
        
    fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=40, r=10, t=10, b=20),
           
            autosize=False,
            width=1000,
            height=300,
          
   
        )
    return fig