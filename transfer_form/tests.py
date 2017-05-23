from decimal import *
from hamcrest import *

from django.test import TestCase
from django.urls import reverse_lazy
from django.contrib.auth.models import User

from .models import Person


class TransferFormTest(TestCase):
    def setUp(self):
        self.user1, created = User.objects.get_or_create(username="Test",
                                                         first_name="TestF",
                                                         last_name="TestL")
        self.user2, created = User.objects.get_or_create(username="Test2",
                                                         first_name="TestF2",
                                                         last_name="TestL2")

        self.person1, created = Person.objects.get_or_create(
            user=self.user1,
            ssn="123",
            balance=Decimal(100.00))
        self.person2, created = Person.objects.get_or_create(
            user=self.user2,
            ssn="555",
            balance=Decimal(200.00))

    def test_transfer_success(self):
        data = {
            "sender": self.person1.id,
            "recipients_list": self.person2.ssn,
            "amount": Decimal(5)
        }
        response = self.client.post(reverse_lazy("transfer_form"),
                                    data=data)
        assert_that(response.json(),
                    is_(equal_to({'status': 'information',
                                  'title': 'Успешно',
                                  'message': 'Транзакция проведена успешно.'})))

    def test_recipients_not_found(self):
        data = {
            "sender": self.person1.id,
            "recipients_list": "wrong recipient ssn",
            "amount": Decimal(5)
        }
        response = self.client.post(reverse_lazy("transfer_form"),
                                    data=data)
        assert_that(response.json(),
                    is_(equal_to({'title': 'Ошибка транзакции',
                                  'status': 'error',
                                  'message': 'Не найдены получатели.'})))

    def test_insufficient_amount(self):
        data = {
            "sender": self.person1.id,
            "recipients_list": self.person2.ssn,
            "amount": Decimal(1000)
        }
        response = self.client.post(reverse_lazy("transfer_form"),
                                    data=data)
        assert_that(response.json(),
                    is_(equal_to({'title': 'Ошибка транзакции',
                                  'status': 'error',
                                  'message': 'Недостаточно средств на счету.'})))

    def test_form_serialization_failed(self):
        data = {
            "sender": self.person1.id,
            "recipients_list": self.person2.ssn,
            # we send not full data
        }
        response = self.client.post(reverse_lazy("transfer_form"),
                                    data=data)
        assert_that(response.json(),
                    is_(equal_to({'title': 'Ошибка транзакции',
                                  'status': 'error',
                                  'message': 'Невозможно выполнить запрос.'})))
