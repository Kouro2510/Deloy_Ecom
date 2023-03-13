import unittest
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session

from .forms import CustomerProfileForm
from .models import Product, Cart, Wishlist, Payment


# test function
class LoginTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'testuser'
        self.email = 'anvu523@gmail.com'
        self.password = 'secret'
        User.objects.create_user(self.username, self.email, self.password)

    def test_login(self):
        response = self.client.login(username=self.username, password=self.password)
        self.assertTrue(response)


class RegisterTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'testuser'
        self.email = 'testuser@gmail.com'
        self.password = 'secret'

    def test_register(self):
        response = self.client.post('/registration/', {
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'confirm_password': self.password
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=self.username).exists())


class SearchTests(TestCase):
    def setUp(self):
        self.client.login(username='root', password='colamcho1320')

    def test_search_page(self):
        client = Client()
        response = client.get('/search/?search=milk')
        # Thay [A-Z] trong /search/?search=[A-Z] bằng 1 tên sản phẩm bất kỳ
        self.assertEqual(response.status_code, 200)

    def test_search_with_invalid_query(self):
        client = Client()
        response = client.get('/search/?search=1234')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "")


class CartTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.product = Product.objects.create(
            title='Test Product',
            description='This is a test product',
            selling_price=10.00,
            discounted_price=8
        )

    def test_adding_to_cart(self):
        self.client.login(username='testuser', password='password')
        session = Session.objects.get(session_key=self.client.session.session_key)
        cart = Cart.objects.create(
            user=self.user,
            product=self.product,
            quantity=1)

        self.assertEqual(cart.product, self.product)
        self.assertEqual(cart.quantity, 1)

    def test_removing_from_cart(self):
        self.client.login(username='testuser', password='password')
        session = Session.objects.get(session_key=self.client.session.session_key)


class WishlistTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.product = Product.objects.create(
            title='Test Product',
            description='This is a test wishlist product',
            selling_price=10.00,
            discounted_price=8
        )

    def test_add_to_wishlist(self):
        self.client.login(username='testuser', password='password')
        session = Session.objects.get(session_key=self.client.session.session_key)
        wishlist = Wishlist.objects.create(
            user=self.user,
            product=self.product,
        )

        self.assertEqual(wishlist.product, self.product)

    def test_removing_from_wishlist(self):
        self.client.login(username='testuser', password='password')
        session = Session.objects.get(session_key=self.client.session.session_key)


# test url
class UrlTest(TestCase):
    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/login.html')

    def test_about_view(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/about.html')

    def test_contact_view(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/contact.html')

    # def test_address_view(self):
    #     response = self.client.get(reverse('address/1'))
    #     self.assertEqual(response.status_code,200)
    #     self.assertTemplateUsed(response,'app/address.html')
    def test_profile_view(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/profile.html')

    def test_category_view(self):
        response = self.client.get('/category/ML')
        # Thay [A-Z] trong category/[A-Z] bằng 1 tag sản phẩm bất kỳ đã được miêu tả ở phần category choices của models
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/category.html')


class PaymentTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='thanhphuong', password='123456')
        self.product = Product.objects.create(
            title='Test Product',
            description='This is a test product',
            selling_price=10.00,
            discounted_price=8
        )
        self.cart = Cart.objects.create(
            user=self.user,
            product=self.product,
            quantity=1)
        self.assertEqual(self.cart.product, self.product)
        self.assertEqual(self.cart.quantity, 1)

    def test_Payment(self):
        self.client.login(username='thanhphuong', password='123456')
        Session.objects.get(session_key=self.client.session.session_key)
        Payment.objects.create(
            user=self.user,
            amount=self.cart.quantity * self.product.discounted_price,
            payment_status='pending',
            payment_option='Card',
            paid=False
        )


class InputValidationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='thanhphuong', password='123456')

    def test_valid_input(self):
        form_data = {'user': self.user, 'name': 'Thanhphuong', 'locality': '2500',
                     'city': 'HCM city', 'mobile': '0933083958',
                     'area': 'N', 'zipcode': '1521'}
        form = CustomerProfileForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_input(self):
        form_data = {'user': self.user, 'name': 'Thanhphuong', 'locality': '2500',
                     'city': 'HCM city', 'mobile': 'áccs',
                     'area': 'N', 'zipcode': '22was'}
        form = CustomerProfileForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)
        self.assertIn('mobile', form.errors)
        self.assertIn('zipcode', form.errors)


class BuynowTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.product = Product.objects.create(
            title='Test Product',
            description='This is a test product',
            selling_price=10.00,
            discounted_price=8,
            product_image='test.png',
        )

    def test_buynow(self):
        self.client.login(username='testuser', password='password')
        session = Session.objects.get(session_key=self.client.session.session_key)
        cart = Cart.objects.create(
            user=self.user,
            product=self.product,
            quantity=1)

        self.assertEqual(cart.product, self.product)
        self.assertEqual(cart.quantity, 1)
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/checkout.html')


if __name__ == '__main__':
    unittest.main()
