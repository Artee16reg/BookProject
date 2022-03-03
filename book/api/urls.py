from django.urls import path, include

app_name = 'book_api'

urlpatterns = [
    path('v1/', include('book.api.v1.urls', namespace='v1'))
]
