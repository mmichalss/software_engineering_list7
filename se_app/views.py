import json
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from .models import Product
from decimal import Decimal

@csrf_exempt
def product_list(request):

    if request.method == 'GET':
        if Product.objects.count() == 0:
            return HttpResponseNotFound('<h1>No products found</h1>')
        products = list(Product.objects.values('id', 'name', 'price', 'available'))
        return JsonResponse(products, safe=False)
    elif request.method == 'POST':
        if request.body == b'':
            return HttpResponseBadRequest('<h1>Empty request body</h1>')
        data = json.loads(request.body)
        if not all(key in data for key in ['id', 'name', 'price', 'available']):
            return HttpResponseBadRequest('<h1>Invalid request body</h1>')
        try:
            product_id = int(data.get('id'))
        except (ValueError, TypeError):
            return HttpResponseBadRequest('<h1>Invalid request body: id has to be an integer</h1>')
        if Product.objects.filter(id=product_id).exists():
            return HttpResponseBadRequest('<h1>Product with this id already exists</h1>')

        product_id = data.get('id')
        try:
            name = str(data.get('name'))
        except (ValueError, TypeError):
            return HttpResponseBadRequest('<h1>Invalid request body: name has to be a string</h1>')
        name = data.get('name')
        try:
            price = float(data.get('price'))
            if price < 0:
                raise ValueError
        except (ValueError, TypeError):
            return HttpResponseBadRequest('<h1>Invalid request body: price has to be a positive floating point number</h1>')
        price = data.get('price')
        try:
            available = bool(data.get('available'))
        except (ValueError, TypeError):
            return HttpResponseBadRequest('<h1>Invalid request body: available has to be a boolean</h1>')
        available = data.get('available')

        product = Product(id=product_id, name=name, price=Decimal(str(price)), available=available)
        product.full_clean()
        product.save()

        return JsonResponse({
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'available': product.available
        }, status=201
        )
    else:
        return HttpResponseBadRequest('<h1>Invalid request method</h1>')

@csrf_exempt
def product_detail(request, product_id):
    if request.method == 'GET':
        try:
            product_id = int(product_id)
        except (ValueError, TypeError):
            return HttpResponseBadRequest('<h1>Invalid product id: it has to be integer value</h1>')
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return HttpResponseNotFound('<h1>Product with id: %d not found</h1>' % product_id)
        return JsonResponse({
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'available': product.available
        })
    else :
        return HttpResponseBadRequest('<h1>Invalid request method</h1>')