-- Added deduplication logic to stop 'join' fan out in mart-models from 
-- job_ads_id

WITH employer_name_raw AS (
    SELECT 
        employer__name,
        workplace_address__municipality,
        workplace_address__country,
        employer__workplace
    FROM {{ ref('src_employer_name') }}
),

deduped_employers as (
SELECT*,
row_number() over (
    partition by 
    {{ dbt_utils.generate_surrogate_key([
        'workplace_address__municipality', 
        'employer__workplace'
    ]) }} 
    order by 
    employer__name
) as rn 
    from employer_name_raw
)
 SELECT
    {{ dbt_utils.generate_surrogate_key(['employer__workplace', 'workplace_address__municipality']) }} AS employer_id,
    employer__name,
    COALESCE(workplace_address__municipality, 'Ej angivet') AS municipality,
    COALESCE(workplace_address__country, 'Ej angivet') AS country,

    CASE
        WHEN workplace_address__municipality IS NULL OR workplace_address__municipality = '' 
        THEN COALESCE(workplace_address__country, 'Ej angivet')
        ELSE CONCAT(workplace_address__municipality, ', ', workplace_address__country)
    END AS municipality_country_text,

    employer__workplace

FROM deduped_employers
WHERE rn = 1
--GROUP BY 
--    employer__name, 
--    workplace_address__municipality, 
--    workplace_address__country,
--    employer__workplace