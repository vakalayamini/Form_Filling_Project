from flask import Flask, render_template, request, redirect, flash
import os
import whisper
from googletrans import Translator
# Render port binding
PORT = int(os.getenv("PORT", 5000))
# Flask app setup
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Load the Whisper model
model = whisper.load_model("tiny")

# Translator for multilingual support
translator = Translator()

# Function to transcribe speech and translate it
def transcribe_speech(audio_path, target_language='en'):
    result = model.transcribe(audio_path)
    original_text = result['text']
    if target_language != 'en':
        translated_text = translator.translate(original_text, dest=target_language).text
        return translated_text
    return original_text

# In-memory user data storage
users = []

# Home route
@app.route('/')
def home():
    return render_template('home.html')

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if email already exists
        if any(user['email'] == email for user in users):
            flash("Account already exists!", "error")
            return redirect('/signup')

        # Add new user
        users.append({'email': email, 'password': password})
        flash("Signup successful! Please login.", "success")
        return redirect('/login')

    return render_template('signup.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check credentials
        if email == 'admin@gmail.com' and password == 'admin123':
            flash("Welcome Admin!", "success")
            return redirect('/form')
        elif any(user['email'] == email and user['password'] == password for user in users):
            flash("Login successful!", "success")
            return redirect('/form')
        else:
            flash("Invalid username or password.", "error")
            return redirect('/login')

    return render_template('login.html')

# Form filling route
@app.route('/form', methods=['GET', 'POST'])
def form_filling():
    if request.method == 'POST':
        try:
            first_name = request.form['firstName']
            last_name = request.form['lastName']
            father_name = request.form['fatherName']
            mother_name = request.form['motherName']
            dob = request.form['dob']
            gender = request.form['gender']
            phone = request.form['phone']
            email = request.form['email']
            bloodgroup = request.form['bloodGroup']
            address = request.form['address']
            branch = request.form['branch']
            section = request.form['section']
            roll_number = request.form['rollNumber']
            year_of_study = request.form['yearOfStudy']
            percentage = request.form['percentage']

            flash("Student details submitted successfully!", "success")
            return redirect('/')
        except Exception as err:
            print(f"Error: {err}")
            flash("There was an error while submitting the form. Please try again.", "error")
            return redirect('/form')

    return render_template('form.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT,debug=True)
