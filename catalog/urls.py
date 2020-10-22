from django.urls import path, include
from . import views
from rest_framework import routers
from .views import BookViewSet
urlpatterns = [
        path('', views.index, name='index'),
        path('books/', views.BookListView.as_view(), name='books'),
        path('books/<int:pk>', views.BookDetailView.as_view(),
            name='book-detail'),
        path('authors/', views.AuthorListView.as_view(), name='authors'),
        path('authors/<int:pk>', views.AuthorDetailView.as_view(),
            name='author-detail'),
]

urlpatterns += [
        path('mybook/', views.LoanedBooksByUserListView.as_view(),
            name='my-borrowed'), 
]

urlpatterns += [
        path('allborrowedbook/', views.LibrarianSetBookListView.as_view(),
            name='all-borrowed'), 
]

urlpatterns += [
        path('book/<uuid:pk>/renew/', views.renew_book_librarian,
            name='renew-book-librarian'), 
]

urlpatterns += [
        path('author/create/', views.AuthorCreate.as_view(),
            name='author_create'),
        path('author/<int:pk>/update/', views.AuthorUpdate.as_view(),
            name='author_update'),
        path('author/<int:pk>/delete/', views.AuthorDelete.as_view(),
            name='author_delete'),
]

urlpatterns += [
        path('book/create/', views.BookCreate.as_view(),
            name='book_create'),
        path('book/<int:pk>/update/', views.BookUpdate.as_view(),
            name='book_update'),
        path('book/<int:pk>/delete/', views.BookDelete.as_view(),
            name='book_delete'),
]


#router = routers.DefaultRouter()
#router.register(r'allbooks', views.BookViewSet)

allbook = BookViewSet.as_view({
    'get': 'list', 
})

urlpatterns += [
        path('allbooks/', allbook, name='allbook')
]
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

urlpatterns += [
        path('api-auth/', include('rest_framework.urls', namespace='rest_framwork'))
] 
