
from category.models import Category
from company.models.models_company import Company
from config.models.models_social import SocialMedia


def get_social_media(request):
    try:
        social_media = SocialMedia.objects.all().first()
    except:
        social_media = None
    return dict(social_media=social_media)

def get_company_profile(request):
    try:
        company_profile = Company.objects.all().first()
    except:
        company_profile = None
    return dict(company_profile=company_profile)

def get_category(request):
    try:
        category = Category.objects.all().first()
    except:
        category = None
    return dict(category=category)


