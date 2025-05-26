
with deduped_ads as (
    select * ,
    row_number() over (partition by id order by _dlt_load_id desc)
    as rn 

from {{ source('job_ads', 'stg_ads') }}
)

select
    id,
    experience_required,
    driving_license_required,
    access_to_own_car
from deduped_ads
where rn = 1

