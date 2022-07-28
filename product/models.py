from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.TextField(max_length=100)
    slug = models.SlugField(primary_key=True, max_length=100, blank=True, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def save(self, *args, **kwargs):
        self.slug = self.name.lower()
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        if self.parent:
            return f'{self.parent} -> {self.slug}'
        else:
            return self.slug


class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    price = models.BigIntegerField(default=0)
    amount = models.PositiveIntegerField(default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', null=True)

    def __str__(self):
        return self.name


class Reviews(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    time = models.DateTimeField()


class Image(models.Model):
    image = models.ImageField(upload_to='products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')


class Rating(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rating', verbose_name='raiting owner')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='rating', verbose_name='product')
    rating = models.SmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=0 )

    def __str__(self):
        return f'{self.product} {self.rating}'


class Like(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like', verbose_name='like owner')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='like', verbose_name='product')
    like = models.BooleanField('like', default=False)




