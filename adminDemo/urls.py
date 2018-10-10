#coding:utf-8
"""adminDemo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from myAdmin.service.site import site
from app01 import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^myAdmin/', site.urls),

    url(r'^myAdmin2/', ([url(r'^book1/',views.index1),
                        url(r'^book2/',([
                            url(r'^change/',views.index2),
                            url(r'^add/',views.index3),
                                       ],None,None))],
                       None,None),
        ),

]

'''
url的多级分发,相当于下面的url：
myAdmin2/book1/
myAdmin2/book2/change/
myAdmin2/book2/add/
'''