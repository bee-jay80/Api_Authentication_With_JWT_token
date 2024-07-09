from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics,status,views,permissions
from .models import User, Organisation
from django.contrib.auth import authenticate,login
from .serializers import OrganisationSerializer, RegisterSerializer, OrganisationCreateSerializer, LoginSerializer ,UserSerializer
import hashlib
from django.http import HttpResponse



class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            user = serializer.save()
            organisation = Organisation.objects.create(name=f"{user.firstName}'s Organisation", description='',orgId=hashlib.sha256(f"{user.firstName}{user.email}".encode()).hexdigest()[:10])
            organisation.users.add(user.id)
            organisation.users.add(request.user)
            organisation.save()
            # refresh = RefreshToken.for_user(user)
            return Response({
                'status': 'success',
                'message': 'Registration successful',
                'data': {
                    'accessToken': serializer.data['token'],
                    'user': UserSerializer(user).data
                }
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'status': 'Bad request',
                'message': 'Registration unsuccessful',
                'statusCode': 400
            }, status=status.HTTP_400_BAD_REQUEST)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request,*args,**kwargs):
        username = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            serilizer = self.serializer_class(user)
            response = HttpResponse()
            response.set_cookie('token', serilizer.data['token'], max_age=31536000, httponly=True, secure=True)
            return Response({
                'status': 'success',
                'message': 'Login successful',
                'data': {
                    'accessToken': serilizer.data['token'],
                    'user': UserSerializer(user).data
                }
            }, status=status.HTTP_200_OK)
        else:
            print("Failed")
            return Response({
                'status': 'Bad request',
                'message': 'Authentication failed',
                'statusCode': 401
            }, status=status.HTTP_401_UNAUTHORIZED)


class UserView(generics.GenericAPIView):
    def get(self, request, userId):
        user = User.objects.get(userId = userId)
        if user == user:
            return Response({
                'status': 'success',
                'message': 'User retrieved successfully',
                'data': UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'Forbidden',
                'message': 'You do not have permission to access this user',
                'statusCode': 403,
                'userId':str(request.user)
            }, status=status.HTTP_403_FORBIDDEN)

class OrganisationView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        organisations = request.user.organisations.all()
        return Response({
            'status': 'success',
            'message': 'Organisations retrieved successfully',
            'data': OrganisationSerializer(organisations, many=True).data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = OrganisationCreateSerializer(data=request.data)
        if serializer.is_valid():
            organisation = serializer.save()
            create_organisation = Organisation.objects.create(name=serializer.data['name'],description=serializer.data['description'],orgId=hashlib.sha256(f"{serializer.data['name']}".encode()).hexdigest()[:10])
            create_organisation.users.add(request.user)
            create_organisation.users.add(request.user.id)
            create_organisation.save()
            return Response({
                'status': 'success',
                'message': 'Organisation created successfully',
                'data': OrganisationSerializer(organisation).data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'status': 'Bad Request',
                'message': 'Client error',
                'statusCode': 400
            }, status=status.HTTP_400_BAD_REQUEST)

class OrganisationDetailView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, orgId):
        organisation = Organisation.objects.get(orgId=orgId)
        if organisation == organisation:
            return Response({
                'status': 'success',
                'message': 'Organisation retrieved successfully',
                'data': OrganisationSerializer(organisation).data
            }, status=status.HTTP_200_OK)
        return Response({
            'status': 'Forbidden',
            'message': 'You do not have permission to access this organisation',
            'statusCode': 403
        }, status=status.HTTP_403_FORBIDDEN)

class AddUserToOrganisationView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, orgId):
        organisation = Organisation.objects.get(orgId=orgId)
        if organisation == organisation:
            user_id = request.data.get('userId')
            user = User.objects.get(userId=user_id)
            if user.DoesNotExist:
                return Response({
                'status': 'Forbidden',
                'message': 'You do not have permission to access this organisation',
                'statusCode': 403
            }, status=status.HTTP_403_FORBIDDEN)
        else:
            create_organisation = Organisation.objects.create(name=f"{user.firstName}'s Organisation",description="",orgId=hashlib.sha256(f"{user.firstName}".encode()).hexdigest()[:10])
            create_organisation.users.add(user.id)
            create_organisation.save()
            return Response({
                'status': 'uccess',
                'message': 'User added to organisation successfully'
            }, status=status.HTTP_200_OK)
