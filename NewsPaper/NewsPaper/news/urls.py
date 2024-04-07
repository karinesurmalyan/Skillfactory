from django.urls import path
from .views import (
   PostsList, PostDetail, NewsSearch, PostFilter, PostCreate, PostUpdate, PostDelete,
)


urlpatterns = [
   path('', PostsList.as_view(), name='posts'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('search', NewsSearch.as_view(), name='news_search'),
   path('news/create/', PostCreate.as_view(), name='news_create'),
   path('news/<int:pk>/edit', PostUpdate.as_view(), name='news_edit'),
   path('news/<int:pk>/delete', PostDelete.as_view(), name='news_delete'),
   path('articles/create/', PostCreate.as_view(), name='articles_create'),
   path('articles/<int:pk>/edit', PostUpdate.as_view(), name='articles_edit'),
   path('articles/<int:pk>/delete', PostDelete.as_view(), name='articles_delete'),

]