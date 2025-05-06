-- create table auxiliary_attributes

with auxiliary_attributes as (select * from {{ ref('src_job_ads') }})

select
    {{ dbt_utils.generate_surrogate_key(['id']) }} as auxiliary_attributes_id,
    coalesce(experience_required, false) as experience_required, -- checking boolean 
    coalesce(driving_license_required, false) as driver_license,
    coalesce(access_to_own_car, false) as access_to_own_car
from auxiliary_attributes