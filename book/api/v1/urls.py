from rest_framework.routers import DefaultRouter

from book.api.v1.views import BookListView, BookDetailView, CommentCreateView, AddStarRatingView, ReadingBook
from django.urls import path
app_name = 'v1'

# router = DefaultRouter()
# router.register('books/', BookListView.as_view(), basename='books')
#
# urlpatterns = router.urls
urlpatterns = [
    path('books/', BookListView.as_view()),
    path('book/<int:pk>', BookDetailView.as_view()),
    path('read/<int:pk>', ReadingBook.as_view()),
    path('comment/', CommentCreateView.as_view()),
    path('rating/', AddStarRatingView.as_view()),
]
