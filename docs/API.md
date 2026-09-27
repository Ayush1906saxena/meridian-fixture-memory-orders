# Orders API

| Method | Path | What it does |
|---|---|---|
| POST | /orders | Create an order from `customer` and `total_cents`; returns its id |
| GET | /orders | Every order, oldest first |
| GET | /orders/<int:order_id> | One order, or 404 |
