from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
from .import Employee_Views
from .import Hod_Views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('base/', views.BASE, name="base"),
    # Login Path    
    path('', views.LOGIN, name="login"),
    path('dologin', views.dologin, name="dologin"),
    path('dologout', views.dologout, name='logout'),

    # Profile Update
    path('profile', views.PROFILE, name='profile'),
    path('profile/update', views.PROFILE_UPDATE, name='profile_update'),
    # This is Hod Panel Url
    path('Hod/home', Hod_Views.home,name='hod_home'),
    #Employee 
    path('Hod/Employee/Add', Hod_Views.ADD_EMPLOYEE, name="add_employee"),
    path('Hod/Employee/View', Hod_Views.VIEW_EMPLOYEE, name="view_employee"),
    path('Hod/Employee/Edit/<str:id>', Hod_Views.EDIT_EMPLOYEE, name="edit_employee"),
    path('Hod/Employee/Update', Hod_Views.UPDATE_EMPLOYEE, name="update_employee"),
    path('Hod/Employee/Delete/<str:admin>', Hod_Views.DELETE_EMPLOYEE, name="delete_employee"),
    #Collecteur
    path('Hod/Collecteur', Hod_Views.ADD_COLLECTEUR, name="add_collecteur"),
    path('Hod/Collecteur/View', Hod_Views.VIEW_COLLECTEUR, name="view_collecteur"),
    path('Hod/Collecteur/Edit/<str:id>', Hod_Views.EDIT_COLLECTEUR, name="edit_collecteur"),
    path('Hod/Collecteur/Update', Hod_Views.UPDATE_COLLECTEUR, name="update_collecteur"),
    path('Hod/Collecteur/Delete/<str:id>', Hod_Views.DELETE_COLLECTEUR, name="delete_collecteur"),

    #Products
    path('Hod/products', Hod_Views.products,name='product-page'),
    path('Hod/manage_product', Hod_Views.manage_product,name='manage-product'),
    path('Hod/manage_product/<int:pk>', Hod_Views.manage_product,name='manage-product-pk'),
    path('Hod/view_product', Hod_Views.view_product,name='view-product'),
    path('Hod/view_product/<int:pk>', Hod_Views.view_product,name='view-product-pk'),
    path('Hod/save_product', Hod_Views.save_product,name='save-product'),
    path('Hod/delete_product/<int:pk>', Hod_Views.delete_product,name='delete-product'),
    
    #invoices
    path('Hod/invoices', Hod_Views.invoices,name='invoice-page'),
    path('Hod/manage_invoice', Hod_Views.manage_invoice,name='manage-invoice'), 
    path('Hod/manage_invoice/<int:pk>', Hod_Views.manage_invoice,name='manage-invoice-pk'),
    path('Hod/view_invoice', Hod_Views.view_invoice,name='view-invoice'),
    path('Hod/view_invoice/<int:pk>', Hod_Views.view_invoice,name='view-invoice-pk'),
    path('Hod/save_invoice', Hod_Views.save_invoice,name='save-invoice'),
    path('Hod/delete_invoice/<int:pk>', Hod_Views.delete_invoice,name='delete-invoice'),
    path('Hod/update_form/<int:pk>', Hod_Views.update_form_position,name='update-position'),
    path('Hod/update_position', Hod_Views.update_position,name='update-invoice-position'),
    path('Hod/daily_report', Hod_Views.daily_report,name='daily-report'),
    path('Hod/daily_report/<str:date>', Hod_Views.daily_report,name='daily-report-date'),

    #employee invoices
    path('Hod/bills', Hod_Views.bills,name='bill-page'),
    path('Hod/manage_bill', Hod_Views.manage_bill,name='manage-bill'), 
    path('Hod/manage_bill/<int:pk>', Hod_Views.manage_bill,name='manage-bill-pk'),
    path('Hod/view_bill', Hod_Views.view_bill, name='view-bill'),
    path('Hod/view_bill/<int:pk>', Hod_Views.view_bill, name='view-bill-pk'),
    path('Hod/save_bill', Hod_Views.save_bill, name='save-bill'),
    path('Hod/delete_bill/<int:pk>', Hod_Views.delete_bill,name='delete-bill'),
    path('Hod/update_transaction_form/<int:pk>', Hod_Views.update_transaction_form_bill,name='transaction-update-status'),
    path('Hod/update_transaction_status', Hod_Views.update_transaction_status,name='update-bill-status'),

    #product report from client
    path('Hod/product_report', Hod_Views.product_report,name='product-report'),
    path('Hod/product_report/<str:date>', Hod_Views.product_report,name='product-report-date'),
    path('Hod/report-sort/', Hod_Views.report_page_sort,name="report_page_sort"),
    #product report from employee
    path('Hod/employee_report_product', Hod_Views.employee_report_product,name='employee-report-product'),
    path('Hod/employee_report_product/<str:date>', Hod_Views.employee_report_product,name='employee-report-product-date'),

    #Expenses
    path('Hod/Expense/Add', Hod_Views.ADD_EXPENSE, name="add_expense"),
    path('Hod/Expense/View', Hod_Views.VIEW_EXPENSE, name="view_expense"),
    path('Hod/Expense/Edit/<str:id>', Hod_Views.EDIT_EXPENSE, name="edit_expense"),
    path('Hod/Expense/Update', Hod_Views.UPDATE_EXPENSE, name="update_expense"),
    path('Hod/Expense/Delete/<str:id>', Hod_Views.DELETE_EXPENSE, name="delete_expense"),


    # Employee urls
    path('Employee/Home', Employee_Views.HOME, name="employee_home"),
    #Client
    path('Employee/Client/Add', Employee_Views.ADD_CLIENT, name="add_client"),
    path('Employee/Client/View', Employee_Views.VIEW_CLIENT, name="view_client"),
    path('Employee/Client/Edit/<str:id>', Employee_Views.EDIT_CLIENT, name="edit_client"),
    path('Employee/Client/Update', Employee_Views.UPDATE_CLIENT, name="update_client"),
    path('Employee/Client/Delete/<str:id>', Employee_Views.DELETE_CLIENT, name="delete_client"),
    #Products
    path('Employee/products_employee', Employee_Views.products_employee,name='product-employee-page'),
    path('Employee/manage_employee_product', Employee_Views.manage_employee_product,name='manage-employee-product'),
    path('Employee/manage_employee_product/<int:pk>', Employee_Views.manage_employee_product,name='manage-employee-product-pk'),
    path('Employee/view_employee_product/<int:pk>', Employee_Views.view_employee_product,name='view-employee-product-pk'),
    path('Employee/save_employee_product', Employee_Views.save_employee_product,name='save-employee-product'),
    path('Employee/delete_employee_product/<int:pk>', Employee_Views.delete_employee_product,name='delete-employee-product'),
    #Purchases
    path('Employee/purchases', Employee_Views.purchases,name='purchase-page'),
    path('Employee/manage_purchase', Employee_Views.manage_purchase,name='manage-purchase'), 
    path('Employee/manage_purchase/<int:pk>', Employee_Views.manage_purchase,name='manage-purchase-pk'),
    path('Employee/view_purchase', Employee_Views.view_purchase,name='view-purchase'),
    path('Employee/view_purchase/<int:pk>', Employee_Views.view_purchase,name='view-purchase-pk'),
    path('Employee/save_purchase', Employee_Views.save_purchase,name='save-purchase'),
    path('Employee/delete_purchase/<int:pk>', Employee_Views.delete_purchase,name='delete-purchase'),
    path('Employee/update_transaction_form/<int:pk>', Employee_Views.update_state_form,name='transacton-update-regulation'),
    path('Employee/update_transaction_regulation', Employee_Views.update_transaction_regulation,name='update-purchase-regulation'),    
    #Purchases report
    path('Employee/purchase_daily_report', Employee_Views.purchase_daily_report, name='purchase-daily-report'),
    path('Employee/purchase_daily_report/<str:date>', Employee_Views.purchase_daily_report,name='purchase-daily-report-date'),
    #Sales
    path('Employee/sales', Employee_Views.sales,name='sale-page'),
    path('Employee/manage_sale', Employee_Views.manage_sale,name='manage-sale'), 
    path('Employee/manage_sale/<int:pk>', Employee_Views.manage_sale,name='manage-sale-pk'),
    path('Employee/view_sale', Employee_Views.view_sale,name='view-sale'),
    path('Employee/view_sale/<int:pk>', Employee_Views.view_sale,name='view-sale-pk'),
    path('Employee/save_sale', Employee_Views.save_sale,name='save-sale'),
    path('Employee/delete_sale/<int:pk>', Employee_Views.delete_sale,name='delete-sale'),
    path('Employee/update_dealing_form/<int:pk>', Employee_Views.update_dealing_form, name='dealing-update-condition'),
    path('Employee/update_dealing_condition', Employee_Views.update_dealing_condition, name='update-sale-condition'),  

    #Costs
    path('Employee/Cost/Add', Employee_Views.ADD_COST, name="add_cost"),
    path('Employee/Cost/View', Employee_Views.VIEW_COST, name="view_cost"),
    path('Employee/Cost/Edit/<str:id>', Employee_Views.EDIT_COST, name="edit_cost"),
    path('Employee/Cost/Update', Employee_Views.UPDATE_COST, name="update_cost"),
    path('Employee/Cost/Delete/<str:id>', Employee_Views.DELETE_COST, name="delete_cost"),


]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
