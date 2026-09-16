### Flask Error Handling & Custom HTTP Status Codes
"""
This module demonstrates:
1. Returning custom HTTP status codes (200, 201, 400, 404, 500)
2. Using abort() to trigger errors explicitly
3. Creating custom error handler functions with @app.errorhandler()
4. Handling unhandled exceptions gracefully
"""

from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# Sample in-memory database
books = [
    {"id": 1, "title": "Flask Web Development", "author": "Miguel Grinberg"},
    {"id": 2, "title": "Fluent Python", "author": "Luciano Ramalho"}
]


@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to the Error Handling & HTTP Status Code demo!",
        "endpoints": {
            "get_all_books": "GET /books",
            "get_book_by_id": "GET /books/<id>",
            "add_book": "POST /books",
            "divide_numbers": "GET /divide?a=<num>&b=<num>",
            "trigger_abort": "GET /trigger-403"
        }
    }), 200


# 1. Custom status code: 200 OK
@app.route("/books", methods=["GET"])
def get_books():
    return jsonify(books), 200


# 2. Using abort() and returning 404 Not Found
@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if book is None:
        # abort(status_code, description) interrupts the request and raises an HTTPException
        abort(404, description=f"Book with id {book_id} not found.")
    return jsonify(book), 200


# 3. Custom status codes: 201 Created and 400 Bad Request
@app.route("/books", methods=["POST"])
def create_book():
    data = request.get_json()

    # Client-side validation: return 400 Bad Request if title is missing
    if not data or "title" not in data:
        return jsonify({
            "error": "Bad Request",
            "message": "'title' field is required."
        }), 400

    new_book = {
        "id": len(books) + 1,
        "title": data["title"],
        "author": data.get("author", "Unknown")
    }
    books.append(new_book)
    # 201 indicates a resource was successfully created
    return jsonify(new_book), 201


# 4. Triggering specific HTTP errors with abort()
@app.route("/trigger-403")
def forbidden_route():
    abort(403, description="You do not have permission to access this resource.")


# 5. Handling calculation error (Internal Server Error / ZeroDivisionError)
@app.route("/divide", methods=["GET"])
def divide():
    a = request.args.get("a", type=float)
    b = request.args.get("b", type=float)

    if a is None or b is None:
        return jsonify({
            "error": "Bad Request",
            "message": "Please provide both 'a' and 'b' query parameters (e.g., /divide?a=10&b=2)"
        }), 400

    # If b == 0, this will raise ZeroDivisionError and trigger @app.errorhandler(ZeroDivisionError)
    result = a / b
    return jsonify({"a": a, "b": b, "result": result}), 200


# -------------------------------------------------------------
# CUSTOM ERROR HANDLERS
# -------------------------------------------------------------

# Custom handler for 404 Not Found
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({
        "error": "Not Found",
        "message": error.description if hasattr(error, "description") else "The requested URL was not found on the server.",
        "status_code": 404
    }), 404


# Custom handler for 403 Forbidden
@app.errorhandler(403)
def forbidden_error(error):
    return jsonify({
        "error": "Forbidden",
        "message": error.description if hasattr(error, "description") else "Access is forbidden.",
        "status_code": 403
    }), 403


# Custom handler for 400 Bad Request
@app.errorhandler(400)
def bad_request_error(error):
    return jsonify({
        "error": "Bad Request",
        "message": error.description if hasattr(error, "description") else "Invalid request data.",
        "status_code": 400
    }), 400


# Custom handler for specific Python exceptions (e.g., ZeroDivisionError)
@app.errorhandler(ZeroDivisionError)
def handle_zero_division(error):
    return jsonify({
        "error": "Math Error",
        "message": "Division by zero is not allowed.",
        "status_code": 400
    }), 400


# Generic handler for uncaught server errors (500 Internal Server Error)
@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "error": "Internal Server Error",
        "message": "An unexpected error occurred on the server.",
        "status_code": 500
    }), 500


if __name__ == "__main__":
    app.run(debug=True)
