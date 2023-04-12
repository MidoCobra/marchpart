from .models import (
    Category,
    Product,
    Brand,
    Model,
    EngineCapacity,
    ManfactureDate,
    Blog_tags,
    Contact_information,
)
from django.shortcuts import get_object_or_404

from urllib.parse import quote, unquote




def Base(request):
    all_types_parts = Category.objects.filter(
        # products__brand=None,
        products__model=None,
        products__engine_capacity=None,
        products__manfacture_date=None,
    )
    search_allCategories = Category.objects.all()
    latest_products = Product.objects.all().order_by("-created_at")[:4]
    Navcategories = Category.objects.all().order_by("name")
    NavBrands = Brand.objects.all().order_by("name")
    Navcategories_arabic = Category.objects.all().order_by("name_arabic")
    NavBrands_arabic = Brand.objects.all().order_by("name_arabic")
    Footercategories = Category.objects.all()[:5]
    Footercategories2 = Category.objects.all()[2:]

    allBlogTags = Blog_tags.objects.all()

    contact_information = get_object_or_404(Contact_information, id=1)

    arabic_language = unquote(request.get_full_path()).replace('englishlanguage','arabiclanguage')  #unquote because in converting symbols changes to %4d etc
    english_language = unquote(request.get_full_path()).replace('arabiclanguage','englishlanguage')
    context = {
        "all_types_parts": all_types_parts,
        "search_allCategories": search_allCategories,
        "latest_products": latest_products,
        "Navcategories": Navcategories,
        "NavBrands": NavBrands,
        "Footercategories": Footercategories,
        "Footercategories2": Footercategories2,
        "Navcategories_arabic": Navcategories_arabic,
        "NavBrands_arabic": NavBrands_arabic,
        "allBlogTags": allBlogTags,
        "contact_information": contact_information,

        "arabic_language": arabic_language,
        "english_language": english_language,
    }
    return context
