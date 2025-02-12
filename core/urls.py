"""core URL Configuration

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
from django.urls import path,include,re_path
from django.contrib.flatpages.sitemaps import FlatPageSitemap
from django.contrib.sitemaps.views import sitemap

from backend.views import index,errors

handler400 = errors.BAD_REQUEST_400.as_view()
handler403 = errors.PERMISSION_DENIED_403.as_view()
handler404 = errors.PAGE_NOT_FOUND_404.as_view()
handler500 = errors.SERVER_ERROR_500.as_view()

urlpatterns = [
    path("admin/", admin.site.urls),
    path("transactions/",include("backend.urls")),

]
