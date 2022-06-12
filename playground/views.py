from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product, OrderItem, Order
from django.db.models import Q, F


def say_hello(request):
    # query_set = Product.objects.all()
    # When to execute the query_set:
    # 1. When we iterate over the query_set
    # for product in query_set:
    #     print(product.title)
    # when we convey the query_set to a list
    # list(query_set)
    # first_product = Product.objects.get(pk=1)
    # eq_20_products = Product.objects.filter(unit_price=20)
    # gt_20_products = Product.objects.filter(unit_price__gt=20)  # > won't work
    # queryset = Product.objects.filter(unit_price__range=(10, 20))
    # title_contains_coffee = Product.objects.filter(title__icontains='coffee')
    # obj_last_update_in_2021 = Product.objects.filter(last_update__year=2021)
    # Multiple filters
    # obj = Product.objects.filter(inventory__lt=10, unit_price__lt=20)
    # obj = Product.objects.filter(inventory__lt=10).filter(unit_price__lt=20)
    # obj = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20))
    # To match the inventory of the unit price
    # obj = Product.objects.filter(inventory=F('collection__id'))
    obj = Product.objects.order_by('title')
    # order by accepts two arguments:
    obj = Product.objects.order_by('unit_price', '-title').reverse()
    obj = Product.objects.earliest('unit_price')
    # == obj = Product.objects.order_by('unit_price').first()
    # show objects in five pages (0-4)
    obj = Product.objects.all()[:5]
    # show objects in five pages (5-9)
    obj = Product.objects.all()[5:10]
    obj = Product.objects.values('id', 'title', 'collection__title')
    obj = OrderItem.objects.values('product__id')    # get the column of a foreign key
    obj = Product.objects.filter(id__in=OrderItem.objects.values('product__id').distinct()).order_by('title')
    obj = Product.objects.only('id', 'title')
    obj_defer_description = Product.objects.defer('description')
    # prefetch_related is used in many-to-many relationships
    # select_related is used in one-to-one relationships (foreign key)
    obj = Product.objects.prefetch_related('promotions').select_related('collection').all()
    orders = Order.objects.prefetch_related('orderitem_set').select_related('customer').order_by('-placed_at')[:5]
    return render(request, 'hello.html', {'name': 'Mosh', 'orders': list(orders)})
