from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
import smtplib
import ssl
import os
import json
import pika
import jinja2
import sys
import config
import ssl

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
        with smtplib.SMTP(*config.SMTP) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(os.getenv('MAIL_SMTP_LOGIN'),os.getenv('MAIL_SMTP_PASSWORD'))
            server.sendmail(config.EMAIL, recipient, mime)
        return True
    else:
        return False


def main():
    contextSsl = ssl.create_default_context(cafile="certs/ca.crt")
    contextSsl.load_cert_chain("certs/tls.crt",
                               "certs/tls.key")
    ssl_options = pika.SSLOptions(contextSsl, 'rabbitmq.default.svc.root.local')   
    credentials = pika.PlainCredentials(os.getenv('RMQ_LOGIN'), os.getenv('RMQ_PASSWORD'))
    parameters = pika.ConnectionParameters('rabbitmq.default.svc.root.local',
                                           5671,
                                           '/',
                                           credentials,
                                           ssl_options=ssl_options)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='customer_contact', durable=True)

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        print(ch)
        print(method.delivery_tag)
        print(properties)


        context = json.loads(body)
        email = format_email(context["template"], context)
        if email[0] is None:
          print('Error in template')
          print(email[1])
    
        html, txt = email

        email = build_email(email[0], email[1], config.FROM_NAME, context["to"], context["subject"])

        if send_email(email, context["to"]):
          ch.basic_ack(delivery_tag = method.delivery_tag)
        else:
          print('Error in sendmail')
          
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='customer_contact', on_message_callback=callback)

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

