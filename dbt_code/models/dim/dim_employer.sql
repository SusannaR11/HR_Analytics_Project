-- create table employer with relevant columns

with employer as (select * from {{ ref('src_job_ads') }})

select
    {{ dbt_utils.generate_surrogate_key(['id']) }} as employer_id,-- id måste va unique muni... kolla code along
    employer_name,
    employer_workplace,
    employer_organization_number,
    workplace_address__street_address,
    workplace_address__region,
    workplace_address__postcode,
    workplace_address__city,
    workplace_address__country
from employer
# gör src för duplicate.. kolla repo...