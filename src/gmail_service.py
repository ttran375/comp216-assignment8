import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class GmailService:
    # Class variables for SMTP server configuration
    _smtp_server = "smtp.gmail.com"
    _smtp_port = 587
    _charset = "UTF-8"
    _mail_body_html = ""
    _mail_body_text = ""
    _subject = ""

    def __init__(self, sender_email, sender_password, recipient_email):
        # Initialize instance variables with email credentials and recipient address
        self._sender_email = sender_email
        self._sender_password = sender_password
        self._recipient_email = recipient_email

    def set_subject(self, subject):
        # Set the subject of the email
        self._subject = subject

    def set_body(self, user_input, normal_low, normal_high):

        # Set the HTML body of the email with dynamic user input and range
        self._mail_body_html = (
            "<html>"
            "<head></head>"
            "<body>"
            "<h1>Warning: Out of bound input value</h1>"
            "<p>The input value {user_input} is outside the normal display range from "
            f"{normal_low} to {normal_high}.</p>"
            "</body>"
            "</html>"
        )

        # Set the plain text body of the email
        self._mail_body_text = (
            "Warning: Out of bound input value\n"
            f"The input value {user_input} is outside the normal display range from "
            f"{normal_low} to {normal_high}."
        )

    def send_email(self):
        # Create a MIMEMultipart message object
        msg = MIMEMultipart("alternative")
        msg["From"] = self._sender_email
        msg["To"] = self._recipient_email
        msg["Subject"] = self._subject

        # Create MIMEText objects for the plain text and HTML parts
        part1 = MIMEText(self._mail_body_text, "plain", self._charset)
        part2 = MIMEText(self._mail_body_html, "html", self._charset)

        # Attach the text parts to the message
        msg.attach(part1)
        msg.attach(part2)

        try:
            # Establish connection to the SMTP server
            server = smtplib.SMTP(self._smtp_server, self._smtp_port)
            server.starttls()  # Secure the connection
            server.login(self._sender_email, self._sender_password)
            server.sendmail(self._sender_email, self._recipient_email, msg.as_string())
            server.quit()  # Terminate the SMTP session
            print("Email sent successfully!")
        except smtplib.SMTPAuthenticationError:
            # Handle authentication errors (e.g., incorrect username or password)
            print(
                "Failed to authenticate with the SMTP server. Check the username and password."
            )
        except smtplib.SMTPConnectError:
            # Handle connection errors (e.g., server address or port issues)
            print(
                "Failed to connect to the SMTP server. Check the server address and port."
            )
        except smtplib.SMTPRecipientsRefused:
            # Handle errors where the recipient address is refused by the server
            print(
                "The server refused the recipient address. Check the recipient email address."
            )
        except smtplib.SMTPSenderRefused:
            # Handle errors where the sender address is refused by the server
            print(
                "The server refused the sender address. Check the sender email address."
            )
        except smtplib.SMTPDataError:
            # Handle unexpected errors in the SMTP data exchange
            print(
                "The server replied with an unexpected error code. Check the email content."
            )
        except smtplib.SMTPException as e:
            # Catch-all for any other SMTP-related exceptions
            print(f"Failed to send email: {str(e)}")
        except (TypeError, ValueError) as e:
            # Handle common errors in data types or values (e.g., during email construction)
            print(f"An error occurred: {e}")
