from django.contrib import admin
from django.urls import path
from order.views import Order


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',Order.as_view(),name='place_order'),
    path('dbupdate/',Order.as_view(),name='db_update'),
]
