from django.urls import path
from .views import home, register, login_view, logout_view, search, category_view, toggle_favorite, favorites_view, \
    write_review, reviews_view, toggle_cart, cart_view

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('search/', search, name='search'),
    path('category/<str:category_name>/', category_view, name='category'),
    path('toggle-favorite/<int:product_id>/', toggle_favorite, name='toggle_favorite'),
    path('favorites/', favorites_view, name='favorites'),
    path('reviews/', reviews_view, name='reviews'),
    path('write-review/<int:product_id>/', write_review, name='write_review'),
    path('toggle-cart/<int:product_id>/', toggle_cart, name='toggle_cart'),
    path('cart/', cart_view, name='cart'),
]
