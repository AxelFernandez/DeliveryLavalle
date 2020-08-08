
# Factory Fot Test with FactoryBoy
from unittest.mock import MagicMock

import factory
from django.core.files import File
from social_core.tests.models import User

from core.models import Company, PaymentMethod

file_mock = MagicMock(spec=File)
file_mock.name = 'test.png'
file_mock.size = 50

class CashPaymentMethod(factory.Factory):
    class Meta:
        model = PaymentMethod
    description = 'Efectivo'


class MeliPaymentMethod(factory.Factory):
    class Meta:
        model = PaymentMethod
    description = 'Mercado Pago'


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    email = factory.Sequence(lambda n: 'person{}@gmail.com'.format(n))

class CompanyFactory(factory.Factory):
    class Meta:
        model = Company

    name = 'CompanyTest'
    description = 'TestDescription'
    phone = '261234543'
    address = 'This is my Address'
    available_now = "Si"
    photo = file_mock
    id_user = factory.SubFactory(UserFactory)
    limits = '{"north": -32.754954,"east": -68.399872,"south": -32.758975,"west": -68.404060}'
    account_debit = 0
