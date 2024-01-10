from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .serializers import *
from .models import Item
from django.db.models import Sum
from django.http import JsonResponse
from rest_framework.authtoken.models import Token

@api_view(['POST'])
def login_view(request):
    """
    :params: request with user credentials
    :process: Authenticate user and if authenticated successful response will be returned
    :return: 200 response for success and 400 for bad request
    """
    try:
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
    
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
    
                # Generate a token for the user and return it in the response
                return Response({'message': "Login Successful!"})
        return Response({'error': "Invalid Credentials! Please try again"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as error:
        return Response({'error': f"Error occured! f{error}."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout_view(request):
    """
    :params: request with user session
    :process: User session will be closed/ended
    :return: 200 response for successful logout and 400 for error
    """
    try:
        logout(request)
        return Response({'message': 'User has been logged out'})
    except Exception as error:
        return Response({'error': f"Error occured! f{error}."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def dashboard(request):
    """
    :params: request with user session
    :process: Collect the Item table data and serialize it
    :return: return the json data with Item table data
    """
    try:
        items = Item.objects.all()
        serialized_items = [{"id":item.id,"name":item.name,"price":item.price} for item in items]
        return Response(serialized_items)
    except Exception as error:
        return Response({'error': f"Error occured! f{error}."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def summary(request):
    """
    :params: request with user session
    :process: Count the sum of price column from Item Table
    :return: Returns the count of prive column value as total_price
    """
    try:
        total_price = Item.objects.aggregate(total=Sum('price'))['total'] or 0
        return JsonResponse({'total_price': total_price})
    except Exception as error:
        return Response({'error': f"Error occured! f{error}."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def signup_view(request):
    """
    :params: request with csrf
    :process: Collect the new user data and register with Django User Table
    :return: 200 response for successful register and 400 for error during signup
    """
    try:
        serializer = UserSignUpSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, password=password)
                return Response({'message': 'User Registration Successful!'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Username Already exists!'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializers.as_serializer_error(), status=status.HTTP_400_BAD_REQUEST)
    except Exception as error:
        return Response({'error': f"Error occured! f{error}."}, status=status.HTTP_400_BAD_REQUEST)

