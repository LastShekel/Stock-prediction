from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^prediction/', include('prediction.urls'), name="prediction"),
    url(r'^admin/', admin.site.urls),
]