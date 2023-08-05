from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('accounts/account', views.account_index),
    path('accounts/sign/up', views.sign_up),
    path('accounts/sign/in', views.sign_in),
    path('accounts/sign/out', views.sign_out),
    path('accounts/history', views.history),
    path('borrow/book/borrow/<str:pk>', views.book_borrow),
    path('borrow/book/giveback/<str:pk>', views.book_give_back),
    path('backend/publisher/new', views.publisher_new),
    path('backend/book/maintenance', views.book_maintenance),
    path('backend/book/new', views.book_new),
    path('backend/book/update/<str:pk>', views.book_update),
    path('backend/book/delete/<str:pk>', views.book_delete),
    path('backend/dashboard/book', views.dashboard_book),
    path('backend/dashboard/user', views.dashboard_user),
    path('backend/history/management', views.history_management),
    path('backend/history/management/approve/<str:pk>', views.giveback_request_approve),
    path('book/details/<str:pk>', views.detail_view),


    # path('borrow/borrowing_index', views.borrowing_index),
]