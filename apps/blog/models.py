import json
from django.db import models
from cloudinary.models import CloudinaryField
from django.shortcuts import reverse
from datetime import datetime
from django.conf import settings
import markdown
import re


# SEO Keywords
class Keyword(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


# Tag blog
class Tag(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(unique=True)
    description = models.TextField(
        max_length=240, help_text="Description of the tag SEO"
    )

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = verbose_name
        ordering = ["id"]

    def __str__(self):
        return self.name


# Category
class Category(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(unique=True)
    description = models.TextField(
        max_length=240, help_text="Description of the category SEO"
    )

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = verbose_name
        ordering = ["id"]

    def __str__(self):
        return self.name


# Temas
class Subject(models.Model):
    STATUS_CHOICES = (
        ("not_started", "Not Started"),
        ("ongoing", "Serializing"),
        ("completed", "Completed"),
    )
    name = models.CharField(max_length=50)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="not_started"
    )
    description = models.CharField(max_length=240)
    sort_order = models.PositiveIntegerField(
        default=99, help_text="Order of the top list page"
    )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    cover_image = CloudinaryField("SubjectImage", blank=True, null=True)

    class Meta:
        verbose_name = "Subject"
        verbose_name_plural = verbose_name
        ordering = ["sort_order"]

    def __str__(self):
        return self.name


# topic articles
class Topic(models.Model):
    name = models.CharField(max_length=50)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    sort_order = models.PositiveIntegerField(
        default=99, help_text="Order of the top list page"
    )
    subject = models.ForeignKey(
        Subject, on_delete=models.PROTECT, related_name="topics"
    )

    class Meta:
        verbose_name = "Topic"
        verbose_name_plural = verbose_name
        ordering = ["sort_order"]

    def __str__(self):
        return f"[{self.subject.name}]{self.name}"


# Artucle model
class Article(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    title = models.CharField(max_length=150)
    summary = models.CharField(max_length=255)
    body = models.TextField()
    img_link = models.URLField(blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)
    slug = models.SlugField(unique=True)
    is_top = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)

    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag, verbose_name="Articles tags")
    keywords = models.ManyToManyField(Keyword, verbose_name="Articles keywords")

    topic = models.ForeignKey(
        Topic, on_delete=models.SET_NULL, null=True, blank=True, related_name="articles"
    )
    topic_order = models.PositiveIntegerField(default=99, null=True, blank=True)
    topic_short_title = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = verbose_name
        ordering = ["-create_date"]

    def __str__(self):
        return f"{self.title[:30]}..." if len(self.title) > 30 else self.title


# ARticle time line
class Timeline(models.Model):
    COLOR_CHOICE = (
        ("primary", "Basic Blue"),
        ("success", "Green"),
        ("info", "Blue"),
        ("warning", "Yellow"),
        ("danger", "Red"),
    )
    SIDE_CHOICE = (
        ("L", "Left"),
        ("R", "Right"),
    )
    STAR_NUM = (
        ("1", "1 Stars"),
        ("2", "2 Stars"),
        ("3", "3 Stars"),
        ("4", "4 Stars"),
        ("5", "5 Stars"),
    )
    side = models.CharField(max_length=1, choices=SIDE_CHOICE, default="L")
    star_num = models.CharField(choices=STAR_NUM, default="3")
    icon = models.CharField(
        max_length=50, blank=True, null=True, default="bi bi-pencil-square"
    )
    icon_color = models.CharField(max_length=20, choices=COLOR_CHOICE, default="info")
    title = models.CharField(max_length=100)
    update_date = models.DateTimeField()
    content = models.TextField("Principal content")

    class Meta:
        verbose_name = "Timeline"
        verbose_name_plural = verbose_name
        ordering = ["-update_date"]

    def __str__(self):
        return self.title[:20]

    def content_to_markdown(self):
        return markdown.markdown(
            self.content,
            extensions=[
                "markdown.extensions.extra",
            ],
        )


# Carousel
class Carousel(models.Model):
    number = models.PositiveIntegerField(help_text="Carousel number")
    title = models.CharField(
        max_length=20, null=True, blank=True, help_text="Carousel title"
    )
    content = models.TextField(blank=True, null=True, max_length=80)
    img_url = models.CharField(
        max_length=200, blank=True, null=True, help_text="Image URL"
    )
    url = models.CharField(max_length=200, blank=True, null=True, help_text="URL")

    class Meta:
        verbose_name = "Carousel"
        verbose_name_plural = verbose_name
        ordering = ["number", "-id"]

    def __str__(self):
        return self.title or ""


# Dead links
class Selian(models.Model):
    bad_url = models.CharField(max_length=200, blank=True, null=True)
    remark = models.CharField(max_length=200, blank=True, null=True)
    add_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Dead Link"
        verbose_name_plural = verbose_name
        ordering = ["-add_date"]

    def __str__(self):
        return self.bad_url


# Freiendly links
class FriendLink(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=200, blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    logo = CloudinaryField("Sites Logo", blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_show = models.BooleanField(default=False)
    not_show_reason = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = "Friend Link"
        verbose_name_plural = verbose_name
        ordering = ["create_date"]

    def __str__(self):
        return self.name

    def get_home_url(self):
        u = re.findall(r"(http|https://.*?)/.*?", self.link)
        home_url = u[0] if u else self.link
        return home_url

    def active_to_false(self):
        self.is_active = False
        self.save(update_fields=["is_active"])

    def show_to_false(self):
        self.is_show = True
        self.save(update_fields=["is_show"])


class AboutBlog(models.Model):
    body = models.TextField(verbose_name="About Blog")
    create_date = models.DateTimeField(verbose_name="Created Date", auto_now_add=True)
    update_date = models.DateTimeField(verbose_name="Updated Date", auto_now=True)

    class Meta:
        verbose_name = "About"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "About"

    def body_to_markdown(self):
        return markdown.markdown(
            self.body,
            extensions=[
                "markdown.extensions.extra",
                "markdown.extensions.codehilite",
            ],
        )


class ArticleView(models.Model):
    date = models.CharField(max_length=10, unique=True)
    body = models.TextField(verbose_name="ARticle body")
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Article viewer"
        verbose_name_plural = verbose_name
        ordering = ["create_date"]

    def __str__(self):
        return self.date


class PageView(models.Model):
    url = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    views = models.IntegerField(default=0)
    is_compute = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.url

    class Meta:
        verbose_name = "Single Page View"
        verbose_name_plural = verbose_name
        ordering = ["url"]

    def update_views(self):
        self.views += 1
        self.save(update_fields=["views", "update_date"])


class FeedHub(models.Model):
    name = models.CharField(max_length=50, unique=True)
    url = models.CharField(max_length=255)
    icon = models.TextField(help_text="You can fill in a base64 image or an icon URL.")
    is_active = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    data = models.TextField(
        help_text="Define task to collect data", blank=True, null=True
    )
    sort_order = models.IntegerField(default=99)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Feed Hub"
        verbose_name_plural = verbose_name
        ordering = ["sort_order"]

    def update_data(self, data):
        self.data = data
        self.save(update_fields=["data"])


class MenuLink(models.Model):
    name = models.CharField(
        max_length=20, unique=True, help_text="For example: GitHub home page"
    )
    icon = models.CharField(
        max_length=20, unique=True, help_text="For example: fa-github"
    )
    link = models.CharField(max_length=200, unique=True)
    title = models.CharField(max_length=50, unique=True)
    active = models.BooleanField(default=True)
    sort_order = models.IntegerField(default=99)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Menu external link"
        verbose_name_plural = verbose_name
        ordering = ["sort_order"]
