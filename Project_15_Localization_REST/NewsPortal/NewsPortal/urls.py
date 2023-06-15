"""NewsPortal URL Configuration

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
from django.urls import path, include

from django.http import HttpResponse

from rest_framework import routers
from news.views import NewsViewset

def multiply(request):
   number = request.GET.get('number')
   multiplier = request.GET.get('multiplier')

   try:
        result = int(number) * int(multiplier)
        html = f"""
        <html>
            <body>
                {number}*{multiplier}={result}
                <p> {request.path} </p>
            </body>
        </html>"""
   except (ValueError, TypeError):
       html = f"<html><body>Invalid input.</body></html>"

   return HttpResponse(html)


router = routers.DefaultRouter()
router.register(r'api_news', NewsViewset, basename="api_news")


urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),

    # path('accounts/', include('django.contrib.auth.urls')),
    # path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),

    path('pages/', include('django.contrib.flatpages.urls')),

    path('news/', include("news.urls")),
    path('multiply/', multiply),

    path('', include(router.urls)),
    path('api_auth/', include('rest_framework.urls', namespace='rest_framework')),
]
