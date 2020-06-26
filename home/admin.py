from django.contrib import admin
from .models import Cinfo,Vinfo,Vendoradd,Feedbacks,Order
# Register your models here.

admin.site.register(Cinfo)
admin.site.register(Vinfo)
admin.site.register(Vendoradd)
admin.site.register(Feedbacks)
admin.site.register(Order)