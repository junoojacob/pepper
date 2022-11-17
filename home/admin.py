from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Products)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(Orders)
admin.site.register(OrderNumber)


# Register your models here.
