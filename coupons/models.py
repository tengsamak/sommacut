from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.
class Coupons(models.Model):
	code 		= models.CharField(max_length=10,unique=True)
	valid_from  = models.DateTimeField()
	valid_to 	= models.DateTimeField()
	discount 	= models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)])
	active 		= models.BooleanField(default=False)
	class Meta:
		verbose_name = "Coupons Code"
		verbose_name_plural = "Coupons"

	def __str__(self):
		return self.code
