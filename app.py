from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import json
import os

app = Flask(__name__)
app.secret_key = 'ideal_star_secret_2026'
DB_NAME = "ideal.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS stars 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  position TEXT,
                  award TEXT,
                  photo_url TEXT,
                  date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS performance 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  target REAL,
                  current REAL,
                  percentage REAL,
                  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS announcements 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT,
                  content TEXT,
                  date TEXT,
                  deadline TEXT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM stars ORDER BY date DESC")
    stars = c.fetchall()
    c.execute("SELECT * FROM performance ORDER BY percentage DESC")
    performance = c.fetchall()
    conn.close()
    return render_template('index.html', stars=stars, performance=performance)

@app.route('/admin')
def admin():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM stars ORDER BY date DESC")
    stars = c.fetchall()
    c.execute("SELECT * FROM performance ORDER BY name")
    performance = c.fetchall()
    conn.close()
    return render_template('admin.html', stars=stars, performance=performance)

@app.route('/add_star', methods=['POST'])
def add_star():
    name = request.form.get('name')
    position = request.form.get('position')
    award = request.form.get('award')
    photo_url = request.form.get('photo_url')
    
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO stars (name, position, award, photo_url) VALUES (?, ?, ?, ?)",
              (name, position, award, photo_url))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

@app.route('/add_performance', methods=['POST'])
def add_performance():
    name = request.form.get('name')
    target = float(request.form.get('target') or 0)
    current = float(request.form.get('current') or 0)
    percentage = round((current / target * 100) if target > 0 else 0, 2)
    
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO performance (name, target, current, percentage) VALUES (?, ?, ?, ?)",
              (name, target, current, percentage))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

@app.route('/delete_star/<int:star_id>', methods=['POST'])
def delete_star(star_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM stars WHERE id = ?", (star_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

@app.route('/delete_performance/<int:perf_id>', methods=['POST'])
def delete_performance(perf_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM performance WHERE id = ?", (perf_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

@app.route('/init_test_data')
def init_test_data():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM stars")
    for i in range(1, 21):
        c.execute("INSERT INTO stars (name, position, award, photo_url) VALUES (?, ?, ?, ?)",
                  ('KEN', '業務副總', '年度業績總冠軍', f'/static/{i:02d}.jpg'))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))
