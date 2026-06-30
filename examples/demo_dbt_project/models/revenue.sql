select
    o.order_id,
    o.customer_id,
    o.order_amount
from {{ ref('orders') }} as o
