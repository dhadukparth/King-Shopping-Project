from django.urls import path
from . import views

urlpatterns = [

    # Home Page URL
    path('', views.productsaction.home, name="home"),

    # Full Product Details Page URL
    path('product/', views.productsaction.product, name="product"),


    # All Products List Page URL
    path('products/<str:catname>/', views.productsaction.productslist, name="productslist"),
    path('products/<str:catname>/<str:bname>/', views.productsaction.menu_product_search, name="menuProduct"),
    path('filter/', views.productsaction.menu_product_filter_search, name="menuFilterProduct"),
    path('search/', views.productsaction.search_user, name="userSearch"),



    # Wishlish Page URL
    path('wishlist/', views.wishlistsaction.wishlist, name="wishlist"),
    path('wishlist/add/', views.wishlistsaction.add_wishlist_product, name="New_Wishlist_product"),
    path('wishlist/remove/', views.wishlistsaction.remove_wishlist_product, name="Remove_Wishlist_product"),



    # Cart Page URL
    path('cart/', views.cartaction.addtocart, name="cart"),
    path('cart/qty/', views.cartaction.product_add_qty, name="QTY_Add_Cart"),
    path('cart/add/', views.cartaction.product_add_cart, name="Add_Cart"),
    path('cart/remove/', views.cartaction.product_remove_cart, name="Remove_Cart"),


    # Buy Product URL
    path('buyproducts/', views.buyproduct.cartbuyproducts, name="Buy_product"),
    path('buyproduct/', views.buyproduct.buyproduct, name="Buy_product"),


    # Orders Page URL
    path('orders/', views.orderaction.orders, name="orders"),
    path('orders/orderdetails/', views.orderaction.ordersdetails, name="order_details"),
    path('orders/orderdetails/cancel/', views.orderaction.ordercancel, name="order_cancel"),
    path('orders/return/', views.orderaction.ordereturn, name="order_return"),


    # Settings Page URL
    path('account/', views.settings.settingProfile, name="Profile"),
    path('account/profile/', views.settings.settingProfile, name="Profile"),


    path('account/address/', views.settings.settingAddress, name="address"),
    path('account/address/edit/', views.settings.address_edit, name="edit_address"),
    path('account/address/remove/', views.settings.address_remove, name="remove_address"),
    
    path('account/security/', views.settings.settingSecurity, name="security"),
    path('account/security/sendotp/', views.settings.sendotpuser, name="password_change_send_otp"),
    path('account/security/checkotp/', views.settings.passwordotp, name="check_password_otp"),
    path('account/security/twocheckemail/', views.settings.twostepemail, name="check_user_emailaddress"),
    path('account/security/twocheckotp/', views.settings.twostepcheckotp, name="check_user_otp"),
    path('account/security/twostepoff/', views.settings.twostepoff, name="two_step_off"),

    path('account/security/deactive/', views.settings.deactiveAccount, name="deactive_account"),

    path('account/lastLocation/', views.settings.lastlocation, name="lastLocation"),


    path('help/', views.helpcenter.userhelp, name="userhelp"),
    path('help/i/2', views.helpcenter.issues_two, name="issues2"),
    path('help/i/3', views.helpcenter.issues_three, name="issues3"),
    path('help/i/4', views.helpcenter.issues_content, name="issues4"),



    
    # Page Not Found Page URL
    path('404/', views.pagenotfound, name="pagenotfound"),


    # User Sign In, Out, Up URL 
    path('signup/', views.useraction.newaccount, name="newaccount"),
    path('signin/', views.useraction.userlogin, name="userlogin"),
    path('checkrequestemail/', views.useraction.otp_signin_email_check, name="OtpUserSignin"),
    path('checkrequestotp/', views.useraction.reqotpcheck, name="request_login_otp_check"),
    path('forgotpassword_username/', views.useraction.forgot_check_username, name="forgot_check_username"),
    path('forgotpassword_otp/', views.useraction.forgot_check_otp, name="forgot_check_otp"),
    path('logout/', views.useraction.userlogout, name="userlogout"),

]