import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from celery import Celery

app = Celery('hello', broker='pyamqp://localhost:6379/0')


@app.task
def send_email():
    sender_email = "fazliddinismoilov234@gmail.com"
    sender_password = "bwml ffmd rfrw veup"
    receiver_email = "fazliddinismoilov234@gmail.com"
    subject = "Test E-pochta"
    message = "Hello world ✅"

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    msg.attach(MIMEText(message, "plain"))

    try:
        smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
        smtp_server.starttls()
        smtp_server.login(sender_email, sender_password)
        text = msg.as_string()
        smtp_server.sendmail(sender_email, receiver_email, text)
        smtp_server.quit()
        print("Xabar yuborildi ✔️️")
    except Exception as e:
        print("Xabar yuborlmadi ✖️")


