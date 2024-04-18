from flask_mail import Message

from Web import mail




class DeletePostMail:
    def __init__(self, email, message):
        self.email = email
        self.message = message

    def send_mail(self):
        try:
            msg = Message("Post törlés", sender="HandBook@gmail.com", recipients=[self.email])
            msg.body = self.message
            mail.send(msg)
            return
        except Exception as error:
            print(error)
            return