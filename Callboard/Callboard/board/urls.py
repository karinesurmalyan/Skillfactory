from django.urls import path
from .views import *
from django.shortcuts import redirect
from allauth.account.views import LogoutView, LoginView

urlpatterns = [
    path('', AnnouncementsList.as_view(), name='posts'),
    path('confirm/', ConfirmUser.as_view(), name='confirm_user'),
    path('<int:pk>', AnnouncementDetail.as_view(), name='post_detail'),
    path('post/create', AnnouncementCreate.as_view(), name='post_create'),
    path('post/<int:pk>/edit', AnnouncementUpdate.as_view(), name='post_edit'),
    path('post/<int:pk>/delete', AnnouncementDelete.as_view(), name='post_delete'),
    path('comment/<int:pk>', CommentCreate.as_view(), name='comment_edit'),
    path('comments/', CommentList.as_view(), name='comments'),
    path('comments/<int:pk>', CommentDetail.as_view(), name='comment'),
    path('comments/<int:pk>/accept/', comment_accept, name='comment_accept'),
    path('comments/<int:pk>/delete/', comment_decline, name='comment_decline'),
    path('profile/', IndexView.as_view(), name='profile'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('signup/', IndexView.as_view(template_name='signup.html'), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
