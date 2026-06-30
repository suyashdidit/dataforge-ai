with customer_orders as (
    select 1 as order_id, 1 as customer_id, 100.0 as order_amount
)

select
    order_id,
    customer_id,
    order_amount
from {{ ref('customers') }}
