CREATE MATERIALIZED VIEW generation_percentage_anual AS 
WITH t1 AS (
  SELECT 
    DATE_TRUNC('year', f.timestamp) AS timestamp, 
    f.countries, 
    f.sources, 
    SUM(generacion) AS generacion 
  FROM 
    (
      SELECT 
        dt.timestamp, 
        country.name_es AS countries, 
        sc.name AS sources, 
        SUM(fact.generation) generacion 
      FROM 
        factgeneration fact 
        JOIN dimensionsources sc ON fact.source_id = sc.id 
        JOIN dimensioncountry country ON fact.country_id = country.id 
        JOIN dimensiondatetime dt ON fact.timestamp_id = dt.id 
      GROUP BY 
        dt.timestamp, 
        country.name_es, 
        sc.name
    ) AS f 
  GROUP BY 
    DATE_TRUNC('year', f.timestamp), 
    f.countries, 
    f.sources
), 
t2 AS (
  SELECT 
    timestamp, 
    countries, 
    SUM(generacion) AS total 
  FROM 
    t1 
  GROUP BY 
    timestamp, 
    countries
) 

SELECT 
  t1.timestamp, 
  t1.countries, 
  t1.sources, 
  (t1.generacion / t2.total)* 100 AS generation 
FROM 
  t1 
  JOIN t2 ON t1.timestamp = t2.timestamp 
  AND t1.countries = t2.countries 
ORDER BY 
  t1.timestamp, 
  t2.countries;



  // CON CASE


  CREATE MATERIALIZED VIEW generation_percentage_month AS 
WITH t1 AS (
  SELECT 
    DATE_TRUNC('month', f.timestamp) AS timestamp, 
    f.countries, 
    f.sources, 
    SUM(generacion) AS generacion 
  FROM 
    (
      SELECT 
        dt.timestamp, 
        country.name_es AS countries, 
        sc.name AS sources, 
        SUM(fact.generation) generacion 
      FROM 
        factgeneration fact 
        JOIN dimensionsources sc ON fact.source_id = sc.id 
        JOIN dimensioncountry country ON fact.country_id = country.id 
        JOIN dimensiondatetime dt ON fact.timestamp_id = dt.id 
      GROUP BY 
        dt.timestamp, 
        country.name_es, 
        sc.name
    ) AS f 
  GROUP BY 
    DATE_TRUNC('month', f.timestamp), 
    f.countries, 
    f.sources
), 
t2 AS (
  SELECT 
    timestamp, 
    countries, 
    SUM(generacion) AS total 
  FROM 
    t1 
  GROUP BY 
    timestamp, 
    countries
) 

SELECT 
  t1.timestamp, 
  t1.countries, 
  t1.sources, 
  CASE 
  WHEN t2.total = 0 THEN NULL
  WHEN t2.total != 0 then (t1.generacion / t2.total)* 100 
END
  AS generation 
FROM 
  t1 
  JOIN t2 ON t1.timestamp = t2.timestamp 
  AND t1.countries = t2.countries 
ORDER BY 
  t1.timestamp, 
  t2.countries;