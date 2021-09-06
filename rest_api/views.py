from rest_api.models import CustomUser
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_api.serializers import CustomUserSerializer
import json

class CustomUserSerializerViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all().order_by('-date_joined')
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]


class PaymentOperationView(APIView):

    def post(self, request):
        json_data = request.data
        user_receiving = CustomUser.users_search(json_data['INN'])
        if CustomUser.transaction_verification(request.user, json_data['amount']):
            divide_amount = CustomUser.divide_amount(json_data['amount'], len(user_receiving))
            for operation in user_receiving:
                CustomUser.send_operations(request.user, operation, divide_amount)
            return Response({
                "error" : "Операция прошла успешно",
                "amount" : "Ваш текущий баланс равен " + str(request.user.amount),
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "error" : "Операция не прошла",
                "amount" : "Ваш текущий баланс равен " + str(request.user.amount) 
            },  status=status.HTTP_400_BAD_REQUEST)