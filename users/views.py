from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import User
import jwt, datetime

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response

class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)
    #
    # def get(self, request, user_id):
    #     # token = request.COOKIES.get('jwt')
    #     # print("View has been triggered")  # Print a basic message
    #     auth_header = request.headers.get('Authorization')  # Get the Authorization header
    #     # print(f"auth_header received: {auth_header}")
    #
    #     if not auth_header or not auth_header.startswith('Bearer '):
    #         raise AuthenticationFailed('Unauthenticated!')
    #
    #     token = auth_header.split(' ')[1]  # Extract the token from 'Bearer <token>'
    #     # print(f"Token received: {token}")
    #     if not token:
    #         raise AuthenticationFailed('Unauthenticated!')
    #
    #     try:
    #         jwt.decode(token, 'secret', algorithms=['HS256'])
    #     except jwt.ExpiredSignatureError:
    #         raise AuthenticationFailed('Unauthenticated!')
    #
    #     user = User.objects.filter(id=user_id).first()
    #     if user is None:
    #         raise AuthenticationFailed('User not found!')
    #
    #     serializer = UserSerializer(user)
    #     return Response(serializer.data)

class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response
