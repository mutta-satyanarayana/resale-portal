from django.db import models
from django.contrib.auth.models import User
from django.utils  import timezone
from django.utils.text import slugify

# Create your models here.
class Product(models.Model):
    """ Contain all products information"""

    CONDITION_TYPE = (
    ("New", "New"),
    ("Used", "Used")
    )
    '''
    CATEGORY_TYPE = (
        ('Mobile','Mobile'),
        ('Car','Car'),
        ('Bike','Bike'),
        ('Laptop','Laptop')
    )

    BRAND_TYPE =(
        ('MI','MI'),
        ('SAMSUNG','SAMSUNG'),
        ('MARUTHI','MARUTHI'),
        ('HERO','HERO'),
        ('BMW','BMW'),
        ('LG','LG'),
        ('SONY','SONY'),
        ('DELL','DELL')
    )
    '''

    name = models.CharField(max_length = 100)
    owner  = models.ForeignKey(User, on_delete = models.CASCADE)
    description = models.TextField(max_length = 500)
    condition = models.CharField(max_length = 100, choices = CONDITION_TYPE)
    category = models.ForeignKey('Category', on_delete= models.CASCADE)
    #category = models.CharField(max_length=100, choices= CATEGORY_TYPE)
    #brand = models.CharField(max_length=100, choices= BRAND_TYPE)
    brand = models.ForeignKey('Brand', on_delete= models.CASCADE)
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    created = models.DateTimeField(default = timezone.now)
    image = models.ImageField(upload_to = "images/products/", blank = True, null = True)
    city = models.CharField(max_length=100, default="No City")
    state = models.CharField(max_length=100, default="No State")
    country = models.CharField(max_length=100, default="No Country")
    slug = models.SlugField(blank = True, null = True)

    # this method for slug [if sulg is declared as manual (OR) auto slug declared]
    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)
        
        # Auto capitalize Product Name
        for field_name in ['name','city','state','country']:
            val = getattr(self, field_name ,False)
            if val:
                setattr(self, field_name, val.title())
        super(Product, self).save(*args, **kwargs)

    # Delete Images 
    def delete(self):

        images = ProductImages.objects.filter(product = self)
        #self.image.delete()
        for image in images:
            image.delete()
        

    # Product name is displayed in Admin Portal
    def __str__(self):
        return self.name


class ProductImages(models.Model):
    """ This class handles Products images """
    product = models.ForeignKey('Product', on_delete = models.CASCADE)
    image = models.ImageField(upload_to = "images/products/", blank = True, null = True)

    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"

    def delete(self):
        self.image.delete()
        super(ProductImages, self).delete()

    def __str__(self):
        return self.product.name


class Category(models.Model):
    # This class for Category class
    category_name = models.CharField(max_length = 50)
    image = models.ImageField(upload_to = "category/", blank = True, null = True)

    slug = models.SlugField(blank = True, null = True)
    """Meta class changes the behaviour of Category class. Category class is act like as a instance to Meta class."""
    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def save(self, *args, **kwargs):
        if not self.slug and self.category_name:
            self.slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.category_name

class Brand(models.Model):
    # This class for Brands
    brand_name = models.CharField(max_length = 50)

    class Meta:
        verbose_name = "brand"
        verbose_name_plural = "brands"

    def __str__(self):
        return self.brand_name
