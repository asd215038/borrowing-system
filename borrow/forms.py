from django import forms
from .models import Book, User, Publisher, BorrowRecord, Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CategoryForm(forms.ModelForm):
    category = forms.TextInput(attrs={'class': 'form-control'})
    fields = ['category']
    widgets = {
            'category': forms.TextInput(attrs={'class': 'form-control'}),
        }
    labels = {
            'category' : '書籍類別',
        }

class BookNewForm(forms.ModelForm):
    book_name = forms.TextInput(attrs={'class': 'form-control'})
    publisher = forms.ModelChoiceField(queryset=Publisher.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    book_category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = Book
        fields = ['book_name', 'publisher', 'book_category']
        labels = {
            'book_name' : '圖書名稱',
            'publisher': '出版社名稱',
            'book_category': '書籍類別',

        }

class PublisherNewForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = ['publisher_name', 'publisher_phone', 'publisher_adress']
        widgets = {
            'publisher_name': forms.TextInput(attrs={'class': 'form-control'}),
            'publisher_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'publisher_adress': forms.TextInput(attrs={'class': 'form-control'}),

        }
        labels = {
            'publisher_name' : '出版社名稱',
            'publisher_phone': '出版社電話',
            'publisher_adress': '出版社地址',

        }

class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label="帳號",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label="電子郵件",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label="密碼確認",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class LoginForm(forms.Form):
    username = forms.CharField(
        label="帳號",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )