with source_data as (
    select 1 as customer_id, 'Alice' as customer_name
)

select
    customer_id,
    customer_name
from source_data
