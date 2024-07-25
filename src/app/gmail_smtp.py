import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class GmailSMTP:
    _smtp_server = "smtp.gmail.com"
    _smtp_port = 587
    _charset = "UTF-8"
    _mail_body_html = ""
    _mail_body_text = ""
    _subject = ""

    def __init__(self, sender_email, sender_password, recipient_email):
        self._sender_email = sender_email
        self._sender_password = sender_password
        self._recipient_email = recipient_email

    def setSubject(self, subject):
        self._subject = subject

    def setBody(self, userInput, normalLow, normalHigh):
        self._mail_body_html = f"""<html>
        <head></head>
        <body>
          <h1>Warning: Out of bound input value</h1>
          <p>The input value {userInput} is outside the normal display range from {normalLow} to {normalHigh}.</p>
        </body>
        </html>"""

        self._mail_body_text = f"""Warning: Out of bound input value
        The input value {userInput} is outside the normal display range from {normalLow} to {normalHigh}."""

    def sendemail(self):
        # Create the email
        msg = MIMEMultipart("alternative")
        msg["From"] = self._sender_email
        msg["To"] = self._recipient_email
        msg["Subject"] = self._subject

        part1 = MIMEText(self._mail_body_text, "plain", self._charset)
        part2 = MIMEText(self._mail_body_html, "html", self._charset)

        msg.attach(part1)
        msg.attach(part2)

        try:
            # Connect to the server and send the email
            server = smtplib.SMTP(self._smtp_server, self._smtp_port)
            server.starttls()
            server.login(self._sender_email, self._sender_password)
            server.sendmail(self._sender_email, self._recipient_email, msg.as_string())
            server.quit()
            print("Email sent successfully!")
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
