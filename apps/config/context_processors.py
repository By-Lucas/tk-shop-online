
from ads.models import ConfigAds
from category.models import Category
from stores.models import ProductStore
from company.models.models_company import Company
from config.models.models_config import ConfigModel
from config.models.models_social import SocialMedia


def get_company_stores(request):
    try:
        company_stores = ProductStore.objects.all()
    except:
        company_stores = None
    return dict(company_stores=company_stores)

def get_ads(request):
    try:
        config_ads = ConfigAds.objects.all().first()
    except:
        config_ads = None
    return dict(config_ads=config_ads)

def get_config_site(request):
    try:
        config_site = ConfigModel.objects.all().first()
    except:
        config_site = None
    return dict(config_site=config_site)

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


