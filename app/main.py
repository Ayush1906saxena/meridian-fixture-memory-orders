from flask import Flask, abort, jsonify, request

from app import db


def create_app(db_path="orders.db"):
    app = Flask(__name__)
    app.config["DB_PATH"] = db_path

    def conn():
        c = db.connect(app.config["DB_PATH"])
        db.init(c)
        return c

    @app.post("/orders")
    def create_order():
        data = request.get_json(silent=True) or {}
        customer = data.get("customer")
        total = data.get("total_cents")
        if not customer or not isinstance(total, int) or total < 0:
            return jsonify(error="customer and a non-negative integer total_cents are required"), 400
        order_id = db.add_order(conn(), customer, total)
        return jsonify(id=order_id), 201

    @app.get("/orders")
    def list_orders():
        return jsonify([dict(r) for r in db.list_orders(conn())])

    @app.get("/orders/<int:order_id>")
    def get_order(order_id):
        row = db.get_order(conn(), order_id)
        if row is None:
            abort(404)
        return jsonify(dict(row))

    return app
