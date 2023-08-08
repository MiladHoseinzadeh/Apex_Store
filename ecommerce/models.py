from io import BytesIO
from django.contrib.auth.models import User
from django.core.files import File
from django.db import models

from PIL import Image


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("title",)
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title
    

class Product(models.Model):
	name = models.CharField(max_length=255)
	slug = models.SlugField()
	category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE)
	description = models.TextField(blank=True, null=True)
	quantity = models.PositiveIntegerField()
	price = models.IntegerField()
	image = models.ImageField(upload_to="uploads/", blank=True, null=True)
	thumbnail = models.ImageField(upload_to="uploads/", blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ("-created_at",)

	def __str__(self):
		return self.name
        
	def get_thumbnail(self):
		if self.thumbnail:
			return self.thumbnail.url
		else:
			if self.image:
				self.thumbnail = self.make_thumbnail(self.image)
				self.save()

				return self.thumbnail.url
			else:
				return "https://via.placeholder.com/500x270.jpg"
	
	def make_thumbnail(self, image, size=(500, 270)):
		img = Image.open(image)
		img.convert("RGB")
		img.thumbnail(size)

		thumb_io = BytesIO()
		img.save(thumb_io, "JPEG", quality=85)

		thumbnail = File(thumb_io, name=image.name)

		return thumbnail

	def get_total_rating(self):
		total_retings = 0

		for review in self.reviews.all():
			total_retings += review.rating

		if total_retings > 0:
			return total_retings / self.reviews.count()
		
		return 0


class Order(models.Model):
	ORDERED = "o"
	SHIPPED = "s"
	STATUS_CHOICES = (
		(ORDERED, "Ordered"),
		(SHIPPED, "Shipped"),
	)
	user = models.ForeignKey(User, related_name="orders", on_delete=models.CASCADE, blank=True, null=True)
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	email = models.EmailField(max_length=255)
	address = models.TextField()
	zip_code = models.CharField(max_length=10)
	place = models.CharField(max_length=255)
	phone = models.CharField(max_length=20)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	paid = models.BooleanField(default=False)
	paid_amount = models.PositiveIntegerField(blank=True, null=True)
	status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=ORDERED)

	class Meta:
		ordering = ("-created_at",)

	def get_total_price(self):
		if self.paid_amount:
			return self.paid_amount
		
		return 0
	
	def __str__(self):
		return f"Ordered by {self.first_name} {self.last_name}"


class OrderItem(models.Model):
	order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
	product = models.ForeignKey(Product, related_name="items", on_delete=models.CASCADE)
	price = models.IntegerField()
	quantity = models.IntegerField(default=1)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


class Review(models.Model):
	product = models.ForeignKey(Product, related_name="reviews", on_delete=models.CASCADE)
	rating = models.IntegerField(default=3)
	content = models.TextField()
	created_by = models.ForeignKey(User, related_name="reviews", on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	

