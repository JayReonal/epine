from django.contrib import admin
from .models import *

admin.site.register(Crop)
admin.site.register(Yield)
admin.site.register(PinePrice)
admin.site.register(PineValue)
admin.site.register(Category)
admin.site.register(WorkerPays)
admin.site.register(BadValuePine)
admin.site.register(BadPine)
admin.site.register(BiddingProcess)