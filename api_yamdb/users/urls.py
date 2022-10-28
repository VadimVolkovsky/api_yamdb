from django.urls import path

from api.views import SignUpApiView, TokenRegApiView

urlpatterns = [
    path('signup/', SignUpApiView.as_view(), name='signup'),
    path('token/', TokenRegApiView.as_view(), name='token_access'),
]
