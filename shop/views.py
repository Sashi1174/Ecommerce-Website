from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Product,Contact,Orders,Order_update
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt
from PayTm import checksum
from django.contrib import messages
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate,login,logout
MERCHANT_KEY = 'kbzk1DSbJiV_03p5'
def index(request):
    products=Product.objects.all()
    n=len(products)
    nSlides=n//4+ceil((n/4)+(n//4))
    #params={'no_of_slides':nSlides,'range':range(1,nSlides),'product':products}
    allProd=[]
    catprods=Product.objects.values('category','id')
    cats={item['category'] for item in catprods}
    for cat in cats:
        prod=Product.objects.filter(category=cat)
        n=len(prod)
        nSlides=n//4+ceil((n/4)-(n//4))
        allProd.append([prod,range(1,nSlides),nSlides])
    params={'allProd':allProd}
    return render(request,'shop/index.html',params)

def searchMatch(query,item):
    if query in item.product_name or query in  item.desc.lower() or query in  item.category:
        return True 
    return False

def search(request):
    query= request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod=[item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nSlides=n//4+ceil((n/4)-(n//4))
        if len(prod)!=0:
            allProds.append([prod,range(1,nSlides),nSlides])
    params = {'allProds': allProds, "msg": ""}
    if len(allProds) == 0 or len(query)<4:
        params = {'msg': "Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', params)

def about(request):
    return render(request,'shop/about.html')
def contact(request):
    if(request.method=='POST'):
        print(request)
        name=request.POST.get('name','')
        print(name)
        email=request.POST.get('email','')
        phone=request.POST.get('phone','')
        desc=request.POST.get('desc','')
        contact=Contact(name=name,email=email,phone=phone,desc=desc)
        contact.save()
        thank=True
        return render(request,'shop/contact.html',{'thank':thank})
    return render(request,'shop/contact.html')
def tracker(request):
    if(request.method=='POST'):
        orderId=request.POST.get('order_id','')
        email=request.POST.get('email','')
       # return HttpResponse(f'{orderId,email}')
        try:
            order=Orders.objects.filter(order_id=orderId,email=email)
            if len(order)>0:
                update=Order_update.objects.filter(order_id=orderId)
                updates=[]
                for item in update:
                    updates.append({'text':item.update_desc,'time':item.timestamp})
                    response=json.dumps([updates,order[0].items_json],default=str)
                return HttpResponse(response)
            else:
                return HttpResponse({})
        except Exception as e:
            return HttpResponse({})
    return render(request,"shop/tracker.html")

def products(request,myid):
    product=Product.objects.filter(id=myid)
    return render(request,"shop/prodView.html",{'product':product[0]})
def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')

        try:
            amount = int(request.POST.get('amount', 0) or 0)  # Convert to int, default to 0
        except ValueError:
            return HttpResponse("Invalid amount", status=400)

        order = Orders(
            items_json=items_json, name=name, amount=amount, email=email,
            address=address, city=city, state=state, zip_code=zip_code, phone=phone
        )
        order.save()

        update = Order_update(order_id=order.order_id, update_desc="The Order has been Placed")
        update.save()

        param_dict = {
            'MID': 'WorldP64425807474247',
            'ORDER_ID': str(order.order_id),  # Ensure ORDER_ID is a string
            'TXN_AMOUNT': str(amount),  # Ensure TXN_AMOUNT is a string
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/shop/handlerequest/',
        }
        param_dict['CHECKSUMHASH'] = checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'shop/paytm.html', {'param_dict': param_dict})

    return render(request, "shop/checkout.html")

# Create your views here.

@csrf_exempt
def handlerequest(request):
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return HttpResponse('done')
    

def handleSignUp(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        if len(username)<10:
            messages.error(request, " Your user name must be under 10 characters")
            return redirect('home')
        if not username.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
            return redirect('home')
        if (pass1!= pass2):
             messages.error(request, " Passwords do not match")
             return redirect('home')
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your iCoder account has been successfully created!")
        return redirect('home')
    else:
        return HttpResponse("404 - Not found")

def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('home')

def handleLogin(request):
    if request.method=="POST":
        # Get the post parameters
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']
        user=authenticate(username= loginusername, password= loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("home")
        else:
            messages.error(request,"Invalid credentials! Please try again")
            return redirect("home")
    return HttpResponse("404-Not found")