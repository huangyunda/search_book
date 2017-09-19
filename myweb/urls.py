"""myweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from learn import views as learn_views 


urlpatterns = [
    url(r'^search', learn_views.search, name='search'),
    url(r'^update_book', learn_views.update_book, name='update_book'),
    url(r'^show_result', learn_views.show_result, name='show_result'),
    url(r'^signup', learn_views.signup, name='signup'),
    url(r'^signin', learn_views.signin, name='signin'),
    url(r'^signout', learn_views.signout, name='signout'),
    url(r'^admin/', admin.site.urls),
]
