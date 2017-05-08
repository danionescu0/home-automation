import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typeguard import typechecked

class EmailNotifier:
    @typechecked()
    def __init__(self, address: str, password: str, notified_address: str):
        self.address = address
        self.password = password
        self.notified_address = notified_address

    @typechecked()
    def send_alert(self, subject: str, body: str) -> None:
        msg = MIMEMultipart()
        msg['From'] = self.address
        msg['To'] = self.notified_address
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.address, self.password)
        text = msg.as_string()
        server.sendmail(self.address, self.notified_address, text)
        server.quit()