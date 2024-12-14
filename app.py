from flask import Flask, render_template, request, redirect, flash
import os
import whisper
from googletrans import Translator

# Flask app setup
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Load the Whisper model
model = whisper.load_model("base")

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

# Home route (Redirect directly to form)
@app.route('/')
def home():
    return redirect('/form')

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

            # Logic for processing and storing data can be added here

            flash("Student details submitted successfully!", "success")
            return redirect('/form')
        except Exception as err:
            print(f"Error: {err}")
            flash("There was an error while submitting the form. Please try again.", "error")
            return redirect('/form')

    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)