from email.mime.text import MIMEText
import smtplib

def send_email(email, height, average_height, count):
    # Config account
    from_email = "txd.test.email@gmail.com"
    from_password = "gxfrzpnnmenbedah"
    to_email = email

    #content of email
    subject = "Height Data"
    message = "Hey there, your height is <strong>%s</strong>. Average height of all users is <strong>%s</strong> and that is calculated out <strong>%s</strong> of people." % (height, average_height, count)

    msg = MIMEText(message, "html")
    msg["Subject"] = subject
    msg["To"] = to_email
    msg["From"] = from_email

    # login and send
    gmail = smtplib.SMTP('smtp.gmail.com', 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_password)
    gmail.send_message(msg)
