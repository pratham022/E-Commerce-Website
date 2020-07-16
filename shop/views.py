from django.shortcuts import render
from  django.shortcuts import HttpResponse
from .models import Product, Contact, Order, OrderTracker
import json
from django.views.decorators.csrf import csrf_exempt
from .PayTm import checksum

MERCHANT_KEY = 'u0mOE7WAorLjgSeN'

# Create your views here.


def index(request):
    all_products = Product.objects.all()
    all_categories = []
    for item in all_products:
        if item.category not in all_categories:
            all_categories.append(item.category)
    all_prodlist = []

    for category in all_categories:
        query_set = Product.objects.all().filter(category=category)
        all_prodlist.append(list((category, query_set)))

    params = {'product_list': all_prodlist}
    print(params)
    return render(request, 'shop/index.html', params)

def search(request):
    print('In search ')
    if request.method == 'GET':
        query = request.GET.get('Search', '')
        query = query.lower()
        all_products = Product.objects.all()
        prod_list = []
        for product in all_products:
            if query in product.category.lower() or query in product.subcategory.lower() or query in product.desc.lower() or query in product.product_name.lower():
                prod_list.append(product)
        params = {'product_list': prod_list}
    return render(request, 'shop/searchPage.html', params)


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    thank = False
    if request.method == "POST":
        print("Entered in function")
        name = request.POST.get('name', '')
        phone = request.POST.get('phone_no', '')
        emailid = request.POST.get('emailid', '')
        desc = request.POST.get('desc', '')
        obj = Contact(contact_name=name, contact_phone=phone, contact_email=emailid, contact_query=desc)
        obj.save()
        thank = True
    return render(request, 'shop/contact.html', {'thank': thank})
    # return HttpResponse("Contacts page")


def tracker(request):
    orderId = 0
    emailId = 0
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        emailId = request.POST.get('emailId', '')
    try:
        order = Order.objects.filter(order_id=orderId, email=emailId)
        if len(order) > 0:
            print("here")
            update = OrderTracker.objects.filter(order_id=orderId)
            updates = []
            for item in update:
                updates.append({'text': item.update_des, 'time': item.timestamp })
            response = json.dumps([updates, order[0].items_json], default=str)
            return HttpResponse(response)
        else:
            pass
    except Exception as e:
        print(e)
    print("Reached at the end")
    return render(request, 'shop/tracker.html')


def productview(request, myid):

    product = Product.objects.filter(id=myid)
    print(product)
    return render(request, 'shop/productView.html', {'product': product[0]})


def checkout(request):
    id = 0
    params = {}
    if request.method == 'POST':
        itemjson = request.POST.get('itemJson', '')
        name = request.POST.get('inputName', '')
        email = request.POST.get('inputEmail', '')
        phone = request.POST.get('inputPhone', '')
        address = request.POST.get('inputAddress', '') + ', '+request.POST.get('inputAddress2', '')
        city = request.POST.get('inputCity', '')
        state = request.POST.get('inputState', '')
        zip_code = request.POST.get('inputZip', '')
        amount = request.POST.get('amountTot', '')
        print('Total price received is ', amount)

        order = Order(items_json=itemjson, name=name, email=email, phone=phone, address=address, city=city, state=state, zip_code=zip_code, price=amount)
        order.save()

        orderTracker = OrderTracker(order_id=order.order_id, update_des="The order has been placed")
        orderTracker.save()
        id = order.order_id
        # return render(request, 'shop/checkout.html', params)
        # request phonepe to transfer amount to your account after payment by the user
        param_dict = {

                'MID': 'uvRJWu01267850357128',
                'ORDER_ID': str(order.order_id),
                'TXN_AMOUNT': str(amount),
                'CUST_ID': email,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlerequest',
        }
        param_dict['CHECKSUMHASH'] = checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'shop/paytm.html', {'param_dict': param_dict, 'orderId': id })
    return render(request, 'shop/checkout.html')

# We cannot send or receive POST request from a cross origin.
# Thus when payment is doen by the user, how eill phonepe inform us about payment status (successfull/failed) ?
# So, we have to bypass the csrf verification for that endpoint

@csrf_exempt
def handlerequest(request):
    # Phonepe will send you post request here
    # We use csrf_exempt so that phonepe can send post request to our website
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            chksum = form[i]

    verify = checksum.verify_checksum(response_dict, MERCHANT_KEY, chksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            orderId = int(response_dict['ORDERID'])
            order = Order.objects.get(order_id=orderId)
            order_stat = OrderTracker.objects.get(order_id=orderId)
            order.delete()
            order_stat.delete()
            print('order was not successful because ' + response_dict['RESPMSG'])
    return render(request, 'shop/paymentstatus.html', {'response': response_dict})


