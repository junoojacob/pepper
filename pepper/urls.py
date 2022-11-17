"""pepper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static  
from django.conf import settings
from home import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('sorthome/<int:value>',views.home_sortby_category,name='sorthome'),
    path('sortoffer/<str:value>',views.home_sortby_product_offer,name='sortoffer'),     
    path('brandsorthome/<str:value>',views.home_sortby_brands,name='brandsorthome'),
    path('pricesorthome/<int:value>',views.home_sortby_price,name='pricesorthome'),   
    path('sortoffer2/<str:value>',views.shome_sortby_category_offer,name='sortoffer2'),
    path('productdetail/<int:id>',views.product_detail,name='productdetail'),                                                    #HOME
    path('signin/',views.sign_in,name='signin'),                                             #LOGIN
    path('signout/',views.sign_out,name='signout'),                                          #LOGOUT
    path('register/',views.register,name='register'),                                       #SIGNUP
    path('registerverification/',views.register_verification,name='registerverification'),   #REGISTER
                                                       #OTP
    path('smslogin/',views.sms_login,name='smslogin'),
    path('resendotp/',views.resend_otp,name='resendotp'),                                       #LOGIN WITH SMS
    path('otplogin/',views.otp_login,name='otplogin'),                                       #VERIFICATION
    path('profile/',views.profile,name='profile'),
    path('updateprofile/',views.update_profile,name='updateprofile'),
    path('addaddress/',views.add_address,name='addaddress'),
    path('adminlogin/',views.admin_login,name='adminlogin'),                                 #ADMIN
    path('admindash/',views.admin_dash,name='admindash'),
    path('admincategory/',views.admin_category,name='addcategory'),                          #CATEGORY
    path('addcategory/',views.add_category,name='addcategory'),
    path('deletecategory/<int:id>',views.delete_category,name='deletecategory'),
    path('editcategory/<int:id>',views.edit_category,name='editcategory'),
    path('adminuser/',views.admin_user,name='adminuser'),                                    #USER
    path('block',views.block,name='block'),
    path('adminproducts/',views.admin_products,name='adminproducts'),
    path('addproduct/',views.add_product,name='addproduct'),                                  #PRODUCT
    path('productdelete/<int:id>',views.product_delete,name='productdelete'),
    path('editproduct/<int:id>',views.edit_product,name='editproduct'),
    path('cart/',views.cart,name='cart'),                                                    #CART
    path('addcart/<int:id>',views.add_cart,name='addcart'),
    path('deleteitem/<int:id>',views.delete_item,name='deleteitem'),
    path('sub',views.sub,name='sub'),
    path('add',views.add,name='add'),
    path('order/',views.order,name='order'),                                                  #ORDER
    path('checkout/',views.checkout,name='checkout'),
    path('cancel_order/<int:id>',views.cancel_order,name='cancelorder'),
    path('retur/<int:id>',views.return_order,name='retur'),
    path('adminorder/',views.admin_order,name='adminorder'),
    path('delivered/<int:id>',views.delivered,name='delivered'),
    path('shipped/<int:id>',views.shipped,name='shipped'),
    path('approve/<int:id>',views.approve,name='approve'),
    path('out_for_delivery/<int:id>',views.out_for_delivery,name='out_for_delivery'),
    path('reports/',views.reports,name='reports'),
    path('coupons/',views.coupons,name='coupons'),
    path('discount',views.discount,name='discount'),
    path('offers/',views.offers,name='offers'),
    path('productoffer/',views.product_offer,name='productoffer'),
    path('cancelloffer/<str:name>',views.cancel_offer_product,name='cancelloffer'),
    path('categoryoffer/',views.category_offer,name='categoryoffer'),
    path('cancelloffer2/<str:name>',views.cancel_offer_category,name='cancelloffer2'),
    path('CSV/',views.CSV,name='CSV'),
    path('PDF/', views.PDF, name='PDF')
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)  
