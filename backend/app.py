from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Connect to MongoDB
def get_db():
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client.bookstore
        return db
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        raise e

# Use the get_db() function to get the books collection
def get_books_collection():
    return get_db().books

# Convert MongoDB ObjectId to string
def book_serializer(book):
    return {
        "id": str(book["_id"]),
        "title": book["title"],
        "author": book["author"]
    }

# Get all books from MongoDB
@app.route('/books', methods=['GET'])
def get_books():
    books = get_books_collection().find()
    return jsonify([book_serializer(book) for book in books]), 200

# Add a new book to MongoDB
@app.route('/books', methods=['POST'])
def add_book():
    new_book = request.json
    if not new_book or 'title' not in new_book or 'author' not in new_book:
        return jsonify({"error": "Invalid data"}), 400
    books_collection = get_books_collection()
    book_id = books_collection.insert_one(new_book).inserted_id
    return jsonify(book_serializer(books_collection.find_one({"_id": book_id}))), 201

# Delete a book by ID from MongoDB
@app.route('/books/<string:id>', methods=['DELETE'])
def delete_book(id):
    books_collection = get_books_collection()
    result = books_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count:
        return jsonify({"message": "Book deleted"}), 200
    return jsonify({"message": "Book not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
