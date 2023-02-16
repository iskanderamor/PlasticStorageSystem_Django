import datetime
from django.shortcuts import redirect, render
import json
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from lsmsApp import models, forms
from django.db.models import Q, Sum
from django.db.models.functions import TruncMonth
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta
def context_data(request):
    fullpath = request.get_full_path()
    abs_uri = request.build_absolute_uri()
    abs_uri = abs_uri.split(fullpath)[0]
    context = {
        'system_host' : abs_uri,
        'page_name' : '',
        'page_title' : '',
        'system_name' : 'Plastic Company',
       
        'topbar' : True,
        'footer' : True,
    }

    return context
    
@login_required
def home(request):
    context = context_data(request)
    context['page'] = 'home'
    context['page_title'] = 'Home'
    
    date = datetime.datetime.now()
    year = date.strftime('%Y')
    month = date.strftime('%m')
    day = date.strftime('%d')
    context['employees'] = models.Employee.objects.all().count()
    context['products'] = models.Products.objects.filter(delete_flag = 0).count()
    context['collecteurs'] = models.Collecteur.objects.all().count()
    context['prods'] = models.Products.objects.all()
    context['all_emp'] = models.Employee.objects.all()
    context['todays_invoice'] = models.Invoice.objects.filter(
            date_added__year = year,
            date_added__month = month,
            date_added__day = day,
    ).count()
    context['todays_achat'] = models.Invoice.objects.filter(
            date_added__year = year,
            date_added__month = month,
            date_added__day = day,
    ).aggregate(Sum('amount_paid'))['amount_paid__sum']

    context['tot_amount'] = None
    if context['todays_achat'] is not None:
        context['tot_amount'] = int(context['todays_achat'])
    else:
        context['tot_amount']=0

    #All products 

    filter_context = {}
    base_url = f''
    date_start_html = ''
    date_end_html = ''
    product_name_list = []
    product_total_list = []
    tot_product=None  
    products = models.Products.objects.all()

    try:
        if 'date_start' in request.GET and request.GET['date_start'] != '':
            date_start = datetime.datetime.strptime(request.GET['date_start'],'%Y-%m-%d')
            filter_context['date_start'] = request.GET['date_start']
            date_start_html = request.GET['date_start']
        
            if 'date_end' in request.GET and request.GET['date_end'] != '':

                date_end = datetime.datetime.strptime(request.GET['date_end'],'%Y-%m-%d')
                filter_context['date_end'] = request.GET['date_end']
                date_end_html = request.GET['date_end']
                for product in products:
                    invoices = models.InvoiceProducts.objects.filter(
                        Q(date_added__gte = date_start)
                        &
                        Q(date_added__lte = date_end),
                        product_type = product.id,
                    ).order_by('-date_added').aggregate(Sum('weight'))['weight__sum']

                    bills = models.BillProducts.objects.filter(
                        Q(date_added__gte = date_start)
                        &
                        Q(date_added__lte = date_end),
                        product_type = product.id,
                    ).order_by('-date_added').aggregate(Sum('weight'))['weight__sum']
                    if invoices and bills is not None:
                        tot_product = invoices + bills
                    elif invoices is not None:
                        tot_product = invoices
                    elif bills is not None:
                        tot_product = bills
                    else:
                        tot_product = 0           

                    product_name_list.append(product.product_type)
                    product_total_list.append(tot_product)    
                
            else:
                for product in products:
                    invoices = models.InvoiceProducts.objects.filter(
                        date_added__gte = date_start,
                        product_type = product.id,
                    ).order_by('-date_added').aggregate(Sum('weight'))['weight__sum']
                    bills = models.BillProducts.objects.filter(
                        date_added__gte = date_start,
                        product_type = product.id,
                    ).order_by('-date_added').aggregate(Sum('weight'))['weight__sum']
                    if invoices and bills is not None:
                        tot_product = invoices + bills
                    elif invoices is not None:
                        tot_product = invoices
                    elif bills is not None:
                        tot_product = bills
                    else:
                        tot_product = 0           

                    product_name_list.append(product.product_type)
                    product_total_list.append(tot_product)               

        elif 'date_end' in request.GET and request.GET['date_end'] != '':

            date_end_html = request.GET['date_end']
            date_end = datetime.datetime.strptime(request.GET['date_end'],'%Y-%m-%d')
            filter_context['date_start'] = request.GET['date_end']
            for product in products:

                invoices = models.InvoiceProducts.objects.filter(
                    date_added__lte = date_end,
                    product_type = product.id,
                ).order_by('-date_added').aggregate(Sum('weight'))['weight__sum']

                bills = models.BillProducts.objects.filter(
                    date_added__lte = date_end,
                    product_type = product.id,
                ).order_by('-date_added').aggregate(Sum('weight'))['weight__sum']
                if invoices and bills is not None:
                    tot_product = invoices + bills
                elif invoices is not None:
                    tot_product = invoices
                elif bills is not None:
                    tot_product = bills
                else:
                    tot_product = 0           

                product_name_list.append(product.product_type)
                product_total_list.append(tot_product)
        else:
            for product in products:
                invoices = models.InvoiceProducts.objects.filter(
                    product_type = product.id,
                ).aggregate(Sum('weight'))['weight__sum']
                bills = models.BillProducts.objects.filter(
                    product_type = product.id,
                ).aggregate(Sum('weight'))['weight__sum']
                if invoices and bills is not None:
                    tot_product = invoices + bills
                elif invoices is not None:
                    tot_product = invoices
                elif bills is not None:
                    tot_product = bills
                else:
                    tot_product = 0           

                product_name_list.append(product.product_type)
                product_total_list.append(tot_product)

    except:
        messages.error(request,'Something went wrong')
        return redirect('hod_home')
    
    base_url = f'?date_start={date_start_html}&date_end={date_end_html}&'
    context['filter_context'] = filter_context
    context['base_url'] = base_url
    context['product_name_list'] = product_name_list
    context['product_total_list'] = product_total_list


    #Daily Expences
    #rest
    #month report
    employee_name_list = []
    employee_expenses_list = []
    employee_rest_list = []
    employee_month_report_list = []
    rest = None
    employees = models.Employee.objects.all()
    for employee in employees:        
        expenses = models.Expenses.objects.filter(
            employee=employee.id,
        ).aggregate(Sum('amount'))['amount__sum']

        expenses_daily = models.Expenses.objects.filter(
            employee=employee.id,
            date_added__year = year,
            date_added__month = month,
            date_added__day = day,
        ).aggregate(Sum('amount'))['amount__sum']

        sales = models.Sales.objects.filter(
            employee_id = employee.id,
        ).aggregate(Sum('amount_paid'))['amount_paid__sum']

        purchases = models.Purchase.objects.filter(
            employee_id =employee.id,
        ).aggregate(Sum('amount_paid'))['amount_paid__sum'] 

        costs = models.Costs.objects.filter(
            employee_id = employee.id,
        ).aggregate(Sum('amount'))['amount__sum']

        month_report = models.Expenses.objects.filter(
            employee=employee.id,
        ).annotate(month=TruncMonth('date_added')).values('month').aggregate(Sum('amount'))['amount__sum']
        if expenses and purchases and costs and sales is not None:
            rest = (expenses + sales) - (purchases + costs)
        elif expenses and purchases and costs is not None:
            rest = expenses - (purchases + costs) 
        elif expenses and purchases and sales is not None:
            rest = (expenses + sales) - purchases 
        elif expenses and costs and sales is not None:
            rest = (expenses + sales) - costs         
        elif expenses and purchases is not None:
            rest = expenses - purchases
        elif expenses and costs is not None:
            rest = expenses - costs
        elif sales and purchases is not None:
            rest = sales - purchases
        elif sales and costs is not None:
            rest = sales - costs            
        elif expenses is not None:
            rest = expenses
        else:
            rest = 0    
        employee_name_list.append(employee.admin.username)
        employee_expenses_list.append(expenses_daily)
        employee_rest_list.append(rest)
        employee_month_report_list.append(month_report)
    context['employee_name_list'] = employee_name_list
    context['employee_expenses_list'] =  employee_expenses_list   
    context['employee_rest_list'] = employee_rest_list
    context['employee_month_report_list'] = employee_month_report_list       
      
    return render(request, 'Hod/hod_home.html', context)



def ADD_EMPLOYEE(request):
    if request.method == 'POST':
        
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')

        if models.CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'Email Is Already Taken')
            return redirect('add_employee')

        gender = request.POST.get('gender')
        if models.CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'Username Is Already Taken')
            return redirect('add_employee')    

        else:
            user = models.CustomUser(
                first_name = first_name,
                last_name = last_name,
                email = email,
                username=username,
               
                user_type = 2,

            )
            user.set_password(password)
            user.save()

            employee = models.Employee(
                admin=user,
                address = address,
                gender = gender,
            )
            employee.save()
            messages.success(request, 'تمت إضافة المزوّد بنجاح')
            return redirect('view_employee')

    
    return redirect('view_employee')


def VIEW_EMPLOYEE(request):
    
    employee = models.Employee.objects.all()

    context = {
        'employee': employee,
    }
    return render(request, 'Hod/view_employee.html', context)


def EDIT_EMPLOYEE(request, id):
    employee = models.Employee.objects.get(id=id)
    
    context = {
        'employee': employee,
    }

    return render(request, 'Hod/edit_employee.html', context)


def UPDATE_EMPLOYEE(request):
    
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')

        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')

        user = models.CustomUser.objects.get(id=employee_id)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username

        if password != None and password != "":
            user.set_password(password)
        if profile_pic != None and profile_pic != "":
            user.profile_pic = profile_pic    
        user.save()

        employee = models.Employee.objects.get(admin=employee_id)
        employee.address = address
        employee.gender = gender
        employee.save()
        messages.success(request, 'تم تحديث المزوّد بنجاح')
        return redirect('view_employee')


    return render(request, 'Hod/edit_employee.html')


def DELETE_EMPLOYEE(request, admin):
    
    employee = models.Employee.objects.get(id=admin)
    employee.delete()
    messages.success(request, 'تم حذف المزوّد بنجاح')
   
    return redirect('view_employee')

def ADD_COLLECTEUR(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        collecteur = models.Collecteur(
            name = name,
            phone = phone,
            address = address,
        )
        collecteur.save()
        messages.success(request, 'تم إضافة الزبون بنجاح')
        return redirect('view_collecteur')
    return render(request, 'Hod/add_collecteur.html')

def VIEW_COLLECTEUR(request):
    collecteur = models.Collecteur.objects.all()

    context = {
        'collecteur': collecteur,
    }
    return render(request, 'Hod/view_collecteur.html', context)

def EDIT_COLLECTEUR(request, id):
    collecteur = models.Collecteur.objects.get(id=id)

    context = {
        'collecteur': collecteur,
    }
    return render(request, 'Hod/edit_collecteur.html', context)

def UPDATE_COLLECTEUR(request):
    if request.method == 'POST':
        collecteur_id = request.POST.get('collecteur_id')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        collecteur = models.Collecteur(
            id = collecteur_id,
            name = name,
            phone = phone,
            address = address,
        )
        collecteur.save()
        messages.success(request, 'تم تحديث الزبون بنجاح')
        return redirect('view_collecteur')

    return render(request, 'Hod/edit_collecteur.html')    

def DELETE_COLLECTEUR(request, id):
    collecteur = models.Collecteur.objects.get(id=id)
    collecteur.delete()
    messages.success(request, 'تم حذف الزبون بنجاح')
    return redirect('view_collecteur')

@login_required
def products(request):
    context = context_data(request)
    context['page'] = 'Product'
    context['page_title'] = "Product List"
    context['products'] = models.Products.objects.filter(delete_flag = 0).all()
    return render(request, 'Hod/products.html', context)

@login_required
def save_product(request):
    resp = { 'status': 'failed', 'msg' : '', 'id': '' }
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            product = models.Products.objects.get(id = post['id'])
            form = forms.SaveProducts(request.POST, instance=product)
        else:
            form = forms.SaveProducts(request.POST) 

        if form.is_valid():
            form.save()
            if post['id'] == '':
                messages.success(request, ".تم تسجيل السّلعة بنجاح") 
                pid = models.Products.objects.last().id
                resp['id'] = pid               
            else:
                messages.success(request, ".تم تحديث السّلعة بنجاح")
                resp['id'] = post['id']
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br/>')
                    resp['msg'] += str(f'[{field.name}] {error}')
    else:
         resp['msg'] = "لا توجد بيانات مرسلة على الطلب"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def view_product(request, pk = None):
    context = context_data(request)
    context['page'] = 'view_product'
    context['page_title'] = 'View Product'
    if pk is None:
        context['product'] = {}        
    else:
        context['product'] = models.Products.objects.get(id=pk)
       
    
    return render(request, 'Hod/view_product.html', context)

@login_required
def manage_product(request, pk = None):
    context = context_data(request)
    context['page'] = 'manage_product'
    context['page_title'] = 'Manage product'
    if pk is None:
        context['product'] = {}
    else:
        context['product'] = models.Products.objects.get(id=pk)
    
    return render(request, 'Hod/manage_product.html', context)

@login_required
def delete_product(request, pk = None):
    resp = { 'status' : 'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'Product ID is invalid'
    else:
        try:
            models.Products.objects.filter(pk = pk).update(delete_flag = 1)
            messages.success(request, ".تم حذف السّلعة بنجاح")
            resp['status'] = 'success'
        except:
            resp['msg'] = "فشل حذف السّلعة"

    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def invoices(request):
    context = context_data(request)
    context['page'] = 'invoice'
    context['page_title'] = "invoice List"
    context['invoices'] = models.Invoice.objects.order_by('-date_added').all()
    context['collecteurs'] = models.Collecteur.objects.all()
    return render(request, 'Hod/invoices.html', context)

@login_required
def save_invoice(request):
    resp = { 'status': 'failed', 'msg' : '', 'id': '' }
    if request.method == 'POST':
        post = request.POST 
        if not post['id'] == '':
            invoice = models.Invoice.objects.get(id = post['id'])
            form = forms.SaveInvoice(request.POST, instance=invoice)
        else:
            form = forms.SaveInvoice(request.POST) 
        if form.is_valid():
            form.save()
            if post['id'] == '':
                messages.success(request, ".تم حفظ الفاتورة بنجاح")
                pid = models.Invoice.objects.last().id
                resp['id'] = pid
            else:
                messages.success(request, ".تم تحديث الفاتورة بنجاح")
                resp['id'] = post['id']
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br/>')
                    resp['msg'] += str(f'[{field.name}] {error}')
    else:
         resp['msg'] = "لا توجد بيانات مرسلة على الطلب"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def view_invoice(request, pk = None):
    context = context_data(request)
    context['page'] = 'view_invoice'
    context['page_title'] = 'View Invoice'
    context['collecteurs'] = models.Collecteur.objects.all()
    if pk is None:
        context['invoice'] = {}
        context['pitems'] = {}
    else:
        context['invoice'] = models.Invoice.objects.get(id=pk)
        context['pitems'] = models.InvoiceProducts.objects.filter(invoice__id = pk).all()
    
    return render(request, 'Hod/view_invoice.html', context)

@login_required
def manage_invoice(request, pk = None):
    context = context_data(request)
    context['page'] = 'manage_invoice'
    context['page_title'] = 'Manage invoice'
    context['products'] = models.Products.objects.filter(delete_flag = 0, status = 1).all()
    context['collecteurs'] = models.Collecteur.objects.all()
    if pk is None:
        context['invoice'] = {}
        context['pitems'] = {}
    else:
        context['invoice'] = models.Invoice.objects.get(id=pk)
        context['pitems'] = models.InvoiceProducts.objects.filter(invoice__id = pk).all()
    
    return render(request, 'Hod/manage_invoice.html', context)

@login_required
def update_form_position(request, pk = None):
    context = context_data(request)
    context['page'] = 'update_invoice'
    context['page_title'] = 'Update Transaction'
    if pk is None:
        context['invoice'] = {}
    else:
        context['invoice'] = models.Invoice.objects.get(id=pk)
    
    return render(request, 'Hod/update_position.html', context)

@login_required
def update_position(request):
    resp = { 'status' : 'failed', 'msg':''}
    if request.POST['id'] is None:
        resp['msg'] = 'Transaction ID is invalid'
    else:
        try:
            models.Invoice.objects.filter(pk = request.POST['id']).update(position = request.POST['position'])
            messages.success(request, ".تم تحديث حالة الفاتورة بنجاح")
            resp['status'] = 'success'
        except:
            resp['msg'] = "فشل حذف الفاتورة"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def delete_invoice(request, pk = None):
    resp = { 'status' : 'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'Invoice ID is invalid'
    else:
        try:
            models.Invoice.objects.filter(pk = pk).delete()
            messages.success(request, ".تم حذف الفاتورة بنجاح")
            resp['status'] = 'success'
        except:
            resp['msg'] = "فشل حذف الفاتورة"

    return HttpResponse(json.dumps(resp), content_type="application/json")

#employee invoice

@login_required
def bills(request):
    context = context_data(request)
    context['page'] = 'invoice'
    context['page_title'] = "invoice List"
    context['bills'] = models.Bill.objects.order_by('-date_added').all()
    context['employees'] = models.Employee.objects.all()
    return render(request, 'Hod/bills.html', context)

@login_required
def save_bill(request):
    resp = { 'status': 'failed', 'msg' : '', 'id': '' }
    if request.method == 'POST':
        post = request.POST 
        if not post['id'] == '':
            bill = models.Bill.objects.get(id = post['id'])
            form = forms.SaveBill(request.POST, instance=bill)
        else:
            form = forms.SaveBill(request.POST)
            
        if form.is_valid():
            form.save()
            if post['id'] == '':
                messages.success(request, ".تم حفظ الفاتورة بنجاح")
                pid = models.Bill.objects.last().id
                resp['id'] = pid
            else:
                messages.success(request, ".تم تحديث الفاتورة بنجاح")
                resp['id'] = post['id']
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br/>')
                    resp['msg'] += str(f'[{field.name}] {error}')
    else:
         resp['msg'] = "لا توجد بيانات مرسلة على الطلب"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def view_bill(request, pk = None):
    context = context_data(request)
    context['page'] = 'view_invoice'
    context['page_title'] = 'View Invoice'
    context['employees'] = models.Employee.objects.all()
    if pk is None:
        context['bill'] = {}
        context['pitems'] = {}
        
    else:
        context['bill'] = models.Bill.objects.get(id=pk)
        context['pitems'] = models.BillProducts.objects.filter(bill__id = pk).all()
        
    
    return render(request, 'Hod/view_bill.html', context)

@login_required
def manage_bill(request, pk = None):
    context = context_data(request)
    context['page'] = 'manage_invoice'
    context['page_title'] = 'Manage invoice'
    context['products'] = models.Products.objects.filter(delete_flag = 0, status = 1).all()
    context['employees'] = models.Employee.objects.all()
    if pk is None:
        context['bill'] = {}
        context['pitems'] = {}
        
    else:
        context['bill'] = models.Bill.objects.get(id=pk)
        context['pitems'] = models.BillProducts.objects.filter(bill__id = pk).all()
        

    return render(request, 'Hod/manage_bill.html', context)

@login_required
def update_transaction_form_bill(request, pk = None):
    context = context_data(request)
    context['page'] = 'update_invoice'
    context['page_title'] = 'Update Transaction'
    if pk is None:
        context['bill'] = {}
    else:
        context['bill'] = models.Bill.objects.get(id=pk)
    
    return render(request, 'Hod/bill_status.html', context)

@login_required
def update_transaction_status(request):
    resp = { 'status' : 'failed', 'msg':''}
    if request.POST['id'] is None:
        resp['msg'] = 'Transaction ID is invalid'
    else:
        try:
            models.Bill.objects.filter(pk = request.POST['id']).update(status = request.POST['status'])
            messages.success(request, ".تم تحديث حالة الفاتورة بنجاح")
            resp['status'] = 'success'
        except:
            resp['msg'] = "فشل حذف الفاتورة"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def delete_bill(request, pk = None):
    resp = { 'status' : 'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'Invoice ID is invalid'
    else:
        try:
            models.Bill.objects.filter(pk = pk).delete()
            messages.success(request, ".تم حذف الفاتورة بنجاح")
            resp['status'] = 'success'
        except:
            resp['msg'] = "فشل حذف الفاتورة"

    return HttpResponse(json.dumps(resp), content_type="application/json")

def ADD_EXPENSE(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        amount = request.POST.get('amount')
        employee = models.Employee.objects.get(id=employee_id)
        
        expense = models.Expenses(
            employee = employee,
            amount = amount,                            
        )
        
        expense.save()
        messages.success(request, 'تمت إضافة التمويل بنجاح')
        return redirect('view_expense')
    return render(request, 'Hod/add_expense.html')

def VIEW_EXPENSE(request):
    expense = models.Expenses.objects.all()
    employee = models.Employee.objects.all()
    context = {
        'expense': expense,
        'employee': employee,
    }
    return render(request, 'Hod/view_expense.html', context)

def EDIT_EXPENSE(request, id):
    expense = models.Expenses.objects.get(id=id)
    employee = models.Employee.objects.all()
    context = {
        'expense': expense,
        'employee': employee,
    }   
    return render(request, 'Hod/edit_expense.html', context)

def UPDATE_EXPENSE(request):
    if request.method == 'POST':
        expense_id = request.POST.get('expense_id')
        amount = request.POST.get('amount')
        employee_id = request.POST.get('employee_id')
        employee = models.Employee.objects.get(id=employee_id)    
        expense = models.Expenses(
            id = expense_id,
            employee = employee,
            amount = amount,
        )
        expense.save()
        messages.success(request, 'تم تحديث التمويل بنجاح')
        return redirect('view_expense')

def DELETE_EXPENSE(request, id):
    expense = models.Expenses.objects.get(id=id)
    expense.delete()
    messages.success(request, 'تم حذف التمويل بنجاح')
    return redirect('view_expense')

@login_required
def daily_report(request, date = None):
    context = context_data(request)
    context['page'] = 'view_invoice'
    context['page_title'] = 'تقرير الشراءات اليومية'
    
    if date is None:
        date = datetime.datetime.now()
        year = date.strftime('%Y')
        month = date.strftime('%m')
        day = date.strftime('%d')
    else:
        date =datetime.datetime.strptime(date, '%Y-%m-%d')
        year = date.strftime('%Y')
        month = date.strftime('%m')
        day = date.strftime('%d')

    context['date'] = date
    context['invoices'] = models.Invoice.objects.filter(
            date_added__year = year,
            date_added__month = month,
            date_added__day = day,
        )   
    grand_total = 0
    for invoice in context['invoices']:
        grand_total += float(invoice.total_amount)
    context['grand_total'] = grand_total
    
    return render(request, 'Hod/report.html', context)

@login_required
def product_report(request, date = None):
    context = context_data(request)
    context['page'] = 'view_invoice'
    context['page_title'] = 'تقرير السّلع اليومية'

    filter_context = {}
    base_url = f''
    date_from_html = ''
    date_to_html = ''
    total_weight=0
    invoices = models.InvoiceProducts.objects.order_by('-date_added').all()
    try:
        if 'date_from' in request.GET and request.GET['date_from'] != '':
            date_from = datetime.datetime.strptime(request.GET['date_from'],'%Y-%m-%d')
            filter_context['date_from'] = request.GET['date_from']
            date_from_html = request.GET['date_from']
        
            if 'date_to' in request.GET and request.GET['date_to'] != '':

                date_to = datetime.datetime.strptime(request.GET['date_to'],'%Y-%m-%d')
                filter_context['date_to'] = request.GET['date_to']
                date_to_html = request.GET['date_to']
                invoices = models.InvoiceProducts.objects.filter(
                    Q(date_added__gte = date_from )
                    &
                    Q(date_added__lte = date_to)
                ).order_by('-date_added')
                
                for i in invoices:
                    total_weight += float(i.weight) 
            else:
                invoices = models.InvoiceProducts.objects.filter(
                    date_added__gte = date_from
                ).order_by('-date_added')
                for i in invoices:
                    total_weight += float(i.weight)

        elif 'date_to' in request.GET and request.GET['date_to'] != '':

            date_to_html = request.GET['date_to']
            date_to = datetime.datetime.strptime(request.GET['date_to'],'%Y-%m-%d')
            filter_context['date_from'] = request.GET['date_to']
            invoices = models.InvoiceProducts.objects.filter(
                date_added__lte = date_to
            ).order_by('-date_added')
            for i in invoices:
                total_weight += float(i.weight)
    
    except:
        messages.error(request,'Something went wrong')
        return redirect('product-report')
    
    base_url = f'?date_from={date_from_html}&date_to={date_to_html}&'
    context['filter_context'] = filter_context
    context['base_url'] = base_url
    context['invoices'] = invoices
    context['total_weight'] = total_weight
    context['date_from_html'] = date_from_html
    context['date_to_html'] = date_to_html
    return render(request, 'Hod/productreport.html', context)    

def report_page_sort(request):
    base_url = ''
    try:
        if 'weight_sort' in request.GET and request.GET.get('weight_sort'):
            base_url = f'?weight_sort={request.GET.get("weight_sort",2)}&'
            if int(request.GET.get('weight_sort',2)) == 1:
                invoices = models.InvoiceProducts.objects.order_by('-weight')
            elif int(request.GET.get('weight_sort',2)) == 2:
                invoices = models.InvoiceProducts.objects.order_by('weight')
        
        if 'date_added_sort' in request.GET and request.GET.get('date_added_sort'):
            base_url = f'?date_added_sort={request.GET.get("date_added_sort",2)}&'
            if int(request.GET.get('date_added_sort',2)) == 1:
                invoices = models.InvoiceProducts.objects.order_by('-date_added')
            elif int(request.GET.get('date_added_sort',2)) == 2:
                invoices = models.InvoiceProducts.objects.order_by('-date_added')
    except:
        messages.error(request,'Something went wrong')
        return redirect('product-report')
    context['invoices'] = invoices
    context['base_url'] = base_url
    return render(request,'Hod/productreport.html', context)

@login_required
def employee_report_product(request, date = None):
    context = context_data(request)
    context['page'] = 'view_invoice'
    context['page_title'] = 'تقرير السّلع اليومية'

    filter_context = {}
    base_url = f''
    date_from_html = ''
    date_to_html = ''
    product_weight_total=0
    bills = models.BillProducts.objects.order_by('-date_added').all()
    try:
        if 'date_from' in request.GET and request.GET['date_from'] != '':
            date_from = datetime.datetime.strptime(request.GET['date_from'],'%Y-%m-%d')
            filter_context['date_from'] = request.GET['date_from']
            date_from_html = request.GET['date_from']
        
            if 'date_to' in request.GET and request.GET['date_to'] != '':

                date_to = datetime.datetime.strptime(request.GET['date_to'],'%Y-%m-%d')
                filter_context['date_to'] = request.GET['date_to']
                date_to_html = request.GET['date_to']
                bills = models.BillProducts.objects.filter(
                    Q(date_added__gte = date_from )
                    &
                    Q(date_added__lte = date_to)
                ).order_by('-date_added')
                
                for i in bills:
                    product_weight_total += float(i.weight) 
            else:
                bills = models.BillProducts.objects.filter(
                    date_added__gte = date_from
                ).order_by('-date_added')
                for i in bills:
                    product_weight_total += float(i.weight)

        elif 'date_to' in request.GET and request.GET['date_to'] != '':

            date_to_html = request.GET['date_to']
            date_to = datetime.datetime.strptime(request.GET['date_to'],'%Y-%m-%d')
            filter_context['date_from'] = request.GET['date_to']
            bills = models.BillProducts.objects.filter(
                date_added__lte = date_to
            ).order_by('-date_added')
            for i in bills:
                product_weight_total += float(i.weight)
    
    except:
        messages.error(request,'Something went wrong')
        return redirect('employee-report-product')
    
    base_url = f'?date_from={date_from_html}&date_to={date_to_html}&'
    context['filter_context'] = filter_context
    context['base_url'] = base_url
    context['bills'] = bills
    context['product_weight_total'] = product_weight_total
    return render(request, 'Hod/employeereportproduct.html', context)    

