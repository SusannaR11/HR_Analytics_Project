-- mart for data it
with ads as (
    select
        fa.*,
        do.occupation_name,
        dj.headline,
        dj.description,
        da.driver_license_text,
        da.access_to_own_car_text,
        de.workplace_city
    from {{ ref('fct_job_ads') }} fa
    left join {{ ref('dim_occupation') }} do on fa.occupation_id = do.occupation_id
    left join {{ ref('dim_job_details') }} dj on fa.job_details_id = dj.job_details_id
    left join {{ ref('dim_auxiliary_attributes') }} da on fa.auxiliary_attributes_id = da.auxiliary_attributes_id
    left join {{ ref('dim_employer') }} de on fa.employer_id = de.employer_id
    where fa.occupation_group_id = 'apaJ_2ja_LuF'
)
select *
from ads
