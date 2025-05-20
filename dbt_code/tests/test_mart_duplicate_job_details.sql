-- testing duplicates
select job_details_id, count(*) as antal
from {{ ref("mart_data_it") }}
group by job_details_id
having
    count(*) > 1
    {# SELECT job_details_id, COUNT(*)
FROM marts.mart_data_it
GROUP BY job_details_id
HAVING COUNT(*) > 1 #}
    
