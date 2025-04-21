from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS
import MySQLdb.cursors

app = Flask(__name__)
CORS(app)

# Database Config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'F11'

mysql = MySQL(app)

# Register Route
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data['name']
    email = data['email']
    password = data['password']

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()

    if user:
        return jsonify({'status': 'error', 'message': 'Email already registered.'})

    cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'status': 'success', 'message': 'User registered successfully.'})


# Login Route
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
    user = cursor.fetchone()
    cursor.close()

    if user:
        return jsonify({'status': 'success', 'message': 'Login successful.', 'user': user})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid credentials.'})


if __name__ == '__main__':
    app.run(debug=True)
