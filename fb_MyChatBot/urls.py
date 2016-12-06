from django.conf.urls import include
from django.conf.urls import url
from .views import MyChatBotView
urlpatterns = [
url(r'^9ff2d5cc7d0c3359a40438f201acebb4f444cba5478399263e/?$', MyChatBotView.as_view()) 
]