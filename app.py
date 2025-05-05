from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_mysqldb import MySQL
import os

app = Flask(__name__)

# Configuration for MySQL
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', 'Sarvesh@123')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'cloudtasker')

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()
    cur.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    title = request.form['title']
    description = request.form['description']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO tasks(title, description) VALUES(%s, %s)", (title, description))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_task(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM tasks WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

@app.route('/health')
def health():
    return jsonify(status="ok"), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
