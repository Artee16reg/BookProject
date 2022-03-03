from rest_framework.routers import DefaultRouter

from book.api.v1.views import BookViewSet

app_name = 'v1'

router = DefaultRouter()
router.register('books', BookViewSet, basename='books')

urlpatterns = router.urls
