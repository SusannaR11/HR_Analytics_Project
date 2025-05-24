-- Find duplicates in occupation_data_it
SELECT 'occupation_data_it' AS source_table, job_details_id, COUNT(*) AS antal
FROM {{ ref('occupation_data_it') }}
GROUP BY job_details_id
HAVING COUNT(*) > 1

UNION ALL

-- Find duplicates in occupation_sakerhet_bevakning
SELECT 'occupation_sakerhet_bevakning' AS source_table, job_details_id, COUNT(*) AS antal
FROM {{ ref('occupation_sakerhet_bevakning') }}
GROUP BY job_details_id
HAVING COUNT(*) > 1

UNION ALL

-- Find duplicates in occupation_socialt_arbete
SELECT 'occupation_socialt_arbete' AS source_table, job_details_id, COUNT(*) AS antal
FROM {{ ref('occupation_socialt_arbete') }}
GROUP BY job_details_id
HAVING COUNT(*) > 1