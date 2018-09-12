# @Author: Tushar(tusharcoder) <tushar>
# @Date:   05/09/18
# @Email:  tamyworld@gmail.com
# @Filename: utils
# @Last modified by:   Tushar
import hashlib
from random import randint

from django.conf import settings


def validate(*args, **kwargs):
    """function to validate the data in kwargs"""
    fields_to_check = args
    errors = []
    for field in fields_to_check:
        if kwargs.get(field) is None or kwargs.get(field).strip() == '':
            errors.append("{} is required and cannot be empty".format(field))
    return not len(errors) > 0, errors

def hexify(val):
    """function to return the hex of the value"""
    return hashlib.sha1(val.encode('utf8')).hexdigest()

def gen_hash():
    """return the random hash string of 6 values"""
    return hashlib.sha1(str(randint(000000,999999)).encode('utf8')).hexdigest()[-6:]

def send_mail(*args,**kwargs):
    """function to send the pdf attachment to the emails
        requires subject, body, html_body(optional), to_email
    """
    try:
        from django.core.mail import EmailMultiAlternatives
        to = kwargs.pop('to_email')
        if not isinstance(to, list):
            if isinstance(to, str):
                to = [to,]
        subject, from_email, to = kwargs.pop('subject'), settings.DEFAULT_FROM_EMAIL, to
        text_content = kwargs.pop('body')
        if 'html_body' in kwargs:
            html_content = kwargs.pop('html_body')
        else:
            html_content = None
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        if html_content:
            msg.attach_alternative(html_content, 'text/html')
        msg.send(fail_silently=True)
    except:
        pass

def get_request_data(request):
    return {key: request.data.get(key) for key in request.data.keys()}