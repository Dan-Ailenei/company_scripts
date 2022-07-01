import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from os.path import basename

from project_config import config

gmail_user = config['CREDENTIALS']['gmail_user']
gmail_password = config['CREDENTIALS']['gmail_password']


def get_smtp_connection():
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(gmail_user, gmail_password)
    return server


def send_email(sent_from, to, subject, body, files=None):
    server = get_smtp_connection()

    msg = MIMEMultipart()
    msg['From'] = sent_from
    msg['To'] = ', '.join(to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(body))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)

    server.sendmail(sent_from, to, msg.as_string())
    server.close()
