from src.configs import Config
from redmail.email.sender import EmailSender

settings = Config()


class EmailNotification():
    def __init__(self, email:dict):
        self.subject = email.get("subject")
        self.text= email.get("text")
        self.host = settings.EMAIL['host']
        self.port = settings.EMAIL['port']
        self.username = settings.EMAIL['username']
        self.password = settings.EMAIL['password']
        self.email_receiver = settings.EMAIL['email_receiver']
        self.sender = self.create_sender()

    def create_sender(self):
        return EmailSender(
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
        )

    def send_email(self):
        self.sender.send(
            sender=self.username,  
            receivers=[self.email_receiver],
            subject=self.subject,
            text=self.text
            )
