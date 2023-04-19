import csv

from flask import current_app
from flask_mail import Mail, Message


def send_mail():
    sender = ("Team matheworkout.at", "info@matheworkout.at")
    subject = "Freie Mathematik-Übungsseite"

    recipients = []
    with open("app/tools/schulen.csv", newline="") as file:
        reader = csv.DictReader(file, fieldnames=["name", "email"])
        for row in reader:
            recipients.append(row["email"])

    with open("app/tools/email_template.txt", "r") as file:
        body = file.read()

    app = current_app
    mail = Mail(app)

    with mail.connect() as conn:
        for recipient in recipients:
            msg = Message(
                subject=subject,
                sender=sender,
                recipients=[recipient],
                body=body,
            )
            conn.send(msg)
