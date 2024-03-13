from django.shortcuts import render,redirect,get_object_or_404
from .forms import Signup,LoginForm,UserProfileForm,AdminProfileForm,ChangePasswordForm,ContactUsForm,CustomerForm
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm,UserChangeForm
from django.views import View
from . models import Customer,Car,Cart,Order
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
#===============For Paypal =========================
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.urls import reverse
#=========================================================


# Create your views here.
def main(request):
    return render(request,'core/main.html')
def about(request):
    return render(request,'core/about.html')
def contact(request):
    return render(request,'core/contact.html')
def privacy(request):
    return render(request,'core/privacy.html')
'''def sedan(request):
    return render(request,'core/sedan.html')'''
def suv(request):
    return render(request,'core/suv.html')
def sports(request):
    return render(request,'core/sports.html')

def signup(request):
  if not request.user.is_authenticated:
    if request.method=='POST':
        su=Signup(request.POST)
        if su.is_valid():
            su.save()
            su=Signup()
            return redirect('signup')
    else:
        su=Signup()
    return render(request,'core/signup.html',{'su':su})
  else:
      return redirect('profile')
      

def log_in(request):
    if not request.user.is_authenticated:  # check whether user is not login ,if so it will show login option
        if request.method == 'POST':       # otherwise it will redirect to the profile page 
            mf = LoginForm(request,request.POST)
            if mf.is_valid():
                name = mf.cleaned_data['username']
                pas = mf.cleaned_data['password']
                user = authenticate(username=name, password=pas)
                if user is not None:
                    login(request, user)
                    return redirect('/')
        else: 
            mf = LoginForm()
        return render(request,'core/login.html',{'mf':mf})
    else:
        return redirect('profile')
    

def profile(request):
    if request.user.is_authenticated:  # This check wheter user is login, if not it will redirect to login page
        if request.method == 'POST':
            if request.user.is_superuser == True:
                mf = AdminProfileForm(request.POST,instance=request.user)
            else:
                mf = UserProfileForm(request.POST,instance=request.user)
            if mf.is_valid():
                mf.save()
        else:
            if request.user.is_superuser == True:
                mf = AdminProfileForm(instance=request.user)
            else:
                mf = UserProfileForm(instance=request.user)
        return render(request,'core/profile.html',{'name':request.user,'mf':mf})
    else:                                                # request.user returns the username
        return redirect('log_in')
    
def changepassword(request):                                       # Password Change Form               
    if request.user.is_authenticated:                              # Include old password 
        if request.method == 'POST':                               
            mf =ChangePasswordForm(request.user,request.POST)
            if mf.is_valid():
                mf.save()
                update_session_auth_hash(request,mf.user)
                return redirect('profile')
        else:
            mf = ChangePasswordForm(request.user)
        return render(request,'core/changepassword.html',{'mf':mf})
    else:
        return redirect('login')
    
def log_out(request):
    logout(request)
    return redirect('main')
    

class Sedan(View):
    def get(self,request):
        car_category = Car.objects.filter(category='SEDAN')  # we are using filter function of queryset, that will filter those data whose category belongs to SEDAN
        return render(request,'core/sedan.html',{'car_category':car_category})
class Suv(View):
    def get(self,request):
        car_category = Car.objects.filter(category='SUV')  # we are using filter function of queryset, that will filter those data whose category belongs to SUV
        return render(request,'core/suv.html',{'car_category':car_category})
class Sports(View):
    def get(self,request):
        car_category = Car.objects.filter(category='SPORTS')  # we are using filter function of queryset, that will filter those data whose category belongs to SPORTS
        return render(request,'core/sports.html',{'car_category':car_category})

class CarDetailView(View):
    def get(self,request,id):     # id = It will fetch id of particular car 
        car_detail = Car.objects.get(pk=id)

        #------ code for caculate percentage -----
        if car_detail.discounted_price !=0:    # fetch discount price of particular car
            percentage = int(((car_detail.selling_price-car_detail.discounted_price)/car_detail.selling_price)*100)
        else:
            percentage = 0
        # ------ code end for caculate percentage ---------
            
        return render(request,'core/car_details.html',{'pd':car_detail,'percentage':percentage})



#=========================== Add TO Cart Section =================================================
    
def add_to_cart(request, id):    # This 'id' is coming from 'car.id' which hold the id of current car , which is passing through {% url 'addtocart' car.id %} from car_detail.html 
    if request.user.is_authenticated:
        product = Car.objects.get(pk=id) # product variable is holding data of current object which is passed through 'id' from parameter
        user=request.user                # user variable store the current user i.e steveroger
        Cart(user=user,product=product).save()  # In cart model current user i.e steveroger will save in user variable and current car object will be save in product variable
        return redirect('cardetails', id)       # finally it will redirect to car_details.html with current object 'id' to display pet after adding to the cart
    else:
        return redirect('login')                # If user is not login it will redirect to login page


def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)      # cart_items will fetch product of only current user, and show product available in the cart of the current user.
    return render(request, 'core/view_cart.html', {'cart_items': cart_items})


def add_quantity(request, id):
    product = get_object_or_404(Cart, pk=id)    # If the object is found, it returns the object. If not, it raises an HTTP 404 exception (Http404).
    product.quantity += 1                   
    product.save()
    return redirect('viewcart')

def delete_quantity(request,id):
    product = get_object_or_404(Cart, pk=id)
    if product.quantity > 1:
        product.quantity -= 1
        product.save()
    return redirect('viewcart')

def contact_us(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact')
    else:
        form = ContactUsForm()

    return render(request, 'core/contact.html', {'form': form})

def delete_cart(request,id):
    if request.method == 'POST':
        de = Cart.objects.get(pk=id)
        de.delete()
    return redirect('viewcart')

#order summary part
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)      # cart_items will fetch product of current user, and show product available in the cart of the current user.
    total =0
    delivery_charge =20000
    for item in cart_items:
        item.product.price_and_quantity_total = item.product.discounted_price * item.quantity
        total += item.product.price_and_quantity_total
    final_price=   delivery_charge + total
    return render(request, 'core/view_cart.html', {'cart_items': cart_items,'total':total,'final_price':final_price})

#===================================== Address ============================================

def address(request):
    if request.method == 'POST':
            print(request.user)
            mf =CustomerForm(request.POST)
            print('mf',mf)
            if mf.is_valid():
                user=request.user                # user variable store the current user i.e steveroger
                name= mf.cleaned_data['name']
                address= mf.cleaned_data['address']
                city= mf.cleaned_data['city']
                state= mf.cleaned_data['state']
                pincode= mf.cleaned_data['pincode']
                print(state)
                print(city)
                print(name)
                Customer(user=user,name=name,address=address,city=city,state=state,pincode=pincode).save()
                return redirect('address')           
    else:
        mf =CustomerForm()
        address = Customer.objects.filter(user=request.user)
        print(address)
    return render(request,'core/address.html',{'mf':mf,'address':address})

def delete_address(request,id):
    if request.method == 'POST':
        de = Customer.objects.get(pk=id)
        de.delete()
    return redirect('address')


def payment_failed(request):
    return render(request,'core/payment_failed.html')


#===================================== Checkout ============================================

def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)      # cart_items will fetch product of current user, and show product available in the cart of the current user.
    total =0
    delhivery_charge =20000
    for item in cart_items:
        item.product.price_and_quantity_total = item.product.discounted_price * item.quantity
        total += item.product.price_and_quantity_total
    final_price= delhivery_charge + total
    
    address = Customer.objects.filter(user=request.user)

    return render(request, 'core/checkout.html', {'cart_items': cart_items,'total':total,'final_price':final_price,'address':address})

#===================================== Payment ============================================

def payment(request):

    if request.method == 'POST':
        selected_address_id = request.POST.get('selected_address')

      # Will fecth the domain site is currently hosted on.

    cart_items = Cart.objects.filter(user=request.user)      # cart_items will fetch product of current user, and show product available in the cart of the current user.
    total =0
    delhivery_charge =20000
    for item in cart_items:
        item.product.price_and_quantity_total = item.product.discounted_price * item.quantity
        total += item.product.price_and_quantity_total
    final_price= delhivery_charge + total
    
    address = Customer.objects.filter(user=request.user)

#=============================== Paypal Code ===============================================
    host = request.get_host() 
    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': final_price,
        'item_name': 'car',
        'invoice': uuid.uuid4(),
        'currency_code': 'USD',
        'notify_url': f"http://{host}{reverse('paypal-ipn')}",
        'return_url': f"http://{host}{reverse('paymentsuccess', args=[selected_address_id])}",
        'cancel_url': f"http://{host}{reverse('paymentfailed')}",
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

#==========================================================================================================
    return render(request, 'core/payment.html', {'cart_items': cart_items,'total':total,'final_price':final_price,'address':address,'paypal':paypal_payment})


#===================================== Payment Success ============================================

def payment_success(request,selected_address_id):
    print('payment sucess',selected_address_id)   # we have fetch this id from return_url': f"http://{host}{reverse('paymentsuccess', args=[selected_address_id])}
                                                  # This id contain address detail of particular customer
    user =request.user
    customer_data = Customer.objects.get(pk=selected_address_id,)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        Order(user=user,customer=customer_data,car=c.product,quantity=c.quantity).save()
        c.delete()
    return render(request,'core/payment_success.html')



#===================================== Order ====================================================

# def order(request):
#     ord=Order.objects.filter(user=request.user)   
#     return render(request,'core/order.html',{'ord':ord})

def buynow(request,id):
    if request.user.is_authenticated:
     #if request.method=='POST':
        car = Car.objects.get(pk=id)     # cart_items will fetch product of current user, and show product available in the cart of the current user.
        delhivery_charge =20000
        final_price= delhivery_charge + car.discounted_price
        
        address = Customer.objects.filter(user=request.user)
    else:
        return redirect('login')
    return render(request, 'core/buynow.html', {'final_price':final_price,'address':address,'car':car})


def buynow_payment(request,id):

    if request.method == 'POST':
        selected_address_id = request.POST.get('buynow_selected_address')

    car = Car.objects.get(pk=id)     # cart_items will fetch product of current user, and show product available in the cart of the current user.
    delhivery_charge =2000
    final_price= delhivery_charge + car.discounted_price
    
    address = Customer.objects.filter(user=request.user)
    #================= Paypal Code ======================================

    host = request.get_host()   # Will fecth the domain site is currently hosted on.

    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': final_price,
        'item_name': 'Car',
        'invoice': uuid.uuid4(),
        'currency_code': 'USD',
        'notify_url': f"http://{host}{reverse('paypal-ipn')}",
        'return_url': f"http://{host}{reverse('buynowpaymentsuccess', args=[selected_address_id,id])}",
        'cancel_url': f"http://{host}{reverse('paymentfailed')}",
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

    #========================================================================

    return render(request, 'core/payment.html', {'final_price':final_price,'address':address,'car':car,'paypal':paypal_payment})

def buynow_payment_success(request,selected_address_id,id):
    print('payment sucess',selected_address_id)   # we have fetch this id from return_url': f"http://{host}{reverse('paymentsuccess', args=[selected_address_id])}
                                                  # This id contain address detail of particular customer
    user =request.user
    customer_data = Customer.objects.get(pk=selected_address_id,)
    
    car = Car.objects.get(pk=id)
    Order(user=user,customer=customer_data,car=car,quantity=1).save()
   
    return render(request,'core/buynow_payment_success.html')