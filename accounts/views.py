from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.urls import reverse,reverse_lazy
from django.views.generic import DetailView,UpdateView,ListView,TemplateView
from django.contrib.auth import views as auth_view
from .forms import CreateUser,UserRegisterCodeForm,UserLoginForm,UserAddAdressForm,UserEditEmailForm
from django.contrib import messages
from .models import User,Profile,Adresse,Wishlist,CartItem,Cart
from home.models import ProductColors,ProductSizes
from django.contrib.auth import login,authenticate,logout
from random import randint
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMessage
from home.models import Product

class UserRegisterView(View):
    template_name = 'accounts/register.html'
    form_class = CreateUser
    def get(self,request,*args,**kwargs):
        return render(request,self.template_name,{'form':self.form_class()})
    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = randint(100000, 999999)
            request.session['register_data'] = form.cleaned_data
            request.session['register_code'] = random_code
            email = EmailMessage(
                'Activation Code',
                f'{random_code}\nThis Service Is Test Tho',
                to=[form.cleaned_data['email']]
            )
            email.send(fail_silently=False)
            return redirect('accounts:registercode')
        return render(request,self.template_name,{'form':form})
    
class UserRegisterCodeView(View):
    template_name = 'accounts/registercode.html'
    form_class = UserRegisterCodeForm
    def get(self,request,*args,**kwargs):
        return render(request,self.template_name,{'exclude_layout': True,'form':self.form_class()})
    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = request.session.get('register_data')
            code = request.session.get('register_code')
            if not data or not code:
                messages.error(request,'session expired')
                return redirect('accounts:register')
            if int(code) == form.cleaned_data['code']:
                user = User.objects.create_user(email=data['email'],username=data['username'],
                                                password=data['password_2'])
                user.save()
                login(request,user)
                messages.success(request,'signed in successfuly')
                request.session.pop('register_data', None)
                request.session.pop('register_code', None)
                return redirect('home:home')
            else:
                messages.error(request,'code is wrong')
            
        return render(request,self.template_name,{'form':form})

class UserLoginView(View):
    template_name = 'accounts/login.html'
    form_class = UserLoginForm
    def get(self,request,*args,**kwargs):
        return render(request,self.template_name,{'form':self.form_class()})
    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request,email=data['email'],password=data['password'])
            if user is not None:
                login(request,user)
                if data['remember_me']:
                    self.request.session.set_expiry(10)
                else:
                    self.request.session.set_expiry(0)
                    self.request.session.modified = True
                messages.success(request,'Welcome')
                return redirect('home:home')
            else:
                messages.error(request,'email or password was invalid')
                return redirect('accounts:login')
        return render(request,self.template_name,{'form':form})
    
class UserProfileView(LoginRequiredMixin,DetailView):
    template_name = 'accounts/profile.html'
    model = Profile
    context_object_name = 'profile'
    def get_object(self, queryset =None,*args,**kwargs):
        return get_object_or_404(Profile,pk=self.kwargs['pk'])
    
class ProfileUpdateView(LoginRequiredMixin,UpdateView):
    template_name = 'accounts/profile.html'
    model = Profile
    context_object_name = 'profile'
    fields = ['username','icon']
    def get_object(self, queryset = None):
        return Profile.objects.get(user=self.request.user)
    def get_success_url(self):
        return reverse('accounts:profile',kwargs={'pk':self.request.user.pk})
    
class UserChangePassView(LoginRequiredMixin,auth_view.PasswordChangeView):
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('accounts:login')

def logoutt(request):
    logout(request)
    return redirect('accounts:login')

class UserAdressesView(LoginRequiredMixin,ListView):
    template_name = 'accounts/my-address.html'
    context_object_name = 'adres'
    model = Adresse

    def get_queryset(self): 
        return Adresse.objects.filter(user=self.request.user)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exclude_layout'] = True
        return context
    
class UserAddAdressView(LoginRequiredMixin,View):
    template_name = 'accounts/add-address.html'
    form_class = UserAddAdressForm
    def get(self,request):
        return render(request,self.template_name,{'exclude_layout': True,'form':self.form_class()})
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            location = f"{data['city']} - {data['street']}"
            Adresse.objects.create(user=self.request.user,user_name=data['user_name'],loc=location,number=data['number'])
            return redirect('accounts:adress')
        return render(request,self.template_name,{'form':form})
    
class UserDeleteAdressView(LoginRequiredMixin,View):
    def post(self,request,*args, **kwargs):
        adress = get_object_or_404(Adresse,id=self.kwargs['id'])
        adress.delete()
        return redirect('accounts:adress')


class UserWishlistView(LoginRequiredMixin, ListView):
    template_name = 'accounts/wishlist.html'
    context_object_name = 'products'

    def get_queryset(self):
        user = User.objects.get(id=self.kwargs['id'])
        try:
            wishlist = Wishlist.objects.get(user=user)
            return wishlist.products.all()  # assuming ManyToManyField to Product
        except Wishlist.DoesNotExist:
            return Product.objects.none()  # return empty queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exclude_layout'] = True
        return context


class UserAddToWishlistView(LoginRequiredMixin, View):
    def post(self, request, id, *args, **kwargs):
        product = get_object_or_404(Product, id=id)
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        wishlist.products.add(product)
        return redirect(request.META.get('HTTP_REFERER', 'home'))


class UserRemoveWishlistView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=self.kwargs['id'])
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        wishlist.products.remove(product)  # ✅ Just remove product
        return redirect(request.META.get('HTTP_REFERER', 'home'))
    
class UserChangeEmail(LoginRequiredMixin, View):
    template_name = 'accounts/change-email.html'
    form_class = UserEditEmailForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'form': self.form_class(),
            'exclude_layout': True
        })

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = randint(100000, 999999)
            email = form.cleaned_data['email']
            request.session['emailchange_data'] = email
            request.session['emailchange_code'] = random_code

            email_msg = EmailMessage(
                subject='Activation Code',
                body=f'{random_code}\nThis Service Is Test Tho',
                to=[email]
            )
            email_msg.send(fail_silently=False)

            return redirect('accounts:changeemailcode')

        return render(request, self.template_name, {
            'form': form,
            'exclude_layout': True
        })

    
class UserChangeEmailCodeView(LoginRequiredMixin, View):
    form_class = UserRegisterCodeForm
    template_name = 'accounts/changeemailcode.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'form': self.form_class(),
            'exclude_layout': True
        })

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            session_email = request.session.get('emailchange_data')
            session_code = request.session.get('emailchange_code')

            if not session_email or not session_code:
                messages.error(request, 'Session expired. Please try again.')
                return redirect('accounts:changeemail')

            if int(form.cleaned_data['code']) == int(session_code):
                request.user.email = session_email
                request.user.save()
                messages.success(request, 'Email successfully changed.')

                # Clean session
                request.session.pop('emailchange_data', None)
                request.session.pop('emailchange_code', None)

                return redirect('accounts:profile', pk=request.user.pk)
            else:
                messages.error(request, 'Incorrect code.')

        return render(request, self.template_name, {
            'form': form,
            'exclude_layout': True
        })


class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)

        size_id = request.POST.get('size_id')
        color_id = request.POST.get('color_id')

        # Validate and fetch size and color objects or None if not provided
        size = None
        color = None
        if size_id:
            size = get_object_or_404(ProductSizes, id=size_id, product=product)
        if color_id:
            color = get_object_or_404(ProductColors, id=color_id, product=product)

        # Get or create cart for the user
        cart, _ = Cart.objects.get_or_create(user=request.user)

        # Try to get existing cart item with the same product, size, and color
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            size=size,
            color=color,
            defaults={'quantity': 1}
        )

        if not created:
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, "Updated quantity in your cart.")
        else:
            messages.success(request, "Added product to your cart.")

        return redirect('home:store') 
    

class UserCartView(LoginRequiredMixin, ListView):
    template_name = 'accounts/cart.html'
    model = CartItem
    context_object_name = 'cart_items'

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = context['cart_items']
        total = sum(item.quantity * item.product.price for item in cart_items)
        context['total'] = total
        return context

class RemoveFromCartView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        item_id = self.kwargs['item_id']
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        cart_item.delete()
        return redirect('accounts:cart')