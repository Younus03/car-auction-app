from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from db_config import get_db_connection

app = Flask(__name__)
app.secret_key = "secret_key"


def ensure_inquiries_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS car_inquiries (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NULL,
                full_name VARCHAR(150) NOT NULL,
                email VARCHAR(150) NOT NULL,
                phone VARCHAR(30) NOT NULL,
                city VARCHAR(100) NOT NULL,
                car_type VARCHAR(100) NOT NULL,
                brand VARCHAR(100) NOT NULL,
                model VARCHAR(100) NOT NULL,
                budget VARCHAR(100) NOT NULL,
                color VARCHAR(50) NOT NULL,
                transmission VARCHAR(50) NOT NULL,
                fuel_type VARCHAR(50) NOT NULL,
                ownership VARCHAR(100) NOT NULL,
                year_range VARCHAR(50) NOT NULL,
                timeline VARCHAR(100) NOT NULL,
                features TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT fk_car_inquiries_user
                    FOREIGN KEY (user_id) REFERENCES users(id)
                    ON DELETE SET NULL
            )
            """
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()

# Home -> Login
@app.route('/')
def home():
    return render_template('login.html', error=None)

# Register Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        phone = request.form['phone']

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (name, email, password, phone) VALUES (%s, %s, %s, %s)",
                (name, email, password, phone)
            )
            conn.commit()

        except Exception as e:
            print("DB ERROR:", e)
            conn.rollback()

        finally:
            cursor.close()
            conn.close()

        return redirect('/')

    return render_template('register.html')

# Login
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user and check_password_hash(user['password'], password):
        session['user'] = user['name']
        session['user_id'] = user.get('id')
        return redirect('/dashboard')

    return render_template('login.html', error="Invalid email or password. Please try again.")

# Dashboard
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user' in session:
        inquiry = None
        form_message = None
        message_type = None

        if request.method == 'POST':
            inquiry = {
                'full_name': request.form['full_name'],
                'email': request.form['email'],
                'phone': request.form['phone'],
                'city': request.form['city'],
                'car_type': request.form['car_type'],
                'brand': request.form['brand'],
                'model': request.form['model'],
                'budget': request.form['budget'],
                'color': request.form['color'],
                'transmission': request.form['transmission'],
                'fuel_type': request.form['fuel_type'],
                'ownership': request.form['ownership'],
                'year_range': request.form['year_range'],
                'timeline': request.form['timeline'],
                'features': request.form.get('features', ''),
                'notes': request.form.get('notes', '')
            }

            conn = get_db_connection()
            cursor = conn.cursor()

            try:
                cursor.execute(
                    """
                    INSERT INTO car_inquiries (
                        user_id, full_name, email, phone, city, car_type, brand, model,
                        budget, color, transmission, fuel_type, ownership, year_range,
                        timeline, features, notes
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        session.get('user_id'),
                        inquiry['full_name'],
                        inquiry['email'],
                        inquiry['phone'],
                        inquiry['city'],
                        inquiry['car_type'],
                        inquiry['brand'],
                        inquiry['model'],
                        inquiry['budget'],
                        inquiry['color'],
                        inquiry['transmission'],
                        inquiry['fuel_type'],
                        inquiry['ownership'],
                        inquiry['year_range'],
                        inquiry['timeline'],
                        inquiry['features'],
                        inquiry['notes']
                    )
                )
                conn.commit()
                form_message = (
                    f"Inquiry saved for {inquiry['brand']} {inquiry['model']}. "
                    "Your buyer preferences are now stored in MySQL."
                )
                message_type = "success"
            except Exception as e:
                print("INQUIRY DB ERROR:", e)
                conn.rollback()
                form_message = "We could not save the inquiry right now. Please check your database setup and try again."
                message_type = "error"
            finally:
                cursor.close()
                conn.close()

        return render_template(
            'dashboard.html',
            user=session['user'],
            inquiry=inquiry,
            form_message=form_message,
            message_type=message_type
        )
    return redirect('/')

# Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('user_id', None)
    return redirect('/')

if __name__ == '__main__':
    ensure_inquiries_table()
    app.run(debug=True)
