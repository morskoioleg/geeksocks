from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
import smtplib
import ssl
import os
import json

import jinja2

import config


app = Flask(__name__)

TEMPLATES = os.path.abspath("./templates")
LOGO_CID = "logo"
LOGO = "logo.png"


def format_template(template, context):
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(TEMPLATES)
    ).get_template(template).render(context)


def format_email(template, params):
    html_p = os.path.expanduser(os.path.abspath(os.path.join(TEMPLATES, template + ".html")))
    text_p = os.path.expanduser(os.path.abspath(os.path.join(TEMPLATES, template + ".txt")))

    if not html_p.startswith(TEMPLATES) or not text_p.startswith(TEMPLATES):
        return None, 400
    
    if not os.path.exists(html_p) or not os.path.exists(text_p):
        return None, 404

    html = format_template(template + ".html", params)
    text = format_template(template + ".txt", params)

    return html, text


def build_email(html, text, from_, to, subject):
    """
    Multipart(mixed)
        Multipart(related)
            Multipart(alternative)
                Text(plain)
                Text(html)
            Image
    """
    mixed = MIMEMultipart("mixed")
    mixed["Subject"] = subject
    mixed["From"] = from_
    mixed["To"] = to
    mixed.preamble = "This is a multi-part message in MIME format."

    related = MIMEMultipart("related")

    alt = MIMEMultipart("alternative")
    alt.attach(MIMEText(text, "plain"))
    alt.attach(MIMEText(html, "html"))
    related.attach(alt)

    with open(LOGO, "rb") as f:
        logo = MIMEImage(f.read())
    logo.add_header("Content-ID", f"<{LOGO_CID}>")
    related.attach(logo)

    mixed.attach(related)

    return mixed.as_string()


def send_email(mime, recipient):
    if config.MODE == "SSL":
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(*config.SMTP, context=context) as server:
            server.login(*config.LOGIN)

            server.sendmail(config.EMAIL, recipient, mime)
        return True
    elif config.MODE == "STARTTLS":
#LOGIN = ("***REMOVED***", "***REMOVED***")
        with smtplib.SMTP(*config.SMTP) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(os.getenv('MAIL_SMTP_LOGIN'),os.getenv('MAIL_SMTP_PASSWORD'))
#            server.login("***REMOVED***", "***REMOVED***")
            server.sendmail(config.EMAIL, recipient, mime)
#            print("***REMOVED***")
#            print("***REMOVED***")
#            print(os.getenv('MAIL_SMTP_LOGIN'))
#            print(os.getenv('MAIL_SMTP_PASSWORD'))
        return True
    else:
        return False


def main():
    context = {k: request.form[k] for k in request.form if request.form[k] and k in ("message","email","phone","name") }
    credentials = pika.PlainCredentials(os.getenv('RMQ_LOGIN'), os.getenv('RMQ_PASSWORD'))
    parameters = pika.ConnectionParameters('hello-world.default.svc.root.local',
                                           5672,
                                           '/',
                                           credentials)
    connection = pika.BlockingConnection(parameters)

    channel.queue_declare(queue='hello')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        context = json.loads(body)
#        email = format_email(request.form["template"], context)
        email = format_email(context["template"], context)
        if email[0] is None:
          print('Error in template')
          print(email[1])
    
        html, txt = email

        email = build_email(email[0], email[1], config.FROM_NAME, context["to"], context["subject"])

        if !send_email(email, context["to"]):
          print('Error in sendmail')       

    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


#@app.route("/mail/send", methods=["POST"])
#def send():
#    if not all(i in request.form for i in ("template", "to", "subject")):
#        return abort(400)

#    context = {k: request.form[k] for k in request.form if request.form[k] and k != "template"}
#    context["logo_cid"] = "cid:" + LOGO_CID

#    email = format_email(request.form["template"], context)
#    if email[0] is None:
#        return abort(email[1])
    
#    html, txt = email
#
#    email = build_email(email[0], email[1], config.FROM_NAME, context["to"], context["subject"])

#    if send_email(email, context["to"]):
#        return "", 200
#    return abort(500)


