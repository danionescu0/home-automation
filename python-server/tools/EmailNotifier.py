import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

class EmailNotifier:
    def __init__(self, address, password, notifiedAddress):
        self.address = address
        self.password = password
        self.notifiedAddress = notifiedAddress

    def send_alert(self, subject, body):
        msg = MIMEMultipart()
        msg['From'] = self.address
        msg['To'] = self.notifiedAddress
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.address, self.password)
        text = msg.as_string()
        server.sendmail(self.address, self.notifiedAddress, text)
        server.quit()