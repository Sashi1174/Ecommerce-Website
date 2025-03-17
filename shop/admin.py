from django.contrib import admin

from .models import Product,Contact,Orders,Order_update
admin.site.register(Product)
admin.site.register(Contact)
admin.site.register(Orders)
admin.site.register(Order_update)
# Register your models here.
