
-- Added deduplication logic to stop 'join' fan out in mart-models from 
-- job_ads_id

WITH employer_name_raw AS (
    SELECT 
        employer_name,
        workplace_address_municipality,
        workplace_address_country,
        employer_workplace
    FROM {{ ref('src_employer_name') }}
),

deduped_employers as (
SELECT*,
row_number() over (
    partition by 
    {{ dbt_utils.generate_surrogate_key([
        'workplace_address_municipality', 
        'employer_workplace'
    ]) }} 
    order by 
    employer_name
) as rn 
    from employer_name_raw
)
 SELECT
    {{ dbt_utils.generate_surrogate_key(['employer_workplace', 'workplace_address_municipality']) }} AS employer_id,
    employer_name,
    COALESCE(workplace_address_municipality, 'Ej angivet') AS municipality,
    COALESCE(workplace_address_country, 'Ej angivet') AS country,

    CASE
        WHEN workplace_address_municipality IS NULL OR workplace_address_municipality = '' 
        THEN COALESCE(workplace_address_country, 'Ej angivet')
        ELSE CONCAT(workplace_address_municipality, ', ', workplace_address_country)
    END AS municipality_country_text,

    employer_workplace

FROM deduped_employers
WHERE rn = 1
--GROUP BY 
--    employer__name, 
--    workplace_address__municipality, 
--    workplace_address__country,
--    employer__workplace



