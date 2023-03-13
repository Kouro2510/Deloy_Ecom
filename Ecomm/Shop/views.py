from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Product, Customer, Cart, Payment, OrderPlaced, Wishlist, Comment, CommentReply, Image
from .forms import CustomerRegistrationForm, CustomerProfileForm, CommentForm, ReplyForm
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test


# Create your views here.

def home(request):
    return render(request, 'app/home.html')


def about(request):
    return render(request, 'app/about.html')


def contact(request):
    return render(request, 'app/contact.html')


def product_detail(request, pk):
    user = request.user
    if user is None:
        product = Product.objects.get(pk=pk)
        images = Image.objects.filter(product_images=pk)
        image_first = Image.objects.filter(product_images=pk).first()
        all_comments = Comment.objects.filter(product=product.id)
        wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user))
        parent_id = request.POST.get('parent_id')
        # print(all_product_images)
        print(parent_id)
        if request.method == "POST":
            form1 = CommentForm(request.POST)
            form2 = ReplyForm(request.POST)
            print(form2.errors)
            if parent_id is None:
                if form1.is_valid():
                    author = request.user
                    product_id = product
                    description = form1.cleaned_data["description"]
                    req = Comment(author=author, product=product_id, description=description)
                    req.save()
                    return redirect(request.META.get('HTTP_REFERER', '/'))
            else:
                if form2.is_valid():
                    author = request.user
                    parent_comment = Comment.objects.get(id=parent_id)
                    description = form2.cleaned_data["description"]
                    req = CommentReply(author=author, parent=parent_comment, description=description)
                    req.save()
                    return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            form1 = CommentForm()
            form2 = ReplyForm()
        context = {
            'product': product,
            'form1': form1,
            'form2': form2,
            'wishlist': wishlist,
            'all_comments': all_comments,
            'images': images,
            'image_first': image_first,
        }
    else:
        return redirect('/accounts/login')

    return render(request, "app/productdetail.html", context)


def delete_comment(request, pk):
    comment = Comment.objects.get(id=pk)
    if comment.author == request.user:
        comment.delete()
        return redirect(request.META.get('HTTP_REFERER', '/'))


def delete_reply(request, pk):
    reply = CommentReply.objects.get(id=pk)
    if reply.author == request.user:
        reply.delete()
        return redirect(request.META.get('HTTP_REFERER', '/'))


class CategoryView(View):
    def get(self, request, val):
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request, "app/category.html", locals())


class CategoryTitle(View):
    def get(self, request, val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request, "app/category.html", locals())


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', locals())

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! User Register Successfully")
            return redirect('/accounts/login')
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, 'app/customerregistration.html', locals())


class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', locals())

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        user = request.user
        if form.is_valid():
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            area = form.cleaned_data['area']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=user, name=name, locality=locality, mobile=mobile, city=city, area=area,
                           zipcode=zipcode)
            reg.save()
            messages.success(request, "Congratulation! Profile save successfully")
        else:
            messages.warning(request, "Invalid Input Data")

        return redirect('/address/')


def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', locals())


class UpdateAddress(View):
    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request, 'app/UpdateAddress.html', locals())

    def post(self, request, pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.area = form.cleaned_data['area']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
        else:
            messages.warning(request, "Invalid Input Data")
        return redirect('/address/')


def remove_address(request, pk):
    add = Customer.objects.get(id=pk)
    add.delete()
    return redirect('/address/')


# @login_required()
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    if Cart.objects.filter(product=product_id).exists():
        c = Cart.objects.get(Q(product=product_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0
        return redirect('/cart')
    else:
        product = Product.objects.get(id=product_id)
        Cart(user=user, product=product).save()
        return redirect('/cart')
    return quantity_change(request)


def buynow(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    if Cart.objects.filter(product=product_id).exists():
        return redirect('/checkout')
    else:
        product = Product.objects.get(id=product_id)
        Cart(user=user, product=product).save()
        return redirect('/checkout')


def quantity_change(request):
    product_id = request.GET.get('prod_id')
    if Cart.objects.filter(product=product_id).exists():
        c = Cart.objects.get(Q(product=product_id) & Q(user=request.user))
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        # print(prod_id)
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)


def plus_cart(request):
    product_id = request.GET.get('prod_id')
    if Cart.objects.filter(product=product_id).exists():
        c = Cart.objects.get(Q(product=product_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        return quantity_change(request)


def minus_cart(request):
    product_id = request.GET.get('prod_id')
    if Cart.objects.filter(product=product_id).exists():
        c = Cart.objects.get(Q(product=product_id) & Q(user=request.user))
        if c.quantity > 1:
            c.quantity -= 1
            c.save()
        else:
            c.quantity = 1
            c.save()
    return quantity_change(request)


def remove_cart(request):
    product_id = request.GET.get('prod_id')
    if Cart.objects.filter(product=product_id).exists():
        c = Cart.objects.get(Q(product=product_id) & Q(user=request.user))
        c.delete()
    return redirect('/cart/')


# @login_required()
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    cart_empty = False
    if cart.exists():
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
            cart_empty = False
    else:
        value = 0
        amount = amount + value
        cart_empty = True
    totalamount = amount + 40
    return render(request, 'app/addtocart.html', locals())


class checkout(View):
    def get(self, request):
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount + value
        totalamount = famount + 40
        return render(request, 'app/checkout.html', locals())

    def post(self, request):
        user = request.user
        Cuss = Customer.objects.filter(user_id=user).first()
        payment = Payment()
        cart_items = Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount + value
        totalamount = famount + 40
        payment.user = request.user
        payment.amount = totalamount
        payment.payment_option = request.POST.get('Payment')
        payment.payment_status = "pending"
        payment.paid = False
        payment.save()
        for c in cart_items:
            OrderPlaced(user=user, customer=Cuss, product=c.product, quantity=c.quantity, payment=payment).save()
            c.delete()
        return redirect('/orders')


@login_required
def orders(request):
    user = request.user
    totalitem = 0
    totalwishlist = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    order_placed = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', locals())


def plus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist(user=user, product=product).save()
        data = {
            'message': 'Wishlist added successfully'
        }
        return JsonResponse(data)


def minus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user))
        wishlist.delete()
        data = {
            'message': 'Wishlist remove successfully'
        }
        return JsonResponse(data)


def search(request):
    query = request.GET['search']
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    product = Product.objects.filter(Q(title__icontains=query))
    return render(request, "app/search.html", locals())


# @login_required()
def show_wishlist(request):
    user = request.user
    totalitem = 0
    totalwishlist = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    product = Wishlist.objects.filter(user=user)
    return render(request, "app/wishlist.html", locals())
