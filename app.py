from flask import Flask, render_template_string, redirect, url_for, Response, request, flash, session
import sqlite3, paho.mqtt.client as mqtt, csv, io, math, re

app = Flask(__name__)
app.secret_key = "saketh_ultra_secure_key"

# --- ANALYTICS ENGINE (The "Brain") ---
def get_analytics(temp, hum):
    vpsat = 0.61078 * math.exp((17.27 * temp) / (temp + 237.3))
    vpair = vpsat * (hum / 100.0)
    vpd = round(vpsat - vpair, 2)
    health = 100
    if temp > 32 or temp < 18: health -= 30
    if vpd < 0.5 or vpd > 1.5: health -= 30
    return vpd, max(health, 0)

# --- STYLING (The "Look") ---
BASE_STYLE = """
<style>
    body { font-family: 'Segoe UI', sans-serif; background: #f0f4f1; margin: 0; }
    .nav { background: #1b5e20; padding: 15px; text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.2); }
    .nav a { color: white; text-decoration: none; margin: 0 15px; font-weight: bold; }
    .container { max-width: 900px; margin: 40px auto; background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); }
    .card { background: #f9f9f9; padding: 20px; border-radius: 10px; border: 1px solid #eee; margin-bottom: 20px; text-align: center; }
    .val { font-size: 3em; font-weight: bold; color: #1b5e20; }
    .btn { display: inline-block; padding: 12px 24px; background: #2e7d32; color: white; border: none; border-radius: 5px; font-weight: bold; cursor: pointer; text-decoration:none; text-align:center;}
    .insight-box { background: #e8f5e9; border-left: 5px solid #1b5e20; padding: 15px; margin: 20px 0; font-size: 0.9em; }
    input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; }
</style>
"""

# --- SHARED NAVIGATION ---
def get_nav():
    return f"""<div class="nav">
        <a href="/">🏠 Home</a>
        <a href="/domain/analytics">🧬 System Health</a>
        <a href="/domain/control">🎮 Remote Protocols</a>
        <a href="/domain/history">📊 Growth Trends</a>
        <a href="/profile">👤 My Profile</a>
        <a href="/logout">🚪 Logout</a>
    </div>"""

# --- LOGIN / REGISTER ROUTES ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email, password = request.form['email'], request.form['password']
        conn = sqlite3.connect('garden.db')
        user = conn.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password)).fetchone()
        conn.close()
        if user:
            session['user_id'], session['user_name'] = user[0], user[1]
            return redirect(url_for('home'))
        flash("Invalid login.")
    return f"<html><head>{BASE_STYLE}</head><body><div class='container'><h2>Guardian Login</h2><form method='POST'><input name='email' placeholder='Gmail' required><input type='password' name='password' placeholder='Password' required><button type='submit' class='btn'>Login</button></form><br><a href='/register'>New? Register</a></div></body></html>"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        f = request.form
        conn = sqlite3.connect('garden.db')
        conn.execute("INSERT INTO users (fname, lname, email, phone, gender, age, password) VALUES (?,?,?,?,?,?,?)",
                     (f['fname'], f['lname'], f['email'], f['phone'], f['gender'], f['age'], f['password']))
        conn.commit(); conn.close()
        return redirect(url_for('login'))
    return f"<html><head>{BASE_STYLE}</head><body><div class='container'><h2>Join the Movement</h2><form method='POST'><input name='fname' placeholder='First Name'><input name='lname' placeholder='Last Name'><input name='email' placeholder='Gmail'><input name='phone' placeholder='Phone'><input type='number' name='age' placeholder='Age'><select name='gender'><option>Male</option><option>Female</option></select><input type='password' name='password' placeholder='Password'><button type='submit' class='btn'>Register</button></form></div></body></html>"

# --- DOMAIN: HOME ---
@app.route('/')
def home():
    if 'user_id' not in session: return redirect(url_for('login'))
    return f"<html><head>{BASE_STYLE}</head><body>{get_nav()}<div class='container' style='text-align:center;'><h1>Welcome, {session['user_name']}</h1><p>Your Horticulture Environment is being monitored 24/7.</p><div class='insight-box'><strong>Global Status:</strong> Smart systems like yours have historically improved crop yields by 25% through precision lighting.</div></div></body></html>"

# --- DOMAIN: ANALYTICS (Health & VPD) ---
@app.route('/domain/analytics')
def analytics():
    if 'user_id' not in session: return redirect(url_for('login'))
    conn = sqlite3.connect('garden.db')
    row = conn.execute('SELECT temperature, humidity FROM sensor_data ORDER BY timestamp DESC LIMIT 1').fetchone()
    conn.close()
    vpd, health = get_analytics(row[0], row[1])
    return f"""<html><head>{BASE_STYLE}</head><body>{get_nav()}
    <div class='container' style='text-align:center;'>
        <h2>Environment Health Analysis</h2>
        <div class='card'><h3>System Health Score</h3><div class='val'>{health}%</div></div>
        <div class='card'><h3>Vapor Pressure Deficit</h3><div class='val'>{vpd} kPa</div></div>
        <div class='insight-box'><strong>Historical Insight:</strong> Maintaining a health score above 80% prevents stomatal closure and ensures nutrient uptake.</div>
    </div></body></html>"""

# --- DOMAIN: HISTORY (The Graphs) ---
@app.route('/domain/history')
def history():
    if 'user_id' not in session: return redirect(url_for('login'))
    conn = sqlite3.connect('garden.db')
    rows = conn.execute('SELECT timestamp, sunlight, temperature FROM sensor_data ORDER BY timestamp DESC LIMIT 20').fetchall()
    conn.close()
    labels = [r[0].split(' ')[1] for r in rows][::-1]
    sun = [r[1] for r in rows][::-1]
    temp = [r[2] for r in rows][::-1]
    
    return f"""<html><head>{BASE_STYLE}<script src="https://cdn.jsdelivr.net/npm/chart.js"></script></head><body>{get_nav()}
    <div class='container'>
        <h2>Growth & Climate Trends</h2>
        <canvas id="chart"></canvas>
        <div class='insight-box'><strong>Trend Analysis:</strong> Historically, consistency in the Lux graph indicates a stable photosynthesis cycle. Fluctuations suggest cloud cover or sensor obstruction.</div>
    </div>
    <script>
        new Chart(document.getElementById('chart'), {{
            type: 'line',
            data: {{ 
                labels: {labels}, 
                datasets: [
                    {{ label: 'Sunlight (Lux)', data: {sun}, borderColor: '#1b5e20', tension: 0.4 }},
                    {{ label: 'Temp (C)', data: {temp}, borderColor: '#f44336', tension: 0.4 }}
                ]
            }}
        }});
    </script></body></html>"""

# --- DOMAIN: PROFILE (Update Logic) ---
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session: return redirect(url_for('login'))
    conn = sqlite3.connect('garden.db')
    if request.method == 'POST':
        conn.execute("UPDATE users SET phone=?, age=? WHERE id=?", (request.form['phone'], request.form['age'], session['user_id']))
        conn.commit()
        flash("Updated!")
    user = conn.execute("SELECT * FROM users WHERE id=?", (session['user_id'],)).fetchone()
    conn.close()
    return f"<html><head>{BASE_STYLE}</head><body>{get_nav()}<div class='container'><h2>Manage Profile</h2><form method='POST'>Phone: <input name='phone' value='{user[4]}'>Age: <input name='age' value='{user[6]}'><button type='submit' class='btn'>Save Changes</button></form></div></body></html>"

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)