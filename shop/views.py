from django.http import HttpResponse
from . models import *
from django.core.paginator import Paginator,EmptyPage,InvalidPage
from django.shortcuts import render,get_object_or_404
from django.db.models import Q

# Create your views here.
def home(request,c_slug=None):
    c_page=None
    cat=None
    product=None
    product_list=None
    if c_slug!=None:
        c_page=get_object_or_404(categ,slug=c_slug)
        product_list=products.objects.filter(category=c_page,available=True)
    else:
        product_list=products.objects.all().filter(available=True)
        cat=categ.objects.all()
        paginator=Paginator(product_list,4)
        try:
            page=int(request.GET.get('page',1))
        except:
            page=1
        try:
            product=paginator.page(page)
        except (EmptyPage,InvalidPage):
            product=paginator.page(paginator.num_pages)
    return render(request,'home.html',{'product':product,'cat':cat})

def proddetails(request,c_slug,product_slug):
    try:
        prod=products.objects.get(category__slug=c_slug,slug=product_slug)
    except Exception as e:
        raise e
    return render(request,'item.html',{'pr':prod})

def searching(request):
    prod = None
    query = None
    if 'q' in request.GET:
        query = request.GET.get('q')
        prod = products.objects.all().filter(Q(name__contains=query)|Q(desc__contains=query))
    return render(request, 'search.html', {'qr': query,'pr': prod})

