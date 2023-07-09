from django import forms
from django.urls import reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView,TemplateView, View
from .models import Product, Category,Order,Payment,Customer
from .forms import OrderForm, ProductForm, CategoryForm, ProductFormUpdate, ProductImageFormSet
from django.contrib.auth import authenticate, get_user_model,login
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from .forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import FormView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import TemplateView
from django.forms import inlineformset_factory
from .models import Product, ProductImage






    
    



class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'auth/login.html'
    success_url = '/'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

class RegisterView(FormView):
    form_class = UserCreationForm
    template_name = 'auth/registration.html'
    success_url = '/login/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)



class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/product_create.html'
    success_url = reverse_lazy('product_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['image_formset'] = ProductImageFormSet(self.request.POST, self.request.FILES)
        else:
            context['image_formset'] = ProductImageFormSet()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        image_formset = ProductImageFormSet(request.POST, request.FILES)
        if form.is_valid() and image_formset.is_valid():
            return self.form_valid(form, image_formset)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, image_formset):
        product = form.save()
        for image_form in image_formset:
            if image_form.cleaned_data.get('image'):
                image = image_form.save(commit=False)
                image.product = product
                image.save()
        return super().form_valid(form)












class ProductListView(ListView):
    model = Product
    template_name = 'product/product_list.html'
    context_object_name = 'products_on_promotion'

    def get_queryset(self):
        return Product.objects.filter(on_promotion=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        flagship_product = Product.objects.filter(flagship=True).first()
        main_image = flagship_product.main_image() if flagship_product else None
        context['main_image'] = main_image
        return context


class ProductUpdateView(UpdateView):
    model = Product
    fields = ['name', 'description', 'price', 'category', 'on_promotion', 'flagship']
    template_name = 'product/product_update.html'

    def get_initial(self):
        initial = super().get_initial()
        initial['name'] = self.object.name
        initial['description'] = self.object.description
        initial['price'] = self.object.price
        initial['category'] = self.object.category
        # ...
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['image_formset'] = ImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['image_formset'] = ImageFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context['image_formset']
        if image_formset.is_valid():
            response = super().form_valid(form)
            image_formset.instance = self.object
            image_formset.save()
            return redirect('product_update_success')
        else:
            return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('product_list')

ImageFormSet = inlineformset_factory(Product, ProductImage, fields=('image', 'is_main'), extra=1)

   






class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('product-deleted')
    template_name = 'product/product_confirm_delete.html'

class CategoryListView(ListView):
    model = Category
    template_name = 'category_list.html'

class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'categories/category_create.html'

    def form_valid(self, form):
        category = form.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('product_list')

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category_detail.html'

class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name', 'image']
    template_name = 'categories/category_update.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        return redirect('category_update_success')
    
    def get_success_url(self):
        return reverse_lazy('product_list')

class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'categories/category_confirm_delete.html'
    success_url = '/categories/delete/success/'


    



class CategoryUpdateSuccessView(TemplateView):
    template_name = 'categories/category_update_success.html'

class CategoryDeleteSuccessView(TemplateView):
    template_name = 'categories/category_delete_success.html'
    
class ProductUpdateSuccessView(TemplateView):
    template_name = 'product/product_updated_success.html'    



class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'transactions/order_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        basket = self.request.session.get('basket', [])
        products = Product.objects.filter(id__in=basket)
        total_price = sum(product.price for product in products)
        context['total_price'] = total_price
        return context

    def form_valid(self, form):
        order = form.save(commit=False)
        user = get_user_model().objects.get(username=self.request.user.username)
        customer, created = Customer.objects.get_or_create(user=user)
        order.customer = customer
        order.save()
        basket = self.request.session.get('basket', [])
        products = Product.objects.filter(id__in=basket)
        order.products.set(products)
        return redirect('order_success')

class OrderSuccessView(TemplateView):
    template_name = 'transactions/order_success.html'

class PaymentCreateView(CreateView):
    model = Payment
    fields = ['order']
    template_name = 'transactions/payment_form.html'
    
    
class BasketView(TemplateView):
    template_name = 'transactions/basket.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        basket = self.request.session.get('basket', [])
        products = Product.objects.filter(id__in=basket)
        context['products'] = products
        return context

class AddToBasketView(View):
    def post(self, request, product_id):
        basket = request.session.get('basket', [])
        if product_id not in basket:
            basket.append(product_id)
        request.session['basket'] = basket
        return redirect('basket')

class RemoveFromBasketView(View):
    def post(self, request, product_id):
        basket = request.session.get('basket', [])
        if product_id in basket:
            basket.remove(product_id)
        request.session['basket'] = basket
        return redirect('basket')   