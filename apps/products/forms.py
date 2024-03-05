from django import forms

from products.models.models_product import Product
from products.models.models_comment import CommentModel


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'category', 'affiliate_link', 'coupon', 'image', 'resend_product', 'company_product', 'product_description']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
            
class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        fields = ['name', 'email', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu nome'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Seu e-mail'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Seu comentário'}),
        }