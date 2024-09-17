import pytest
import mongomock
from pymongo import MongoClient
from app import app, get_db

@pytest.fixture
def client():
    """Flask's built-in test client for making requests."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Mock the entire database client instead of just the collection
@pytest.fixture(autouse=True)
def mock_db(monkeypatch):
    """Mock MongoDB client using mongomock."""
    mock_client = mongomock.MongoClient()

    # Override the get_db function to return the mock database
    def mock_get_db():
        return mock_client['bookstore']

    # Patch the get_db function used in your application
    monkeypatch.setattr('app.get_db', mock_get_db)

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

    # Ensure that the book is actually added in the mock database
    book_in_db = get_db().books.find_one({"_id": ObjectId(data["id"])})
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
    # First, add a book to the mock database
    book_id = get_db().books.insert_one({
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee"
    }).inserted_id

    # Then, try to delete the book
    response = client.delete(f'/books/{str(book_id)}')
    assert response.status_code == 200
    assert response.json == {"message": "Book deleted"}

    # Ensure that the book is actually deleted from the mock database
    book_in_db = get_db().books.find_one({"_id": book_id})
    assert book_in_db is None

def test_delete_book_not_found(client):
    """Test deleting a non-existent book."""
    # Use a random ObjectId that doesn't exist in the mock database
    response = client.delete(f'/books/{str(ObjectId())}')
    assert response.status_code == 404
    assert response.json == {"message": "Book not found"}
