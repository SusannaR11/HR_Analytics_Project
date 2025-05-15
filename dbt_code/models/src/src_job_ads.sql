{# with stg_job_ads as (select * from {{ source("job_ads", "stg_ads") }})

select
    occupation__label,
    id,
    employer__workplace,
    workplace_address__municipality,
    number_of_vacancies as vacancies,
    relevance,
    application_deadline,
    occupation_field__concept_id
from
    stg_job_ads #}
with stg_job_ads as (select * from {{ source("job_ads", "stg_ads") }})

select
    id,
    employer__workplace,
    workplace_address__municipality,
    occupation__label,
    number_of_vacancies as vacancies,
    relevance,
    application_deadline,
    occupation_field__label as occupation_field
from stg_job_ads
order by application_deadline
