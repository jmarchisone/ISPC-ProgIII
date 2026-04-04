from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, UserSerializer, UserProfileSerializer, PasswordResetRequestSerializer, PasswordResetVerifySerializer, ChangePasswordSerializer
from .models import UserProfile
import random
from django.utils import timezone
from datetime import timedelta

# Create your views here.

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
class PasswordResetRequestView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)

                #Verificar que exista el perfil
                profile, created = UserProfile.objects.get_or_create(user=user)

                #Generar OTP
                otp = str(random.randint(1000, 9999))
                profile.reset_otp = otp
                profile.otp_created_at = timezone.now()
                profile.save()

                #Imprimir en consola (simulando envio de email)
                print(f"OTP para {email}: {otp}")

                return Response({'message': 'Si el email existe en nuestro sistema, se ha enviado un código OTP.'}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'message': 'Si el email existe en nuestro sistema, se ha enviado un código OTP.'}, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PasswordResetVerifyView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = PasswordResetVerifySerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            new_password = serializer.validated_data['new_password']

            try:
                user = User.objects.get(email=email)
                profile = user.userprofile

                #Verificar OTP y tiempo de validez (5 minutos)
                if profile.reset_otp == otp:
                    expiration_time = profile.otp_created_at + timedelta(minutes=5)
                    if timezone.now() <= expiration_time:
                        user.set_password(new_password)
                        user.save()

                        #Limpiar OTP
                        profile.reset_otp = None
                        profile.otp_created_at = None
                        profile.save()

                        return Response({'message': 'Contraseña restablecida exitosamente.'}, status=status.HTTP_200_OK)
                    else:
                        return Response({'error': 'El código OTP ha expirado.'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'error': 'Código OTP inválido.'}, status=status.HTTP_400_BAD_REQUEST)
                
            except (User.DoesNotExist, UserProfile.DoesNotExist):
                return Response({'error': 'Usuario no encontrado.'}, status=status.HTTP_400_BAD_REQUEST)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserDetailView(APIView):
    # EXIGE EL TOKEN
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        # request.user ya contiene el usuario autenticado gracias al token
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ChangePasswordView(APIView):
    # EXIGE EL TOKEN
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            
            # Verificamos que la contraseña actual sea correcta
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({"error": "La contraseña actual es incorrecta."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Si es correcta, seteamos la nueva y guardamos
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"message": "Contraseña actualizada exitosamente."}, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)