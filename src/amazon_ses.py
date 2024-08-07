import os

import boto3
from botocore.exceptions import (
    ClientError,
    EndpointConnectionError,
    NoCredentialsError,
    PartialCredentialsError,
)
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()


class AmazonSES:
    # Initialize class variables with environment variables
    _aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    _aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    _aws_region = os.getenv("AWS_REGION")
    _configuration_set = os.getenv("CONFIGURATION_SET")
    _charset = "UTF-8"
    _mail_body_html = ""
    _mail_body_text = ""
    _subject = ""

    def __init__(self, sender, recipient):
        # Initialize instance variables
        self._sender = sender
        self._recipient = recipient

        # Create an SES client using boto3 with the specified AWS credentials and region
        self._sesClient = boto3.client(
            "ses",
            region_name=self._aws_region,
            aws_access_key_id=self._aws_access_key_id,
            aws_secret_access_key=self._aws_secret_access_key,
        )

    def setSubject(self, subject):
        # Set the subject of the email
        self._subject = subject

    def setBody(self, userInput, normalLow, normalHigh):
        # Set the HTML body of the email with dynamic user input and range
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

        # Set the plain text body of the email
        self._mail_body_text = (
            "Amazon SES Test (Python)\r\n"
            "This email was sent with Amazon SES using the "
            "AWS SDK for Python (Boto)."
        )

    def sendemail(self):
        try:
            # Attempt to send the email using the SES client
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
                ConfigurationSetName=self._configuration_set,
            )
        except NoCredentialsError:
            print("Credentials not available.")
        except PartialCredentialsError:
            print("Incomplete credentials provided.")
        except EndpointConnectionError:
            print("Could not connect to the endpoint URL.")
        except ClientError as e:
            # Print error message if sending fails
            print(e.response["Error"]["Message"])
        except Exception as e:
            # Catch-all for any other exceptions
            print(f"An error occurred: {e}")
        else:
            # Print message ID if sending is successful
            print("Email sent! Message ID:"),
            print(response["MessageId"])
