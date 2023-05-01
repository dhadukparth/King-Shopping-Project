from django.urls import path
from . import views
# from django.conf.urls import handler400

urlpatterns = [
    
    # User Action URL
    path('', views.user_action.user_login, name="adminlogin"),
    path('forgotpassword/', views.user_action.user_forgot_password, name="forgotpassword"),
    path('forgotpassword_email/', views.user_action.user_forgot_check_email, name="forgotcheckemail"),
    path('forgotpassword_otp/', views.user_action.user_forgot_check_otp, name="forgotcheckotp"),
    path('twosecurity/', views.user_action.user_two_step_authontication, name="twostepauthontication"),
    path('logout/', views.user_action.user_logout, name="twostepauthontication"),




    # Dashbord URL    
    path('dashboard/', views.dashboard, name="dashboard"),

    # Header Bar Search URL
    path('search/', views.Others.headerbar_search, name="headerbar_search"),

    
    # Products URL
    path('products/', views.Products.products, name="Products"),
    path('products/edit/', views.Products.product_data_edit, name="ProductEdit"),


    # Product Update records all urls
    path('products/edit/shortdata/', views.Products.product_data_shortdata_update, name="ProsuctShortDataUpdate"),
    path('products/edit/proimages/', views.Products.product_data_images_update, name="ProsuctImageDataUpdate"),
    path('products/edit/generaldata/', views.Products.product_data_general_update, name="ProsuctGeneralDataUpdate"),
    path('products/edit/displaydata/', views.Products.product_data_display_update, name="ProsuctDisplayDataUpdate"),
    path('products/edit/connectivitydata/', views.Products.product_data_connectivity_update, name="ProsuctConnectivityDataUpdate"),
    path('products/edit/osprocessordata/', views.Products.product_data_osprocessor_update, name="ProsuctOSProcessorDataUpdate"),
    path('products/edit/otherdata/', views.Products.product_data_other_update, name="ProsuctOtherDataUpdate"),
    path('products/edit/dimensions_warrantydata/', views.Products.product_data_dimensions_warranty_update, name="ProsuctDimensionsWarrantyDataUpdate"),



    path('products/change/brands/', views.Products.product_data_edit_brands, name="ProductEditBrands"),
    path('products/remove/', views.Products.product_data_remove, name="Product_Delete"),

    path('new product/', views.Products.add_product, name="newProduct"),
    path('new product/<str:catname>/', views.Products.add_productdetails, name="newProductDetails"),


    # Replace Products URL
    path('replace product/', views.Products.replace_product, name="replaceProducts"),
    path('return product/', views.Products.return_product, name="returnProducts"),
    path('return product/edit/', views.Products.edit_return_product, name="editReturnProducts"),


    # Categorys URL
    path('categorys/', views.Category.all_categorys, name="Categorys"),
    path('categorys/edit/', views.Category.category_data_edit, name="edit_category"),
    path('categorys/remove/', views.Category.category_data_remove, name="remove_category"),


    # Brands URL
    path('brands/', views.Brands.all_brands, name="Brands"),
    path('brands/edit/', views.Brands.brands_data_edit, name="edit_Brands"),
    path('brands/remove/', views.Brands.brands_data_remove, name="Remove_Brands"),


    # Users URL
    path('users/', views.allUsers.users, name="users"),
    path('users/edit/', views.allUsers.user_data_show, name="usersEdit"),
    path('users/remove/', views.allUsers.user_data_remove, name="usersY"),


    # Employee URL
    path('employees/', views.Employees.employees, name="employees"),
    path('employees/edit/', views.Employees.employee_data_edit, name="employeeEdit"),
    path('employees/remove/', views.Employees.employee_data_remove, name="employeeRemove"),
    path('new employee/', views.Employees.new_employees, name="newEmployee"),


    # Orders URL
    path('orders/', views.Orders.orders, name="Orders"),
    path('orders/edit/', views.Orders.order_data_edit, name="OrderEdit"),


    # Cancel Orders URL
    path('cancel orders/', views.Orders.cancel_orders, name="CancelOrders"),


    # Notification URL
    path('notification/', views.Others.notifications, name="Notifications"),
    path('notification/edit/', views.Others.notifications_edit, name="Notificationsedit"),


    # Banners URL
    path('banner/', views.Others.banner, name="Banners"),
    path('banner/remove/', views.Others.bannerRemove, name="BannerRemove"),




    # Settings URL
    path('settings/', views.Settings.settings, name="settings"),

    path('settings/general/', views.Settings.general_settings, name="generalSetting"),
    
    # Settings Bin
    path('settings/restore/', views.Settings.restore_settings, name="restoreSetting"),
    path('settings/restore/reback/', views.Settings.restore_record_settings, name="restoreRecordSetting"),
    

    path('settings/security/', views.Settings.security_settings, name="securitySetting"),
    path('settings/security/OTP/', views.Settings.securityOTP_settings, name="securityOTPSetting"),
    path('settings/security/OTPcheck/', views.Settings.securityOTPcheck_settings, name="securityOTPcheckSetting"),
    path('settings/security/twostepcheckemail/', views.Settings.twostepchekemail, name="Two_step_CheckEmail"),
    path('settings/security/twostepcheckotp/', views.Settings.twostepcheckotp, name="Two_step_Checkotp"),
    path('settings/security/twostepoff/', views.Settings.twosteponoff, name="Two_stepoff"),


    # Page Not Found
    path('404/', views.All_Errors.error_404_view, name="PageNotFound"),


]





# handler400 = 'webadminsiteapp.views.error_404_view'