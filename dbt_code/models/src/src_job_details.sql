with deduped_ads as (
    select *,
    row_number() over (partition by id order by _dlt_load_id desc)
    as rn 

from {{ source('job_ads', 'stg_ads') }}
)

select
    id,
    headline,
    description__text as description,
    description__text_formatted as description_html,
    duration__label as duration,
    employment_type__label as employment_type,
    salary_type__label as salary_type,
    salary_description, 
    working_hours_type__label as working_hours_type,
    scope_of_work__min as scope_of_work_min,
    scope_of_work__max as scope_of_work_max
from deduped_ads
where rn = 1
order by application_deadline

