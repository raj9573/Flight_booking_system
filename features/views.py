from django.shortcuts import render

# Create your views here.

from .models import Flight, Ticket

from .serializers import FlightSerializer, TicketSerializer, UserSerializer

from rest_framework.views import APIView

from rest_framework import viewsets, filters, status

from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth import authenticate

from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.tokens import AccessToken

class UserCreationView(APIView):
    # This View is used to perform the user creation
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(TokenObtainPairView):
    #This view is used to perform the login operation and generate the unique token for the user 
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        # Authenticate the user using Django's authenticate method
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # User authenticated successfully, generate tokens manually
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token

            # Construct the response with tokens and user info
            response_data = {
                "refresh": str(refresh),  # Manually converting to string
                "access": str(access),    # Manually converting to string
                "user": {
                    "username": user.username,
                    "email": user.email,   # Any additional user fields you want
                }
            }
            return Response(response_data, status=status.HTTP_200_OK)

        # Return an error if authentication failed
        return Response({
            "detail": "Invalid username or password."
        }, status=status.HTTP_401_UNAUTHORIZED)


class FlightViewSet(viewsets.ModelViewSet):
    # to perfrom crud operations on flights and filter operations.
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    # permission_classes =  [IsAuthenticated]

    # Search for flights by departure city, destination city, and date
    filter_backends = [filters.SearchFilter]
    search_fields = ['departure_city', 'destination_city', 'departure_time']


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    # Ticket.objects.get(id=1)
    serializer_class = TicketSerializer

    filter_backends = [filters.SearchFilter]
    #this is used to filter the data
    search_fields = ['user__username']




# class GetUserFromTokenView(APIView):
#     def get(self, request, *args, **kwargs):
        
#         auth_header = request.headers.get('Authorization')
        
#         if auth_header and auth_header.startswith('Bearer '):
#             token = auth_header.split(' ')[1]  

#             try:
                
#                 access_token = AccessToken(token)
                
#                 print("the access token is ",access_token)

#                 print("the type of atoken is ", type(access_token))
                
#                 user_id = access_token['user_id'] 
                
#                 return Response({"user_id": user_id}, status=status.HTTP_200_OK)
#             except Exception as e:
#                 return Response({"detail": "Invalid or expired token."}, status=status.HTTP_401_UNAUTHORIZED)

#         return Response({"detail": "Authorization header missing or malformed."}, status=status.HTTP_400_BAD_REQUEST)
