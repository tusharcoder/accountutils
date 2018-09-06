from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import ForgotPasswordModel
from .utils import validate, gen_hash, hexify, send_mail


# Create your views here.
@api_view(['POST', ])
def forgot_password_view(request):
    if request.method == "POST":
        data = request.data
        valid, errors = validate(*['username'], **request.data)
        if not valid:
            return Response({"error": errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        username = data.get("username")
        user = User.objects.get(username=username)
        # hash code
        code = gen_hash()
        hex_code = hexify(code)
        ForgotPasswordModel.objects.create(code=hex_code, user=user)
        send_mail(**{"body": "Reset password code is {}".format(code), "subject": "Forgot Password", "to_email":user.email})
        return Response({'message': ['Reset code generated', ], 'code': code}, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': ['{} method is not allowed'.format(request.method)]},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST', ])
def forgot_password_confirm(request):
    if request.method == "POST":
        valid, errors = validate(*['code'], **request.data)
        if not valid:
            return Response({"error": errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        data = request.data
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
        valid, errors = validate(*['code', 'password'], **request.data)
        if not valid:
            return Response({"error": errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        data = request.data
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
        valid, errors = validate(*['current_password', 'new_password'], **request.data)
        if not valid:
            return Response({"error": errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        data = request.data
        user = request.user
        if user.check_password(data.get("current_password")):
            user.set_password(data.get('new_password'))
            user.save(update_fields=('password',))
        else:
            return Response({"errors": ['Current password is not correct']}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"message": "Password change successfully"}, status=status.HTTP_202_ACCEPTED)
    else:
        return Response({'error': ['{} method is not allowed'.format(request.method)]},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST', ])
def login(request):
    """function for login and return the token for the user"""
    email = request.data.get('email')
    password = request.data.get('password')
    valid, errors = validate('email', 'password', **{"email": email, "password": password})
    if not valid:
        return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(**{'username': email, 'password': password})
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_200_OK)
    else:
        return Response({"errors": ['Wrong Credentials']}, status=status.HTTP_401_UNAUTHORIZED)
