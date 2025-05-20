{# WITH example_ids AS (
    SELECT 123 AS user_id, 123 AS product_id
    UNION ALL
    SELECT 123 AS user_id, NULL AS product_id
    UNION ALL
    SELECT NULL AS user_id, 123 AS product_id
    UNION ALL
    SELECT 1231 AS user_id, 23 AS product_id
)

SELECT
    user_id,
    product_id,
    {{ dbt_utils.generate_surrogate_key(['user_id', 'product_id']) }} AS skey
FROM
    example_ids #}
-- this is to test that the macro can handle null value and separator when generating
-- surrogate key
-- run with dbt test -s
with
    example as (
        select 123 as user_id, 123 as product_id
        union all
        select 123 as user_id, null as product_id
        union all
        select null as user_id, 123 as product_id
        union all
        select 1231 as user_id, 23 as product_id
    ),
    example_with_key as (
        select
            user_id,
            product_id,
            {{ dbt_utils.generate_surrogate_key(["user_id", "product_id"]) }} as skey
        from example
    )

-- for an overview of data with jinja sql
{# select *
from
    example_with_key #}

    -- for dbt test to check if there is duplicates in skey
    SELECT skey
FROM example_with_key
GROUP BY skey
HAVING COUNT(*) > 1
    
