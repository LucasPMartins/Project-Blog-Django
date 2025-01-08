from django.db import models
from django.urls import reverse
from utils.rands import new_slugify
from django.contrib.auth.models import User
from utils.images import resize_image
from django_summernote.models import AbstractAttachment

# Create your models here.

class PostAttachment(AbstractAttachment):
    class Meta:
        verbose_name = "Post Attachment"
        verbose_name_plural = "Post Attachments"

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.file.name

        current_file_name = str(self.file.name)
        super_save = super().save(*args, **kwargs)
        file_changed = False
        if self.file:
            file_changed = current_file_name != self.file.name
        if file_changed:
            resize_image(self.file, new_width=900,quality=70)

        return super_save

    def __str__(self):
        return self.name

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
    is_published = models.BooleanField(default=False,help_text="If checked, the page will be visible to users")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        if not self.is_published:
            return reverse('blog:index')
        return reverse("blog:page", args=(self.slug,))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = new_slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class PostManager(models.Manager):
    def get_published(self):
        return self.filter(is_published=True).order_by('-pk')

class Post(models.Model):
    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    objects = PostManager()

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

    def get_absolute_url(self):
        if not self.is_published:
            return reverse('blog:index')
        return reverse("blog:post", args=(self.slug,))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = new_slugify(self.title)

        current_cover_name = str(self.cover.name)
        super_save = super().save(*args, **kwargs)
        cover_changed = False
        if self.cover:
            cover_changed = current_cover_name != self.cover.name
        if cover_changed:
            resize_image(self.cover, new_width=900,quality=70)
        
        return super_save