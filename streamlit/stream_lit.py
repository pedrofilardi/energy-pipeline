import streamlit as st
from streamlit_functions import *
from utils.getters import *
import datetime


# Configuraciones iniciales
st.set_page_config(layout='wide', initial_sidebar_state='expanded')
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


st.write(
    """
    <style>
    [data-testid="stMetricDelta"] svg {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)



if "countries" not in st.session_state:
    lista_paises = countries()
    st.session_state["countries"] = lista_paises
        
with st.sidebar:
    

        st.markdown("## Configuración")
        paginas = st.radio("", ["Por países", "Por fuentes"], label_visibility="collapsed")
        
            
        
    
 
#configuración de tabs   
listTabs = ["Generación", "Precio", "Estadísticas"]
whitespace = 80
tab1, tab2, tab3 = st.tabs([s.center(whitespace, "\u2001") for s in listTabs])


with tab1:

    sources_list = ['Fossil Gas', 'Biomass',
                     'Fossil Brown coal/Lignite',
                     'Fossil Coal-derived gas',
                     'Fossil Gas',
                     'Fossil Hard coal',
                     'Fossil Oil',
                     'Fossil Oil shale',
                     'Fossil Peat',
                     'Geothermal',
                     'Hydro Pumped Storage',
                     'Hydro Run-of-river and poundage',
                     'Hydro Water Reservoir',
                     'Marine',
                     'Nuclear',
                     'Other',
                     'Other renewable',
                     'Solar',
                     'Waste',
                     'Wind Onshore',
                     'Wind Offshore']

    if paginas == "Por fuentes":
        
        source = st.selectbox(label="Seleccione fuente",
                              options=sources_list, 
                              key="source")
            
        with st.sidebar:
            
            
    
            from_date = st.date_input(label="Desde", value=datetime.date(2022, 7, 6))
            date = from_date.strftime("%Y-%m-%d")
            select_country = st.sidebar.multiselect(label='País',
                                            options=st.session_state.countries,
                                            default="España",
                                            key="pais_2")
            if select_country:
                countries = query_list("country", select_country)
                st.session_state["line_evolution_countries"]=countries
        col1, col2 = st.columns((6, 4))    
            
    #DASHBOARD         
            
        with col1:
            with st.expander(f"Generación de {source} en MW por país", True):
                if "line_evolution_sources" not in st.session_state:
                    st.session_state["line_evolution_sources"] = get_line_evolution_sources(source, "country=España")
                    
                if source != "Seleccione":  
                    countries=st.session_state["line_evolution_countries"]
                    st.session_state["line_evolution_sources"]=get_line_evolution_sources(source, countries)
                    fig = line_evolution_sources(st.session_state["line_evolution_sources"])
                    st.plotly_chart(fig, use_container_width=True) 
        
        with col2:
            
            with st.expander("Contribución porcentual a generación total", True):
                
                    st.session_state["percentage_source_day"]=get_percentage_source_day(source, date)
                    fig = sources_percentage2(st.session_state["percentage_source_day"])
                    st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("Mapa coroplético", True):
            chart_map_source = st.plotly_chart(mapa(st.session_state["percentage_source_day"]), use_container_width=True)

    
                   
    else:
        
        
        country = st.selectbox(label="Seleccione país",
                              options=st.session_state["countries"],   
                              key="paises")  
        
        
        col1, col2, col3 = st.columns(3)
        
        
        df=get_line_evolution_countries(country)
        st.session_state["evolution_percentage_sources_countries"]=df
        max_energy=df[df["Timestamp"]==df.Timestamp.max()].sort_values(by="Generation").tail(1).Type.values[0]
        st.session_state["max_energy"]=max_energy
        
        
        df=get_bar_evolution_country_type(country)
        st.session_state["bar_evolution_country_type"]=df
        total_renovable=round(df[(df["Timestamp"]==df.Timestamp.max()) & (df["Type"].isin(["Renovable", "Nuclear"]))].sort_values(by="Generation").tail(1).Generation.values[0], 3)
        
        
        
        col1.metric("Principal fuente hoy", max_energy, "20%")
        col2.metric("Energía limpia hoy", f"{total_renovable} %", "+8%")
        col3.metric("Humidity", "86%", "4%")
       
        col1, col2 = st.columns((7, 3))  
            
            
        with col1:
            with st.expander(f"Generación porcentual por tipo de energía", True):
              
                fig = plot_line_evolution_country_type(st.session_state["bar_evolution_country_type"])
                st.plotly_chart(fig, use_container_width=True)
            
                
        with col2:
            year = st.sidebar.selectbox(label="Seleccione año",
                              options=[2015, 2016, 2017, 2018, 2019, 2020], 
                              key="año")  
            
            with st.expander(f"Año {year}", True):
                
                st.session_state["evolution_total_categories_countries"]=get_evolution_total_categories_countries(country)
                fig = plot_polar_category_total(st.session_state["evolution_total_categories_countries"], year)
        
                st.plotly_chart(fig, use_container_width=True)
                
            
            
        
            

            
        

                    
                    
                    
        with st.expander(f"Generación total en MW", True):
                st.session_state["evolution_percentage_sources_countries"]=get_line_evolution_countries(country)
                fig = plot_percentage_countries_sources_total(st.session_state["evolution_percentage_sources_countries"])
                st.plotly_chart(fig, use_container_width=True)

        