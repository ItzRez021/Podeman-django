from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.views.generic import ListView,DetailView
from django.conf import settings
from .models import Blog,Product,ProductColors,ProductSizes
from django.contrib import messages
from .forms import PriceFilterForm,CategoryFilterForm
from django.db import models
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import CartItem
from django.urls import reverse

class HomePage(View):
    template_name = 'home/index.html'
    def get(self,request):
        blog = Blog.objects.all()
        product = Product.objects.all()
        return render(request,self.template_name,{'MEDIA_URL':settings.MEDIA_URL,'blog':blog,'product':product})
    
class BlogView(ListView):
    template_name = 'home/blog.html'
    model = Blog
    context_object_name = 'blog'

    def get_queryset(self):
        return Blog.objects.all()
    

class BlogPostView(DetailView):
    template_name = 'home/blog-post.html'
    model = Blog
    context_object_name = 'blog'
    def get_object(self, queryset = None,*args, **kwargs):
        return Blog.objects.get(pk=self.kwargs['pk'])
    

class StoreView(ListView):
    template_name = 'home/shop.html'
    model = Product
    context_object_name = 'product'

    def get_queryset(self):
        queryset = super().get_queryset()
        selected_categories = self.request.GET.getlist('category')
        selected_price = self.request.GET.get('price')
        query = self.request.GET.get('q')

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(info__icontains=query)
            )

        if selected_categories:
            queryset = queryset.filter(category__title__in=selected_categories)

        if selected_price == '0-50':
            queryset = queryset.filter(price__gte=0, price__lte=50)
        elif selected_price == '51-100':
            queryset = queryset.filter(price__gte=51, price__lte=100)
        elif selected_price == '101+':
            queryset = queryset.filter(price__gte=101)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_categories'] = self.request.GET.getlist('category')
        context['selected_price'] = self.request.GET.get('price')
        context['query'] = self.request.GET.get('q', '')
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_categories'] = self.request.GET.getlist('category')
        context['selected_price'] = self.request.GET.get('price')
        context['query'] = self.request.GET.get('q', '')
        return context



class productdetailView(DetailView):
    template_name = 'home/product-page.html'
    model = Product
    context_object_name = 'product'
    def get_object(self,queryset=None):
        return get_object_or_404(Product,pk=self.kwargs['pk'])



def product_search(request):
    query = request.GET.get('q')
    products = Product.objects.filter(
        Q(title__icontains=query) | Q(info__icontains=query)
    ) if query else Product.objects.none()
    
    return render(request, 'home/shop.html', {
        'query': query,
        'products': products
    })


