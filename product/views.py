from django.shortcuts import render, redirect
from .models import Product
#from .models import ProductImages, Category
## this is for product pages in products list
from django.core.paginator import Paginator
## this is for categories counts visible in Frentend pages
from django.db.models import Count, Q
## this for returns 404 error page
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import AddProductForm, UpdateProductForm, AddProductImagesForm
from django.contrib import messages
from django.http import HttpResponse
from .models import Category, ProductImages, Brand
from django.forms.models import modelformset_factory
# for send Mail
from django.core.mail import send_mail
from django.conf import settings

# this is for cart
from cart.forms import CartAddProductForm


# Create your views here.
def productlist(request, category_slug = None, brand_slug = None):
    category = None
    productlist = Product.objects.all()
    categorylist = Category.objects.annotate(total_products = Count('product'))
    brandslist = Brand.objects.annotate(total_products = Count('product'))
    
    if category_slug:
        category = get_object_or_404(Category, slug = category_slug)
        productlist = productlist.filter(category = category)

    if brand_slug:
        brand = get_object_or_404(Brand, brand_name = brand_slug)
        productlist = productlist.filter(brand = brand)

    ## Search code for using  products, categories, brands
    search_query = request.GET.get('q')
    if search_query:
        productlist = productlist.filter(
        Q(name__icontains = search_query) |
        Q(description__icontains = search_query) |
        Q(condition__icontains = search_query) |
        Q(brand__brand_name__icontains = search_query) |
        Q(brand__brand_name__icontains = search_query)
        #Q(brand__icontains = search_query)
        )

    # setup Paginator for pages in frentend
    paginator = Paginator(productlist, 5)  # products count limit in per page
    page = request.GET.get('page')
    productlist = paginator.get_page(page)
    template = "Product/product_list.html"
    context = {'product_list' : productlist, 'category_list' : categorylist, 'category' : category,'brands':brandslist}
    return render(request, template, context)


def productdetail(request, product_id):
    productdetail = Product.objects.get(id = product_id)
    template = "Product/product_detail.html"
    productimages = ProductImages.objects.filter(product = productdetail)
    cart_product_form = CartAddProductForm()
    context = {"product_detail" : productdetail, "product_images": productimages,'cart_product_form': cart_product_form}
    return render(request, template, context)


@login_required
def add_product(request):
    imagesFormSet = modelformset_factory(ProductImages,form = AddProductImagesForm, extra = 3)
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)        
        formset = imagesFormSet(request.POST, request.FILES, queryset = ProductImages.objects.none())

        if form.is_valid() and formset.is_valid():
            new_product = form.save(commit= False)
            new_product.owner =request.user
            new_product.save()
            messages.warning(request,"Hi your Product is added successfully.")
            photos_count = 0
        
            for form in formset.cleaned_data:
                if form:
                    photos_count += 1
                    image = form['image']
                    photo = ProductImages(product = new_product, image = image)
                    photo.save()
            return redirect('products:product_list')
        else:
            messages.warning(request,"Enter details properly.")
            return HttpResponse("Something Wrong!")
    else:
        form = AddProductForm()
        formset = imagesFormSet(queryset=ProductImages.objects.none())
        return render(request, 'product/add_product.html',{'form':form, 'formset':formset})


@login_required
def user_products(request):
    category = None
    current_user = request.user
    categorylist = Category.objects.annotate(total_products = Count('product'))
    category ={}
    productlist = Product.objects.filter(owner = current_user.id)
    context = {'product_list' : productlist, 'category_list' : categorylist, 'category' : category}
    return render(request,'Product/product_list.html', context)


@login_required
def update_product(request,product_slug):
    form = get_object_or_404(Product, slug = product_slug)
    if request.method == 'POST':
        form = UpdateProductForm(request.POST, request.FILES, instance=form)
        if form.is_valid():
            update_form = form.save(commit= False)
            update_form.owner = request.user
            update_form.save()
            messages.warning(request,"Hi your Product is Updated successfully.")
            return redirect('/')
        else:
            messages.warning(request,"Some thing is WRONG!.")
            return HttpResponse("Some thing is WRONG! in your Updations.")
    else:
        form = UpdateProductForm(instance=form)
        return render(request, 'Product/update_product.html', {'form':form})


# Remove Product
@login_required
def deleteProduct(request, product_slug):
    delete_product = Product.objects.filter(slug = product_slug).delete()    
    messages.warning(request, f"Your  Product deleted Successfully.")    
    return redirect('/')

