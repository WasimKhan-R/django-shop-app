import imp
from itertools import product
from pydoc import describe
from turtle import update
from unicodedata import name
from urllib import response
from django.shortcuts import render
from django.http import HttpResponse
from .models import Product,Contact,Orders,OrderUpdate
from math import ceil
import json
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect
# Create your views here.

def index(request):
    # products = Product.objects.all()
    # print(products)

    # n =len(products)
    # nSlides = n//4 +ceil((n/4)-(n//4))

    allProds = []
    catprods = Product.objects.values('category','id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        n =len(prod)
        nSlides = n//4 +ceil((n/4)-(n//4))
        allProds.append([prod, range(1,nSlides), nSlides])
    # params = {'no_of_slides':nSlides, 'range':range(nSlides), 'product': products}
    # allProds=[[products, range(1, len(products)), nSlides],[products, range(1, len(products)), nSlides]]
    # params={'allProds':allProds }
    params = {'allProds':allProds}
    return render(request,'shop/index.html', params)

def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    thank = False
    if request.method == 'POST':
        name =request.POST.get('name','')
        # print(name);
        email =request.POST.get('email','')
        contact =request.POST.get('phone','')
        desc =request.POST.get('desc','')
        contact = Contact(name=name, email=email, phone=contact, desc=desc)
        contact.save()
        thank = True
        # messages.info(request, 'Your password has been changed successfully!')
        # return HttpResponseRedirect('/');

        # print(name, email , contact, desc);
        # print(request);
    return render(request,'shop/contact.html',{'thank':thank})

def track(request):
    if request.method == 'POST':
        orderId = request.POST.get('orderId','')
        email = request.POST.get('email', '')
        # comment line is for print the orderid and email in console
        # return HttpResponse(f'{orderId} and {email}')
        try:
            order = Orders.objects.filter(order_id=orderId,email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps([updates , order[0].items_json], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')    
    return render(request,'shop/tracker.html')


# def track(request):
#     if request.method=="POST":
#         orderId = request.POST.get('orderId', '')
#         email = request.POST.get('email', '')
#         try:
#             order = Orders.objects.filter(order_id=orderId, email=email)
#             if len(order)>0:
#                 update = OrderUpdate.objects.filter(order_id=orderId)
#                 updates = []
#                 for item in update:
#                     updates.append({'text': item.update_desc, 'time': item.timestamp})
#                     response = json.dumps(updates, default=str)
#                 return HttpResponse(response)
#             else:
#                 return HttpResponse('{}')
#         except Exception as e:
#             return HttpResponse('{}')

#     return render(request, 'shop/tracker.html')


def search(request):
    return render(request,'shop/search.html')


def checkout(request):
    if request.method=="POST":
        items_json= request.POST.get('itemsJson', '')
        name=request.POST.get('name', '')
        amount=request.POST.get('amount', '')
        email=request.POST.get('email', '')
        address=request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city=request.POST.get('city', '')
        state=request.POST.get('state', '')
        zip_code=request.POST.get('zip_code', '')
        phone=request.POST.get('phone', '')
        order = Orders(items_json= items_json, name=name, email=email, address= address, city=city, state=state, zip_code=zip_code, phone=phone , amount=amount)
        order.save()
        update = OrderUpdate(order_id= order.order_id , update_desc = "THE order has been placed")
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})
    return render(request,'shop/checkout.html')

def productView(request, myid):
    # Fetch the product using id 
    product = Product.objects.filter(id = myid)
    # print(product);
    return render(request,'shop/productview.html', {'product':product[0]})


