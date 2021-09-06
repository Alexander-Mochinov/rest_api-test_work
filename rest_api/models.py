from datetime import datetime
 
from django.utils import timezone
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models
from django.forms import model_to_dict
from django.urls import reverse
from django.db.models.signals import post_save

from decimal import *


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Расширенный пользователь"""
    username = models.CharField(
        verbose_name = 'Пользователь',
        max_length=25,
        unique=True
    )
    email = models.EmailField(
        verbose_name = 'Email', 
        unique=True
    )
    date_joined = models.DateTimeField(
        verbose_name = 'Дата регистрации', 
        auto_now_add=True
    )
    is_active = models.BooleanField(
        verbose_name = 'is_active', 
        default=True
    )
    is_staff = models.BooleanField(
        verbose_name = 'is_staff',
        default=False
    )
    user_photo = models.ImageField(
        verbose_name = 'Фотография профиля',
        upload_to = 'users_photos/',
        null = True,
        blank = True
    )
    INN = models.CharField(
        verbose_name = 'Идентификационный номер налогоплательщика',
        max_length = 12,
        null = False,
        unique = True
    )
    amount = models.DecimalField(
        verbose_name = 'Cумма на счету',
        max_digits = 10, 
        decimal_places = 2,
        default = 0,
        null = False
    )
 
    objects = UserManager()
 
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
 
    def __str__(self):
        return self.username
 
    @property
    def get_inn(self):
        """
            Вывод INN пользователя
        """
        return self.INN


    @staticmethod
    def users_search(array_list_inn):
        """
            Поиск пользователя по списку ИНН ["...", ...]
        """
        users_found = []
        for user in CustomUser.objects.filter(INN__in = array_list_inn):
            users_found.append(user)
        return users_found

    @staticmethod
    def divide_amount(amount, count_users):
        """
            Кол-во средств на одного человека
        """
        return amount / count_users

    @staticmethod
    def transaction_verification(user, amount):
        """
            Проверка на достаточность средств на балансе
        """
        if user.amount > amount:
            return True
        else: return False

    @staticmethod
    def send_operations(sender, receiving, amount):
        """
            Операция перевода средств на счёт получателя
        """
        sender = CustomUser.objects.get(id = sender.id)
        receiving = CustomUser.objects.get(id = receiving.id)
        if CustomUser.transaction_verification(sender, amount):
            sender.amount = sender.amount - Decimal(amount)
            sender.save()

            receiving.amount = receiving.amount + Decimal(amount)
            receiving.save()

            Operation.transfer_operation(
                sender, 
                receiving, 
                amount
            )
            return {
                "message" : "Операция проведена успешно !",
                "status" : True
            }
        else:
            return {
                "message" : "Операция не прошла !",
                "status" : False
            }

    class Meta:
        db_table = 'user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Operation(models.Model):
    """История операций"""
    sender = models.ForeignKey(
        CustomUser,
        verbose_name = 'Отправитель',
        related_name = 'sender_user',
        on_delete = models.CASCADE
    )

    receiving = models.ForeignKey(
        CustomUser, 
        verbose_name = 'Получатель',
        related_name = 'receiving_user',
        on_delete = models.CASCADE
    )

    amount = models.DecimalField(
        verbose_name = 'Перевод суммы', 
        max_digits=10,
        decimal_places = 2,
        default=0,
        null=False
    )
    confirmation_of_transfer = models.BooleanField(
        verbose_name = 'Подтверждение операции', 
        default = False
    )



    @staticmethod
    def transfer_operation(sender, receiving, amount):
        """
            История операций
        """
        Operation.objects.create(
            sender = sender,
            receiving = receiving,
            amount = amount,
            confirmation_of_transfer = True
        )


    def __str__(self):
        return 'Сумма перевода : ' + str(self.amount) + ', Отправитель : ' + str(self.sender) + ', Получатель : '  + str(self.receiving)


    class Meta:
        db_table = 'operation'
        verbose_name = 'История операции'
        verbose_name_plural = 'История операций'