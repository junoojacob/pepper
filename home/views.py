from subprocess import check_output
from unicodedata import category, name
from urllib import request
from django.shortcuts import render,redirect
from home import *
from django.contrib.auth.models import User,auth
from django.contrib.auth import *
import random as r
from twilio.rest import Client
from .models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.core.cache import cache
import razorpay
import copy
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test
from datetime import *
import datetime
from datetime import date
from django.http import HttpResponse
from django.template.loader import render_to_string
import csv
import uuid 
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.pagesizes import A4
from django.core.paginator import Paginator


phone=''
User = get_user_model()

#USER LOGIN
@never_cache
def home(request):
    '''Displays home page without filter'''
    #request.session.flush()
    category=Category.objects.all()
    brand=Products.objects.all().distinct()
    product=Products.objects.filter(stock__gte=1)
    product_offers=Productoffer.objects.all()
    category_offers=Categoryoffer.objects.all()
    cart_items=Cart.objects.filter(cart_id=_cart_id(request))
    paginator = Paginator(product, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'home.html',{'products':page_obj,'category'
                :category,'brand':brand,'poffers':product_offers,
                'coffers':category_offers,'cart_items':cart_items})


def home_sortby_category(request,value):
    '''Displays home page filtered by category '''
    category_offers=Categoryoffer.objects.all()
    brand=Products.objects.all().distinct()
    product_offers=Productoffer.objects.all()
    category=Category.objects.all()
    cart_items=Cart.objects.filter(cart_id=_cart_id(request))
    if value==1:
        product=Products.objects.all()
        return render(request,'home.html',{'products':product,'category':category,
            'brand':brand,'poffers':product_offers,'coffers':category_offers,
            'cart_items':cart_items})
    else:
        product=Products.objects.filter(stock__gte=1,category=value)
        paginator = Paginator(product, 8)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request,'home.html',{'products':page_obj,'category':category,
            'brand':brand,'poffers':product_offers,'coffers':category_offers,
            'cart_items':cart_items})


def home_sortby_product_offer(request,value):
    '''Displays home page filtered by product offers'''
    category_offers=Categoryoffer.objects.all()
    brand=Products.objects.all().distinct()
    product_offers=Productoffer.objects.all()
    category=Category.objects.all()
    product=Products.objects.filter(stock__gte=1,name=value)
    cart_items=Cart.objects.filter(cart_id=_cart_id(request))
    paginator = Paginator(product, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'home.html',{'products':page_obj,'category':category,
                'brand':brand,'poffers':product_offers,'coffers':category_offers
                ,'cart_items':cart_items})


def shome_sortby_category_offer(request,value):
    '''Displays home page filtered by category offers'''
    brand=Products.objects.all().distinct()
    product_offers=Productoffer.objects.all()
    category=Category.objects.all()
    category_offers=Categoryoffer.objects.all()
    cat=Category.objects.get(category=value).pk
    product=Products.objects.filter(stock__gte=1,category=cat)
    cart_items=Cart.objects.filter(cart_id=_cart_id(request))
    paginator = Paginator(product, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'home.html',{'products':page_obj,'category':category,
            'brand':brand,'poffers':product_offers,'coffers':category_offers,
            'cart_items':cart_items})


def home_sortby_brands(request,value):
    '''Displays home page filtered by brands'''
    category_offers=Categoryoffer.objects.all()
    brand=Products.objects.all().distinct()
    product_offers=Productoffer.objects.all()
    category=Category.objects.all()
    product=Products.objects.filter(stock__gte=1,brand=value)
    cart_items=Cart.objects.filter(cart_id=_cart_id(request))
    paginator = Paginator(product, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'home.html',{'products':page_obj,'category':category,
            'brand':brand,'poffers':product_offers,'coffers':category_offers,
            'cart_items':cart_items})


def home_sortby_price(request,value):
    '''Displays home page filtered by price range'''
    coffers=Categoryoffer.objects.all()
    category=Category.objects.all()
    brand=Products.objects.all().distinct()
    poffers=Productoffer.objects.all()
    cart_items=Cart.objects.filter(cart_id=_cart_id(request))

    if value==1:
        product=Products.objects.filter(price__lte=200)
        paginator = Paginator(product, 8)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request,'home.html',{'products':page_obj,'category'
                    :category,'brand':brand,'poffers':poffers,'coffers':coffers,
                    'cart_items':cart_items})
    if value==2:
        product=Products.objects.filter(price__gte=200,price__lte=500)
        paginator = Paginator(product, 8)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request,'home.html',{'products':page_obj,'category':category,
                                            'brand':brand,'poffers':poffers,
                                        'coffers':coffers,'cart_items':cart_items})
    if value==3:
        product=Products.objects.filter(price__gte=500)
        paginator = Paginator(product, 8)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request,'home.html',{'products':page_obj,'category':category,
                                            'brand':brand,'poffers':poffers,
                                        'coffers':coffers,'cart_items':cart_items})


def product_detail(request,id):
    '''Displays page with individual product detail'''
    product=Products.objects.get(id=id)
    cart_items=Cart.objects.filter(cart_id=_cart_id(request))
    return render(request,'productdetail.html',{'product':product,
                                                'cart_items':cart_items})


@never_cache
def sign_in(request):
    '''User login'''
    cart_items=Cart.objects.filter(cart_id=_cart_id(request))
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user is not None :
            temp=_cart_id(request)
            login(request,user)
            cart=Cart.objects.filter(cart_id=temp)
        
            for item in cart:
            
                if Cart.objects.filter(product=item.product, cart_id
                                        =_cart_id(request)).exists():
                    usercart=Cart.objects.get(cart_id=_cart_id(request),
                                                product=item.product)
                    usercart.quantity=int(usercart.quantity)+int(item.quantity)
                    usercart.save()
                    item.delete()
                    item.save()
                    pass
                else:
                    print('in else')
                    cart=Cart.objects.filter(cart_id=temp).update(cart_id
                                                            =_cart_id(request))
            return redirect('home')
        else:
            return render(request,'login.html',{'message'
                                                :"Invalid User Credentials",'cart_items':cart})
    return render(request,'login.html',{'cart_items':cart_items})

def sign_out(request):
    '''Logs-out user'''
    logout(request)        
    return redirect(home)

def register(request):
    '''Requests user details for User Registeration'''
    if request.method=='POST':
        global username,password,email,phone
        username=request.POST.get('username')
        password=request.POST.get('password')
        email=request.POST.get('email')
        password1=request.POST.get('password1')
        phone=request.POST.get('phone')
        
        if User.objects.filter(username=username).exists():
            return render(request,'register.html',{'message':"User name taken"})
        elif User.objects.filter(email=email).exists():
            return render(request,'register.html',{'message'
                                        :"Already registered with Same email"})
        elif password1 != password:
            return render(request,'register.html',{'message'
                                            :"Retype Password did not Match!"})
        elif User.objects.filter(phone=phone).exists():
            return render(request,'register.html',{'message'
                                        :"Already registered with Same mobile"})
        else:
             client = Client('ACadba95c4d4ec74cfc0c3653669372c39',
                                            'xxxxxxxxxxxxxxxxxxxxxxxxx')
             verification = client.verify \
                    .services('VA43ac7cbc65d5fbed5c8d59b8fc1ff10d') \
                    .verifications \
                    .create(to='+91{}'.format(phone), channel='sms')
        
             return render(request,'registerverification.html')
    else:
        return render(request,'register.html')


def register_verification(request):
    '''Completes user Registation after verification'''
    if request.method=='POST':
        otp1=request.POST.get('otp')
        client = Client('ACadba95c4d4ec74cfc0c3653669372c39', 
                        'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        verification_check = client.verify \
                .v2 \
                .services('VA43ac7cbc65d5fbed5c8d59b8fc1ff10d') \
                .verification_checks \
                .create(to='+91{}'.format(phone), code=otp1)
        print(verification_check.status)
        if verification_check.status == "approved":
            user=User.objects.create_user(username=username,password=
                                    password,email=email,phone=phone)
            user.save()
            return render(request,'login.html',{'message':
                                                "New User Created"})
        else:
            return render(request,'registerverification.html',
                                            {'message':"invalid OTP"})
    else:
        return render(request,'registerverification.html')


def sms_login(request):
    '''Gets user info for SMS based login'''
    if request.method=='POST':
        global phone
        phone=request.POST.get('phone')

        if User.objects.filter(phone=phone).exists():
             user=User.objects.get(phone=phone).username
             client = Client('ACadba95c4d4ec74cfc0c3653669372c39',
                                    'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
             verification = client.verify \
                    .v2 \
                    .services('VA43ac7cbc65d5fbed5c8d59b8fc1ff10d') \
                    .verifications \
                    .create(to='+91{}'.format(phone), channel='sms')
             return render(request,'otplogin.html')
        else:
        
            return render(request,'smslogin.html',{'message':"invalid phone"})

    else:
        return render(request,'smslogin.html')


def otp_login(request):
    '''Verifys and Logs in user with SMS OTP'''
    user=User.objects.get(phone=phone)
    if request.method=='POST':
        Otp1=request.POST.get('otp')
        client = Client('ACadba95c4d4ec74cfc0c3653669372c39', 
                            'xxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        verification_check = client.verify \
                .v2 \
                .services('VA43ac7cbc65d5fbed5c8d59b8fc1ff10d') \
                .verification_checks \
                .create(to='+91{}'.format(phone), code=Otp1)
        
        print(verification_check.status)
        if verification_check.status == "approved":
            temp=_cart_id(request)
            auth.login(request,user)
            cart=Cart.objects.filter(cart_id=temp)
        
            for item in cart:
            
                if Cart.objects.filter(product=item.product, 
                                        cart_id=_cart_id(request)).exists():   
                    usercart=Cart.objects.get(cart_id=_cart_id(request),
                                                        product=item.product)
                    usercart.quantity=int(usercart.quantity)+int(item.quantity)
                    usercart.save()
                    item.delete()
                    item.save()
                    pass
                else:
                    print('in else')
                    cart=Cart.objects.filter(cart_id=temp).update(cart_id=
                                                            _cart_id(request))
            return redirect(home)

        else:
            return render (request,'otplogin.html',{'message':'Invalid OTP'})
    else:
        return render(request,'otplogin.html')


def resend_otp(request):
    '''Resends OTP for User Registeration and SMS based login'''
    client = Client('ACadba95c4d4ec74cfc0c3653669372c39',
                                            'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
    verification = client.verify \
                    .v2 \
                    .services('VA43ac7cbc65d5fbed5c8d59b8fc1ff10d') \
                    .verifications \
                    .create(to='+91{}'.format(phone), channel='sms')
    return render(request,'otplogin.html')


def profile(request):
    '''Displays user profile details of Current User'''
    user=User.objects.get(username=_cart_id(request))
    order=Orders.objects.filter(cartID=_cart_id(request))
    address=Address.objects.filter(username=_cart_id(request))
    cart_items=Cart.objects.filter(cart_id=_cart_id(request))

    return render(request,'profile.html',{'user':user,'orders':order,
                        'address':address,'cart_items':cart_items})



def update_profile(request):
    '''Lets Current User Edit User info'''
    user=User.objects.get(username=_cart_id(request))
    if request.method=='POST':
        first_name=request.POST['name']
        phone=request.POST['phone']
        user.first_name=first_name
        user.phone=phone
        user.save()
        return redirect (profile)
        
    else:
        return render(request,'updateprofile.html',{'user':user})


def add_address(request):
    '''Lets Current user Add Address to his profile'''
    if request.method=='POST':
        building=request.POST['building']
        street=request.POST['street']
        area=request.POST['area']
        po=request.POST['po']
        district=request.POST['district']
        state=request.POST['state']
        Address.objects.create(username=_cart_id(request),building=building,
                             street=street,area=area,po=po,district=district
                             ,state=state)
        return redirect (profile)


#ADMIN LOGIN
def admin_login(request):
    '''Logs in Administrator'''
    if 'username' in request.session :
        return redirect(admin_dash)
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate (username=username,password=password)
        if  user is not None and user.is_superuser :
            request.session['username']=username
            auth.login(request,user)
            mydata=User.objects.all()
            return redirect(admin_dash)
        else:
            return render(request,'adminlogin.html',{'message'
                                            :"Invalid Admin Credentials"})

    return render(request,'adminlogin.html')

@never_cache
@user_passes_test(lambda u: u.is_superuser)   
def admin_dash(request):
    '''Renders Administrator Dashboard to admin'''
    labels=[]
    data=[]
    label=[]
    querryset =Orders.objects.order_by('orderDate').distinct('orderDate')
    for date in querryset:
        labels.append(date.orderDate)
    for date in labels:
        count=Orders.objects.filter(orderDate=date).count()
        data.append(count)
    for date in querryset:
        da=date.orderDate.strftime('%m/%d/%Y')
        label.append(da)
    
    plabels=[]
    pdata=[]
    pquerryset =Orders.objects.order_by('product').distinct('product')
    for product in pquerryset:
        plabels.append(product.product)
    for product in plabels:
        count=Orders.objects.filter(product=product).count()
        pdata.append(count)

    slabels=[]
    sdata=[]
    slabel=[]
    squerryset =Orders.objects.order_by('orderDate').distinct('orderDate')
    for date in squerryset:
        slabels.append(date.orderDate)
    for date in slabels:
        sale=Orders.objects.filter(orderDate=date)
        tsale=0
        for item in sale:
            tsale=item.sale+tsale
        sdata.append(tsale)
    for date in squerryset:
        da=date.orderDate.strftime('%m/%d/%Y')
        slabel.append(da)


    if 'username' in request.session :
        mydata=User.objects.all()
        return render(request,'admindash.html',{'datas':mydata,'labels':label,
                                                'data':data,'plabel':plabels,
                                                'pdata':pdata,'slabel':slabel,
                                                'sdata':sdata})
    else:
        return redirect(admin_login)

#CATEGORY MANAGEMNT
@never_cache
@user_passes_test(lambda u: u.is_superuser)
def admin_category(request):
    '''Renders Category page for admin'''   
    data=Category.objects.all()
    return render(request,'admincategory.html',{'datas':data})

@never_cache
@user_passes_test(lambda u: u.is_superuser)
def add_category(request):
    '''Allows admin to add category'''
    category=request.POST.get('category')
    data=Category.objects.all()
    if Category.objects.filter(category=category).exists():
        return render(request,'admincategory.html',{'datas':data,'message':"Category Exists"})
    Category.objects.create(category=category)
    return redirect(admin_category)
        
    
@never_cache
@user_passes_test(lambda u: u.is_superuser)   
def delete_category(request,id):
    '''Allows admin to delete Category'''
    mydata=Category.objects.get(id=id)
    mydata.delete()
    return redirect(admin_category)


@never_cache
@user_passes_test(lambda u: u.is_superuser) 
def edit_category(request,id):
    '''Allows admin to edit category'''
    mydata=Category.objects.get(id=id)
    category=mydata.category
    if request.method=='POST':
        newcategory=request.POST.get('category')
        if Category.objects.filter(category=newcategory).exists():
            return render(request,'editcategory.html',{'message':"Category Exists"})
        mydata.category=newcategory
        mydata.save()
        return redirect(admin_category)
    return render(request,'editcategory.html',{'data':mydata})    

#USER MANAGEMENT
@never_cache
@user_passes_test(lambda u: u.is_superuser)
def admin_user(request):
    '''Dispalys user details to admin'''   
    data=User.objects.all()
    return render(request,'adminuser.html',{'datas':data})


@never_cache
@user_passes_test(lambda u: u.is_superuser)
def block(request):
    '''Allows Admin to block and unblock users'''
    if request.method=='POST':
        id=request.POST.get('id')
        action=request.POST.get('action')
        user=User.objects.get(id=id)
        if action=='False':
           user.block="True"
           button="Unblock"
           user.save()
        else:
            user.block="False"
            user.save()
            button="Block"
        update=user.block
        return JsonResponse({
            'update':update,'button':button
            })
    

#PRODUCT MANAGEMENT
@never_cache
@user_passes_test(lambda u: u.is_superuser)
def admin_products(request):
    '''Renders the Avalible products in the inventory'''
    labels=[]
    data=[]
    label=[]
    querryset =Orders.objects.order_by('product').distinct('product')
    for product in querryset:
        labels.append(product.product)
    for product in labels:
        count=Orders.objects.filter(product=product).count()
        data.append(count)

    productdata=Products.objects.all()
    return render(request,'adminproducts.html',{'datas':productdata,'label':labels,'data':data})


@never_cache
@user_passes_test(lambda u: u.is_superuser)
def add_product(request):
    '''Allows admin to add New Products'''
    if request.method=='POST':
        name=request.POST['name']
        detail=request.POST['detail']
        price=request.POST['price']
        stock=request.POST['stock']
        brand=request.POST['brand']
        category=request.POST['category']
        image1=request.FILES['image1']
        image2=request.FILES['image2']
        image3=request.FILES['image3']
        image4=request.FILES['image4']
        cat=Category.objects.get(category=category)
        new_product=Products.objects.create(name=name,detail=detail,price=price,stock=stock,brand=brand,category=cat,product_image1=image1,product_image2=image2,product_image3=image3,product_image4=image4)
        new_product.save()
        return redirect(admin_products)
    else:
        data=Category.objects.all()
        return render(request,'addproduct.html',{'datas':data})


@never_cache
@user_passes_test(lambda u: u.is_superuser)    
def product_delete(request,id):
    '''Allows admin to delete product from inventory'''
    mydata=Products.objects.get(id=id)
    mydata.delete()
    return redirect(admin_products) 


@never_cache
@user_passes_test(lambda u: u.is_superuser)
def edit_product(request,id):
    '''Allows admin to edit product and inventory status'''
    mydata=Products.objects.get(id=id)
    if request.method=='POST':
        mydata.name=request.POST['name']
        mydata.detail=request.POST['detail']
        mydata.price=request.POST['price']
        mydata.stock=request.POST['stock']
        mydata.brand=request.POST['brand']
        mydata.save()
        productdata=Products.objects.all()
        return render(request,'adminproducts.html',{'datas':productdata})
    return render(request,'editproduct.html',{'data':mydata})


#CART MANAGEMENT
def _cart_id(request):
    '''Returns the current user/if no user exist returns session key'''
    current_user = request.user
    if request.user.is_authenticated:
        cart=current_user.username
        print('in current user')
        print(cart)
    else:
        cart=request.session.session_key
        print('get session key')
        if not cart:
            cart=request.session.create()
            print('create session')
    return cart


def cart(request):
    '''Renders the cart items to the User'''
    try:
        cart=Cart.objects.filter(cart_id=_cart_id(request))    
        total=0    
        for item in cart:
            total= total+ item.price

        return render(request,'cart.html',{'cart_items':cart,'total':total})
    except Cart.DoesNotExist:
        return render(request,'cart.html')

def add_cart(request,id):
    '''Adds itmes to the cart of currentuser'''
    product=Products.objects.get(id=id)
    price=int(round(float(product.price)))
    try:
        cart=Cart.objects.get(product=product,cart_id=_cart_id(request))
        cart.quantity +=1
        product.stock =int(product.stock)-1
        product.save()
        cart.price =int(price)*int(cart.quantity)
        cart.save()
    except Cart.DoesNotExist:
        cart=Cart.objects.create(
            product=product,
            quantity=1,
            price=price,
            cart_id=_cart_id(request)
        )
        cart.save()
        product.stock =int(product.stock)-1
        product.save()
    return redirect('home')

def delete_item(request,id):
    '''Deletes itmes in cart of the current user '''
    product=Products.objects.get(id=id)
    cart_item=Cart.objects.get(product=product,cart_id=_cart_id(request))
    cart_quantity=cart_item.quantity
    product.stock=int(product.stock)+int(cart_quantity)
    product.save()
    cart_item.delete()
    return redirect('cart')


def sub(request):
    '''Substracts the quantity of specfic item in cart'''
    if request.method=='POST':
        id=request.POST.get('id')
        product=Products.objects.get(id=id)
        cart_item=Cart.objects.get(cart_id=_cart_id(request),product=product)
        if cart_item.quantity>1:
            product.stock=int(product.stock)+1
            product.save()
            cart_item.quantity -=1
            cart_item.price=int(cart_item.quantity)*int(product.price)
            cart_item.save()
            updated_quantity=cart_item=Cart.objects.get(cart_id=_cart_id(request),product=product).quantity
            updated_price=cart_item=Cart.objects.get(cart_id=_cart_id(request),product=product).price
            cart=Cart.objects.filter(cart_id=_cart_id(request))    
            total=0    
            for item in cart:
                total= total+ item.price
            
            return JsonResponse({
                'updated_quantity':updated_quantity,
                'updated_price':updated_price,
                'updatedtotal':total

             })


def add(request):
    '''Adds the quantity of specfic item in cart'''
    if request.method=='POST':
        id=request.POST.get('id')
        product=Products.objects.get(id=id)
        cart_item=Cart.objects.get(cart_id=_cart_id(request),product=product)
        if int(product.stock)>1:
            product.stock=int(product.stock)-1
            product.save()
            cart_item.quantity +=1
            cart_item.price=int(cart_item.quantity)*int(product.price)
            cart_item.save()
            updated_price=cart_item=Cart.objects.get(cart_id=_cart_id(request),product=product).price
            updated_quantity=cart_item=Cart.objects.get(cart_id=_cart_id(request),product=product).quantity
            cart=Cart.objects.filter(cart_id=_cart_id(request))    
            total=0    
            for item in cart:
                total= total+ item.price
            
            return JsonResponse({
                'updated_quantity':updated_quantity,
                'updated_price':updated_price,
                'updatedtotal':total
            })
    
    
def order(request):
    '''Item in the cart are billed and pament made'''
 
    if request.user.is_authenticated :
        cart_item=Cart.objects.filter(cart_id=_cart_id(request))
        user=User.objects.get(username=_cart_id(request))
        address=Address.objects.filter(username=_cart_id(request))
        print (address)
        try:
            print(request.session['discount'])
        except:
            request.session['discount']=1

        if len(cart_item)!=0:
            Total=0
            Gtotal=0
            for item in cart_item:
                 Total=Total+item.price
            Total=Total*(request.session['discount'])
            Gtotal=Total*100
            if request.method=='POST':
                client = razorpay.Client(auth=("rzp_test_HxUuQwTNW4Y560", "g4Vy7wQcsFBOnhdtQT06fi4A"))
                DATA = {
                    "amount": 100,
                    "currency": "INR",
                    "receipt": "receipt#1",
                    "notes": {
                    "key1": "value3",
                    "key2": "value2"
                            }
                        }
                client.order.create(data=DATA)
            dtotal=round(Total/83)
            return render(request,'order.html',{'cart_items':cart_item,
                                                'total':Total,'Gtotal':Gtotal,
                                                'dtotal':dtotal,'address':address})
        else:
            return redirect('cart')        
    else:
        return redirect('signin')
    
def checkout(request):
    '''Item in the cart is converted to order'''
    address=request.POST.get('address')
    user=User.objects.get(username=_cart_id(request))
    cart_item=Cart.objects.filter(cart_id=_cart_id(request))
    current_order=copy.copy(cart_item)
    try:
        ordernumber=int(OrderNumber.objects.get(id=1).orderNumber)
    except:
        ordernumber='0'
    ordernumber=ordernumber+1
    Total=0
    for item in cart_item:
        price=int(item.price)*int(item.quantity)*(request.session['discount'])
        order=Orders.objects.create(orderNumber=ordernumber,cartID=_cart_id(request),
                                    product=item.product.name,quantity=item.quantity,
                                    address=address,status='Ordered',sale=price)
        Total=Total+item.price
    for item in current_order:
        item.price=item.price*request.session['discount']
    Total=Total*(request.session['discount'])
    cart_item.delete()
    del request.session['discount']
    try:
        order_number=OrderNumber.objects.get(id=1)
    except: 
        OrderNumber.objects.create(id=1,orderNumber='0')
    order_number=OrderNumber.objects.get(id=1)
    order_number.orderNumber=ordernumber
    order_number.save()
    phone=User.objects.get(username=_cart_id(request)).phone
    order=Orders.objects.filter(cartID=_cart_id(request))
    return render(request,'checkout.html',{'currentorders':current_order,'total':Total,'orders':order})


def admin_order(request):
    '''Provides Admin with status of orders'''
    order=Orders.objects.order_by('id').all()
    return render(request,'adminorder.html',{'order':order})


def cancel_order(request,id):
    '''Alows the user to Cancel the order'''
    Orders.objects.filter(id=id).update(status='Cancelled')
    return redirect('profile')


def return_order(request,id):
    '''Allows User to return the order'''
    Orders.objects.filter(id=id).update(status='Return')
    return redirect('profile')


def shipped(request,id):
    '''Lets Admin changes the order status to shipped'''
    Orders.objects.filter(id=id).update(status='Shipped')
    return redirect('adminorder')
      

def out_for_delivery(request,id):
    '''Lets Admin changes the order status to out for delivery'''
    Orders.objects.filter(id=id).update(status='Out for Delivery')
    return redirect('adminorder')


def delivered(request,id):
    '''Lets Admin changes the order status to delivered'''
    Orders.objects.filter(id=id).update(status='Delivered')
    return redirect('adminorder')


def approve(request,id):
    '''Lets the Admin to approve the Return request by user'''
    Orders.objects.filter(id=id).update(status='Approved')
    return redirect('adminorder')


def reports(request):
    '''Generates Sales Report by date'''
    if request.method=='POST':
        startdate=request.POST.get('startdate')
        enddate=request.POST.get('enddate')
        print(startdate)
        print(enddate)
        order=Orders.objects.order_by('orderDate').filter(orderDate__gte=
                                        startdate,orderDate__lte=enddate)
        Total=0
        for item in order:
            if item.status != "Cancelled" or item.status !="Approved":
                Total=item.sale+Total
            else:
                pass
        return render (request,'report.html',{'order':order,'total':Total})
    order=Orders.objects.order_by('orderDate').all()
    Total=0
    for item in order:
        Total=item.sale+Total
    return render (request,'report.html',{'order':order,'total':Total})


def coupons(request):
    '''Lets Admin generate discout coupons'''
    coupon=Coupon.objects.all()
    if request.method=='POST':
        discount=request.POST.get('discount')
        
        if int(discount) > 20:
            return render (request,'coupons.html',{'message':
                'Discount can not be Greater than 20%','datas':coupon})
        else:
            code=uuid.uuid4().hex[:6].upper()
            Coupon.objects.create(code=code,discount=discount,status='Active')
            return redirect(coupons)

    return render (request,'coupons.html',{'datas':coupon})

def discount(request):
    '''Lets User Apply Discounts using coupons'''
    if request.method=='POST':
        code=request.POST.get('code')
        coupon=Coupon.objects.get(code=code)
        if Coupon.objects.filter(code=code).exists() and coupon.status =='Active':
            coupon=Coupon.objects.get(code=code)
       
            dis=(1-int(coupon.discount)/100)
            request.session['discount'] = dis
            coupon.status="Used"
            coupon.save()
            return JsonResponse({
                'dis':dis
                })
        else:
            print('coupon do not ')


def offers(request):
    '''Displays Active offers to admin'''
    product=Products.objects.all()
    category=Category.objects.all()
    poffers=Productoffer.objects.all()
    coffers=Categoryoffer.objects.all()
    return render (request,'offers.html',{'product':product,
                'category':category,'poffers':poffers,'coffers':coffers})


def product_offer(request):
    '''Lets Admin create Offers for individual products'''
    if request.method=='POST':
        discount=request.POST.get('discount')
        product=request.POST.get('product')
        Productoffer.objects.create(product=product,discount=discount)
        product=Products.objects.get(name=product)
        product.price=float(product.price)-float(product.price)*float(discount)/100
        product.save()
        return redirect(offers)


def category_offer(request):
    '''Let Admin create offers for a whole category of products'''
    if request.method=='POST':
        discount=request.POST.get('discount')
        category=request.POST.get('category')
        Categoryoffer.objects.create(category=category,discount=discount)
        cat=Category.objects.get(category=category).pk
        product=Products.objects.filter(category=cat)
        for items in product:
            price=float(items.price)
            items.price=price-price*float(discount)/100
            items.save()
        return redirect(offers)


def cancel_offer_product(request,name):
    '''Lets Admin cancel offer for individual product'''
    offer=Productoffer.objects.get(product=name)
    discount=float(offer.discount)
    offer.delete()
    
    return redirect(offers)


def cancel_offer_category(request,name):
    '''Lets Admin cancel offer for category '''
    offer=Categoryoffer.objects.get(category=name)
    discount=float(offer.discount)
    cat=Category.objects.get(category=name).pk
    product=Products.objects.filter(category=cat)
    for items in product:
        price=float(items.price)
        items.price=round(price/(1-discount/100))
        items.save()
    offer.delete()
    return redirect(offers)


def CSV(request):
    '''Generates CSV file of Sales Report'''
    order=Orders.objects.order_by('orderNumber').all()
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="Report.csv"'},
    )
    writer = csv.writer(response)
    writer.writerow(['Sl', 'Date', 'Order No', 'Item', 'Quantity', 'Price'])
    sl=1
    for item in order:
        writer.writerow([sl,item.orderDate,item.orderNumber,item.product,
                                                    item.quantity,item.sale])
        sl +=1
    return response


def PDF(request):
    '''Generate PDF file of Sales Report'''
    order=Orders.objects.order_by('orderNumber').all()
    response=HttpResponse(content_type='application/pdf')
    d=datetime.date.today().strftime('%Y-%m-%d')
    response['Content-Disposition'] =f'inline;filename="{d}.pdf"'
    buffer =BytesIO()
    p= canvas.Canvas(buffer,pagesize=A4)
    p.setFont("Helvetica",15,leading=None)
    p.setFillColorRGB(0.29296875,0.453125,0.609375)
    p.drawString(260,800,"Report")
    p.line(0,780,1000,780)
    p.line(0,778,1000,778)
    xl=20
    yl=750-20
    k=0
    sl=1
    p.drawString(xl,750,f"{'Sl'}")
    p.drawString(xl+50,750,f"{'Date'}")
    p.drawString(xl+175,750,f"{'Order#'}")
    p.drawString(xl+250,750,f"{'Item'}")
    p.drawString(xl+470,750,f"{'Nos.'}")
    p.drawString(xl+500,750,f"{'Sale'}")
    for items in order:
        p.setFont("Helvetica",15,leading=None)
        p.drawString(xl,yl+k,f"{sl}")
        #p.drawString(xl,yl+k,f"{sl}{items.product}{items.orderNumber}{items.product}{items.quantity}{items.sale}")
        p.drawString(xl+50,yl+k,f"{items.orderDate}")
        p.drawString(xl+175,yl+k,f"{items.orderNumber}")
        p.drawString(xl+250,yl+k,f"{items.product}")
        p.drawString(xl+470,yl+k,f"{items.quantity}")
        p.drawString(xl+500,yl+k,f"{items.sale}")
        k-=15
        sl +=1
    p.setTitle(f'Report on {d}')
    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


