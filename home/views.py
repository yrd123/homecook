from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import  User,auth
from .models import Cinfo,Vinfo,Vendoradd,Feedbacks,Order
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import VendorForm, CustomerForm
from django.views.generic import DetailView, CreateView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import re

# Create your views here.
def index(request):   
    return render(request,'index.html')

def contacts(request):
    if request.method=="POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        phoneNo=request.POST.get("num")
        feedback=request.POST.get("feedback")
        stars=request.POST.get("stars")
        info_var=Feedbacks(name=name,email=email,phoneNo=phoneNo,feedback=feedback,stars=stars)
        info_var.save()
    return render(request,'contacts.html')

def about(request):
    return render(request,"about.html")

#login

def logout(request):
    auth.logout(request)
    return redirect('/')


def login(request):
    if request.method=="POST":
        Username=request.POST.get('Username')
        Password=request.POST.get('Password')
        
        if Vinfo.objects.filter(Username=Username,Password=Password).exists() :
            user = User.objects.get(username=Username)
            auth.login(request,user)
            if request.GET.get("next",None):
                return HttpResponseRedirect(request.GET['next'])
            return redirect("vendoradd")

        elif Cinfo.objects.filter(Username=Username,Password=Password).exists():
            user = User.objects.get(username=Username)
            auth.login(request, user)
            if request.GET.get("next",None):
                return HttpResponseRedirect(request.GET['next'])
            return redirect("customer1")
        
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('login')

    else:
        return render(request,'login.html')


#signin

def vsignin(request):            #vendor signin
    context = {}
    if request.method == 'POST':
        v_form = VendorForm(request.POST,request.FILES)
        context['v_form'] = v_form
        if v_form.is_valid():
            username = v_form.cleaned_data.get('Username')
            password = v_form.cleaned_data.get('Password')
            Email = v_form.cleaned_data.get('Email')
            if User.objects.filter(email=Email).exists():
                messages.info(request, 'Email already exists')
                return redirect('vsignin')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists')
                return redirect('vsignin')
            else:
                v_form.save()
                user = User.objects.create_user(username=username,password=password,email=Email)
                user.save()
                login(request)
                return redirect('vendoradd')
        else:
            return render(request, 'vsignin.html', context)
    else:
        v_form = VendorForm()
        context['v_form'] = v_form
        return render(request, 'vsignin.html', context)

def csignin(request):            #customer signin
    context = {}
    if request.method == 'POST':
        c_form = CustomerForm(request.POST,request.FILES)
        context['c_form'] = c_form
        if c_form.is_valid():
            username = c_form.cleaned_data.get('Username')
            password = c_form.cleaned_data.get('Password')
            Email = c_form.cleaned_data.get('Email')
            if User.objects.filter(email=Email).exists():
                messages.info(request, 'Email already exists')
                return redirect('csignin')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists')
                return redirect('csignin')
            else:
                c_form.save()
                user = User.objects.create_user(username=username,password=password,email=Email)
                user.save()
                login(request)
                return redirect('customer1')
        else:
            return render(request, 'csignin.html', context)
    else:
        c_form = CustomerForm()
        context['c_form'] = c_form
        return render(request, 'csignin.html', context)




#vendor
@login_required(login_url="login")
def vendoradd(request):
    items=Vendoradd.objects.filter(Username=request.user.username)
    Dp = Vinfo.objects.get(Username=request.user.username)
    return render(request,'vendoradd.html',{'items':items,'Dp':Dp})

@login_required(login_url="login")
def vendoradd_upload(request):
    name=request.POST['name']
    price=request.POST['price']
    quantity=request.POST['quantity']
    if(name!="" and price!="" and quantity!=""):
        vendoradd_obj=Vendoradd.objects.filter(Username=request.user.username,name=name,price=price)
        if vendoradd_obj.exists():
            quantity = vendoradd_obj[0].quantity + int(quantity)
            Vendoradd.objects.filter(Username=request.user.username,name=name,price=price).update(quantity=quantity)
        else:
            info_var3=Vendoradd(Username=request.user.username,name=name,price=price,quantity=quantity)
            info_var3.save()
        name=""
        price=""
        quantity=""
    return redirect('vendoradd')

@login_required(login_url="login")
def vendordel(request):
    demou = request.user.username
    demon = request.POST.get('n')
    demop = request.POST.get('p')
    demoq = request.POST.get('q')
    Vendoradd.objects.filter(Username=demou,name=demon, price=demop, quantity=demoq).delete()
    return redirect('vendoradd')

@login_required(login_url="login")
def vprofile(request):
    if request.method == 'POST':
        Name = request.POST['Name']
        Email = request.POST['Email']
        Password = request.POST['Password']
        Confirm = request.POST['Confirm']
        Aadhar = request.POST['Aadhar']
        Code = request.POST['Code']
        PhoneNo = request.POST['PhoneNo']
        Address = request.POST['Address']
        Kitchen = request.POST['Kitchen']
        if(Confirm==Password):
            Vinfo.objects.filter(Username=request.user.username).update(Username=request.user.username, Name=Name,
                                                                        Email=Email, Password=Password,
                                                                        Aadhar=Aadhar, Code=Code, PhoneNo=PhoneNo,
                                                                        Address=Address, Kitchen=Kitchen,
                                                                        Confirm=Confirm
                                                                        )

            User.objects.filter(username=request.user.username).update(password=Password,email=Email)
            user = User.objects.get(username=request.user.username)
            auth.login(request, user)
            return redirect('vprofile')
        else:
            messages.info(request, 'Password does not match')
            return redirect('vprofile')

    else:
        info = Vinfo.objects.get(Username=request.user.username)
        context = {}
        context['info'] = info
        return render(request, 'vprofile.html', context)

@login_required(login_url="login")
def vendor_orders(request):
    username=request.user.username
    orders=Order.objects.filter(vendor_username=username).order_by("-orderDate")
    placed_orders=[order for order in orders if order.status=="placed"]
    accepted_orders=[order for order in orders if order.status=="accepted"]
    rejected_orders=[order for order in orders if order.status=="rejected"]
    delivering_orders=[order for order in orders if order.status=="delivering"]
    delivered_orders=[order for order in orders if order.status=="delivered"]
    context={'placed_orders':placed_orders,'accepted_orders':accepted_orders,'rejected_orders':rejected_orders,'delivering_orders':delivering_orders,'delivered_orders':delivered_orders}
    return render(request,"vendor_orders.html",context)

@login_required(login_url="login")
def order_status(request,orderId,status):
    Order.objects.filter(orderId=orderId).update(status=status)
    if status=="delivered":
        ordered_items=Order.objects.filter(orderId=orderId)[0].ordered_items.replace(" ","")
        ordered_items=re.split('-|x|,',ordered_items)
        username=Order.objects.filter(orderId=orderId)[0].vendor_username
        vendoradd_items=Vendoradd.objects.filter(Username=username)
        for i in range(0,len(ordered_items),3):
            Vendoradd.objects.filter(Username=username,name=ordered_items[i]).update(quantity=Vendoradd.objects.filter(Username=username,name=ordered_items[i])[0].quantity-int(ordered_items[i+1]))
    return redirect("vendor_orders")


#customer

@login_required(login_url="login")
def cprofile(request):
    if request.method == 'POST':
        Name = request.POST['Name']
        Email = request.POST['Email']
        Password = request.POST['Password']
        Confirm= request.POST['Confirm']
        Code = request.POST['Code']
        PhoneNo = request.POST['PhoneNo']
        Address = request.POST['Address']
        if(Confirm==Password):
            Cinfo.objects.filter(Username=request.user.username).update(Name=Name, Email=Email, Password=Password,
                                                                        Code=Code, PhoneNo=PhoneNo,
                                                                        Address=Address, Confirm=Confirm)

            User.objects.filter(username=request.user.username).update(password=Password,email=Email)
            user = User.objects.get(username=request.user.username)
            auth.login(request, user)
            return redirect('cprofile')
        else:
            messages.info(request,'Password does not match')
            return redirect('cprofile')

    else:
        info = Cinfo.objects.get(Username=request.user.username)
        context = {}
        context['info'] = info
        return render(request, 'cprofile.html', context)

@login_required(login_url="login")
def customer1(request):
    cprofile=Cinfo.objects.filter(Username=request.user.username)
    customer_code=cprofile[0].Code
    vendor=Vinfo.objects.filter(Code=customer_code)
    items=Vendoradd.objects.filter()
    return render(request,'customer1.html',{'vendor':vendor,'items':items,'cprofile':cprofile})

@login_required(login_url="login")
def customer2(request,vendorname):
    vkitchen = '0'
    userv=vendorname
    items = Vendoradd.objects.filter(Username=userv)
    vendor = Vinfo.objects.filter(Username=userv)
    vkitchen=vendor[0].Kitchen
    return render(request,'customer2.html',{'items':items,'userv':userv,'vendor':vendor,'vkitchen':vkitchen})

@login_required(login_url="login")
def mycart(request,vendorname):
    userv = vendorname
    vendor=Vinfo.objects.get(Username=userv)
    return render(request,'mycart.html',{'userv':userv,'vendor':vendor})

@login_required(login_url="login")
def payment(request):
    if request.method=="POST":
        cprofile=Cinfo.objects.filter(Username=request.user.username)
        userv=request.POST.get("userv")
        priceDetails={}
        priceDetails['subTotal']=request.POST.get("subTotalInput")
        priceDetails['tax']=request.POST.get("taxInput")
        priceDetails['delivery']=request.POST.get("deliveryInput")
        priceDetails['discount']=request.POST.get("discountInput")
        priceDetails['grandTotal']=request.POST.get("grandTotalInput")
        return render(request,"payment.html",{'priceDetails':priceDetails,'cprofile':cprofile[0], 'userv':userv})
    else:
        return render(request,"payment.html")

@login_required(login_url="login")
def customer_orders(request):
    if request.method=="POST":
        customer_username=request.user.username
        customer=Cinfo.objects.filter(Username=request.user.username)[0]
        vendor_username=request.POST.get("userv")
        vendor=Vinfo.objects.filter(Username=vendor_username)[0]
        ordered_items=request.POST.get("ordered_items")

        li=ordered_items[1:len(ordered_items)-1].split('"')
        li2=[]
        li3=[]
        for i in range(1,len(li),2):
            if (li[i]!="quantity" and li[i]!="price"):
                li2.append(li[i])         
        for i in range(0,len(li2),3):
            item=str(li2[i])+" - "+str(li2[i+1])+" x ₹"+str(li2[i+2])
            li3.append(item)
        ordered_items=" ,  ".join(li3)

        grandTotal=float(request.POST.get("grandTotal"))
        email=request.POST.get("email")
        address=request.POST.get("address")
        zipCode=request.POST.get("zip")
        phoneNo=request.POST.get("phone")
        paymentMode=request.POST.get("tab1")
        info_var2=Order(customer=customer,customer_username=customer_username,vendor=vendor,vendor_username=vendor_username,ordered_items=ordered_items,grandTotal=grandTotal,email=email,address=address,zipCode=zipCode,phoneNo=phoneNo,paymentMode=paymentMode)
        info_var2.save()
        return redirect("customer_orders")
    else:
        orders=Order.objects.filter(customer_username=request.user.username).order_by("-orderDate")
        completed_orders=[order for order in orders if (order.status=="delivered" or order.status=="rejected")]
        current_orders=[order for order in orders if (order.status=="placed" or order.status=="accepted" or order.status=="delivering")]
        context={'completed_orders':completed_orders,'current_orders':current_orders}
        return render(request,"customer_orders.html",context)

        

def sitemap(request):
    return HttpResponse(open('sitemap.xml').read(), content_type='text/xml')
