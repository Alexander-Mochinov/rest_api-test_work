from django.urls import include, path
from rest_framework import routers
from rest_api import views

from rest_framework_jwt.views import obtain_jwt_token

from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'users', views.CustomUserSerializerViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/',     include('djoser.urls.authtoken')),
    path('api-token-auth/', obtain_jwt_token),
    path('api-auth/', include('rest_framework.urls')),
    path('create-payment-operations/', views.PaymentOperationView.as_view(), name='create_payment_operations'),
]
