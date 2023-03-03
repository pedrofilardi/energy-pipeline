
-- DIMENSIONS


-- Creation of date table table

CREATE TABLE IF NOT EXISTS dimension_date
    (id VARCHAR PRIMARY KEY,
    timestamp TIMESTAMP,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    UNIQUE(id)
    );



-- Creation of soruce table

CREATE TABLE IF NOT EXISTS dimension_source
(id INT,
name VARCHAR,
code VARCHAR, 
type varchar,
UNIQUE(id)
);


-- Creation of soruce table

    CREATE TABLE IF NOT EXISTS dimension_country
    (id INT,
    ISO2 VARCHAR,
    ISO3 VARCHAR,
    name_en VARCHAR,
    name_es VARCHAR,
    utc VARCHAR,
    UNIQUE(id)
    );

-- FACTS

CREATE TABLE IF NOT EXISTS fact_generation
(id SERIAL PRIMARY KEY,
country_id INT,
source_id INT,
timestamp_id VARCHAR,
generation DECIMAL,
CONSTRAINT fk_country_id
      FOREIGN KEY(country_id) 
	  REFERENCES dimension_country(id)
	  ON DELETE CASCADE,
CONSTRAINT fk_source_id
      FOREIGN KEY(source_id) 
	  REFERENCES dimension_source(id)
	  ON DELETE CASCADE,
CONSTRAINT fk_timestamp_id
      FOREIGN KEY(timestamp_id) 
	  REFERENCES dimension_date(id)
	  ON DELETE CASCADE

);

-- INCREMENTAL LOADING

CREATE TABLE IF NOT EXISTS logs_incremental
    (id SERIAL PRIMARY KEY,
    country_id integer, 
    timestamp VARCHAR,
    last integer,
    CONSTRAINT fk_country_id_logs
      FOREIGN KEY(country_id) 
	  REFERENCES dimension_country(id)
	  ON DELETE CASCADE
    );

    -- POPULATE DIMENSIONS

INSERT INTO public.dimension_source VALUES (1, 'Biomass', 'BIO', 'Renovable');
INSERT INTO public.dimension_source VALUES (2, 'Fossil Brown coal/Lignite', 'LIGNITE', 'Fósil');
INSERT INTO public.dimension_source VALUES (3, 'Fossil Coal-derived gas', 'COALGAS', 'Fósil');
INSERT INTO public.dimension_source VALUES (4, 'Fossil Gas', 'GAS', 'Fósil');
INSERT INTO public.dimension_source VALUES (5, 'Fossil Hard coal', 'HARDCOAL', 'Fósil');
INSERT INTO public.dimension_source VALUES (6, 'Fossil Oil', 'OIL', 'Fósil');
INSERT INTO public.dimension_source VALUES (7, 'Fossil Oil shale', 'OILSHALE', 'Fósil');
INSERT INTO public.dimension_source VALUES (8, 'Fossil Peat', 'PEAT', 'Fósil');
INSERT INTO public.dimension_source VALUES (9, 'Geothermal', 'GEO', 'Renovable');
INSERT INTO public.dimension_source VALUES (10, 'Hydro Pumped Storage', 'HYDROSTORAGE', 'Renovable');
INSERT INTO public.dimension_source VALUES (11, 'Hydro Run-of-river and poundage', 'HYDRORIVER', 'Renovable');
INSERT INTO public.dimension_source VALUES (12, 'Hydro Water Reservoir', 'HYDRORESERVOIR', 'Renovable');
INSERT INTO public.dimension_source VALUES (13, 'Marine', 'MARINE', 'Renovable');
INSERT INTO public.dimension_source VALUES (14, 'Nuclear', 'NUC', 'Nuclear');
INSERT INTO public.dimension_source VALUES (15, 'Other', 'OTHER', 'Otra');
INSERT INTO public.dimension_source VALUES (16, 'Other renewable', 'OTHER_REN', 'Renovable');
INSERT INTO public.dimension_source VALUES (17, 'Solar', 'SUN', 'Renovable');
INSERT INTO public.dimension_source VALUES (18, 'Waste', 'WASTE', 'Renovable');
INSERT INTO public.dimension_source VALUES (19, 'Wind Onshore', 'WINDONSHORE', 'Renovable');
INSERT INTO public.dimension_source VALUES (20, 'Wind Offshore', 'WINDOFFSHORE', 'Renovable'); 


INSERT INTO public.dimension_country VALUES (1, 'AT', 'AUT', 'Austria', 'Austria', 'Europe/Vienna');
INSERT INTO public.dimension_country VALUES (2, 'BE', 'BEL', 'Belgium', 'Bélgica', 'Europe/Brussels');
INSERT INTO public.dimension_country VALUES (3, 'BA', 'BIH', 'Bosnia and Herzegovina', 'Bosnia y Erzegovina', 'Europe/Sarajevo');
INSERT INTO public.dimension_country VALUES (4, 'BG', 'BGR', 'Bulgaria', 'Bulgaria', 'Europe/Sofia');
INSERT INTO public.dimension_country VALUES (5, 'HR', 'HRV', 'Croatia', 'Croacia', 'Europe/Zagreb');
INSERT INTO public.dimension_country VALUES (6, 'CY', 'CYP', 'Cyprus', 'Chipre', 'Asia/Nicosia');
INSERT INTO public.dimension_country VALUES (7, 'CZ', 'CZE', 'Czech Republic', 'República Checa', 'Europe/Prague');
INSERT INTO public.dimension_country VALUES (8, 'DK', 'DNK', 'Denmark', 'Dinamarca', 'Europe/Copenhagen');
INSERT INTO public.dimension_country VALUES (9, 'EE', 'EST', 'Estonia', 'Estonia', 'Europe/Tallinn');
INSERT INTO public.dimension_country VALUES (10, 'FI', 'FIN', 'Finland', 'Finlandia', 'Europe/Helsinki');
INSERT INTO public.dimension_country VALUES (11, 'FR', 'FRA', 'France', 'Francia', 'Europe/Paris');
INSERT INTO public.dimension_country VALUES (12, 'GR', 'GEO', 'Georgia', 'Georgia', 'Europe/Athens');
INSERT INTO public.dimension_country VALUES (13, 'DE', 'DEU', 'Germany', 'Alemania', 'Europe/Berlin');
INSERT INTO public.dimension_country VALUES (14, 'GR', 'GRC', 'Greece', 'Grecia', 'Europe/Athens');
INSERT INTO public.dimension_country VALUES (15, 'HU', 'HUN', 'Hungary', 'Hungría', 'Europe/Budapest');
INSERT INTO public.dimension_country VALUES (16, 'IE_SEM', 'IRL', 'Ireland', 'Irlanda', 'Europe/Dublin');
INSERT INTO public.dimension_country VALUES (17, 'IT', 'ITA', 'Italy', 'Italia', 'Europe/Rome');
INSERT INTO public.dimension_country VALUES (18, 'XK', 'XXK', 'Kosovo', 'Kosovo', 'Europe/Rome');
INSERT INTO public.dimension_country VALUES (19, 'LV', 'LVA', 'Latvia', 'Letonia', 'Europe/Riga');
INSERT INTO public.dimension_country VALUES (20, 'LT', 'LTU', 'Lituania', 'Lituania', 'Europe/Vilnius');
INSERT INTO public.dimension_country VALUES (21, 'MD', 'MDA', 'Moldova', 'Moldavia', 'Europe/Chisinau');
INSERT INTO public.dimension_country VALUES (22, 'ME', 'MNE', 'Montenegro', 'Montenegro', 'Europe/Podgorica');
INSERT INTO public.dimension_country VALUES (23, 'NL', 'NLD', 'Netherlands', 'Países Bajos', 'Europe/Amsterdam');
INSERT INTO public.dimension_country VALUES (24, 'NO', 'NOR', 'Norway', 'Noruega', 'Europe/Oslo');
INSERT INTO public.dimension_country VALUES (25, 'PL', 'POL', 'Poland', 'Polonia', 'Europe/Warsaw');
INSERT INTO public.dimension_country VALUES (26, 'PT', 'PRT', 'Portugal', 'Portugal', 'Europe/Lisbon');
INSERT INTO public.dimension_country VALUES (27, 'RO', 'ROU', 'Romania', 'Rumanía', 'Europe/Moscow');
INSERT INTO public.dimension_country VALUES (28, 'RS', 'SRB', 'Serbia', 'Serbia', 'Europe/Belgrade');
INSERT INTO public.dimension_country VALUES (29, 'SK', 'SVK', 'Slovakia', 'Eslovaquia', 'Europe/Bratislava');
INSERT INTO public.dimension_country VALUES (30, 'SI', 'SVN', 'Slovenia', 'Eslovenia', 'Europe/Ljubljana');
INSERT INTO public.dimension_country VALUES (31, 'ES', 'ESP', 'Spain', 'España', 'Europe/Madrid');
INSERT INTO public.dimension_country VALUES (32, 'SE', 'SWE', 'Sweden', 'Suecia', 'Europe/Stockholm');
INSERT INTO public.dimension_country VALUES (33, 'CH', 'CHE', 'Switzerland', 'Suiza', 'Europe/Zurich');


INSERT INTO logs_incremental (country_id, timestamp, last)
(SELECT id, '20150101' AS TIMESTAMP, 1 AS LAST 
FROM public.dimension_country)