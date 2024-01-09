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
    print("############################")
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

@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({'message': 'User has been logged out'})

@api_view(['GET'])
def dashboard(request):
    items = Item.objects.all()
    serialized_items = [{"id":item.id,"name":item.name,"price":item.price} for item in items]
    return Response(serialized_items)

@api_view(['GET'])
def summary(request):
    total_price = Item.objects.aggregate(total=Sum('price'))['total'] or 0
    return JsonResponse({'total_price': total_price})

@api_view(['POST'])
def signup_view(request):
    print("inside")
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

