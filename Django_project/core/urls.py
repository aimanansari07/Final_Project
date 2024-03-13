from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',views.main,name='main'),
    path('core/about/',views.about,name='about'),
    path('core/contact/',views.contact_us,name='contact'),
    path('core/privacy/',views.privacy,name='privacy'),
    #path('core/sedan/',views.sedan,name='sedan'),
    path('sedan',views.Sedan.as_view(),name='sedan'),
    #path('core/suv/',views.suv,name='suv'),
     path('suv',views.Suv.as_view(),name='suv'),
    path('sports',views.Sports.as_view(),name='sports'),
    
    path('car_details/<int:id>/',views.CarDetailView.as_view(),name='cardetails'),
   path('core/signup/',views.signup,name='signup'),
    path('core/login/',views.log_in,name='login'),
    
    path('core/profile/',views.profile,name='profile'),

    path('logout/',views.log_out, name="logout"),

    path('core/changepassword/',views.changepassword, name="changepassword"),
    path('add_to_cart/<int:id>/',views.add_to_cart, name="addtocart"),
    path('view_cart/',views.view_cart, name="viewcart"),
    path('add_quantity/<int:id>/', views.add_quantity, name='add_quantity'),

    path('delete_quantity/<int:id>/', views.delete_quantity, name='delete_quantity'),
     path('delete_cart/<int:id>',views.delete_cart, name="deletecart"),
    path('address/',views.address,name='address'),
    path('delete_address/<int:id>',views.delete_address,name='deleteaddress'),
        path('checkout/',views.checkout,name='checkout'),
        
    #path('payment_success/',views.payment_success,name='paymentsuccess'),
     path('payment_success/<int:selected_address_id>/',views.payment_success,name='paymentsuccess'),

    path('payment_failed/',views.payment_failed,name='paymentfailed'),
        path('payment/',views.payment,name='payment'),
        #    path('order/',views.order,name='order'),

    path('buynow/<int:id>',views.buynow,name='buynow'),

    path('buynow_payment/<int:id>',views.buynow_payment,name='buynowpayment'),

    path('buynow_payment_success/<int:selected_address_id>/<int:id>',views.buynow_payment_success,name='buynowpaymentsuccess'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

