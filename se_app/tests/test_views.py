from decimal import Decimal

from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken
from se_app.models import Product, Customer, Order


class ProductApiTest(APITestCase):
    def setUp(self):
        self.regular_user = User.objects.create_user(username='testuser',password ='testpassword')
        self.admin_user = User.objects.create_superuser(username='testadmin',password ='testpassword')
        self.product = Product.objects.create(name='Temporary Product', price=1.99, available=True)
        self.product_list_url = reverse('product-list')
        self.product_detail_url = reverse('product-detail',kwargs={'pk': self.product.id})

        self.client = APIClient()
    def test_get_all_products(self):
        self.token = str(AccessToken.for_user(self.regular_user))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get(self.product_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Temporary Product')
        self.assertEqual(response.data[0]['price'], '1.990')
        self.assertTrue(response.data[0]['available'])

    def test_get_one_product(self):
        self.token = str(AccessToken.for_user(self.regular_user))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Temporary Product')
        self.assertEqual(response.data['price'], '1.990')
        self.assertTrue(response.data['available'])

    def test_create_new_product_with_valid_data_admin_user(self):
        self.token = str(AccessToken.for_user(self.admin_user))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        data = {'name': 'New Product', 'price': '2.99', 'available': True}
        response = self.client.post(self.product_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Product')
        self.assertEqual(response.data['price'], '2.990')
        self.assertTrue(response.data['available'])

    def test_create_new_product_with_valid_data_regular_user(self):
        self.token = str(AccessToken.for_user(self.regular_user))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        data = {'name': 'New Product', 'price': '2.99', 'available': True}
        response = self.client.post(self.product_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_new_product_with_invalid_data_admin_user(self):
        self.token = str(AccessToken.for_user(self.admin_user))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        data = {'name': 'New Product', 'price': '-2.99', 'available': True}
        response = self.client.post(self.product_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_product_admin_user(self):
        self.token = str(AccessToken.for_user(self.admin_user))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        data = {'name': 'Updated Product'}
        response = self.client.patch(self.product_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Product')

    def test_patch_product_regular_user(self):
        self.token = str(AccessToken.for_user(self.regular_user))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        data = {'name': 'Updated Product'}
        response = self.client.patch(self.product_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_product_with_invalid_data(self):
        self.token = str(AccessToken.for_user(self.admin_user))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        data = {'price': '-5.99'}
        response = self.client.patch(self.product_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_product_admin_user(self):
        self.token = str(AccessToken.for_user(self.admin_user))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.delete(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)

    def test_delete_product_regular_user(self):
        self.token = str(AccessToken.for_user(self.regular_user))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.delete(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Product.objects.count(), 1)


    def test_invalid_endpoint(self):
        self.token = str(AccessToken.for_user(self.regular_user))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        invalid_url = reverse('product-list') + 'invalid/'
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)




