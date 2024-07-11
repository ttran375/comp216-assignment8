# Lab 8 – Email Services.

Email integrations provide an easy, cost-effective way to send and
receive emails for various use cases (e.g., marketing, notifications,
order confirmations, etc.). Email solutions are available in different
"flavours", which may employ on-prem infrastructure and software
(Microsoft Exchange), private cloud services (AWS, Azure, etc.), or
third-party service parties (SendGrid).

## Exercise – Notification Emails via Gmail:

Augment the functionality of the Display application built for Lab 7 by
sending an email when the user enters a number value beyond the normal
range. The email notification must capture and record the user’s input
that is too low or high and send an email notification via Gmail. Note:
Create a temporary Gmail account for the group to utilize. Implement the
code with the standard SMTP library.

**Exercise – Notification Emails via AWS:**

To continue the exploration of cloud computing and networks via Amazon
Web Services (AWS), deploy and configure Amazon Simple Email Service
(SES). Follow the following tutorial: [Send an Email with Amazon
SES](https://aws.amazon.com/getting-started/hands-on/send-an-email-with-amazon-ses/)
to get started.

Subsequently, leverage the [AWS SDK for Python (Boto3) for
SES](https://docs.aws.amazon.com/ses/latest/dg/send-an-email-using-sdk-programmatically.html)
to send an email programmatically when the user enters a number value
beyond the normal range in the Display application (built for Lab 7).
The email notification must capture and record the user’s input that is
too low or high.

Upload a recording demonstrating the email connectivity for both
exercises.

**Due:**

See course shell.

***Submission***

1.  You must use only the libraries that are available in the standard
    Python distribution (unless specified by the instructor).

2.  Your code file will be named
    group\_«your_group_number»\_email_service.py e.g., group_1\_
    email_service.py.

3.  Must be uploaded to course dropbox before the deadline.

4.  See schedule for due date.

***Rubrics***

See requirements above.
