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