from django.db import models
from utils.rands import new_slugify
from django.contrib.auth.models import User

# Create your models here.
class Tag(models.Model):
    class Meta:
        verbose_name_plural = "Tags"

    name = models.CharField(max_length=100)
    slug = models.SlugField(
        max_length=100, unique=True, 
        default=None, null=True, blank=True
        )
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = new_slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Category(models.Model):
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=100)
    slug = models.SlugField(
        max_length=100, unique=True, 
        default=None, null=True, blank=True
        )
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = new_slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Page(models.Model):
    title = models.CharField(max_length=65)
    slug = models.SlugField(
        max_length=100, unique=True, 
        default=None, null=True, blank=True
        )
    content = models.TextField()
    is_published = models.BooleanField(default=False,help_text="If checked, the page will be visible to users")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = new_slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
class Post(models.Model):
    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
    
    title = models.CharField(max_length=65)
    slug = models.SlugField(
        max_length=100, unique=True, 
        default=None, null=True, blank=True
        )
    excerpt = models.CharField(max_length=200)
    is_published = models.BooleanField(
        default=False,
        help_text="If checked, the page will be visible to users"
        )
    content = models.TextField()
    cover = models.ImageField(upload_to='posts/%Y/%m/',blank=True, default='')
    cover_in_post_content = models.BooleanField(
        default=True, 
        help_text="If checked, the cover will be displayed in the post content"
        )
    created_at = models.DateTimeField(auto_now_add=True)
    # user.post_created_by.all()
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        blank=True,related_name='post_created_by',
        )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        blank=True,related_name='post_updated_by',
        )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True,
        blank=True,default=None,
        )
    tags = models.ManyToManyField(Tag, blank=True,default='')

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = new_slugify(self.title)
        return super().save(*args, **kwargs)