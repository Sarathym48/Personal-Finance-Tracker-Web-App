from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="financeuser",
    password="financepass",
    database="finance_db"
)
cursor = db.cursor(dictionary=True)  # dictionary=True makes fetch return dicts

# ---------------- User Authentication ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = generate_password_hash(password)

        # Check if user exists
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        if cursor.fetchone():
            flash("Username already exists!", "error")
            return redirect(url_for('register'))

        cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, password_hash))
        db.commit()
        flash("Registration successful! Please login.", "success")
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('index'))
        else:
            flash("Invalid username or password!", "error")
            return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ---------------- HTML Routes ----------------
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cursor.execute("SELECT * FROM transactions WHERE user_id=%s ORDER BY transaction_date DESC", (session['user_id'],))
    transactions = cursor.fetchall()
    return render_template('index.html', transactions=transactions, username=session['username'])


@app.route('/add', methods=['GET', 'POST'])
def add_transaction():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        category = request.form['category']
        amount = float(request.form['amount'])
        description = request.form['description']

        cursor.execute(
            "INSERT INTO transactions (user_id, category, amount, description) VALUES (%s, %s, %s, %s)",
            (session['user_id'], category, amount, description)
        )
        db.commit()
        return redirect(url_for('index'))
    return render_template('add_transaction.html')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_transaction(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        category = request.form['category']
        amount = float(request.form['amount'])
        description = request.form['description']

        cursor.execute(
            "UPDATE transactions SET category=%s, amount=%s, description=%s WHERE id=%s AND user_id=%s",
            (category, amount, description, id, session['user_id'])
        )
        db.commit()
        return redirect(url_for('index'))
    else:
        cursor.execute("SELECT * FROM transactions WHERE id=%s AND user_id=%s", (id, session['user_id']))
        transaction = cursor.fetchone()
        return render_template('edit_transaction.html', transaction=transaction)


@app.route('/delete/<int:id>')
def delete_transaction(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cursor.execute("DELETE FROM transactions WHERE id=%s AND user_id=%s", (id, session['user_id']))
    db.commit()
    return redirect(url_for('index'))

# ---------------- RESTful API Routes ----------------
@app.route('/api/transactions', methods=['GET'])
def api_get_transactions():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    cursor.execute("SELECT * FROM transactions WHERE user_id=%s ORDER BY transaction_date DESC", (session['user_id'],))
    transactions = cursor.fetchall()
    return jsonify(transactions)


@app.route('/api/transactions/<int:id>', methods=['GET'])
def api_get_transaction(id):
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    cursor.execute("SELECT * FROM transactions WHERE id=%s AND user_id=%s", (id, session['user_id']))
    transaction = cursor.fetchone()
    if transaction:
        return jsonify(transaction)
    else:
        return jsonify({"error": "Transaction not found"}), 404


@app.route('/api/transactions', methods=['POST'])
def api_add_transaction():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    category = data.get('category')
    amount = data.get('amount')
    description = data.get('description', '')

    cursor.execute(
        "INSERT INTO transactions (user_id, category, amount, description) VALUES (%s, %s, %s, %s)",
        (session['user_id'], category, amount, description)
    )
    db.commit()
    return jsonify({"message": "Transaction added successfully"}), 201


@app.route('/api/transactions/<int:id>', methods=['PUT'])
def api_update_transaction(id):
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    category = data.get('category')
    amount = data.get('amount')
    description = data.get('description', '')

    cursor.execute(
        "UPDATE transactions SET category=%s, amount=%s, description=%s WHERE id=%s AND user_id=%s",
        (category, amount, description, id, session['user_id'])
    )
    db.commit()
    return jsonify({"message": "Transaction updated successfully"})


@app.route('/api/transactions/<int:id>', methods=['DELETE'])
def api_delete_transaction(id):
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    cursor.execute("DELETE FROM transactions WHERE id=%s AND user_id=%s", (id, session['user_id']))
    db.commit()
    return jsonify({"message": "Transaction deleted successfully"})

# ---------------- Run App ----------------
if __name__ == '__main__':
    app.run(debug=True)
