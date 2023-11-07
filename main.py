from flask import Flask, render_template, url_for, request, redirect, flash
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
EMAIL_ADDRESS = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASS')

@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)


@app.route('/submit_form', methods=['GET', 'POST'])
def submit_form():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        # Send confirmation email to the sender
        confirmation_message = f"""
        Dear {name},

        Thank you for contacting me! Your message has been received, and I will get back to you as soon as possible.

        Here are the details of your inquiry:
        Subject: {subject}
        Message: {message}

        I appreciate your interest and look forward to helping you further.

        Best regards,
        Raj Sahu
        """

        confirmation_msg = EmailMessage()
        confirmation_msg['From'] = EMAIL_ADDRESS
        confirmation_msg['To'] = email
        confirmation_msg['Subject'] = "Confirmation: " + subject
        confirmation_msg['Bcc'] = [EMAIL_ADDRESS]
        confirmation_msg.set_content(confirmation_message)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(confirmation_msg)

        # flash('Thank you for your message! We will get back to you soon.', 'success')
        return render_template('message.html')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)