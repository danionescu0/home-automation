import smtplib

class emailNotifier:
    def __init__(self, address, password, notifiedAddress):
        self.address = address
        self.password = password
        self.notifiedAddress = notifiedAddress

    def sendAlert(self, subject, body):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.address, self.password)

        msg = subject
        server.sendmail(self.address, self.notifiedAddress, msg)
        server.quit()