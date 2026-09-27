def test_create_and_read_an_order(client):
    created = client.post("/orders", json={"customer": "Asha", "total_cents": 1250})
    assert created.status_code == 201
    order = client.get(f"/orders/{created.get_json()['id']}").get_json()
    assert order["customer"] == "Asha"
    assert order["total_cents"] == 1250


def test_rejects_a_negative_total(client):
    assert client.post("/orders", json={"customer": "Asha", "total_cents": -1}).status_code == 400


def test_lists_orders_in_order(client):
    client.post("/orders", json={"customer": "A", "total_cents": 1})
    client.post("/orders", json={"customer": "B", "total_cents": 2})
    assert [o["customer"] for o in client.get("/orders").get_json()] == ["A", "B"]


def test_missing_order_is_404(client):
    assert client.get("/orders/99").status_code == 404
