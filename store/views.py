from django.shortcuts import render , get_object_or_404
from .models import *
from category.models import Category
from cart.models import CartItem
from cart.views import _cart_id
from django.db.models import Q
from .forms import ReviewForm
from orders.models import *

from django.contrib import messages
from django.shortcuts import redirect

# Create your views here.
from django.core.paginator import EmptyPage, PageNotAnInteger , Paginator

def store(request , category_slug=None):
    
    if category_slug != None:
        categories = get_object_or_404(Category,slug = category_slug)
        product = Product.objects.filter(category = categories , is_available=True)
        paginator = Paginator(product , 2)
        page = request.GET.get('page')
        paged_products= paginator.get_page(page)
        count = product.count()
    else:
        product = Product.objects.all().filter(is_available=True).order_by('id')
        count = product.count()
        
        # creating paginator
        paginator = Paginator(product , 6)
        page = request.GET.get('page')
        paged_products= paginator.get_page(page)
                
    context ={
        'product':paged_products,
        'count':count,
           
    }
    return render(request, 'store/store.html',context)

def store_details(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id =_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e
    #handle who can post the review
    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id = single_product.id).exists()
        except orderproduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None
        
    
    #show all reviews
    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)
    
    #product_gallery
    product_gallery = ProductGallery.objects.filter(product=single_product)
    context={
        'single_product': single_product,
        'in_cart':in_cart,
        'orderproduct':orderproduct,
        'reviews':reviews,
        'product_gallery':product_gallery,
    }
    return render(request,'store/store_details.html', context) 




    


def search(request):
    product = None  # 1. Provide a default value to prevent crash
    count = 0 
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            product = Product.objects.filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword)).order_by('-created_date')
            count = product.count()
    context ={
            'product':product,
              'count':count}
    return render(request ,'store/store.html' , context)


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER') # Storing previous URL
    if request.method == 'POST':
        try:
           
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews) 
            if form.is_valid():
                form.save()
                messages.success(request, 'Thank you! Your review has been updated.') 
            
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR') 
                data.product_id = product_id
                data.user_id = request.user.id  
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.') 
        return redirect(url)

    

                
               
            
        
    
