# import tempfile
# from django.contrib.auth import get_user_model
# from django.test import override_settings
#
# from django.core.files.uploadedfile import SimpleUploadedFile
# from django.test import TestCase
# from django.urls import reverse
#
# from core.factory.factory_boy import CompanyFactory, CashPaymentMethod
# from core.models import PaymentMethod, Company, CompanyCategory
# from core.test import get_company_form, get_products_form
#
#
# @override_settings(MEDIA_ROOT=tempfile.mkdtemp())
# class Test(TestCase):
#
#     def setUp(self):
#         User = get_user_model()
#         self.user = User.objects.create_user(username='testuser', password='12345')
#         self.image = self._create_image()
#         PaymentMethod.objects.create(description='Efectivo')
#
#     def _create_image(self):
#         from PIL import Image
#         with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
#             image = Image.new('RGB', (200, 200), 'white')
#             image.save(f, 'PNG')
#         return open(f.name, mode='rb')
#
#     def tearDown(self):
#         self.image.close()
#
#     def test_correct_create_company(self):
#         self.client.force_login(self.user)
#         category = CompanyCategory()
#         category.description = 'comidas'
#         category.save()
#         company = get_company_form(self.image)
#         response = self.client.post("/company/", data=company,follow=True)
#         # Contact mail
#         self.assertContains(response, 'axel.fernandez0145@gmail.com')
#
#     def test_create_product(self):
#         self.client.force_login(self.user)
#         company = get_company_form(self.image)
#         self.client.post("/company/", data=company)
#         message = get_products_form(self._create_image())
#         response = self.client.post(reverse('create-products'), data=message, follow=True)
#         self.assertContains(response, message['name'])
#
#     def test_configuration_of_company(self):
#         self.client.force_login(self.user)
#         self.client.post("/company/", data=get_company_form(self.image))
#         response = self.client.get(reverse('configuration'))
#         self.assertContains(response, get_company_form(None)['description'])
#
#     def test_orders_empty(self):
#         self.client.force_login(self.user)
#         self.client.post("/company/", data=get_company_form(self.image))
#         response = self.client.get(reverse('orders'))
#         self.assertContains(response, 'Nada por aqui :(')
#
