from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import ForgotPasswordModel
from .utils import validate, gen_hash, hexify, send_mail, get_request_data

from .app_settings import SEND_REGISTRATION_MAILS


# Create your views here.
@api_view(['POST', ])
def forgot_password_view(request):
    if request.method == "POST":
        data = get_request_data(request)
        valid, errors = validate(*['username'], **get_request_data(request))
        if not valid:
            return Response({"error": errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        username = data.get("username")
        user = User.objects.get(username=username)
        # hash code
        code = gen_hash()
        hex_code = hexify(code)
        ForgotPasswordModel.objects.create(code=hex_code, user=user)
        send_mail(
            **{"body": "Reset password code is {}".format(code), "subject": "Forgot Password", "to_email": user.email})
        return Response({'message': ['Reset code generated', ], 'code': code}, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': ['{} method is not allowed'.format(request.method)]},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST', ])
def forgot_password_confirm(request):
    if request.method == "POST":
        valid, errors = validate(*['code'], **get_request_data(request))
        if not valid:
            return Response({"error": errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        data = get_request_data(request)
        hex_code = hexify(data.get("code"))
        exists = ForgotPasswordModel.objects.filter(code=hex_code).exists()
        if exists:
            return Response({"message": ['code exists']}, status=status.HTTP_200_OK)
        else:
            return Response({"error": ['code invalid']}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': ['{} method is not allowed'.format(request.method)]},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST', ])
def reset_password(request):
    """view to reset the password"""
    if request.method == "POST":
        valid, errors = validate(*['code', 'password'], **get_request_data(request))
        if not valid:
            return Response({"error": errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        data = get_request_data(request)
        hex_code = hexify(data.get("code"))
        try:
            forgot_password_model = ForgotPasswordModel.objects.get(code=hex_code)
        except ForgotPasswordModel.DoesNotExist:
            return Response({"error": ['code invalid']}, status=status.HTTP_404_NOT_FOUND)
        user = forgot_password_model.user
        user.set_password(data.get('password'))
        user.save(update_fields=("password",))
        forgot_password_model.delete()
        return Response({"message": "Password reset successfully"}, status=status.HTTP_202_ACCEPTED)
    else:
        return Response({'error': ['{} method is not allowed'.format(request.method)]},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST', ])
@authentication_classes([TokenAuthentication, ])
@permission_classes([IsAuthenticated, ])
def change_password(request):
    """view to change password of the user"""
    if request.method == "POST":
        valid, errors = validate(*['current_password', 'new_password'], **get_request_data(request))
        if not valid:
            return Response({"error": errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        data = get_request_data(request)
        user = request.user
        if user.check_password(data.get("current_password")):
            user.set_password(data.get('new_password'))
            user.save(update_fields=('password',))
            if SEND_REGISTRATION_MAILS:
                send_mail(
                    **{"body": "Hi {}!Your password changes successfully".format(user.username), "subject": "Password Changed",
                       "to_email": user.email})
            return Response({"message": "Password change successfully"}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"errors": ['Current password is not correct']}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': ['{} method is not allowed'.format(request.method)]},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST', ])
def login(request):
    """function for login and return the token for the user"""
    username = get_request_data(request).get('username')
    password = get_request_data(request).get('password')
    valid, errors = validate('username', 'password', **{"username": username, "password": password})
    if not valid:
        return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(**{'username': username, 'password': password})
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_200_OK)
    else:
        return Response({"errors": ['Wrong Credentials']}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST', ])
def registration_view(request):
    """view to implement the registration of thr user"""
    data = get_request_data(request)
    valid, errors = validate('username', 'password', 'email', **data)
    if not valid:
        return Response({'error': errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if User.objects.filter(email=email).exists():
        return Response({"error": "User already registered with email"}, status=status.HTTP_409_CONFLICT)
    try:
        User.objects.create_user(username, email, password)
        if SEND_REGISTRATION_MAILS:
            send_mail(
                **{"body": "Hi {}! your registration is successful".format(username), "subject": "Registration Successful",
                   "to_email": email})
    except IntegrityError as e:
        error_text = str(e)
        error_field = error_text.split(".")[-1]
        return Response({"error":["user is already registered with {}".format(error_field)]},status=status.HTTP_409_CONFLICT)
    return Response({"message": [
        'User registered successfully'
    ]}, status=status.HTTP_201_CREATED)
