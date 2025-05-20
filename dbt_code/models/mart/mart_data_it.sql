-- mart for data it
{# with ads as (
    select
        fact.*,
        occ.occupation,
        job.headline,
        job.description,
        aux.driver_license_text,
        aux.access_to_own_car_text,
        emp.municipality
    from {{ ref('fct_job_ads') }} fact
    left join {{ ref('dim_occupation') }} occ on fact.occupation_id = occ.occupation_id
    left join {{ ref('dim_job_details') }} job on fact.job_details_id = job.job_details_id
    left join {{ ref('dim_auxiliary_attributes') }} aux on fact.auxiliary_attributes_id = aux.auxiliary_attributes_id
    left join {{ ref('dim_employer_name') }} emp on fact.employer_id = emp.employer__name
    where fact.occupation_field__concept_id = 'apaJ_2ja_LuF'
)
select *
from ads #}
with
    fct_job_ads as (select * from {{ ref("fct_job_ads") }}),
    dim_job_details as (select * from {{ ref("dim_job_details") }}),
    dim_occupation as (select * from {{ ref("dim_occupation") }}),
    dim_employer as (select * from {{ ref("dim_employer") }}),
    dim_auxiliary_attributes as (select * from {{ ref("dim_auxiliary_attributes") }})
select
    jd.headline,
    f.vacancies,
    f.relevance,
    e.employer_name,
    e.workplace_city,
    e.employer_workplace,
    e.workplace_country,
    e.workplace_region,
    e.workplace_municipality,
    o.occupation,
    o.occupation_group,
    o.occupation_field,
    f.application_deadline,
    jd.description,
    jd.description_html,
    jd.duration,
    jd.salary_type,
    jd.salary_description,
    jd.working_hours_type
from fct_job_ads f
left join dim_job_details jd on f.job_details_id = jd.job_details_id
left join dim_occupation o on f.occupation_id = o.occupation_id
left join dim_employer e on f.employer_id = e.employer_id
left join
    dim_auxiliary_attributes a on f.auxiliary_attributes_id = a.auxiliary_attributes_id
where o.occupation_field = 'Data/IT'
