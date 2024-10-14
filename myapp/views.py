from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserLoginForm, ReviewForm
from django.contrib.auth import login, authenticate, logout
from .models import Product, Favorite, Review, Cart

def home(request):
    products = Product.objects.all()
    favorite_products = Favorite.objects.filter(user=request.user).values_list('product_id', flat=True) if request.user.is_authenticated else []
    return render(request, 'home.html', {'products': products, 'favorite_products': favorite_products})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'myapps/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'myapps/login.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect('login')

def search(request):
    query = request.GET.get('q', '').strip()
    results = Product.objects.filter(name__icontains=query) if query else []
    return render(request, 'myapps/search_results.html', {'query': query, 'results': results})



def category_view(request, category_name):
    cards = {
        'bballs': [
            {
                'title': 'Wilson EVO nxt',
                'image': 'images/wilson1.jpg',
                'description': 'Оригинальный баскетбольный мяч в коллаборации с лигой NBA для тренировок',
                'price': '199$'
            },
        ],
        'shoes': [
            {
                'title': 'Jordan Luka 3',
                'image': 'images/jordan-luka-3.webp',
                'description': 'Именные кроссовки с коллаборацией Nike и Luka Doncic',
                'price': '130$'
            },
        ],
        'tees': [
            {
                'title': 'Eric Emanuel Tee',
                'image': 'images/eric_emanuel_black.jpg',
                'description': 'Футболка для повседневной жизни/тренировок от Eric Emanuel',
                'price': '19$'
            },
        ],
        'jerseys': [
            {
                'title': 'GSW Jersey',
                'image': 'images/gsw.jpg',
                'description': 'Оригинальный баскетбольный мяч в коллаборации с лигой NBA для тренировок',
                'price': '70$'
            },
        ],
    }

    selected_cards = cards.get(category_name, [])

    return render(request, 'myapps/category.html', {'cards': selected_cards, 'category_name': category_name})


def toggle_favorite(request, product_id):
    if request.user.is_authenticated:
        favorite, created = Favorite.objects.get_or_create(user=request.user, product_id=product_id)
        if not created:
            favorite.delete()

    return redirect(request.META.get('HTTP_REFERER', 'home'))

def favorites_view(request):
    if request.user.is_authenticated:
        favorites = Favorite.objects.filter(user=request.user)
        favorite_product_ids = [favorite.product_id for favorite in favorites]
        favorite_products = Product.objects.filter(id__in=favorite_product_ids)
        return render(request, 'myapps/favorites.html', {'favorite_products': favorite_products})
    return redirect('login')

def write_review(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user
                review.product = product
                review.save()
                return redirect('home')
        else:
            form = ReviewForm()
        return render(request, 'myapps/write_review.html', {'form': form, 'product': product})
    else:
        return render(request, 'myapps/not_authenticated.html')

def reviews_view(request):
    reviews = Review.objects.all()
    return render(request, 'myapps/reviews.html', {'reviews': reviews})

def toggle_cart(request, product_id):
    if request.user.is_authenticated:
        cart_item, created = Cart.objects.get_or_create(user=request.user, product_id=product_id)
        if not created:
            cart_item.delete()

    return redirect(request.META.get('HTTP_REFERER', 'home'))

def cart_view(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        cart_product_ids = [cart_item.product_id for cart_item in cart_items]
        cart_products = Product.objects.filter(id__in=cart_product_ids)
        return render(request, 'myapps/cart.html', {'cart_products': cart_products})
    return redirect('login')
