import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';  // Import the CSS file for styling

const API_URL = 'http://localhost:5000/books';  // Adjust if your Flask server runs on a different port

function App() {
  const [books, setBooks] = useState([]);
  const [title, setTitle] = useState('');
  const [author, setAuthor] = useState('');

  useEffect(() => {
    fetchBooks();
  }, []);

  const fetchBooks = async () => {
    try {
      const response = await axios.get(API_URL);
      setBooks(response.data);
    } catch (error) {
      console.error("Error fetching books:", error);
    }
  };

  const addBook = async () => {
    try {
      const newBook = { title, author };
      await axios.post(API_URL, newBook);
      setTitle('');
      setAuthor('');
      fetchBooks();  // Refresh the book list
    } catch (error) {
      console.error("Error adding book:", error);
    }
  };

  const deleteBook = async (id) => {
    try {
      await axios.delete(`${API_URL}/${id}`);
      fetchBooks();  // Refresh the book list
    } catch (error) {
      console.error("Error deleting book:", error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Bookstore</h1>
      </header>
      <main className="App-main">
        <div className="AddBookForm">
          <input
            type="text"
            placeholder="Title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="Form-input"
          />
          <input
            type="text"
            placeholder="Author"
            value={author}
            onChange={(e) => setAuthor(e.target.value)}
            className="Form-input"
          />
          <button onClick={addBook} className="Form-button">Add Book</button>
        </div>
        <ul className="BookList">
          {books.map((book) => (
            <li key={book.id} className="BookItem">
              <span className="BookTitle">{book.title}</span> by <span className="BookAuthor">{book.author}</span>
              <button onClick={() => deleteBook(book.id)} className="BookButton">Delete</button>
            </li>
          ))}
        </ul>
      </main>
    </div>
  );
}

export default App;
