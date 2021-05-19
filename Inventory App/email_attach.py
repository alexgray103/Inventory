import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

class email_sender:
    def send_email(self, reciever, file):
        sender_email = "bmolab512@gmail.com"
        receiver_email = reciever
        message = MIMEMultipart()
        message["From"] = sender_email
        message['To'] = receiver_email
        message['Subject'] = "BMO Lab order"
        attachment = open(file,'rb')
        obj = MIMEBase('application','octet-stream')
        obj.set_payload((attachment).read())
        encoders.encode_base64(obj)
        obj.add_header('Content-Disposition',"attachment; filename= "+file)
        message.attach(obj)
        my_message = message.as_string()
        email_session = smtplib.SMTP('smtp.gmail.com',587)
        email_session.starttls()
        email_session.login(sender_email,'BMOPHO512!')
        email_session.sendmail(sender_email,receiver_email,my_message)
        email_session.quit()
        print("YOUR MAIL HAS BEEN SENT SUCCESSFULLY")
