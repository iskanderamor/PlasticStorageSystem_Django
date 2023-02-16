import datetime
from django.shortcuts import redirect, render
import json
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from lsmsApp import models, forms
from django.db.models import Q, Sum
from django.contrib.auth.decorators import login_required

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

@login_required(login_url='/')
def HOME(request):
    context = context_data(request)
    context['page'] = 'home'
    context['page_title'] = 'Home'
    date = datetime.datetime.now()
    year = date.strftime('%Y')
    month = date.strftime('%m')
    day = date.strftime('%d')
    employee_id = models.Employee.objects.get(admin=request.user.id)
    
    context['products'] = models.EmployeeProducts.objects.filter(employee_id=employee_id, delete_flag = 0).count()
    context['clients'] = models.Client.objects.filter(employee_id=employee_id).all().count()
    context['todays_invoice'] = models.Purchase.objects.filter(
            employee_id = employee_id,
            date_added__year = year,
            date_added__month = month,
            date_added__day = day,
    ).count()
    context['todays_purchases'] = models.Purchase.objects.filter(
            employee_id = employee_id,
    ).aggregate(Sum('amount_paid'))['amount_paid__sum']

    context['purchases_today'] = models.Purchase.objects.filter(
            employee_id = employee_id,
            date_added__year = year,
            date_added__month = month,
            date_added__day = day,
    ).aggregate(Sum('amount_paid'))['amount_paid__sum']
    context['tot_purchase'] = None
    if context['purchases_today'] is not None:
        context['tot_purchase'] = int(context['purchases_today'])
    else:
        context['tot_purchase']=0        
    context['costs'] = models.Costs.objects.filter(
        employee_id=employee_id,
        ).aggregate(Sum('amount'))['amount__sum']
    context['costs_today'] = models.Costs.objects.filter(
        employee_id=employee_id,
        date_added__year = year,
        date_added__month = month,
        date_added__day = day,
        ).aggregate(Sum('amount'))['amount__sum']    
    context['tot_cost']=None
    if context['costs_today'] is not None:
        context['tot_cost'] = int(context['costs_today'])
    else:
        context['tot_cost']=0     
    context['expenses'] = models.Expenses.objects.filter(
        employee=employee_id,
        ).aggregate(Sum('amount'))['amount__sum']
    context['expenses_today'] = models.Expenses.objects.filter(
        employee=employee_id,
        date_added__year = year,
        date_added__month = month,
        date_added__day = day,
        ).aggregate(Sum('amount'))['amount__sum']    
    context['tot_expense'] = None
    if context['expenses_today'] is not None:
        context['tot_expense'] = int(context['expenses_today'])
    else:
        context['tot_expense'] = 0    
    context['sales'] = models.Sales.objects.filter(
        employee_id = employee_id,
    ).aggregate(Sum('amount_paid'))['amount_paid__sum']
    context['sales_today'] = models.Sales.objects.filter(
        employee_id = employee_id,
        date_added__year = year,
        date_added__month = month,
        date_added__day = day,
    ).aggregate(Sum('amount_paid'))['amount_paid__sum']
    context['tot_sale'] = None
    if context['sales_today'] is not None:
        context['tot_sale'] = int(context['sales_today'])
    else:
        context['tot_sale']=0 
    context['rest'] = None

    if context['todays_purchases'] and context['costs'] and  context['expenses'] and context['sales'] is not None:
        context['rest'] = (int(context['expenses']) + int(context['sales'])) - (int(context['todays_purchases']) + int(context['costs']))  
    elif context['expenses'] and context['sales'] and context['todays_purchases'] is not None:
        context['rest'] = (int(context['expenses']) + int(context['sales'])) - int(context['todays_purchases'])
    elif context['expenses'] and context['sales'] and context['costs'] is not None:
        context['rest'] = (int(context['expenses']) + int(context['sales'])) - int(context['costs'])
    elif context['expenses'] and context['todays_purchases'] and context['costs'] is not None:
        context['rest'] = int(context['expenses']) - (int(context['todays_purchases']) + int(context['costs']))
    elif context['expenses'] and context['sales'] is not None:
        context['rest'] = int(context['expenses']) + int(context['sales'])
    elif context['expenses'] and context['todays_purchases'] is not None:
        context['rest'] = int(context['expenses']) - int(context['todays_purchases'])
    elif context['expenses'] and context['costs'] is not None:
        context['rest'] = int(context['expenses']) - int(context['costs'])
    elif context['sales'] and context['todays_purchases'] is not None:
        context['rest'] = int(context['sales']) - int(context['todays_purchases'])
    elif context['sales'] and context['costs'] is not None:
        context['rest'] = int(context['sales']) - int(context['costs'])
    elif context['todays_purchases'] and context['costs'] is not None:
        context['rest'] = int(context['todays_purchases']) + int(context['costs'])
    elif context['expenses'] is not None:
        context['rest'] = int(context['expenses'])
    elif context['sales'] is not None:
        context['rest'] = int(context['sales'])              
    else:
        context['rest']=0

    #Products
    
    context['products_type'] = models.Products.objects.all()
    #bessim products
    #All Products
    context['carduna'] = None
    context['carduna_company'] = models.BillProducts.objects.filter(
        bill__employee= employee_id,
        product_type__product_type = 'كردونة',
    ).aggregate(Sum('weight'))['weight__sum']    
    context['carduna_purchase'] = models.PurchaseProducts.objects.filter(
        purchase__employee_id=employee_id,        
        product_type__product_type='كردونة',
        ).aggregate(Sum('weight'))['weight__sum']
    context['carduna_sale'] = models.SalesProducts.objects.filter(
        sale__employee_id=employee_id,        
        product_type__product_type='كردونة',
        ).aggregate(Sum('weight'))['weight__sum'] 
    if context['carduna_purchase'] and context['carduna_company'] and context['carduna_sale'] is not None:
        context['carduna'] = int(context['carduna_purchase']) - (int(context['carduna_company']) + int(context['carduna_sale']))
    elif context['carduna_purchase'] and context['carduna_company'] is not None:
        context['carduna'] = int(context['carduna_purchase']) - int(context['carduna_company'])
    elif context['carduna_purchase'] and context['carduna_sale'] is not None:
        context['carduna'] = int(context['carduna_purchase']) - int(context['carduna_sale'])    
    elif context['carduna_purchase'] is not None:
        context['carduna'] = int(context['carduna_purchase'])
    else:
        context['carduna']=0  
       
    context['dabouza'] = None
    context['dabouza_company'] = models.BillProducts.objects.filter(
        bill__employee= employee_id,
        product_type__product_type = 'دبوزة',
    ).aggregate(Sum('weight'))['weight__sum']    
    context['dabouza_purchase'] = models.PurchaseProducts.objects.filter(
        purchase__employee_id=employee_id,        
        product_type__product_type='دبوزة',
        ).aggregate(Sum('weight'))['weight__sum']
    context['dabouza_sale'] = models.SalesProducts.objects.filter(
        sale__employee_id=employee_id,        
        product_type__product_type='كردونة',
        ).aggregate(Sum('weight'))['weight__sum']    
    if context['dabouza_purchase'] and context['dabouza_company'] and context['dabouza_sale'] is not None:
        context['dabouza'] = int(context['dabouza_purchase']) - (int(context['dabouza_company']) + int(context['dabouza_sale']))    
    elif context['dabouza_purchase'] and context['dabouza_company'] is not None:
        context['dabouza'] = int(context['dabouza_purchase']) - int(context['dabouza_company'])
    elif context['dabouza_purchase'] and context['dabouza_sale'] is not None:
        context['dabouza'] = int(context['dabouza_purchase']) - int(context['dabouza_sale'])    
    elif context['dabouza_purchase'] is not None:
        context['dabouza'] = int(context['dabouza_purchase'])
    else:
        context['dabouza']=0 

    context['bidoun'] = None
    context['bidoun_company'] = models.BillProducts.objects.filter(
        bill__employee= employee_id,
        product_type__product_type = 'بيدون أصفر',
    ).aggregate(Sum('weight'))['weight__sum']    
    context['bidoun_purchase'] = models.PurchaseProducts.objects.filter(
        purchase__employee_id=employee_id,        
        product_type__product_type='بيدون أصفر',
        ).aggregate(Sum('weight'))['weight__sum']
    context['bidoun_sale'] = models.SalesProducts.objects.filter(
        sale__employee_id=employee_id,        
        product_type__product_type='بيدون أصفر',
        ).aggregate(Sum('weight'))['weight__sum']  
    if context['bidoun_purchase'] and context['bidoun_company'] and context['bidoun_sale'] is not None:
        context['bidoun'] = int(context['bidoun_purchase']) - (int(context['bidoun_company']) + int(context['bidoun_sale']))
    elif context['bidoun_purchase'] and context['bidoun_company'] is not None:
        context['bidoun'] = int(context['bidoun_purchase']) - int(context['bidoun_company'])
    elif context['bidoun_purchase'] and context['bidoun_sale'] is not None:
        context['bidoun'] = int(context['bidoun_purchase']) - int(context['bidoun_sale'])    
    elif context['bidoun_purchase'] is not None:
        context['bidoun'] = int(context['bidoun_purchase'])
    else:
        context['bidoun']=0 

    context['maoun'] = None
    context['maoun_company'] = models.BillProducts.objects.filter(
        bill__employee= employee_id,
        product_type__product_type = 'ماعون',
    ).aggregate(Sum('weight'))['weight__sum']    
    context['maoun_purchase'] = models.PurchaseProducts.objects.filter(
        purchase__employee_id=employee_id,        
        product_type__product_type='ماعون',
        ).aggregate(Sum('weight'))['weight__sum']
    context['maoun_sale'] = models.SalesProducts.objects.filter(
        sale__employee_id=employee_id,        
        product_type__product_type='ماعون',
        ).aggregate(Sum('weight'))['weight__sum'] 
    if context['maoun_purchase'] and context['maoun_company'] and context['maoun_sale'] is not None:
        context['maoun'] = int(context['maoun_purchase']) - (int(context['maoun_company']) + context['maoun_sale'])       
    elif context['maoun_purchase'] and context['maoun_company'] is not None:
        context['maoun'] = int(context['maoun_purchase']) - int(context['maoun_company'])
    elif context['maoun_purchase'] and context['maoun_sale'] is not None:
        context['maoun'] = int(context['maoun_purchase']) - int(context['maoun_sale'])    
    elif context['maoun_purchase'] is not None:
        context['maoun'] = int(context['maoun_purchase'])
    else:
        context['maoun']=0    

    context['kopogajo'] = None
    context['kopogajo_company'] = models.BillProducts.objects.filter(
        bill__employee= employee_id,
        product_type__product_type = 'كوبو+ڨاجو',
    ).aggregate(Sum('weight'))['weight__sum']    
    context['kopogajo_purchase'] = models.PurchaseProducts.objects.filter(
        purchase__employee_id=employee_id,        
        product_type__product_type='كوبو+ڨاجو',
        ).aggregate(Sum('weight'))['weight__sum']
    context['kopogajo_sale'] = models.SalesProducts.objects.filter(
        sale__employee_id=employee_id,        
        product_type__product_type='كوبو+ڨاجو',
        ).aggregate(Sum('weight'))['weight__sum']
    if context['kopogajo_purchase'] and context['kopogajo_company'] and context['kopogajo_sale'] is not None:
        context['kopogajo'] = int(context['kopogajo_purchase']) - (int(context['kopogajo_company']) + int(context['kopogajo_sale']))
    elif context['kopogajo_purchase'] and context['kopogajo_company'] is not None:
        context['kopogajo'] = int(context['kopogajo_purchase']) - int(context['kopogajo_company'])
    elif context['kopogajo_purchase'] and context['kopogajo_sale'] is not None:
        context['kopogajo'] = int(context['kopogajo_purchase']) - int(context['kopogajo_sale'])
    elif context['kopogajo_purchase'] is not None:
        context['kopogajo'] = int(context['kopogajo_purchase'])
    else:
        context['kopogajo']=0     

    context['kopo'] = None
    context['kopo_company'] = models.BillProducts.objects.filter(
        bill__employee= employee_id,
        product_type__product_type = 'كوبو',
    ).aggregate(Sum('weight'))['weight__sum']    
    context['kopo_purchase'] = models.PurchaseProducts.objects.filter(
        purchase__employee_id=employee_id,        
        product_type__product_type='كوبو',
        ).aggregate(Sum('weight'))['weight__sum']
    context['kopo_sale'] = models.SalesProducts.objects.filter(
        sale__employee_id=employee_id,        
        product_type__product_type='كوبو',
        ).aggregate(Sum('weight'))['weight__sum']    
    if context['kopo_purchase'] and context['kopo_company'] and context['kopo_sale'] is not None:
        context['kopo'] = int(context['kopo_purchase']) - (int(context['kopo_company']) + int(context['kopo_sale']))
    elif context['kopo_purchase'] and context['kopo_company'] is not None:
        context['kopo'] = int(context['kopo_purchase']) - int(context['kopo_company'])
    elif context['kopo_purchase'] and context['kopo_sale'] is not None:
        context['kopo'] = int(context['kopo_purchase']) - int(context['kopo_sale'])    
    elif context['kopo_purchase'] is not None:
        context['kopo'] = int(context['kopo_purchase'])
    else:
        context['kopo']=0  

    context['gajo'] = None
    context['gajo_company'] = models.BillProducts.objects.filter(
        bill__employee= employee_id,
        product_type__product_type = 'ڨاجو',
    ).aggregate(Sum('weight'))['weight__sum']    
    context['gajo_purchase'] = models.PurchaseProducts.objects.filter(
        purchase__employee_id=employee_id,        
        product_type__product_type='ڨاجو',
        ).aggregate(Sum('weight'))['weight__sum']
    context['gajo_sale'] = models.SalesProducts.objects.filter(
        sale__employee_id=employee_id,        
        product_type__product_type='ڨاجو',
        ).aggregate(Sum('weight'))['weight__sum']
    if context['gajo_purchase'] and context['gajo_company'] and context['gajo_sale'] is not None:
        context['gajo'] = int(context['gajo_purchase']) - (int(context['gajo_company']) + int(context['gajo_sale']))        
    elif context['gajo_purchase'] and context['gajo_company'] is not None:
        context['gajo'] = int(context['gajo_purchase']) - int(context['gajo_company'])
    elif context['gajo_purchase'] and context['gajo_sale'] is not None:
        context['gajo'] = int(context['gajo_purchase']) - int(context['gajo_sale'])    
    elif context['gajo_purchase'] is not None:
        context['gajo'] = int(context['gajo_purchase'])
    else:
        context['gajo']=0 

    context['zitmahroug'] = None
    context['zitmahroug_company'] = models.BillProducts.objects.filter(
        bill__employee= employee_id,
        product_type__product_type = 'زيت محروق',
    ).aggregate(Sum('weight'))['weight__sum']    
    context['zitmahroug_purchase'] = models.PurchaseProducts.objects.filter(
        purchase__employee_id=employee_id,        
        product_type__product_type='زيت محروق',
        ).aggregate(Sum('weight'))['weight__sum']
    context['zitmahroug_sale'] = models.SalesProducts.objects.filter(
        sale__employee_id=employee_id,        
        product_type__product_type='زيت محروق',
        ).aggregate(Sum('weight'))['weight__sum']    
    if context['zitmahroug_purchase'] and context['zitmahroug_company'] and context['zitmahroug_sale'] is not None:
        context['zitmahroug'] = int(context['zitmahroug_purchase']) - (int(context['zitmahroug_company']) + int(context['zitmahroug_sale']))
    elif context['zitmahroug_purchase'] and context['zitmahroug_company'] is not None:
        context['zitmahroug'] = int(context['zitmahroug_purchase']) - int(context['zitmahroug_company'])
    elif context['zitmahroug_purchase'] and context['zitmahroug_sale'] is not None:
        context['zitmahroug'] = int(context['zitmahroug_purchase']) - int(context['zitmahroug_sale'])
    elif context['zitmahroug_purchase'] is not None:
        context['zitmahroug'] = int(context['zitmahroug_purchase'])
    else:
        context['zitmahroug']=0  

    context['bidounzit'] = None
    context['bidounzit_company'] = models.BillProducts.objects.filter(
        bill__employee= employee_id,
        product_type__product_type = 'بيدون زيت',
    ).aggregate(Sum('weight'))['weight__sum']    
    context['bidounzit_purchase'] = models.PurchaseProducts.objects.filter(
        purchase__employee_id=employee_id,        
        product_type__product_type='بيدون زيت',
        ).aggregate(Sum('weight'))['weight__sum']
    context['bidounzit_sale'] = models.SalesProducts.objects.filter(
        sale__employee_id=employee_id,        
        product_type__product_type='بيدون زيت',
        ).aggregate(Sum('weight'))['weight__sum'] 
    if context['bidounzit_purchase'] and context['bidounzit_company'] and context['bidounzit_sale'] is not None:
        context['bidounzit'] = int(context['bidounzit_purchase']) - (int(context['bidounzit_company']) + int(context['bidounzit_sale']))
    elif context['bidounzit_purchase'] and context['bidounzit_company'] is not None:
        context['bidounzit'] = int(context['bidounzit_purchase']) - int(context['bidounzit_company'])
    elif context['bidounzit_purchase'] and context['bidounzit_sale'] is not None:
        context['bidounzit'] = int(context['bidounzit_purchase']) - int(context['bidounzit_sale'])
    elif context['bidounzit_purchase'] is not None:
        context['bidounzit'] = int(context['bidounzit_purchase'])
    else:
        context['bidounzit']=0             

    context['alumunium'] = None
    context['alumunium_company'] = models.BillProducts.objects.filter(
        bill__employee= employee_id,
        product_type__product_type = 'أليمنيوم',
    ).aggregate(Sum('weight'))['weight__sum']    
    context['alumunium_purchase'] = models.PurchaseProducts.objects.filter(
        purchase__employee_id=employee_id,        
        product_type__product_type='أليمنيوم',
        ).aggregate(Sum('weight'))['weight__sum']
    context['alumunium_sale'] = models.SalesProducts.objects.filter(
        sale__employee_id=employee_id,        
        product_type__product_type='أليمنيوم',
        ).aggregate(Sum('weight'))['weight__sum']    
    if context['alumunium_purchase'] and context['alumunium_company'] and context['alumunium_sale'] is not None:
        context['alumunium'] = int(context['alumunium_purchase']) - (int(context['alumunium_company']) + int(context['alumunium_sale']))
    elif context['alumunium_purchase'] and context['alumunium_company'] is not None:
        context['alumunium'] = int(context['alumunium_purchase']) - int(context['alumunium_company'])
    elif context['alumunium_purchase'] and context['alumunium_sale'] is not None:
        context['alumunium'] = int(context['alumunium_purchase']) - int(context['alumunium_sale'])    
    elif context['alumunium_purchase'] is not None:
        context['alumunium'] = int(context['alumunium_purchase'])
    else:
        context['alumunium']=0

    context['rigide'] = None
    context['rigide_company'] = models.BillProducts.objects.filter(
        bill__employee= employee_id,
        product_type__product_type = 'PVC rigide',
    ).aggregate(Sum('weight'))['weight__sum']    
    context['rigide_purchase'] = models.PurchaseProducts.objects.filter(
        purchase__employee_id=employee_id,        
        product_type__product_type='PVC rigide',
        ).aggregate(Sum('weight'))['weight__sum']
    context['rigide_sale'] = models.SalesProducts.objects.filter(
        sale__employee_id=employee_id,        
        product_type__product_type='PVC rigide',
        ).aggregate(Sum('weight'))['weight__sum']    
    if context['rigide_purchase'] and context['rigide_company'] and context['rigide_sale'] is not None:
        context['rigide'] = int(context['rigide_purchase']) - (int(context['rigide_company']) + int(context['rigide_sale']))
    elif context['rigide_purchase'] and context['rigide_company'] is not None:
        context['rigide'] = int(context['rigide_purchase']) - int(context['rigide_company'])
    elif context['rigide_purchase'] and context['rigide_sale'] is not None:
        context['rigide'] = int(context['rigide_purchase']) - int(context['rigide_sale'])    
    elif context['rigide_purchase'] is not None:
        context['rigide'] = int(context['rigide_purchase'])
    else:
        context['rigide']=0

    context['filmw'] = None
    context['filmw_company'] = models.BillProducts.objects.filter(
        bill__employee= employee_id,
        product_type__product_type = 'فيلم أبيض',
    ).aggregate(Sum('weight'))['weight__sum']    
    context['filmw_purchase'] = models.PurchaseProducts.objects.filter(
        purchase__employee_id=employee_id,        
        product_type__product_type='فيلم أبيض',
        ).aggregate(Sum('weight'))['weight__sum']
    context['filmw_sale'] = models.SalesProducts.objects.filter(
        sale__employee_id=employee_id,        
        product_type__product_type='فيلم أبيض',
        ).aggregate(Sum('weight'))['weight__sum']    
    if context['filmw_purchase'] and context['filmw_company'] and  context['filmw_sale'] is not None:
        context['filmw'] = int(context['filmw_purchase']) - (int(context['filmw_company']) + int( context['filmw_sale']))
    elif context['filmw_purchase'] and context['filmw_company'] is not None:
        context['filmw'] = int(context['filmw_purchase']) - int(context['filmw_company'])
    elif context['filmw_purchase'] and context['filmw_sale'] is not None:
        context['filmw'] = int(context['filmw_purchase']) - int(context['filmw_sale'])    
    elif context['filmw_purchase'] is not None:
        context['filmw'] = int(context['filmw_purchase'])
    else:
        context['filmw']=0

    context['filmb'] = None
    context['filmb_company'] = models.BillProducts.objects.filter(
        bill__employee= employee_id,
        product_type__product_type = 'فيلم أكحل',
    ).aggregate(Sum('weight'))['weight__sum']    
    context['filmb_purchase'] = models.PurchaseProducts.objects.filter(
        purchase__employee_id=employee_id,        
        product_type__product_type='فيلم أكحل',
        ).aggregate(Sum('weight'))['weight__sum']
    context['filmb_sale'] = models.SalesProducts.objects.filter(
        sale__employee_id=employee_id,        
        product_type__product_type='فيلم أكحل',
        ).aggregate(Sum('weight'))['weight__sum']    
    if context['filmb_purchase'] and context['filmb_company'] and context['filmb_sale'] is not None:
        context['filmb'] = int(context['filmb_purchase']) - (int(context['filmb_company']) + int(context['filmb_sale']))
    elif context['filmb_purchase'] and context['filmb_company'] is not None:
        context['filmb'] = int(context['filmb_purchase']) - int(context['filmb_company'])
    elif context['filmb_purchase'] and context['filmb_sale'] is not None:
        context['filmb'] = int(context['filmb_purchase']) - int(context['filmb_sale'])
    elif context['filmb_purchase'] is not None:
        context['filmb'] = int(context['filmb_purchase'])
    else:
        context['filmb']=0 

    context['bouchons'] = None
    context['bouchons_company'] = models.BillProducts.objects.filter(
        bill__employee= employee_id,
        product_type__product_type = 'Bouchons',
    ).aggregate(Sum('weight'))['weight__sum']    
    context['bouchons_purchase'] = models.PurchaseProducts.objects.filter(
        purchase__employee_id=employee_id,        
        product_type__product_type='Bouchons',
        ).aggregate(Sum('weight'))['weight__sum']
    context['bouchons_sale'] = models.SalesProducts.objects.filter(
        sale__employee_id=employee_id,        
        product_type__product_type='Bouchons',
        ).aggregate(Sum('weight'))['weight__sum']    
    if context['bouchons_purchase'] and context['bouchons_company'] and context['bouchons_sale'] is not None:
        context['bouchons'] = int(context['bouchons_purchase']) - (int(context['bouchons_company']) + int(context['bouchons_sale']))
    elif context['bouchons_purchase'] and context['bouchons_company'] is not None:
        context['bouchons'] = int(context['bouchons_purchase']) - int(context['bouchons_company'])
    elif context['bouchons_purchase'] and context['bouchons_sale'] is not None:
        context['bouchons'] = int(context['bouchons_purchase']) - int(context['bouchons_sale'])
    elif context['bouchons_purchase'] is not None:
        context['bouchons'] = int(context['bouchons_purchase'])
    else:
        context['bouchons']=0           

    context['bargataire'] = None
    context['bargataire_company'] = models.BillProducts.objects.filter(
        bill__employee= employee_id,
        product_type__product_type = 'Bargataire',
    ).aggregate(Sum('weight'))['weight__sum']    
    context['bargataire_purchase'] = models.PurchaseProducts.objects.filter(
        purchase__employee_id=employee_id,        
        product_type__product_type='Bargataire',
        ).aggregate(Sum('weight'))['weight__sum']
    context['bargataire_sale'] = models.SalesProducts.objects.filter(
        sale__employee_id=employee_id,        
        product_type__product_type='Bargataire',
        ).aggregate(Sum('weight'))['weight__sum']    
    if context['bargataire_purchase'] and context['bargataire_company'] and context['bargataire_sale'] is not None:
        context['bargataire'] = int(context['bargataire_purchase']) - (int(context['bargataire_company']) + int(context['bargataire_sale']))
    elif context['bargataire_purchase'] and context['bargataire_company'] is not None:
        context['bargataire'] = int(context['bargataire_purchase']) - int(context['bargataire_company'])
    elif context['bargataire_purchase'] and context['bargataire_sale'] is not None:
        context['bargataire'] = int(context['bargataire_purchase']) - int(context['bargataire_sale'])
    elif context['bargataire_purchase'] is not None:
        context['bargataire'] = int(context['bargataire_purchase'])
    else:
        context['bargataire']=0

    context['sauple'] = None
    context['sauple_company'] = models.BillProducts.objects.filter(
        bill__employee= employee_id,
        product_type__product_type = 'PVC Sauple',
    ).aggregate(Sum('weight'))['weight__sum']    
    context['sauple_purchase'] = models.PurchaseProducts.objects.filter(
        purchase__employee_id=employee_id,        
        product_type__product_type='PVC Sauple',
        ).aggregate(Sum('weight'))['weight__sum']
    context['sauple_sale'] = models.SalesProducts.objects.filter(
        sale__employee_id=employee_id,        
        product_type__product_type='PVC Sauple',
        ).aggregate(Sum('weight'))['weight__sum']    
    if context['sauple_purchase'] and context['sauple_company'] and context['sauple_sale'] is not None:
        context['sauple'] = int(context['sauple_purchase']) - (int(context['sauple_company']) + int(context['sauple_sale']))
    elif context['sauple_purchase'] and context['sauple_company'] is not None:
        context['sauple'] = int(context['sauple_purchase']) - int(context['sauple_company'])
    elif context['sauple_purchase'] and context['sauple_sale'] is not None:
        context['sauple'] = int(context['sauple_purchase']) - int(context['sauple_sale'])    
    elif context['sauple_purchase'] is not None:
        context['sauple'] = int(context['sauple_purchase'])
    else:
        context['sauple']=0   

    context['melenge'] = None
    context['melenge_company'] = models.BillProducts.objects.filter(
        bill__employee= employee_id,
        product_type__product_type = 'مخلّط',
    ).aggregate(Sum('weight'))['weight__sum']    
    context['melenge_purchase'] = models.PurchaseProducts.objects.filter(
        purchase__employee_id=employee_id,        
        product_type__product_type='مخلّط',
        ).aggregate(Sum('weight'))['weight__sum']
    context['melenge_sale'] = models.SalesProducts.objects.filter(
        sale__employee_id=employee_id,        
        product_type__product_type='مخلّط',
        ).aggregate(Sum('weight'))['weight__sum']    
    if context['melenge_purchase'] and context['melenge_company'] and context['melenge_sale'] is not None:
        context['melenge'] = int(context['melenge_purchase']) - (int(context['melenge_company']) + int(context['melenge_sale']))    
    elif context['melenge_purchase'] and context['melenge_company'] is not None:
        context['melenge'] = int(context['melenge_purchase']) - int(context['melenge_company'])
    if context['melenge_purchase'] and context['melenge_sale'] is not None:
        context['melenge'] = int(context['melenge_purchase']) - int(context['melenge_sale'])
    elif context['melenge_purchase'] is not None:
        context['melenge'] = int(context['melenge_purchase'])
    else:
        context['melenge']=0 
      
    return render(request, 'Employee/employee_home.html', context)

@login_required(login_url='/')
def ADD_CLIENT(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        employee = models.Employee.objects.get(admin=request.user.id)
        client = models.Client(
            employee_id = employee,
            name = name,
            phone = phone,
            address = address,
        )
        client.save()
        messages.success(request, 'تم إضافة الزبون بنجاح')
        return redirect('view_client')
    return render(request, 'Employee/add_client.html')

@login_required(login_url='/')
def VIEW_CLIENT(request):
    employee_id = models.Employee.objects.get(admin=request.user.id)
    client = models.Client.objects.filter(employee_id=employee_id)

    context = {
        'client': client, 
    }
    return render(request, 'Employee/view_client.html', context)

@login_required(login_url='/')
def EDIT_CLIENT(request, id):
    client = models.Client.objects.get(id=id)

    context = {
        'client': client,
    }
    return render(request, 'Employee/edit_client.html', context)

@login_required(login_url='/')
def UPDATE_CLIENT(request):
    if request.method == 'POST':
        client_id = request.POST.get('client_id')
        employee = models.Employee.objects.get(admin=request.user.id)
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        client = models.Client(
            id = client_id,
            employee_id = employee,
            name = name,
            phone = phone,
            address = address,
        )
        client.save()
        messages.success(request, 'تم تحديث الزبون بنجاح')
        return redirect('view_client')
    return render(request, 'Employee/edit_client.html')

@login_required(login_url='/')
def DELETE_CLIENT(request, id):
    client = Client.objects.get(id=id)
    client.delete()
    messages.success(request, 'تم حذف الزبون بنجاح')
    return redirect('view_client')    

@login_required(login_url='/')
def products_employee(request):
    context = context_data(request)
    context['page'] = 'Product'
    context['page_title'] = "Product List"
    employee_id = models.Employee.objects.get(admin=request.user.id)
    context['employeeproducts'] = models.EmployeeProducts.objects.filter(employee_id=employee_id).all()
    return render(request, 'Employee/products_employee.html', context)

@login_required(login_url='/')
def save_employee_product(request):
    resp = { 'status': 'failed', 'msg' : '', 'id': '' }
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            employeeproduct = models.EmployeeProducts.objects.get(id = post['id'])
            form = forms.SaveEmployeeProducts(request.POST, instance=employeeproduct)
        else:
            form = forms.SaveEmployeeProducts(request.POST) 

        if form.is_valid():
            obj=form.save()
            obj.employee_id = models.Employee.objects.get(admin=request.user.id)
            obj.save()
            if post['id'] == '':
                messages.success(request, ".تم تسجيل السّلعة بنجاح") 
                pid = models.EmployeeProducts.objects.last().id
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

@login_required(login_url='/')
def view_employee_product(request, pk = None):
    context = context_data(request)
    context['page'] = 'view_product'
    context['page_title'] = 'View Product'
    if pk is None:
        context['employeeproduct'] = {}        
    else:
        context['employeeproduct'] = models.EmployeeProducts.objects.get(id=pk)
       
    
    return render(request, 'Employee/view_employee_product.html', context)

@login_required(login_url='/')
def manage_employee_product(request, pk = None):
    context = context_data(request)
    context['page'] = 'manage_product'
    context['page_title'] = 'Manage product'
    if pk is None:
        context['employeeproduct'] = {}
    else:
        context['employeeproduct'] = models.EmployeeProducts.objects.get(id=pk)
    
    return render(request, 'Employee/manage_employee_product.html', context)

@login_required(login_url='/')
def delete_employee_product(request, pk = None):
    resp = { 'status' : 'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'Product ID is invalid'
    else:
        try:
            models.EmployeeProducts.objects.filter(pk = pk).delete()
            messages.success(request, ".تم حذف السّلعة بنجاح")
            resp['status'] = 'success'
        except:
            resp['msg'] = "فشل حذف السّلعة"

    return HttpResponse(json.dumps(resp), content_type="application/json")    

@login_required(login_url='/')
def purchases(request):
    context = context_data(request)
    context['page'] = 'purchase'
    context['page_title'] = "Purchase List"
    employee_id = models.Employee.objects.get(admin=request.user.id)
    context['purchases'] = models.Purchase.objects.filter(employee_id=employee_id).order_by('-date_added').all()
    context['clients'] = models.Client.objects.filter(employee_id=employee_id).all()
    return render(request, 'Employee/purchases.html', context)

@login_required(login_url='/')
def save_purchase(request):
    resp = { 'status': 'failed', 'msg' : '', 'id': '' }
    
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            purchase = models.Purchase.objects.get(id = post['id'])
            form = forms.SavePurchase(request.POST, instance=purchase)
        else:
            form = forms.SavePurchase(request.POST) 
        if form.is_valid():
            form.instance.employee_id = models.Employee.objects.get(admin=request.user.id)
            form.save()
            
            if post['id'] == '':
                messages.success(request, ".تم حفظ الفاتورة بنجاح")
                pid = models.Purchase.objects.last().id
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

@login_required(login_url='/')
def view_purchase(request, pk = None):
    context = context_data(request)
    context['page'] = 'view_purchase'
    context['page_title'] = 'View Purchase'
    employee_id = models.Employee.objects.get(admin=request.user.id)
    context['clients'] = models.Client.objects.filter(employee_id=employee_id).all()
    if pk is None:
        context['purchase'] = {}
        context['pitems'] = {}
    else:
        context['purchase'] = models.Purchase.objects.get(id=pk)
       
        context['pitems'] = models.PurchaseProducts.objects.filter(purchase__id = pk).all()
    
    return render(request, 'Employee/view_purchase.html', context)

@login_required(login_url='/')
def manage_purchase(request, pk = None):
    context = context_data(request)
    context['page'] = 'manage_purchase'
    context['page_title'] = 'Manage purchase'
    employee_id = models.Employee.objects.get(admin=request.user.id)
    context['products'] = models.EmployeeProducts.objects.filter(employee_id=employee_id, delete_flag = 0, status = 1).all()
    context['clients'] = models.Client.objects.filter(employee_id=employee_id).all()
    if pk is None:
        context['purchase'] = {}
        context['pitems'] = {}
    else:
        context['purchase'] = models.Purchase.objects.get(id=pk)
        context['pitems'] = models.PurchaseProducts.objects.filter(purchase__id = pk).all()
    
    return render(request, 'Employee/manage_purchase.html', context)

@login_required(login_url='/')
def update_state_form(request, pk = None):
    context = context_data(request)
    context['page'] = 'update_purchase'
    context['page_title'] = 'Update Transaction'
    if pk is None:
        context['purchase'] = {}
    else:
        context['purchase'] = models.Purchase.objects.get(id=pk)
    
    return render(request, 'Employee/update_regulation.html', context)    

@login_required(login_url='/')
def update_transaction_regulation(request):
    resp = { 'status' : 'failed', 'msg':''}
    if request.POST['id'] is None:
        resp['msg'] = 'Transaction ID is invalid'
    else:
        try:
            models.Purchase.objects.filter(pk = request.POST['id']).update(regulation = request.POST['regulation'])
            messages.success(request, ".تم تحديث حالة الفاتورة بنجاح")
            resp['status'] = 'success'
        except:
            resp['msg'] = "فشل حذف الفاتورة"

    return HttpResponse(json.dumps(resp), content_type="application/json")    

@login_required(login_url='/')
def delete_purchase(request, pk = None):
    resp = { 'status' : 'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'Purchase ID is invalid'
    else:
        try:
            models.Purchase.objects.filter(pk = pk).delete()
            messages.success(request, ".تم حذف الفاتورة بنجاح")
            resp['status'] = 'success'
        except:
            resp['msg'] = "فشل حذف الفاتورة"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required(login_url='/')
def purchase_daily_report(request, date = None):
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
    employee_id = models.Employee.objects.get(admin=request.user.id)
    context['purchases'] = models.Purchase.objects.filter(
            employee_id = employee_id,
            date_added__year = year,
            date_added__month = month,
            date_added__day = day,
        )
    grand_total = 0
    for purchase in context['purchases']:
        grand_total += float(purchase.total_amount)
    context['grand_total'] = grand_total
    
    return render(request, 'Employee/purchase_report.html', context)

@login_required(login_url='/')
def ADD_COST(request):
    if request.method == 'POST':
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        employee = models.Employee.objects.get(admin=request.user.id)
        cost = models.Costs(
            employee_id = employee,
            description = description,
            amount = amount,
        )
        cost.save()
        messages.success(request, 'تمت إضافة المصاريف بنجاح')
        return redirect('view_cost')
    return render(request, 'Employee/add_cost.html')

@login_required(login_url='/')
def VIEW_COST(request):
    employee_id = models.Employee.objects.get(admin=request.user.id)
    cost = models.Costs.objects.filter(employee_id=employee_id)
    context = {
        'cost': cost, 
    }
    return render(request, 'Employee/view_cost.html', context)

@login_required(login_url='/')
def EDIT_COST(request, id):
    cost = models.Costs.objects.get(id=id)
    context = {
        'cost': cost,
    }
    return render(request, 'Employee/edit_cost.html', context)

@login_required(login_url='/')
def UPDATE_COST(request):
    if request.method == 'POST':
        cost_id = request.POST.get('cost_id')
        employee = models.Employee.objects.get(admin=request.user.id)
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        cost = models.Costs(
            id = cost_id,
            employee_id = employee,
            description = description,
            amount = amount,
        )
        cost.save()
        messages.success(request, 'تم تحديث المصاريف بنجاح')
        return redirect('view_cost')
    return render(request, 'Employee/edit_cost.html')

@login_required(login_url='/')
def DELETE_COST(request, id):
    cost = models.Costs.objects.get(id=id)
    cost.delete()
    messages.success(request, 'تم حذف المصاريف بنجاح')
    return redirect('view_cost')
    
@login_required(login_url='/')
def sales(request):
    context = context_data(request)
    context['page'] = 'sale'
    context['page_title'] = "Sales List"
    employee_id = models.Employee.objects.get(admin=request.user.id)
    context['sales'] = models.Sales.objects.filter(employee_id=employee_id).order_by('-date_added').all()
    context['clients'] = models.Client.objects.filter(employee_id=employee_id).all()
    return render(request, 'Employee/sales.html', context)

@login_required(login_url='/')
def save_sale(request):
    resp = { 'status': 'failed', 'msg' : '', 'id': '' }
    
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            sale = models.Sales.objects.get(id = post['id'])
            form = forms.SaveSales(request.POST, instance=sale)
        else:
            form = forms.SaveSales(request.POST) 
        if form.is_valid():
            form.instance.employee_id = models.Employee.objects.get(admin=request.user.id)
            form.save()
            
            if post['id'] == '':
                messages.success(request, ".تم حفظ الفاتورة بنجاح")
                pid = models.Sales.objects.last().id
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

@login_required(login_url='/')
def view_sale(request, pk = None):
    context = context_data(request)
    context['page'] = 'view_sale'
    context['page_title'] = 'View Sale'
    employee_id = models.Employee.objects.get(admin=request.user.id)
    context['products'] = models.EmployeeProducts.objects.filter(employee_id=employee_id, delete_flag = 0, status = 1).all()
    context['clients'] = models.Client.objects.filter(employee_id=employee_id).all()
    if pk is None:
        context['sale'] = {}
        context['pitems'] = {}
    else:
        context['sale'] = models.Sales.objects.get(id=pk)
       
        context['pitems'] = models.SalesProducts.objects.filter(sale__id = pk).all()
    
    return render(request, 'Employee/view_sale.html', context)

@login_required(login_url='/')
def manage_sale(request, pk = None):
    context = context_data(request)
    context['page'] = 'manage_sale'
    context['page_title'] = 'Manage sale'
    employee_id = models.Employee.objects.get(admin=request.user.id)
    context['products'] = models.EmployeeProducts.objects.filter(employee_id=employee_id, delete_flag = 0, status = 1).all()
    context['clients'] = models.Client.objects.filter(employee_id=employee_id).all()
    if pk is None:
        context['sale'] = {}
        context['pitems'] = {}
    else:
        context['sale'] = models.Sales.objects.get(id=pk)
        context['pitems'] = models.SalesProducts.objects.filter(sale__id = pk).all()
        
    return render(request, 'Employee/manage_sale.html', context)

@login_required(login_url='/')
def update_dealing_form(request, pk = None):
    context = context_data(request)
    context['page'] = 'update_ranking'
    context['page_title'] = 'Update Transaction'
    if pk is None:
        context['sale'] = {}
    else:
        context['sale'] = models.Sales.objects.get(id=pk)
    
    return render(request, 'Employee/update_condition.html', context)    

@login_required(login_url='/')
def update_dealing_condition(request):
    resp = { 'status' : 'failed', 'msg':''}
    if request.POST['id'] is None:
        resp['msg'] = 'Transaction ID is invalid'
    else:
        try:
            models.Sales.objects.filter(pk = request.POST['id']).update(condition = request.POST['condition'])
            messages.success(request, ".تم تحديث حالة الفاتورة بنجاح")
            resp['status'] = 'success'
        except:
            resp['msg'] = "فشل حذف الفاتورة"

    return HttpResponse(json.dumps(resp), content_type="application/json")    

@login_required(login_url='/')
def delete_sale(request, pk = None):
    resp = { 'status' : 'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'Purchase ID is invalid'
    else:
        try:
            models.Sales.objects.filter(pk = pk).delete()
            messages.success(request, ".تم حذف الفاتورة بنجاح")
            resp['status'] = 'success'
        except:
            resp['msg'] = "فشل حذف الفاتورة"

    return HttpResponse(json.dumps(resp), content_type="application/json")    