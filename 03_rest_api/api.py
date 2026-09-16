"""
RESTful API in Flask
--------------------
Demonstrates standard HTTP verbs and JSON handling:
- GET    /items        : Retrieve all items
- GET    /items/<id>   : Retrieve a specific item
- POST   /items        : Create a new item (201 Created)
- PUT    /items/<id>   : Update an existing item
- DELETE /items/<id>   : Delete an item
"""

from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory storage for demo items
items = [
    {"id": 1, "name": "Item 1", "description": "This is item 1"},
    {"id": 2, "name": "Item 2", "description": "This is item 2"}
]


@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to the Sample To-Do List REST API",
        "endpoints": {
            "get_all": "GET /items",
            "get_one": "GET /items/<id>",
            "create": "POST /items",
            "update": "PUT /items/<id>",
            "delete": "DELETE /items/<id>"
        }
    })


# 1. GET: Retrieve all items
@app.route("/items", methods=["GET"])
def get_items():
    return jsonify(items), 200


# 2. GET: Retrieve a specific item by ID
@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = next((item for item in items if item["id"] == item_id), None)
    if item is None:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item), 200


# 3. POST: Create a new item
@app.route("/items", methods=["POST"])
def create_item():
    if not request.is_json or "name" not in request.json:
        return jsonify({"error": "Bad Request", "message": "'name' is required"}), 400

    new_id = items[-1]["id"] + 1 if items else 1
    new_item = {
        "id": new_id,
        "name": request.json["name"],
        "description": request.json.get("description", "")
    }
    items.append(new_item)
    return jsonify(new_item), 201


# 4. PUT: Update an existing item
@app.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    item = next((item for item in items if item["id"] == item_id), None)
    if item is None:
        return jsonify({"error": "Item not found"}), 404

    payload = request.get_json(silent=True) or {}
    item["name"] = payload.get("name", item["name"])
    item["description"] = payload.get("description", item["description"])
    return jsonify(item), 200


# 5. DELETE: Remove an item
@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    global items
    original_count = len(items)
    items = [item for item in items if item["id"] != item_id]
    if len(items) == original_count:
        return jsonify({"error": "Item not found"}), 404
    return jsonify({"result": "Item deleted", "id": item_id}), 200


if __name__ == "__main__":
    app.run(debug=True)
