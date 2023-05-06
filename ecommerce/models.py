from django.db import models


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
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ("-created_at",)

	def __str__(self):
		return self.name

