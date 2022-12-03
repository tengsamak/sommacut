from import_export import resources
from products.models import Color

class ColorResource(resources.ModelResource):
    class Meta:
        model=Color