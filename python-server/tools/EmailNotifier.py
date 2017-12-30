import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from logging import RootLogger

from typeguard import typechecked

from model.configuration.EmailCfg import EmailCfg
from model.configuration.HomeDefenceCfg import HomeDefenceCfg


class EmailNotifier:
    __EMAIL_HOST = 'smtp.gmail.com'
    __EMAIL_PORT = 587

    @typechecked()
    def __init__(self, email_config: EmailCfg, home_defence_config: HomeDefenceCfg, logging: RootLogger):
        self.__email_config = email_config
        self.__home_defence_config = home_defence_config
        self.__logging = logging

    @typechecked()
    def send_alert(self, subject: str, body: str) -> None:
        address = self.__email_config.sender_address
        receiver = self.__home_defence_config.notified_email_address
        msg = MIMEMultipart()
        msg['From'] = address
        msg['To'] = receiver
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP(self.__EMAIL_HOST, self.__EMAIL_PORT)
        try:
            server.starttls()
            server.login(address, self.__email_config.password)
            text = msg.as_string()
            server.sendmail(address, receiver, text)
            server.quit()
        except Exception as e:
            self.__logging.error(e)