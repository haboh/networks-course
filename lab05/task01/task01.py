import sys
import email.message
import smtplib

def main():
    filename = sys.argv[1]
    reciever = sys.argv[2]
    login = sys.argv[3]
    password = sys.argv[4]

    print(login)
    print(password)

    msg = email.message.EmailMessage()

    msg["From"] = login
    msg["To"] = reciever
    msg["Subject"] = "Hi"

    with open(filename, "r") as f:
        data = f.read()
    if filename.endswith('html'):
        msg.add_alternative(data, "html")
    else:
        msg.set_content(data)

    # If an error occurs, read this:
    # https://forum.infostart.ru/forum86/topic281182/

    smtp = smtplib.SMTP_SSL("smtp.mail.ru", 465)
    smtp.ehlo()
    smtp.login(login, password)
    smtp.send_message(msg)
    smtp.quit()

if __name__ == "__main__":
    main()