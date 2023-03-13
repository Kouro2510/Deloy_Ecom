from django.contrib import admin
from .models import Product, Customer, Cart, Payment, OrderPlaced, Wishlist, Comment, CommentReply, Image
from django.contrib.auth.models import Group


# Register your models here.
@admin.register(Image)
class ImageModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'product_images']


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'discounted_price', 'category']


@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'locality', 'city', 'area', 'zipcode']


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']


@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'payment_status', 'payment_option',
                    'paid']


@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer', 'product', 'quantity', 'ordered_date', 'status', 'payment']


@admin.register(Wishlist)
class WishlistModeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product']


admin.site.unregister(Group)


@admin.register(CommentReply)
class CommentReplyModeAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'description']


@admin.register(Comment)
class CommentModeAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'description']
