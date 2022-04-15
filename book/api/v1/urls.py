from rest_framework.routers import DefaultRouter

from book.api.v1 import views
from django.urls import path
app_name = 'v1'

# router = DefaultRouter()
# router.register('books/', BookListView.as_view(), basename='books')
#
# urlpatterns = router.urls
urlpatterns = [
    path('books/', views.BookListView.as_view()),
    path('book/<int:pk>', views.BookDetailView.as_view()),
    path('read/<int:pk>', views.ChapterBookView.as_view()),
    path('comment/', views.CommentCreateView.as_view()),
    path('comment/<int:pk>', views.CommentUpdateView.as_view()),
    path('rating/', views.AddStarRatingView.as_view()),
]
