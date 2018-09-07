# @Author: Tushar(tusharcoder) <tushar>
# @Date:   07/09/18
# @Email:  tamyworld@gmail.com
# @Filename: app_settings
# @Last modified by:   Tushar

from django.conf import settings
try:
    SEND_REGISTRATION_MAILS = settings.SEND_REGISTRATION_MAILS
except:
    SEND_REGISTRATION_MAILS = True