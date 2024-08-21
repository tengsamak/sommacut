from django.db import models

# Create your models here.
# """Models for the Wishlist app."""
#from django.db import models
from products.models import Product,Variants
from user.models import UserProfile
from django.contrib.auth.models import User

#for testing
class wish_list(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='wish_list')
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='wish_list')
    #variant=models.ForeignKey(Variants,on_delete=models.CASCADE,related_name='wishl_ist')
    created_at = models.DateTimeField(auto_now_add=True,editable=False,blank=True,null=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Wish_list'
        verbose_name_plural='Wish_lists'
    
    def __str__(self):
        """Return the string representation of the model."""
        return str(self.user) + '\'s wish_list'
        
class Wishlist(models.Model):
    """Model for a wishlist."""
    user = models.OneToOneField(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='wishlist'
    )
    products = models.ManyToManyField(
        Product,
        blank=True,
        related_name='wishlist'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        blank=True,
        null=True,
    )

    class Meta:
        """Meta class for the Wishlist model."""
        ordering = ['-created_at']
        verbose_name = 'Wishlist'
        verbose_name_plural = 'Wishlists'

    def __str__(self):
        """Return the string representation of the model."""
        return str(self.user) + '\'s wishlist'

    def add_to_wishlist(self, product):
        """Add a product to the wishlist."""
        # check that product is not already in the wishlist
        if product not in self.products.all():
            self.products.add(product)
            return True
        return False

    def remove_from_wishlist(self, product):
        """Remove a product from the wishlist."""
        # check that product is in the wishlist
        if product in self.products.all():
            self.products.remove(product)
            return True
        return False

    def remove_all_from_wishlist(self):
        """Remove all products from the wishlist."""
        self.products.clear()
        return True

    def get_products(self):
        """Return the products in the wishlist."""
        return self.products.all()


