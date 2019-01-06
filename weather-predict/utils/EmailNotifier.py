import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailNotifier:
    __EMAIL_HOST = 'smtp.gmail.com'
    __EMAIL_PORT = 587

    def configure(self, from_addr: str, from_pass: str) -> None:
        self.__from_addr = from_addr
        self.__from_pass = from_pass

    def send(self, to_address: str, subject: str, body: str) -> None:
        msg = MIMEMultipart()
        msg['From'] = self.__from_addr
        msg['To'] = to_address
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP(self.__EMAIL_HOST, self.__EMAIL_PORT)
        try:
            server.starttls()
            server.login(self.__from_addr, self.__from_pass)
            text = msg.as_string()
            server.sendmail(self.__from_addr, to_address, text)
            server.quit()
        except Exception as e:
            print("Error trying to send an email: " + str(e))