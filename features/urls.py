
from django.urls import path,include

from rest_framework.routers import DefaultRouter 

from .views import FlightViewSet, TicketViewSet, UserCreationView, UserLoginView

router = DefaultRouter()


router.register(r'FlightViewSet',FlightViewSet)

router.register(r'TicketViewSet',TicketViewSet)

from rest_framework_simplejwt.views import (   
    TokenRefreshView,
)


urlpatterns = [ 
    
    path('api/',include(router.urls)),

    path('register/', UserCreationView.as_view(), name='register'),

    path('user-login/', UserLoginView.as_view(), name='custom_login'),
    
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Token refresh endpoint


]