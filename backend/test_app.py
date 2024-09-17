import pytest
from app import app, books_collection
from bson import ObjectId

@pytest.fixture
def client():
    # Use Flask's built-in test client
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Helper function to clean up the database after each test
@pytest.fixture(autouse=True)
def cleanup():
    # Drop the collection before each test to ensure isolation
    books_collection.delete_many({})
    yield
    books_collection.delete_many({})

def test_get_books_empty(client):
    """Test the GET /books endpoint when no books exist."""
    response = client.get('/books')
    assert response.status_code == 200
    assert response.json == []

def test_add_book(client):
    """Test adding a new book using POST /books."""
    new_book = {
        "title": "The Catcher in the Rye",
        "author": "J.D. Salinger"
    }
    response = client.post('/books', json=new_book)
    assert response.status_code == 201
    data = response.json
    assert "id" in data
    assert data["title"] == new_book["title"]
    assert data["author"] == new_book["author"]

    # Ensure that the book is actually added in the database
    book_in_db = books_collection.find_one({"_id": ObjectId(data["id"])})
    assert book_in_db is not None
    assert book_in_db["title"] == new_book["title"]
    assert book_in_db["author"] == new_book["author"]

def test_add_book_invalid_data(client):
    """Test adding a new book with invalid data."""
    # Missing title
    invalid_book = {"author": "Author without a title"}
    response = client.post('/books', json=invalid_book)
    assert response.status_code == 400
    assert response.json == {"error": "Invalid data"}

def test_delete_book(client):
    """Test deleting a book using DELETE /books/<id>."""
    # First, add a book to the database
    book_id = books_collection.insert_one({
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee"
    }).inserted_id

    # Then, try to delete the book
    response = client.delete(f'/books/{str(book_id)}')
    assert response.status_code == 200
    assert response.json == {"message": "Book deleted"}

    # Ensure that the book is actually deleted from the database
    book_in_db = books_collection.find_one({"_id": book_id})
    assert book_in_db is None

def test_delete_book_not_found(client):
    """Test deleting a non-existent book."""
    # Use a random ObjectId that doesn't exist in the database
    response = client.delete(f'/books/{str(ObjectId())}')
    assert response.status_code == 404
    assert response.json == {"message": "Book not found"}
