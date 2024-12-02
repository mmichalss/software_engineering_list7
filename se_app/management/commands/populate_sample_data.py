from django.core.management import BaseCommand

from se_app.models import Product, Order, Customer


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        Product.objects.all().delete()
        Customer.objects.all().delete()
        Order.objects.all().delete()

        product1 = Product.objects.create(
            id=1,
            name='First products',
            price=19.99,
            available=True
        )

        customer1 = Customer.objects.create(
            id=1,
            name='Our first customer',
            address='1 First Street'
        )

        order1 = Order.objects.create(
            id=1,
            customer=customer1,
            status='N',
            date='2011-11-11'
        )
        order1.products.add(product1)

        product2 = Product.objects.create(
            id=2,
            name='Second product',
            price=29.99,
            available=True
        )

        customer2 = Customer.objects.create(
            id=2,
            name='Our second customer',
            address='2 Second Street'
        )

        order2 = Order.objects.create(
            id=2,
            customer=customer2,
            status='N',
            date='2022-12-22'
        )
        order2.products.add(product2)

        product3 = Product.objects.create(
            id=3,
            name='Third product',
            price=39.99,
            available=True
        )

        customer3 = Customer.objects.create(
            id=3,
            name='Our third customer',
            address='3 Third Street'
        )

        order3 = Order.objects.create(
            id=3,
            customer=customer3,
            status='N',
            date='2033-03-31'
        )
        order3.products.add(product3)

        self.stdout.write("Data created successfully.")