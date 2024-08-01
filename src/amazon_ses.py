import boto3
import os
from botocore.exceptions import ClientError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class AmazonSES:
    _aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    _aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    _aws_region = os.getenv("AWS_REGION")
    _configuration_set = os.getenv("CONFIGURATION_SET")
    _charset = "UTF-8"
    _mail_body_html = ""
    _mail_body_text = ""
    _subject = ""

    def __init__(self, sender, recipient):
        self._sender = sender
        self._recipient = recipient
        self._sesClient = boto3.client(
            "ses",
            region_name=self._aws_region,
            aws_access_key_id=self._aws_access_key_id,
            aws_secret_access_key=self._aws_secret_access_key,
        )

    def setSubject(self, subject):
        self._subject = subject

    def setBody(self, userInput, normalLow, normalHigh):
        self._mail_body_html = (
            """<html>
            <head></head>
            <body>
              <h1>Warning: Out of bound input value</h1>
              <p>The input value """
            + str(userInput)
            + """ is outside the normal display range from """
            + str(normalLow)
            + """ to """
            + str(normalHigh)
            + """ .</p>
            </body>
            </html>"""
        )

        self._mail_body_text = (
            "Amazon SES Test (Python)\r\n"
            "This email was sent with Amazon SES using the "
            "AWS SDK for Python (Boto)."
        )

    def sendemail(self):
        # Try to send the email.
        try:
            # Provide the contents of the email.
            response = self._sesClient.send_email(
                Destination={
                    "ToAddresses": [
                        self._recipient,
                    ],
                },
                Message={
                    "Body": {
                        "Html": {
                            "Charset": self._charset,
                            "Data": self._mail_body_html,
                        },
                        "Text": {
                            "Charset": self._charset,
                            "Data": self._mail_body_text,
                        },
                    },
                    "Subject": {
                        "Charset": self._charset,
                        "Data": self._subject,
                    },
                },
                Source=self._sender,
                # If you are not using a configuration set, comment or delete the following line
                ConfigurationSetName=self._configuration_set,
            )
        # Display an error if something goes wrong.
        except ClientError as e:
            print(e.response["Error"]["Message"])
        else:
            print("Email sent! Message ID:"),
            print(response["MessageId"])
