from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from django.views.generic.edit import FormView, View
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from cart.forms import CartAddProductForm
from .recommender import Recommender


class ProductList(ListView):
	template_name = 'shop/product/list.html'

	def get(self, request, *args, **kwargs):
		category = None
		categories = Category.objects.all()
		products = Product.objects.filter(available=True)
		if 'category_slug' in kwargs:
			# language = request.LANGUAGE_CODE
			# category = get_object_or_404(Category, translations__language_code=language,translations__slug=category_slug)
		
			category = get_object_or_404(Category, slug=kwargs['category_slug'])
			products = products.filter(category=category)
		return render(request,self.template_name,{'category': category,'categories': categories,'products': products})


class ProductDetail(DetailView):
	template_name = 'shop/product/detail.html'

	def get(self, request, *args, **kwargs):
		cart_product_form = CartAddProductForm()
		product = get_object_or_404(Product,id=kwargs['id'],slug=kwargs['slug'],available=True)
		r = Recommender()
		recommended_products = r.suggest_products_for([product], 4)
		# language = request.LANGUAGE_CODE
		# product = get_object_or_404(Product,id=kwargs['id'],translations__language_code=language,translations__slug=slug,available=True)
		
		return render(request,self.template_name,{'product': product, 'cart_product_form': cart_product_form, 'recommended_products': recommended_products})
