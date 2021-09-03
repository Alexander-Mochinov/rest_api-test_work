from rest_api.models import CustomUser, Operation
from rest_framework import serializers


class CustomUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['url', 'username', 'email', 'INN']

class PaymentOperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        field = ['id', 'amount']


class PaymentOperationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Operation
        field = ['sender', 'receiving', 'amount', 'confirmation_of_transfer']