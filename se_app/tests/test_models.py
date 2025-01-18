from decimal import Decimal
from unittest import TestCase
from django.core.exceptions import ValidationError
from django.db import DataError, IntegrityError
from django.forms import DecimalField

from se_app.models import Product, Customer, Order


class ProductModelTest(TestCase):
    def test_create_product_with_valid_data(self):
        temp_product = Product.objects.create(name='Temporary product', price=1.99, available=True)
        self.assertEqual(temp_product.name, 'Temporary product')
        self.assertEqual(temp_product.price, 1.99)
        self.assertTrue(temp_product.available)

    def test_create_product_with_negative_price(self):
        with self.assertRaises(ValidationError):
            temp_product = Product.objects.create(name='Invalid product', price=-1.99, available=True)
            temp_product.full_clean()

    def test_create_product_with_missing_name(self):
        with self.assertRaises(ValidationError):
            temp_product = Product.objects.create(price=1.99, available=True)
            temp_product.full_clean()

    def test_create_product_with_boundary_of_name_length_below(self):
        temp_product = Product.objects.create(name='A' * 254, price=1.99, available=True)
        self.assertEqual(temp_product.name, 'A' * 254)
        self.assertEqual(temp_product.price, 1.99)
        self.assertTrue(temp_product.available)

    def test_create_product_with_boundary_of_name_length_exact(self):
        temp_product = Product.objects.create(name='A' * 255, price=1.99, available=True)
        self.assertEqual(temp_product.name, 'A' * 255)
        self.assertEqual(temp_product.price, 1.99)
        self.assertTrue(temp_product.available)

    def test_create_product_with_boundary_of_name_length_above(self):
        with self.assertRaises(DataError):
            temp_product = Product.objects.create(name='A' * 256, price=1.99, available=True)
            temp_product.full_clean()

    def test_create_product_with_boundary_min_value_of_price(self):
        temp_product = Product.objects.create(name='Boundary product', price=0, available=True)
        self.assertEqual(temp_product.name, 'Boundary product')
        self.assertEqual(temp_product.price, 0)
        self.assertTrue(temp_product.available)

    def test_create_product_with_boundary_above_max_value_of_price(self):
        with self.assertRaises(DataError):
            temp_product = Product.objects.create(name='Boundary product', price=10 ** 51, available=True)
            temp_product.full_clean()

    def test_create_product_with_too_high_decimal_places(self):
        with self.assertRaises(ValidationError):
            temp_product = Product.objects.create(name='Invalid product', price=1.9999, available=True)
            temp_product.full_clean()


class CustomerModelTest(TestCase):

    def test_create_customer_with_valid_data(self):
        temp_customer = Customer.objects.create(name='Temporary customer', address='Temporary address')
        self.assertEqual(temp_customer.name, 'Temporary customer')
        self.assertEqual(temp_customer.address, 'Temporary address')

    def test_create_customer_with_field_missing(self):
        with self.assertRaises(ValidationError):
            temp_customer = Customer.objects.create(name='Temporary customer')
            temp_customer.full_clean()

    def test_create_customer_with_edge_value_name_length_below(self):
        temp_customer = Customer.objects.create(name='A' * 99, address='Temporary address')
        self.assertEqual(temp_customer.name, 'A' * 99)
        self.assertEqual(temp_customer.address, 'Temporary address')

    def test_create_customer_with_edge_value_name_length_exact(self):
        temp_customer = Customer.objects.create(name='A' * 100, address='Temporary address')
        self.assertEqual(temp_customer.name, 'A' * 100)
        self.assertEqual(temp_customer.address, 'Temporary address')

    def test_create_customer_with_edge_value_name_length_above(self):
        with self.assertRaises(DataError):
            temp_customer = Customer.objects.create(name='A' * 101, address='Temporary address')
            temp_customer.full_clean()


class OrderModelTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(name='Test customer', address='Test address')
        self.product = Product.objects.create(name='Test product', price=1.99, available=True)
        self.product_n = Product.objects.create(name='not available product', price=1.99, available=False)

    def test_create_order_with_valid_data(self):
        temp_order = Order.objects.create(customer=self.customer, date='2024-12-01', status='N')
        temp_order.products.add(self.product)
        self.assertEqual(temp_order.customer, self.customer)
        self.assertEqual(temp_order.date, '2024-12-01')
        self.assertEqual(temp_order.status, 'N')

    def test_create_order_with_missing_customer(self):
        with self.assertRaises(IntegrityError):
            temp_order = Order.objects.create(date='2024-12-01', status='N')
            temp_order.products.add(self.product)
            temp_order.full_clean()

    def test_total_price_for_orders_with_valid_data(self):
        temp_order = Order.objects.create(customer=self.customer, date='2024-12-01', status='N')
        temp_order.products.add(self.product)
        self.assertEqual(temp_order.price_sum(), Decimal('1.990'))

    def test_total_price_for_orders_without_products(self):
        temp_order = Order.objects.create(customer=self.customer, date='2024-12-01', status='N')
        self.assertEqual(temp_order.price_sum(), 0)

    def test_order_fulfillment_with_unavailable_product(self):
        temp_order = Order.objects.create(customer=self.customer, date='2024-12-01', status='N')
        temp_order.products.add(self.product)
        temp_order.products.add(self.product_n)
        self.assertFalse(all(p.available for p in temp_order.products.all()))
