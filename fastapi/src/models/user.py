from typing import List
from enum import Enum


class CountryType(str, Enum):
    AUSTRIA =  "Austria" 
    BELGICA =  "Bélgica" 
    BOSNIA_ERZEGOVINA =  "Bosnia y Erzegovina" 
    BULGARIA =  "Bulgaria" 
    CROACIA =  "Croacia" 
    CHIPRE =  "Chipre" 
    REPUBLICA_CHECA =  "República Checa" 
    DINAMARCA =  "Dinamarca" 
    ESTONIA =  "Estonia" 
    FINLANDIA =  "Finlandia" 
    FRANCIA =  "Francia" 
    ALEMANIA =  "Alemania" 
    GRECIA =  "Grecia" 
    HUNGRIA =  "Hungría" 
    IRLANDA =  "Irlanda" 
    ITALIA =  "Italia" 
    KOSOVO =  "Kosovo" 
    LETONIA =  "Letonia" 
    LITUANIA =  "Lituania" 
    MOLDAVIA =  "Moldavia" 
    MONTENEGRO =  "Montenegro" 
    PAISES_BAJOS =  "Países Bajos" 
    NORUEGA =  "Noruega" 
    POLONIA =  "Polonia" 
    PORTUGAL =  "Portugal" 
    RUMANIA =  "Rumanía" 
    SERBIA =  "Serbia" 
    ESLOVAQUIA =  "Eslovaquia" 
    ESLOVENIA =  "Eslovenia" 
    ESPAÑA =  "España" 
    SUECIA =  "Suecia" 
    SUIZA =  "Suiza" 
    GEORGIA =  "Georgia" 
    #### ÑADIR TODOS
      

class SourcesType(str, Enum):
    BIO ='Biomass'
    LIGNITE = 'Fossil Brown coal/Lignite',
    COALGAS = 'Fossil Coal-derived gas',
    GAS = 'Fossil Gas',
    HARDCOAL = 'Fossil Hard coal',
    OIL = 'Fossil Oil',
    OILSHALE = 'Fossil Oil shale',
    PEAT = 'Fossil Peat',
    GEO = 'Geothermal',
    HYDROSTORAGE = 'Hydro Pumped Storage',
    HYDRORIVER = 'Hydro Run-of-river and poundage',
    HYDRORESERVOIR = 'Hydro Water Reservoir',
    MARINE = 'Marine',
    NUC = 'Nuclear',
    OTHER = 'Other',
    OTHER_REN ='Other renewable',
    SUN = 'Solar',
    WASTE = 'Waste',
    WINDONSHORE = 'Wind Onshore',
    WINDOFFSHORE = 'Wind Offshore'

class CategoriesType(str, Enum):
    NUCLEAR = "Nuclear"
    RENOVABLE = "Renovable"
    FOSIL = "Fósil"
    OTRA = "Otra"

    
class FrecuencyType(str, Enum):
    DIARIO = "Diario"
    SEMANAL = "Semanal"
    MENSUAL = "Mensual"
    ANUAL = "Anual"
    