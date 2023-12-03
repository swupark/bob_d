from django.urls import path

from mypageapp.views import AccountDetailView, change_pw, AccountDeleteView, UserInfoUpdateView

#AccountUpdateView

app_name='mypageapp'
urlpatterns=[

    path('<int:pk>', AccountDetailView.as_view(), name='mypage'),
    path('update/<int:pk>', change_pw, name='update'),
    path('delete/<int:pk>', AccountDeleteView.as_view(), name='delete'),
    path('infoupdate/<int:pk>', UserInfoUpdateView.as_view(), name='infoupdate'),
]