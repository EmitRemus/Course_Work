import os
from encryption import encrypt, generate_salt, decrypt
import pyrebase
from flask import Flask, render_template, request, redirect, url_for, flash, session
from db_interactions import get_user_by_email, insert_user, get_user_id, get_encrypted_passwords, \
    insert_password, update_password, delete_password_by_id, get_password_by_id

config = {
    'apiKey': os.environ["FIREBASE_API_KEY"],
    'authDomain': "passsave-7682c.firebaseapp.com",
    'databaseURL': "https://passsave-7682c-default-rtdb.europe-west1.firebasedatabase.app",
    'projectId': "passsave-7682c",
    'storageBucket': "passsave-7682c.appspot.com",
    'messagingSenderId': "672840974598",
    'appId': "1:672840974598:web:0a25248cc03b313409de87",
    'measurementId': "G-9YYBMQJH5Z"
}

app = Flask(__name__)
app.secret_key = 'admin'

firebase = pyrebase.initialize_app(config)
authi = firebase.auth()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            user = authi.sign_in_with_email_and_password(email, password)
            session["user"] = user["email"]

            flash('Logged in successfully')
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash(f'Error logging in: {str(e)}')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        try:
            authi.send_password_reset_email(email)
            flash('Password reset link sent to your email')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Error sending password reset email: {str(e)}')
            return redirect(url_for('forgot_password'))

    return render_template('forgot_password.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        if password != confirm_password:
            flash('Passwords do not match')
            return redirect(url_for('signup'))

        existing_user = get_user_by_email(email)

        if existing_user:
            flash('This email is already in use')
            return redirect(url_for('signup'))

        try:

            authi.create_user_with_email_and_password(email, password)

            name = email.split('@')[0]
            insert_user(email, name)

            flash('User created successfully')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Error creating user: {str(e)}')
            return redirect(url_for('signup'))

    return render_template('signup.html')


@app.route('/info')
def info():
    return render_template('info.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    passwords = []

    if request.method == 'POST':
        passcode = request.form['passcode']
        if passcode:  # Ensure passcode is provided
            user_id = get_user_id(session['user'])
            encrypted_passwords = get_encrypted_passwords(user_id)

            for ep in encrypted_passwords:
                try:
                    decrypted_password = decrypt(ep['password'], ep['salt'], ep['iv_password'], passcode)
                except Exception:
                    decrypted_password = "Decryption failed"

                try:
                    decrypted_description = decrypt(ep['used_for'], ep['salt'], ep['iv_used_for'], passcode)
                except Exception:
                    decrypted_description = "Decryption failed"

                passwords.append({'what_for': decrypted_description, 'password': decrypted_password,
                                  'password_id': ep['password_id']})

            return render_template('dashboard.html', user=session["user"], passwords=passwords)

        else:
            flash('Passcode is required')
            return redirect(url_for('dashboard'))

    return render_template('dashboard.html', user=session["user"], passwords=passwords)


@app.route('/add_password', methods=['GET', 'POST'])
def add_password():
    if 'user' not in session:
        flash('You need to log in first')
        return redirect(url_for('login'))

    if request.method == 'POST':
        password = request.form['password']
        description = request.form['description']
        passcode = request.form['passcode']

        salt = generate_salt()

        encrypted_password, iv_password = encrypt(password, passcode, salt)
        encrypted_description, iv_description = encrypt(description, passcode, salt)

        user_id = get_user_id(session['user'])

        insert_password(user_id, encrypted_password, encrypted_description, salt, iv_password, iv_description)

        flash('Password saved successfully')
        return redirect(url_for('dashboard'))

    return render_template('add_password.html')


@app.route('/edit_password/<int:id>', methods=['GET', 'POST'])
def edit_password(id):
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        password = request.form['password']
        description = request.form['description']
        passcode = request.form['passcode']

        salt = generate_salt()

        encrypted_password, iv_password = encrypt(password, passcode, salt)
        encrypted_description, iv_description = encrypt(description, passcode, salt)

        update_password(id, encrypted_password, encrypted_description, salt, iv_password, iv_description)

        flash('Password updated successfully')
        return redirect(url_for('dashboard'))

    password_entry = get_password_by_id(id)

    passcode = request.args.get('passcode', None)
    if passcode:
        try:
            password_entry['password'] = decrypt(password_entry['password'], password_entry['salt'],
                                                 password_entry['iv_password'], passcode)
            password_entry['used_for'] = decrypt(password_entry['used_for'], password_entry['salt'],
                                                 password_entry['iv_used_for'], passcode)
        except Exception:
            flash('Decryption failed. Please provide the correct passcode.')
            return redirect(url_for('dashboard'))

    return render_template('edit_password.html', password_entry=password_entry)


@app.route('/delete_password/<int:id>')
def delete_password(id):
    if 'user' not in session:
        return redirect(url_for('login'))

    delete_password_by_id(id)

    flash('Password deleted successfully')
    return redirect(url_for('dashboard'))


@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
