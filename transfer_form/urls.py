from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.TransferView.as_view(), name='transfer_form'),
    url(r'success/', views.SuccessView.as_view(), name='success'),
]
