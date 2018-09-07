INSTALLATION
=====
pip install django-accountutils

=====
Account Utils
=====

Accountutils is a simple django application to facilitate basic functionalities, like forgot password, change password, for api based projects.

Quick start
-----------

1. Add "accountutils" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'accountutils',
    ]

2. Include the accountutils URLconf in your project urls.py like this::

    url('utils/', include('accountutils.urls')),

3. Run `python manage.py migrate` to create the accountutils models.

4. Add required settings in settings.py::

        USEEMAIL='youremail@somewhere.com'
        EMAIL_USE_TLS = True or False
        EMAIL_HOST = 'your host'
        EMAIL_PORT = <port>
        EMAIL_HOST_USER = USEEMAIL
        EMAIL_HOST_PASSWORD ='your password'
        DEFAULT_FROM_EMAIL = USEEMAIL
        DEFAULT_TO_EMAIL = ''
        EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
        #if communication mails has to be send
        SEND_REGISTRATION_MAILS = True or False #dafault True

5. Now you will have the api endpoints for registration, login, change password, forgot password etc.
        #incase, use use the utils in step 2
        /utils/request/forgot/password/  #post request
        /utils/check/forgot_password_code/  #post request
        /utils/reset/password/    #post request
        /utils/change/password/    #post request
        #login user
        /utils/login/    #post request
        #register user
        /utils/register/    #post request