# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_email(message_, title='sample title'):
    message = Mail(
        from_email='dondakarai@gmail.com',
        to_emails='dilisharanasinghe@gmail.com',
        subject=title,
        html_content= """\
                     <html>
                       <body>
                       {0}
                       </body>
                     </html>
                     """.format(message_))

    try:
        sg = SendGridAPIClient('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')
        response = sg.send(message)
        # print(response.status_code)
        # print(response.body)
        # print(response.headers)
    except Exception as e:
        print(e)