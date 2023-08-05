from django.shortcuts import render, redirect, get_object_or_404
from .models import Publisher, Book, BorrowRecord
from .forms import  RegisterForm, LoginForm, BookNewForm, PublisherNewForm, Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
import json
from django.core.paginator import Paginator
from django.views.generic import ListView
from datetime import datetime
from collections import Counter
# Create your views here.
def index(request):
    books = Book.objects.all()
    paginator = Paginator(books, 8)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'frontend/index.html', locals())

def account_index(request):
    return render(request, 'frontend/accounts.html')

def sign_up(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '註冊成功')
            return redirect('/accounts/sign/in', locals())
    return render(request, 'frontend/sign_up.html', locals())

#登入
def sign_in(request):
    form = LoginForm()
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, '登入成功！')
            return redirect('/')  #重新導向到首頁
    return render(request, 'frontend/sign_in.html', locals())

#登出
def sign_out(request):

    logout(request)
    messages.success(request, '登出成功！')
    return redirect('/')

@staff_member_required
def book_maintenance(request):
    data = Book.objects.all()

    return render(request, 'backend/book_maintenance.html', locals())

@staff_member_required
def book_new(request):
    form = BookNewForm()
    publisher = Publisher.objects.all()
    category = Category.objects.all()
    if request.method == "POST":
        form = BookNewForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '新增成功')
            return redirect('/backend/book/maintenance')
        else:
            messages.error(request, '新增失敗')
    return render(request, 'backend/book_new.html', locals())

@staff_member_required
def book_update(request, pk):
    book_info = Book.objects.get(id=pk)
    form = BookNewForm(instance=book_info)   
    if request.method == "POST":
        form = BookNewForm(request.POST, request.FILES or None, instance=book_info)
        if form.is_valid():
            form.save()
            messages.success(request, '修改成功')
            return redirect('/backend/book/maintenance')
        else:
            messages.error(request, '修改失敗')
        return render(request, 'backend/book_maintenance.html')
    return render(request, 'backend/book_update.html', locals())

@staff_member_required
def book_delete(request, pk):
    book_info = Book.objects.get(id=pk)
    if request.method == "POST":
        book_info.delete()
        messages.success(request, '刪除成功')
        return redirect('/backend/book/maintenance')
    else:
        messages.error(request, '刪除失敗')
    return render(request, 'backend/book_maintenance.html')

@staff_member_required
def publisher_new(request):
    form = PublisherNewForm()
    if request.method == "POST":
        form = PublisherNewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            messages.error(request, 'createfail')
    return render(request, 'backend/publisher_new.html', locals())

@login_required(login_url="/accounts/sign/in")
def history(request):
    user_borrow_records = BorrowRecord.objects.filter(user=request.user)
    r = []
    for i in user_borrow_records:
        p = i.book.book_category.category
        r.append(p)
    c_dict = {}
    for c in r:
        if c in c_dict:
            c_dict[c]+=1
        else:
            c_dict[c]=1
    category_list = list(c_dict.keys())
    count_list = list(c_dict.values())
    c_zip = zip(category_list, count_list)
    category_data = json.dumps(category_list)
    count_data = json.dumps(count_list)

    return render(request, 'frontend/history.html', locals())

@staff_member_required
def history_management(request):
    giveback_requests = BorrowRecord.objects.all()
    return render(request, 'backend/history_management.html', locals())

@staff_member_required
def giveback_request_approve(request, pk):
    request_approve = BorrowRecord.objects.get(id=pk)
    request_approve.book.give_back=1
    request_approve.book.save()
    request_approve.return_state=1
    request_approve.save()
    request_approve.return_state_request=0
    request_approve.save()

    return redirect('/backend/history/management')

@login_required(login_url="/accounts/sign/in")
def book_borrow(request, pk):
    book = Book.objects.get(id=pk)
    book.give_back=0
    book.save()
    borrow_records = BorrowRecord(user=request.user, book=book, return_state=0)
    borrow_records.save()
    messages.success(request, '借閱成功！')
    return redirect('/')  # 重新導向到首頁

@login_required(login_url="/accounts/sign/in")
def book_give_back(request, pk):
    borrow_records = BorrowRecord.objects.get(id=pk)
    borrow_records.return_state_request=1
    borrow_records.save()
    return redirect('/accounts/history')  # 重新導向到首頁

def dashboard_book(request):
    borrows_data = BorrowRecord.objects.all()
    borrows_count = Book.objects.count() #借閱次數總計
    not_returned_count = BorrowRecord.objects.filter(return_state=False).count() #未歸還總計
    books = Book.objects.count() #書籍總數
    returned_count = books - not_returned_count #總數 - 未歸還 = 歸還總計
    publisher_counts = Book.objects.values('publisher').annotate(count=Count('publisher'))
    publisher_data_list = []
    name = []
    count = []
    for item in publisher_counts:
        p = Publisher.objects.get(id=item['publisher'])
        name.append(p.publisher_name)
        count.append(item['count'])
    publisher_data_list={'publisher': name, 'count':count}
    publisher_data_list_len = range(len(publisher_data_list['publisher']))
    publisher_data_list_zip = zip(name, count)
    category_counts = Book.objects.values('book_category').annotate(count=Count('book_category'))
    category_data_list = []
    for a in category_counts:
        category_data_list.append(a)
    c_name = []
    c_count = []
    for i in category_counts:
        c = Category.objects.get(id=i['book_category'])
        c_name.append(c.category)
        c_count.append(i['count'])
    category_data_list={'book_category': c_name, 'count':c_count}
    category_data_list_zip = zip(c_name, c_count)
    user_count = User.objects.count()
    return render(request, 'backend/dashboard_book.html', locals())

def dashboard_user(request):
    records = BorrowRecord.objects.all()
    borrow_dates = [record.borrow_time.strftime('%Y-%m-%d') for record in records]
    borrow_counts = [records.filter(borrow_time=record.borrow_time).count() for record in records]
    dates_list = []
    for d in borrow_dates:
        d_mon = d.split('-')[1]
        dates_list.append(d_mon)
    month_dict = {}
    month_list = []
    count_dict = Counter(dates_list)
    month_count = list(count_dict.values())
    for k in dates_list:
        if k not in month_list:
            month_list.append(k)

    for i in dates_list:
        if i not in month_dict:
            month_dict[i] = 1
        else:
            month_dict[i] += 1
    month_zip = zip(month_list, month_count)

    all_users = User.objects.all()
    date_joined_list = [user.date_joined.strftime('%m') for user in all_users]
    menber_dict = {}
    menber_list = []
    count_m_dict = Counter(date_joined_list)
    menber_count = list(count_m_dict.values())
    for m in date_joined_list:
        if m not in menber_list:
            menber_list.append(m)

    for d in date_joined_list:
        if d not in menber_dict:
            menber_dict[d] = 1
        else:
            menber_dict[d] += 1
    menber_zip = zip(menber_list, menber_count)

    today = datetime.today()
    year = today.year
    return render(request, 'backend/dashboard_user.html', locals())

def detail_view(request, pk):
    book = Book.objects.get(id=pk)
    return render(request, 'frontend/book_details.html', locals())