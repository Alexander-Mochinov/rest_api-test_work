
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from django.test import TestCase
from rest_api.models import CustomUser, Operation


class CustomUserTestCase(TestCase):
    def setUp(self):
        CustomUser.objects.create(username = "User1", email="test1@mail.ru", INN = "123323323332", amount = 100.0)
        CustomUser.objects.create(username = "User2", email="test2@mail.ru", INN = "324234233433", amount = 100.0)
        CustomUser.objects.create(username = "User3", email="test3@mail.ru", INN = "534543234234", amount = 100.0)

    def test_create_user(self):
        """
        Creating a record in the database
        """
        user1 = CustomUser.objects.filter(username = "User1").exists()
        self.assertEqual(user1, True)

    def test_users_search(self):
        user1 = CustomUser.objects.get(username = "User1")
        user2 = CustomUser.objects.get(username = "User2")
        user3 = CustomUser.objects.get(username = "User3")

        list_user = [user1, user2, user3]
        list_inn  = [user.INN for user in list_user]

        self.assertEqual(CustomUser.users_search(list_inn), list_user)

    def test_divide_amount(self):
        self.assertEqual(CustomUser.divide_amount(100.0, 5), 20.0)

    def test_transaction_verification(self):
        user1 = CustomUser.objects.get(username = "User1")
        self.assertEqual(CustomUser.transaction_verification(user1, 50), True)
        self.assertEqual(CustomUser.transaction_verification(user1, 150), False)
    
    def test_send_operations(self):
        user1 = CustomUser.objects.get(username = "User1")
        user2 = CustomUser.objects.get(username = "User2")
        success = {
            "message" : "Операция проведена успешно !",
            "status" : True
        }
        fail = {
            "message" : "Операция не прошла !",
            "status" : False
        }
        self.assertEqual(CustomUser.send_operations(user1, user2, 150.0), fail)
        self.assertEqual(CustomUser.send_operations(user1, user2, 50.0), success)



class OperationTestCase(TestCase):
    def setUp(self):
        sender = CustomUser.objects.create(username = "User1", email="test1@mail.ru", INN = "123323323332", amount = 100.0)
        receiving = CustomUser.objects.create(username = "User2", email="test2@mail.ru", INN = "324234234234", amount = 100.0)
        Operation.objects.create(
            sender = sender,
            receiving = receiving,
            amount = 15,
            confirmation_of_transfer = True
        )

    
    def test_create_user(self):
        """
        Creating a record in the database
        """
        user1 = CustomUser.objects.get(username = "User1")
        user2 = CustomUser.objects.get(username = "User2")
        operations = Operation.objects.filter(sender = user1, receiving = user2).exists()
        self.assertEqual(operations, True)



class AccountTests(APITestCase):
    def test_create_payment_operations(self):
        """
        Ensure we can create a new account object.
        """

        user1 = CustomUser.objects.create(username = "User2", email="test2@mail.ru", INN = "324234233433", amount = 100.0)
        user2 = CustomUser.objects.create(username = "User3", email="test3@mail.ru", INN = "534543234234", amount = 100.0)
        url = reverse('create_payment_operations')
        data = {
            "amount" : 50,
            "INN" : [f"{user1.INN}", f"{user2.INN}"]
        }

        user = CustomUser.objects.create(username = "User1", email="test1@mail.ru", INN = "123323323332", amount = 100.0)
        self.client = APIClient()
        self.client.force_authenticate(user = user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)