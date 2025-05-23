-- checking api load id to deduplicate
with
    stg_job_ads as (
        select
            *, row_number() over (partition by id order by _dlt_load_id desc) as row_num
        from {{ source("job_ads", "stg_ads") }}
    ),

    latest_ads as (select * from stg_job_ads where row_num = 1)

select
    id,
    employer__workplace,
    workplace_address__municipality,
    occupation__label,
    number_of_vacancies as vacancies,
    relevance,
    application_deadline,
    occupation_field__label as occupation_field
from latest_ads
order by application_deadline
