# Import necessary modules
from flask import Flask, jsonify, request
import db
from flask_cors import CORS

# Create Flask app instance
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS)
CORS(app)

# Create database table if not exists
db.create_table()

# Define route for serving the frontend HTML file
@app.route('/')
def index():
    return app.send_static_file('frontend.html')

# Define route for handling GET and POST requests to '/books'
@app.route('/books', methods=['GET', 'POST'])
def books():
    # Establish database connection
    conn = db.db_connection()
    cursor = conn.cursor()

    # Handle GET request to retrieve all books
    if request.method == 'GET':
        sql = """ 
                SELECT * FROM books 
            """
        cursor.execute(sql)
        books = [
            dict(
                id=row['id'],
                title=row['title'],
                author=row['author'],
                publisher=row['publisher'],
                language=row['language']
            )
            for row in cursor.fetchall()
        ]
        if books is not None:
            return jsonify(books)
    
    # Handle POST request to add a new book
    elif request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        publisher = request.form['publisher']
        language = request.form['language']

        sql = """
                INSERT INTO books (title, author, publisher, language)
                VALUES (%s, %s, %s, %s)
            """
        cursor.execute(sql, (title, author, publisher, language))
        conn.commit()
        return jsonify({'message': 'Book added successfully!'})

# Define route for handling GET, PUT, and DELETE requests to '/books/<book_id>'
@app.route('/books/<int:book_id>', methods=['GET', 'PUT', 'DELETE'])
def single_book(book_id):
    # Establish database connection
    conn = db.db_connection()
    cursor = conn.cursor()

    # Initialize book variable
    book = None

    # Handle GET request to retrieve a single book
    if request.method == 'GET':
        sql_query = '''
                        SELECT * FROM books WHERE id = %s
                    '''
        cursor.execute(sql_query, (book_id,))
        rows = cursor.fetchall()
        for row in rows:
            book = row  
        if book is not None:
            return jsonify(book), 200
        else:
            return jsonify({'message': 'Book not found!'})

    # Handle PUT request to update a book
    elif request.method == 'PUT':
        sql_query = '''
                    UPDATE books 
                    SET title = %s, author = %s, publisher = %s, language = %s
                    WHERE id = %s
                '''
        title = request.form['title']
        author = request.form['author']
        publisher = request.form['publisher']
        language = request.form['language']

        updated_book = {
            'id': book_id,
            'title': title,
            'author': author,
            'publisher': publisher,
            'language': language,
        }
 
        cursor.execute(sql_query, (title, author, publisher, language, book_id))
        conn.commit()
        return jsonify({'message': 'Book updated successfully!'}, updated_book)

    # Handle DELETE request to delete a book
    elif request.method == 'DELETE':
        sql_query = """
                        DELETE FROM books WHERE id = %s
                    """
        cursor.execute(sql_query, (book_id,))
        conn.commit()
        return jsonify({'message': f'Book {book_id} deleted successfully!'})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
