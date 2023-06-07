from io import BytesIO
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

