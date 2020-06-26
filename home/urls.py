from django.urls import path
from . import views,urls
from django.conf import settings


urlpatterns = [
    path('', views.index,name="index"),
    path('login',views.login,name='login'),
    path('logout' ,views.logout,name="logout"),
    path('contacts',views.contacts,name='contacts'),
    path('about',views.about,name='about'),
    path('csignin',views.csignin,name='csignin'),
    path('vsignin',views.vsignin,name='vsignin'),
    path('vendoradd',views.vendoradd,name="vendoradd"),
    path('vendoradd_upload',views.vendoradd_upload,name='vendoradd_upload'),
    path('vendordel',views.vendordel,name='vendordel'),
    path('vprofile',views.vprofile,name='vprofile'),
    path('vendor_orders',views.vendor_orders,name='vendor_orders'),
    path('order_status/<str:orderId>/<str:status>',views.order_status,name="order_status"),
    path('customer1',views.customer1,name="customer1"),
    path('cprofile',views.cprofile,name='cprofile'),
    path('customer2/<str:vendorname>',views.customer2,name="customer2"),
    path('mycart/<str:vendorname>',views.mycart,name="mycart"),
    path('payment',views.payment,name="payment"),
    path('customer_orders',views.customer_orders,name="customer_orders"),  
    
]



if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns +=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)