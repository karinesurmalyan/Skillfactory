from django.urls import path
from .views import (
   PostsList, PostDetail, NewsSearch, PostCreate, PostUpdate, PostDelete, IndexView, CategoryListView, subscribe,
)
from allauth.account.views import LogoutView, LoginView
from .views import upgrade_me
from django.views.decorators.cache import cache_page


urlpatterns = [
   path('', PostsList.as_view(), name='posts'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('search', NewsSearch.as_view(), name='post_search'),
   path('news/create/', PostCreate.as_view(), name='post_create'),
   path('news/<int:pk>/edit', PostUpdate.as_view(), name='post_edit'),
   path('news/<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
   path('articles/create/', PostCreate.as_view(), name='post_create'),
   path('articles/<int:pk>/edit', PostUpdate.as_view(), name='post_edit'),
   path('articles/<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
   path('profile/', IndexView.as_view(), name='profile'),
   path('login/', LoginView.as_view(template_name='login.html'), name='login'),
   path('signup/', IndexView.as_view(template_name='signup.html'), name='signup'),
   path('logout/', LogoutView.as_view(), name='logout'),
   path('upgrade/', upgrade_me, name='upgrade'),
   path('categories/<int:pk>/', CategoryListView.as_view(), name='category_list'),
   path('categories/<int:pk>/subscribe/', subscribe, name='subscribe'),
]
