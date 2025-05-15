{# WITH employer_name AS (
    SELECT 
        employer__name,
        workplace_address__municipality,
        workplace_address__country,
        employer__workplace
    FROM {{ source('job_ads', 'stg_ads') }}
)

SELECT
    {{ dbt_utils.generate_surrogate_key([
        'employer__name', 
        'workplace_address__municipality', 
        'workplace_address__country',
        'employer__workplace'
    ]) }} AS employer_location_id,
    
    employer__name,
    COALESCE(workplace_address__municipality, 'Ej angivet') AS municipality,
    COALESCE(workplace_address__country, 'Ej angivet') AS country,

    CASE
        WHEN workplace_address__municipality IS NULL OR workplace_address__municipality = '' THEN COALESCE(workplace_address__country, 'Ej angivet')
        ELSE CONCAT(workplace_address__municipality, ', ', workplace_address__country)
    END AS municipality_country_text,

    employer__workplace

FROM employer_name
GROUP BY 
    employer__name, 
    workplace_address__municipality, 
    workplace_address__country,
    employer__workplace #}
with src_employer as (select * from {{ ref("src_employer") }})

select
    {{
        dbt_utils.generate_surrogate_key(
            ["employer_workplace", "workplace_municipality"]
        )
    }} as employer_id,
    max(
        coalesce(employer_organization_number, 'saknar organisationsnummer')
    ) as employer_organization_number,
    max(coalesce(employer_name, 'namn ej angiven')) as employer_name,
    max(coalesce(employer_workplace, 'plats ej angiven')) as employer_workplace,
    max(coalesce(workplace_country, 'land ej angiven')) as workplace_country,
    max(coalesce(workplace_region, 'region ej angiven')) as workplace_region,
    max(
        coalesce(workplace_municipality, 'kommun ej angiven')
    ) as workplace_municipality,
    max(
        coalesce(
            {{
                capitalize_first_letter(
                    "coalesce(workplace_city, workplace_municipality)"
                )
            }},
            'stad ej angiven'
        )
    ) as workplace_city,
    max(coalesce(employer_url, 'webbplats ej angiven')) as employer_url
from src_employer
group by employer_id
