from threading import Thread
from flask import current_app
from flask_mail import Message
from app import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body,
                attachments=None, sync=False):
    """
    Send emails.
    
    Keyword arguments:
    subject -- (String) subject line of email
    sender -- (String) email of the sender
    recipients -- (List of Strings) emails of recipients
    text_body -- 
    html_body -- 
    attachments -- (List of tuples, default None) (filename, mediatype, file data)
    sync -- (Boolean, default False) 'True' sends email asynchronously
    """
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    if attachments:
        for attachment in attachments:
            # * expands the tuple into individual arguments
            msg.attach(*attachment)
    if sync:
        mail.send(msg)
    else:
        Thread(target=send_async_email,
            args=(current_app._get_current_object(), msg)).start()