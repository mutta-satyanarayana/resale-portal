from django import forms
from django.forms import ModelForm
from .models import Product
from .models import Brand, Category, ProductImages

class AddProductForm(forms.ModelForm):
    #name = forms.CharField(max_length = 100, required = True)
    #city = forms.CharField(required= True),
    #state = forms.CharField(required= True),
    #country = forms.CharField(required= True),
    #image= forms.ImageField(required= True)
    class Meta:
        model = Product
        fields = ['name','description','city','state','country','condition','category','brand','price','image']
        #required = ('name','city','state','country','image')

class UpdateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','description','city','state','country','condition','category','brand','price','image']


class AddProductImagesForm(forms.ModelForm):
    class Meta:
        model = ProductImages
        fields = ('image',)

'''
class AddBrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['brand_name']


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name']'''