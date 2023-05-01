from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from webadminsiteapp.models import *
from datetime import datetime
import json, random, time, re


# Send Mail
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

import threading


# Get Today Date
today = datetime.now()


# ================================================== User Action Class ==================================================
class user_action:

    # ------------------------------------------------- Signin Function -------------------------------------------------
    def user_login(request):
        if request.method == 'POST':
            empusername = request.POST["empusername"]
            emppassword = request.POST["emppassword"]
            global twostepuserid, floginuser

            user = auth.authenticate(username=empusername, password=emppassword)

            if user is not None:
                checkemp = User.objects.get(username = empusername)

                # Check Two Step Varification
                checkemptwostep = employees.objects.filter(eid = checkemp, removestate=0)
                if checkemptwostep.exists():

                    if checkemptwostep[0].etwostepauthonetication == 1:
                        twostepuserid = checkemp
                        changepscode = generatcode(6)

                        setuserotp = employees.objects.get(eid=checkemp, removestate=0)
                        floginuser = user

                        sendUserMail(checkemp.email, 'common/email/sendcode/twostepcode.html', f'King Shopping Account {changepscode} is your verification code for secure access', changepscode).start()

                        setuserotp.eOTP = changepscode
                        setuserotp.save()

                        logininfo = {
                            'twostep' : 'on'
                        }
                        return render(request, 'signin.html', logininfo)

                    else:
                        auth.login(request, user)
                        messages.success(request, "Login SuccessFully.")
                        sendUserMail(checkemp.email, 'common/email/loginaccount.html', 'New device login detected in your king shopping account', '').start()

                        return redirect('/adminsideproweb/dashboard/')

                else:
                    messages.error(request, "Please, Check Your Username and Password")
                    return redirect('/adminsideproweb/')

            else:
                messages.error(request, "Please, Check Your Username and Password")
                return redirect('/adminsideproweb/')

        else:
            return render(request, 'signin.html')


    # ------------------------------------------------- Forgot Password Function -------------------------------------------------
    def user_forgot_password(request):
        if request.method == "POST":
            getpassword = request.POST['empforgotpassword']
            getrepassword = request.POST['empforgotrepassword']
            global twostepuserid, floginuser

            if(len(getpassword) >= 8):

                if(bool(re.findall("[a-z]", getpassword)) == False):
                    messages.error(request, 'Please, Enter Any One Lowercase.')

                elif(bool(re.findall("[A-Z]", getpassword)) == False):
                    messages.error(request, 'Please, Enter Any One Uppercase.')

                elif(bool(re.findall("[!@#$%^&*-_+=<>,.?:;|]", getpassword)) == False):
                    messages.error(request, 'Please, Enter Any One Symbol.')
                
                elif(bool(re.findall("[0-9]", getpassword)) == False):
                    messages.error(request, 'Please, Enter Any One Number.')

                else:
                    if getpassword == getrepassword:
                        getuser = User.objects.filter(id=forgoruserid)
                        forgotsetpassword = User.objects.get(username=getuser[0].username)
                        forgotsetpassword.set_password(getpassword)
                        forgotsetpassword.save()
                        
                        forgotuserlogin = auth.authenticate(username=getuser[0].username, password=getpassword)

                        # Check Two Step Verfication
                        forgottwoset = employees.objects.get(eid_id=getuser[0].id, removestate=0)
                        if(forgottwoset.etwostepauthonetication == 1):
                            changepscode = generatcode(6)
                            twostepuserid = getuser[0].id

                            setuserotp = employees.objects.get(eid_id=getuser[0].id, removestate=0)
                            getcustemail = getuser[0].email
                            floginuser = forgotuserlogin
                            setuserotp.eOTP = changepscode
                            setuserotp.save()

                            sendUserMail(getcustemail, 'common/email/sendcode/twostepcode.html', f'King Shopping Account {changepscode} is your verification code for secure access', changepscode).start()

                            logininfo = {
                                'twostep' : 'on'
                            }

                            return render(request, 'signin.html', logininfo)

                        else:
                            auth.login(request, forgotuserlogin)
                            messages.success(request, 'User Login SuccessFully.')
                            sendUserMail(getuser[0].email, 'common/email/loginaccount.html', 'New device login detected in your king shopping account', '').start()
                            return redirect('/adminsideproweb/dashboard/')


                    else:
                        messages.success(request, 'Sorry! Both Password Are Not Match.')

            else:
                messages.error(request, 'Please, Enter The minimum 8 Characture.')

        return render(request, 'forgotpassword.html')


    # ------------------------------------------------- Forgot Password Check Email Address Function -------------------------------------------------
    def user_forgot_check_email(request):
        getadminemail = request.GET.get('adminemail')
        getadminuserid = User.objects.filter(email=getadminemail)
        global forgoruserid

        forgotemail = 0

        if getadminuserid.exists():
            checkemployee = employees.objects.filter(eid_id=getadminuserid[0].id, removestate=0)
            if checkemployee.exists():
                changepscode = generatcode(6)
                forgoruserid = getadminuserid[0].id

                setempotp = employees.objects.get(eid_id=getadminuserid[0].id, removestate=0)
                setempotp.eOTP = changepscode
                setempotp.save()
                forgotemail = 1

                sendUserMail(getadminuserid[0].email, 'common/email/sendcode/resetpassword.html', f'King Shopping Account - {changepscode} is your verification code for secure access', changepscode).start()

            else:
                forgotemail = 0
        else:
            forgotemail = 0


        foremail = json.dumps({
            'forgotemail' : forgotemail
        })
        return HttpResponse(foremail, content_type="application/json")


    
    # ------------------------------------------------- Forgot Password Check OTP Function -------------------------------------------------
    def user_forgot_check_otp(request):
        getforgototp = request.GET.get('forgototp')

        checkempotp = employees.objects.filter(eid_id=forgoruserid, removestate=0)
        otpstatus = 0
        if checkempotp.exists():
            if checkempotp[0].eOTP == getforgototp:
                otpstatus = 1
            else:
                otpstatus = 0
            
        else:
            otpstatus = 0

        forotpdata = json.dumps({
            'empotpstatus' : otpstatus
        })
        return HttpResponse(forotpdata, content_type="application/json")
    


    # ------------------------------------------------- Two Step Authontication Function -------------------------------------------------
    def user_two_step_authontication(request):
        # Check The Two Step Varification OTP
        if request.method == "POST":
            gettwostepotp = request.POST['twostepOTP']

            # check Twostep Otp 
            checktwostepotp = employees.objects.get(eid_id=twostepuserid, etwostepauthonetication=1)
            if checktwostepotp.eOTP == gettwostepotp:
                checktwostepotp.eOTP = 0
                checktwostepotp.save()

                auth.login(request, floginuser)

                messages.success(request, 'User Login SuccessFully')
                return redirect('/adminsideproweb/dashboard/')

            else:
                checktwostepotp.eOTP = 0
                checktwostepotp.save()
                messages.error(request, 'Sorry! OTP Is Not Correct.')
                return redirect('/adminsideproweb/')


    # ------------------------------------------------- Two Step Authontication Function -------------------------------------------------
    def user_logout(request):
        auth.logout(request)
        return redirect("/adminsideproweb/")




# ------------------------------------------------- Dashboard Function -------------------------------------------------
@login_required(login_url="/adminsideproweb/")
def dashboard(request):    
    productprocess = ['conform', 'shipped', 'outofdelivery', 'delived']
    user_object = User.objects.get(username=request.user.username)
    employee_profile = employees.objects.get(eid=user_object, removestate=0)
    employee_profile.eOTP = '0'
    employee_profile.save()

    # Total Products
    totalproducts = products.objects.filter(removestate=0).count()

    # Total Orders
    totalorders = orders.objects.filter(removestate=0, returnpro='No', productstatus__in=productprocess).count()

    # Cancel Orders
    totalcancels = orders.objects.filter(removestate=0, returnpro='No', productstatus='cancel').count()

    # Total Categorys
    totalcategorys = categorys.objects.filter(removestate=0).count()

    # Total Brands
    totalbrands = brands.objects.filter(removestate=0).count()

    # Total Users
    totalusers = userprofile.objects.filter(removestate=0).count()

    # Total Employees
    totalemp = employees.objects.filter(removestate=0).count()

    # Total Replace Orders
    replaceorder = orders.objects.filter(Q(returnpro="Replace") | Q(returnpro="Return")).count()


    dashboarddata = {
        'user' : user_object,
        'employee_profile' : employee_profile,
        'tproducts' : totalproducts,
        'torders' : totalorders,
        'tcancel' : totalcancels,
        'tusers' : totalusers,
        'temp' : totalemp,
        'tcategory' : totalcategorys,
        'tbrands' : totalbrands,
        'treplaceorder' : replaceorder,
    }

    return render(request, 'dashboard.html', dashboarddata)





# ================================================== Product Class ==================================================
class Products:

    # ------------------------------------------------- All Product Function -------------------------------------------------
    @login_required(login_url="/adminsideproweb")
    def products(request):
        employee_profile = getuser(req=request)
        emp_deparement = str(employee_profile.edeparements).lower()

        if emp_deparement == 'administrator' or emp_deparement == 'hr' or emp_deparement == 'manager':

            if request.method == "GET":
                allpro = products.objects.filter(removestate__exact = 0)

                allpropasscont = {
                    'allprodata' : allpro,
                    'employee_profile' : employee_profile,
                }

                return render(request, 'adminfiles/products/products.html', allpropasscont)

            else:
                return redirect('/adminsideproweb/products/')

        else:
            return redirect('/adminsideproweb/404/')


    # ------------------------------------------------- Edit Products All Records Function -------------------------------------------------
    @login_required(login_url="/adminsideproweb/")
    def product_data_edit(request):
        try:
            employee_profile = getuser(req=request)
            emp_deparement = str(employee_profile.edeparements).lower()

            if emp_deparement == 'administrator' or emp_deparement == 'hr' or emp_deparement == 'manager' or emp_deparement == 'employee' or emp_deparement == 'packing' or emp_deparement == 'delivery':
                
                if request.method == "GET":
                    try:
                        geturlproname = request.GET['proname']
                        geturlprocat = request.GET['procat']
                        geturlprobrand = request.GET['probrand']
                        geturlprocolor = request.GET['procolor']


                        # Get Category Data
                        getcategory = categorys.objects.filter(removestate=0).order_by('catname')

                        # Get Brands Data
                        getcatid = categorys.objects.filter(catname=geturlprocat, removestate=0)
                        getbrands = brands.objects.filter(cid=getcatid[0].cid, removestate=0).order_by('bname')

                        # Get Product Data
                        getproductedit = products.objects.filter(proname__istartswith=geturlproname[:len(geturlproname)//4], procolorname=geturlprocolor, removestate=0)

                        # Product All Deatils
                        generaldata = products_general_details.objects.filter(proid_id=getproductedit[0].proid, removestate=0)
                        displaydata = products_displays_details.objects.get(proid_id=getproductedit[0].proid, removestate=0)
                        connectivitydata = products_connectivity_details.objects.get(proid_id=getproductedit[0].proid, removestate=0)
                        osprocesserdata = products_osprocesser_details.objects.get(proid_id=getproductedit[0].proid, removestate=0)
                        otherdata = products_other_details.objects.get(proid_id=getproductedit[0].proid, removestate=0)
                        dimensionsdata = products_dimensions_warranty_details.objects.get(proid_id=getproductedit[0].proid, removestate=0)

                        producteditdata = {
                            'employee_profile' : employee_profile,
                            'setdata':{
                                'gprocategory' : geturlprocat,
                                'allcategorys': getcategory,
                                'allbrands': getbrands,
                                'proname' : getproductedit[0].proname,
                                'productdata': getproductedit,
                            },

                            'othersdata':{
                                'gendata': generaldata,
                                'disdata': displaydata,
                                'conndata': connectivitydata,
                                'osprodata': osprocesserdata,
                                'otherdata': otherdata,
                                'dimwarrdata': dimensionsdata,
                            },
                        }

                        return render(request, 'adminfiles/products/productEdit.html', producteditdata)

                    except:
                        return redirect('/adminsideproweb/products/')

                else:
                    return redirect('/adminsideproweb/404/')
            else:
                return redirect('/adminsideproweb/404/')

        except:
            return redirect('/adminsideproweb/products/')


    # ------------------------------------------------- Edit Product Change Category Change Brands This Function -------------------------------------------------
    @login_required(login_url="/adminsideproweb/")
    def product_data_edit_brands(request):
        employee_profile = getuser(req=request)
        emp_deparement = str(employee_profile.edeparements).lower()

        if emp_deparement == 'administrator' or emp_deparement == 'hr' or emp_deparement == 'manager':

            if request.method == 'GET':
                getcat = request.GET.get('setcat')

                # Get Category Id
                getcatid = categorys.objects.get(catname=getcat, removestate=0)

                # Get Category Releted Brands
                getbrands = list(brands.objects.filter(cid=getcatid.cid, removestate=0).values('bname').order_by('bname'))

                editproductbrandsdata = json.dumps({
                    'setbrands' : getbrands,
                    'employee_profile' : employee_profile,
                })

                return HttpResponse(editproductbrandsdata, content_type="application/json")

            else:
                return redirect('/adminsideproweb/products/')

        else:
            return redirect('/adminsideproweb/404/')





    # ================================================== Product Update All Details Start Line ==================================================





    # ------------------------------------------------- Product Short Details Update Function -------------------------------------------------
    @login_required(login_url="/adminsideproweb/")
    def product_data_shortdata_update(request):
        if request.method == "GET":
            employee_profile = getuser(req=request)
            emp_deparement = str(employee_profile.edeparements).lower()

            if emp_deparement == 'administrator' or emp_deparement == 'hr' or emp_deparement == 'manager':
                try:
                    if request.method == 'POST':
                        cprocat = request.POST['uprocategory']
                        cprobrand = request.POST['uprobrands']
                        uproductid = request.POST['uproid']
                        cproname = request.POST['uproname']
                        cproprice = request.POST['uproprice']
                        cprostock = request.POST['uprostock']
                        cprocolor = request.POST['uprocolor']
                        cprocolorname = request.POST['uprocolorname']
                        cprodesc = request.POST['uprodescription']
                        getram = request.POST['ram']
                        getrom = request.POST['rom']
                        clothesgender = request.POST['clothe_gender']
                        clothesize = request.POST['clothes_size']
                        watchtype = request.POST['watch_type']

                        if cprocat != None and cprobrand != None and uproductid != None and cproname != None and cproprice != None and cprostock != None and cprocolor != None and cprodesc != None:
                            getcatid = categorys.objects.get(catname=cprocat, removestate=0)
                            getprocatid = getcatid.cid

                            getbrandid = brands.objects.get(cid_id=getprocatid, bname=cprobrand , removestate=0)
                            getprobrandid = getbrandid.bid

                            changeproduct = products.objects.get(proid=uproductid, removestate=0)
                            changeproduct.cid_id = getprocatid
                            changeproduct.bid_id = getprobrandid
                            changeproduct.proname = cproname
                            changeproduct.proprice = cproprice
                            changeproduct.prostock = cprostock
                            changeproduct.procolor = cprocolor
                            changeproduct.procolorname = cprocolorname
                            changeproduct.prodescription = cprodesc
                            changeproduct.ram = getram
                            changeproduct.rom = getrom
                            changeproduct.clothes_gender = clothesgender
                            changeproduct.clothes_size = clothesize
                            changeproduct.watch_type = watchtype
                            changeproduct.prodate = today
                            changeproduct.save()

                            messages.success(request, "Product Short Details Update SuccessFully.")
                            return redirect(f'/adminsideproweb/products/edit/?proname={changeproduct.proname}&procat={changeproduct.cid}&probrand={changeproduct.bid}&procolor={changeproduct.procolorname}')

                        else:
                            messages.error(request, "Please, Enter The values into the fileds.")
                            return redirect('/adminsideproweb/products/')

                    else:
                        return redirect('/adminsideproweb/products/')

                except:
                    messages.warning(request, "Sorry, Product Is Not Update.")
                    return redirect('/adminsideproweb/products/')

            else:
                messages.warning(request, "Sorry, You Can't Update The Product.")
                return redirect('/adminsideproweb/products/')

        else:
            return redirect('/adminsideproweb/products/')


    # ------------------------------------------------- Product All Images Change Update Function -------------------------------------------------
    @login_required(login_url="/adminsideproweb/")
    def product_data_images_update(request):
        employee_profile = getuser(req=request)
        emp_deparement = str(employee_profile.edeparements).lower()

        if emp_deparement == 'administrator' or emp_deparement == 'hr' or emp_deparement == 'manager':

            if request.method == 'POST':
                uproductid = request.POST['uproid']

                productdata = products.objects.get(proid=uproductid, removestate=0)

                # User Images is Select New Image
                global upimage1, upimage2, upimage3, upimage4, upimage5

                if request.FILES.get('uproimage1') == None:
                    upimage1 = productdata.proimage1
                else:
                    upimage1 = request.FILES.get('uproimage1')

                if request.FILES.get('uproimage2') == None:
                    upimage2 = productdata.proimage2
                else:
                    upimage2 = request.FILES.get('uproimage2')

                if request.FILES.get('uproimage3') == None:
                    upimage3 = productdata.proimage3
                else:
                    upimage3 = request.FILES.get('uproimage3')

                if request.FILES.get('uproimage4') == None:
                    upimage4 = productdata.proimage4
                else:
                    upimage4 = request.FILES.get('uproimage4')

                if request.FILES.get('uproimage5') == None:
                    upimage5 = productdata.proimage5
                else:
                    upimage5 = request.FILES.get('uproimage5')

                Products.productupdateimage(proid=uproductid, image1=upimage1, image2=upimage2, image3=upimage3, image4=upimage4, image5=upimage5)

                messages.success(request, "Product Images Update SuccessFully.")
                return redirect(f'/adminsideproweb/products/edit/?proname={productdata.proname}&procat={productdata.cid}&probrand={productdata.bid}&procolor={productdata.procolorname}')

            else:
                return redirect('/adminsideproweb/products/')

        else:
            messages.warning(request, "Sorry, You Can't Update The Product.")
            return redirect('/adminsideproweb/products/')

    # Product Images Update Function
    def productupdateimage(**dataproimages):
        productdata = products.objects.get(proid=dataproimages['proid'], removestate=0)
        productdata.proimage1 = dataproimages['image1'] 
        productdata.proimage2 = dataproimages['image2'] 
        productdata.proimage3 = dataproimages['image3'] 
        productdata.proimage4 = dataproimages['image4'] 
        productdata.proimage5 = dataproimages['image5'] 
        productdata.save()


    # ------------------------------------------------- Product General Details Update Function -------------------------------------------------
    @login_required(login_url="/adminsideproweb/")
    def product_data_general_update(request):
        employee_profile = getuser(req=request)
        emp_deparement = str(employee_profile.edeparements).lower()

        if emp_deparement == 'administrator' or emp_deparement == 'hr' or emp_deparement == 'manager':

            if request.method == "POST":
                proid = request.POST['uproid']
                generaldetails = request.POST['update_general_details']

                checkproduct = products.objects.filter(proid=proid, removestate=0)
                if checkproduct.exists():
                    update_general_product = products_general_details.objects.get(proid_id=proid, removestate=0)
                    update_general_product.general_details = generaldetails
                    update_general_product.save()

                    messages.success(request, "Product Update Successfully")
                    return redirect(f'/adminsideproweb/products/edit/?proname={checkproduct[0].proname}&procat={checkproduct[0].cid}&probrand={checkproduct[0].bid}&procolor={checkproduct[0].procolorname}')

                else:
                    messages.error(request, "Sorry! Product Update Failed")
                    return redirect('/adminsideproweb/products/')

            else:
                return redirect('/adminsideproweb/products/')

        else:
            messages.warning(request, "Sorry, You Can't Update The Products")
            return redirect('/adminsideproweb/products/')



    # ------------------------------------------------- Product Display Update Function -------------------------------------------------
    @login_required(login_url="/adminsideproweb/")
    def product_data_display_update(request):
        employee_profile = getuser(req=request)
        emp_deparement = str(employee_profile.edeparements).lower()

        if emp_deparement == 'administrator' or emp_deparement == 'hr' or emp_deparement == 'manager':

            if request.method == "POST":
                proid = request.POST['uproid']
                showdis = request.POST['displayshow']
                udatedisplaydata = request.POST['update_display_details']

                checkproduct = products.objects.filter(proid=proid, removestate=0)
                if checkproduct.exists():
                    displayupdate = products_displays_details.objects.get(proid_id=proid, removestate=0)
                    if showdis == "show":
                        displayupdate.show_display = showdis
                        displayupdate.display_details = udatedisplaydata
                        displayupdate.save()

                    elif showdis == "hide":
                        displayupdate.show_display = showdis
                        displayupdate.save()

                    else:
                        displayupdate.show_display = "hide"
                        displayupdate.save()
                    


                    messages.success(request, "Product Update Successfully.")
                    return redirect(f'/adminsideproweb/products/edit/?proname={checkproduct[0].proname}&procat={checkproduct[0].cid}&probrand={checkproduct[0].bid}&procolor={checkproduct[0].procolorname}')

                else:
                    return redirect('/adminsideproweb/products/')

            else:
                return redirect('/adminsideproweb/products/')
        
        else:
            messages.warning(request, "Sorry, You Can't Update The Products")
            return redirect('/adminsideproweb/404/')



    # ------------------------------------------------- Product Connectivity Update Function -------------------------------------------------
    @login_required(login_url="/adminsideproweb/")
    def product_data_connectivity_update(request):
        employee_profile = getuser(req=request)
        emp_deparement = str(employee_profile.edeparements).lower()

        if emp_deparement == 'administrator' or emp_deparement == 'hr' or emp_deparement == 'manager':

            if request.method == "POST":
                proid = request.POST['uproid']
                connshow = request.POST['connectivityshow']
                connectivitydata = request.POST['update_connectivity_details']

                
                checkproduct = products.objects.filter(proid=proid, removestate=0)
                if checkproduct.exists():
                    connectivityupdate = products_connectivity_details.objects.get(proid_id=proid, removestate=0)
                    if connshow == "show":
                        connectivityupdate.show_connectivity = connshow
                        connectivityupdate.connectivity_details = connectivitydata
                        connectivityupdate.save()
                    else:
                        connectivityupdate.show_connectivity = connshow
                        connectivityupdate.save()


                    messages.success(request, "Product Update Successfully.")
                    return redirect(f'/adminsideproweb/products/edit/?proname={checkproduct[0].proname}&procat={checkproduct[0].cid}&probrand={checkproduct[0].bid}&procolor={checkproduct[0].procolorname}')
                
                else:
                    return redirect('/adminsideproweb/products/')

            else:
                return redirect('/adminsideproweb/products/')

        else:
            messages.warning(request, "Sorry, You Can't Update The Products")
            return redirect('/adminsideproweb/404/')



    # ------------------------------------------------- Product OS & Processor Update Function -------------------------------------------------
    @login_required(login_url="/adminsideproweb/")
    def product_data_osprocessor_update(request):
        employee_profile = getuser(req=request)
        emp_deparement = str(employee_profile.edeparements).lower()

        if emp_deparement == 'administrator' or emp_deparement == 'hr' or emp_deparement == 'manager':

            if request.method == "POST":
                proid = request.POST['uproid']
                osproshow = request.POST['osprocessorshow']
                osprocesserdata = request.POST['update_os_processer_details']

                checkproduct = products.objects.filter(proid=proid, removestate=0)
                if checkproduct.exists():
                    osprocesserupdate = products_osprocesser_details.objects.get(proid_id=proid, removestate=0)
                    if osproshow == "show":
                        osprocesserupdate.show_osprocesser = osproshow
                        osprocesserupdate.osprocesser_details = osprocesserdata
                        osprocesserupdate.save()

                    elif osproshow == "hide":
                        osprocesserupdate.show_osprocesser = osproshow
                        osprocesserupdate.save()

                    else:
                        osprocesserupdate.show_osprocesser = "hide"
                        osprocesserupdate.save()

                    messages.success(request, "Product Update Successfully.")
                    return redirect(f'/adminsideproweb/products/edit/?proname={checkproduct[0].proname}&procat={checkproduct[0].cid}&probrand={checkproduct[0].bid}&procolor={checkproduct[0].procolorname}')
                
                else:
                    return redirect('/adminsideproweb/products/')

            else:
                return redirect('/adminsideproweb/products/')

        else:
            messages.warning(request, "Sorry, You Can't Update The Products")
            return redirect('/adminsideproweb/404/')



    # ------------------------------------------------- Product Clothes Update Function -------------------------------------------------
    @login_required(login_url="/adminsideproweb/")
    def product_data_other_update(request):
        employee_profile = getuser(req=request)
        emp_deparement = str(employee_profile.edeparements).lower()

        if emp_deparement == 'administrator' or emp_deparement == 'hr' or emp_deparement == 'manager':
            
            if request.method == "POST":
                proid = request.POST['uproid']
                clotheshow = request.POST['clothesshow']
                clothesdata = request.POST['update_clothes_details']

                checkproduct = products.objects.filter(proid=proid, removestate=0)
                if checkproduct.exists():
                    clothesupdate = products_other_details.objects.get(proid_id=proid, removestate=0)
                    if clotheshow == "show":
                        clothesupdate.show_other = clotheshow
                        clothesupdate.other_details = clothesdata
                        clothesupdate.save()

                    elif clotheshow == "hide":
                        clothesupdate.show_other = clotheshow
                        clothesupdate.save()

                    else:
                        clothesupdate.show_other = "hide"
                        clothesupdate.save()

                    messages.success(request, "Product Update Successfully.")
                    return redirect(f'/adminsideproweb/products/edit/?proname={checkproduct[0].proname}&procat={checkproduct[0].cid}&probrand={checkproduct[0].bid}&procolor={checkproduct[0].procolorname}')
                
                else:
                    return redirect('/adminsideproweb/products/')

            else:
                return redirect('/adminsideproweb/products/')

        else:
            messages.warning(request, "Sorry, You Can't Update The Products")
            return redirect('/adminsideproweb/404/')



    # ------------------------------------------------- Product Dimensions and Warranty Update Function -------------------------------------------------
    @login_required(login_url="/adminsideproweb/")
    def product_data_dimensions_warranty_update(request):
        employee_profile = getuser(req=request)
        emp_deparement = str(employee_profile.edeparements).lower()

        if emp_deparement == 'administrator' or emp_deparement == 'hr' or emp_deparement == 'manager':

            if request.method == "POST":
                proid = request.POST['uproid']
                dimwarrshow = request.POST['dimwarrshow']
                dimwarrdata = request.POST['update_dimension_warranty']

                checkproduct = products.objects.filter(proid=proid, removestate=0)
                if checkproduct.exists():
                    dimensionsdata = products_dimensions_warranty_details.objects.get(proid_id=proid, removestate=0)
                    if dimwarrshow == "show":
                        dimensionsdata.show_dimwarr = dimwarrshow
                        dimensionsdata.dimension_warranty_details = dimwarrdata
                        dimensionsdata.save()

                    elif dimwarrshow == "hide":
                        dimensionsdata.show_dimwarr = dimwarrshow
                        dimensionsdata.save()

                    else:
                        dimensionsdata.show_dimwarr = "hide"
                        dimensionsdata.save()

                    messages.success(request, "Product Update Successfully")
                    return redirect(f'/adminsideproweb/products/edit/?proname={checkproduct[0].proname}&procat={checkproduct[0].cid}&probrand={checkproduct[0].bid}&procolor={checkproduct[0].procolorname}')

                else:
                    return redirect('/adminsideproweb/products/')

            else:
                return redirect('/adminsideproweb/products/')

        else:
            messages.warning(request, "Sorry, You Can't Update The Products")
            return redirect('/adminsideproweb/404/')




    # ================================================== Product Update All Details End Line ==================================================







    # ------------------------------------------------- Delete Product Function -------------------------------------------------
    @login_required(login_url="/adminsideproweb/")
    def product_data_remove(request):
        employee_profile = getuser(req=request)
        emp_deparement = str(employee_profile.edeparements).lower()

        if emp_deparement == 'administrator' or emp_deparement == 'hr' or emp_deparement == 'manager':

            if request.method == "GET":
                global getproid
                getproid = request.GET.get('rmproid')
                return HttpResponse()

            elif request.method == "POST":
                rmproduct = products.objects.get(proid=getproid, removestate=0)

                rmproduct.removestate = 1
                rmproduct.prormdate = today
                rmproduct.save()

                messages.success(request, "Product Is Delete SuccessFully.")
                return redirect('/adminsideproweb/products/')

            else:
                return redirect('/adminsideproweb/products/')

        else:
            return redirect('/adminsideproweb/404/')






    # ------------------------------------------------- New Product Function -------------------------------------------------
    @login_required(login_url="/adminsideproweb/")
    def add_product(request):
        employee_profile = getuser(req=request)
        emp_deparement = str(employee_profile.edeparements).lower()

        if emp_deparement == 'administrator' or emp_deparement == 'hr' or emp_deparement == 'manager':

            if request.method == 'GET':
                getcat = categorys.objects.filter(removestate=0).order_by('catname')

                passcat = {
                    'getcat' : getcat,
                    'employee_profile' : employee_profile,
                }

                return render(request, 'adminfiles/products/newproduct.html', passcat)

            else:
                return  redirect('/adminsideproweb/dashboard/')

        else:
            return redirect('/adminsideproweb/404/')


    # ------------------------------------------------- New Product Details Function -------------------------------------------------
    @login_required(login_url="/adminsideproweb/")
    def add_productdetails(request, catname):
        employee_profile = getuser(req=request)
        emp_deparement = str(employee_profile.edeparements).lower()

        if emp_deparement == 'administrator' or emp_deparement == 'hr' or emp_deparement == 'manager':
            if len(catname) != 0:

                if request.method == "GET":

                    # check Cattegory ID
                    getcat = categorys.objects.filter(catname__exact=catname, removestate__exact=0)
                    getbrand = brands.objects.filter(cid__exact=getcat[0].cid, removestate__exact=0).order_by('bname')

                    prodetailspass = {
                        'employee_profile' : employee_profile,
                        'catname' : catname,
                        'fetchbrands' : getbrand,
                    }

                    return render(request, 'adminfiles/products/newproductdetails.html', prodetailspass)

                elif request.method == "POST":
            
                    # ------------------------ Product Short Details Get Data ------------------------
                    brandname = request.POST['newbrand']
                    proname = request.POST['newProName']
                    proprice = request.POST['newProprice']
                    prostock = request.POST['newProstock']
                    procolorname = request.POST['NewProductName']
                    procolor = request.POST['newProductCode']

                    clothesgender = request.POST['new_clothes_gender']
                    clothesize = request.POST['new_clothes_size']
                    watchtype = request.POST['new_watch_type']
                    getram = request.POST['newram']
                    getrom = request.POST['newrom']

                    prodesc = request.POST['new_product_description_data']

                    image1 = request.FILES.get('nproimage1')
                    image2 = request.FILES.get('nproimage2')
                    image3 = request.FILES.get('nproimage3')

                    image4 = ""
                    image5 = ""

                    if request.FILES.get('nproimage4') == None:
                        image4 = "noimage.png"
                    else:
                        request.FILES.get('nproimage4')

                    if request.FILES.get('nproimage5') == None:
                        image5 = "noimage.png"
                    else:
                        image5 = request.FILES.get('nproimage5')

                    products.objects.create(bid_id=brandname, cid_id=getcat[0].cid, proname=proname, prodescription = prodesc, prostock=prostock, procolorname=procolorname, procolor=procolor, proprice = proprice, ram = getram, rom = getrom, clothes_gender = clothesgender, clothes_size = clothesize, watch_type = watchtype, proimage1 = image1, proimage2 = image2, proimage3 = image3, proimage4 = image4, proimage5 = image5).save()



                    getnewproid = products.objects.filter(bid_id=brandname, cid_id=getcat[0].cid, proname=proname,procolorname=procolorname, procolor=procolor, removestate=0)

                    # ------------------------ Product General Details Get Data ------------------------
                    generaldata = request.POST['new_general_data']
                    products_general_details.objects.create(proid_id=getnewproid[0].proid, general_details=generaldata, removestate=0).save()



                    # ------------------------ Product Display Details Get Data ------------------------
                    show_displaydata = request.POST['newdisplayshow']
                    displaynewdata = request.POST['new_display_data']
                    if show_displaydata == "hide":
                        products_displays_details.objects.create(proid_id=getnewproid[0].proid, show_display=show_displaydata, removestate=0).save()
                    else:
                        products_displays_details.objects.create(proid_id=getnewproid[0].proid, show_display=show_displaydata, display_details=displaynewdata, removestate=0).save()


                    # ------------------------ Product Connectivity Details Get Data ------------------------
                    connectivitynewdata = request.POST['new_connectivity_data']
                    show_connectivity = request.POST['newconnectivityshow']
                    if show_connectivity == "hide":
                        products_connectivity_details.objects.create(proid_id=getnewproid[0].proid, show_connectivity=show_connectivity, removestate=0).save()
                    else:
                        products_connectivity_details.objects.create(proid_id=getnewproid[0].proid, connectivity_details=connectivitynewdata, show_connectivity=show_connectivity, removestate=0).save()


                    # ------------------------ Product OS & Processor Details Get Data ------------------------
                    osprocessernewdata = request.POST['new_os_processor_data']
                    show_osprocesser = request.POST['newosprocessorshow']
                    if show_osprocesser == "hide":
                        products_osprocesser_details.objects.create(proid_id=getnewproid[0].proid, show_osprocesser=show_osprocesser, removestate=0).save()
                    else:
                        products_osprocesser_details.objects.create(proid_id=getnewproid[0].proid, osprocesser_details=osprocessernewdata, show_osprocesser=show_osprocesser, removestate=0).save()


                    # ------------------------ Product Cloths Details Get Data ------------------------
                    othernewdata = request.POST['new_clothes_data']
                    show_other = request.POST['newclothesshow']
                    if show_other == "hide":
                        products_other_details.objects.create(proid_id=getnewproid[0].proid, show_other=show_other, removestate=0).save()
                    else:
                        products_other_details.objects.create(proid_id=getnewproid[0].proid, other_details=othernewdata, show_other=show_other, removestate=0).save()




                    # ------------------------ Product Dimension / Warranty Details Get Data ------------------------
                    dimensionwarrantynewdata = request.POST['new_dimension_warranty_data']
                    show_dimwarr = request.POST['newdimwarrshow']
                    if show_dimwarr == "hide":
                        products_dimensions_warranty_details.objects.create(proid_id=getnewproid[0].proid, show_dimwarr=show_dimwarr, removestate=0).save()
                    else:
                        products_dimensions_warranty_details.objects.create(proid_id=getnewproid[0].proid, dimension_warranty_details=dimensionwarrantynewdata, show_dimwarr=show_dimwarr, removestate=0).save()


                    messages.success(request, "Create New Product SuccessFully.")
                    return redirect('/adminsideproweb/new product/')

                else:
                    return  redirect('/adminsideproweb/dashboard/')

            else:
                return  redirect('/adminsideproweb/new product/')
        else:
            return redirect('/adminsideproweb/404/')




    # ------------------------------------------------- Replace Products Function -------------------------------------------------
    @login_required(login_url="/adminsideproweb/")
    def replace_product(request):
        employee_profile = getuser(req=request)
        emp_deparement = str(employee_profile.edeparements).lower()

        if request.method == "GET":
            orderprocess = ['conform', 'shipped', 'outofdelivery', 'delived']
            returndata = products.objects.raw("SELECT * FROM webadminsiteapp_orders AS wo INNER JOIN webadminsiteapp_userprofile AS wu ON wo.user_id = wu.user_id INNER JOIN webadminsiteapp_products AS wp ON wo.proid_id = wp.proid INNER JOIN webadminsiteapp_useraddress AS wa ON wo.deliaddr_id = wa.addid WHERE wo.removestate=0 AND wo.returnpro = 'Replace' AND wo.productstatus IN %s", params=[orderprocess])

            retundata = {
                'allreturn' : returndata,
                'employee_profile' : employee_profile,
            }

            return render(request, 'adminfiles/reproducts/replaceProducts.html', retundata)

        else:
            return render(request, 'adminfiles/replace product/')


    # ------------------------------------------------- Return Products Function -------------------------------------------------
    @login_required(login_url="/adminsideproweb/")
    def return_product(request):
        employee_profile = getuser(req=request)
        emp_deparement = str(employee_profile.edeparements).lower()

        if emp_deparement == 'administrator' or emp_deparement == 'hr' or emp_deparement == 'manager' or emp_deparement == 'employee':

            if request.method == "GET":
                orderprocess = ['conform', 'shipped', 'outofdelivery', 'delived']
                returndataall = products.objects.raw("SELECT * FROM webadminsiteapp_orders AS wo INNER JOIN webadminsiteapp_userprofile AS wu ON wo.user_id = wu.user_id INNER JOIN webadminsiteapp_products AS wp ON wo.proid_id = wp.proid INNER JOIN webadminsiteapp_useraddress AS wa ON wo.deliaddr_id = wa.addid WHERE wo.removestate=0 AND wo.returnpro = 'Return' AND wo.productstatus IN %s", params=[orderprocess])

                retundata = {
                    'allreturn' : returndataall,
                    'employee_profile' : employee_profile,
                }

                return render(request, 'adminfiles/reproducts/returnProducts.html', retundata)

            else:
                return render(request, 'adminfiles/replace product/')

        else:
                return redirect('/adminsideproweb/404/')


    # ------------------------------------------------- Return Products Function -------------------------------------------------
    @login_required(login_url="/adminsideproweb/")
    def edit_return_product(request):
        employee_profile = getuser(req=request)
        emp_deparement = str(employee_profile.edeparements).lower()

        if emp_deparement == 'administrator' or emp_deparement == 'hr' or emp_deparement == 'manager' or emp_deparement == 'employee':
            if request.method == "GET":
                returnoid = request.GET.get('returnoid')

                orderdata = orders.objects.get(oid=returnoid)

                getprodata = products.objects.get(proid=orderdata.proid_id)
                getusers = userprofile.objects.get(user=orderdata.user_id)
                getaddress = useraddress.objects.get(addid=orderdata.deliaddr_id)
                getreturnpro = returnproduct.objects.get(oid_id=returnoid)

                returndata = json.dumps({
                    'orderdate' : str(orderdata.ordate),
                    'ordercenceldate' : str(orderdata.canceldate),
                    'deliverydate' : str(orderdata.deliveddate),
                    'oid' : returnoid,
                    'prostatus' : orderdata.productstatus,
                    'productid' : str(getprodata.proid),
                    'product' : getprodata.proname,
                    'productimage' : getprodata.proimage1.url,
                    'totalprice' : getprodata.proprice * orderdata.proqty,
                    'procolor' : getprodata.procolor,
                    'proqty' : orderdata.proqty,
                    'fullname' : getusers.firstname + " " + getusers.lastname,
                    'phone' : getusers.phone,
                    'userstate' : getusers.state,
                    'delivery' : getaddress.adddescription,
                    'prorestatus' : orderdata.returnpro,

                    'returndate' : str(getreturnpro.rndate),
                })

                return HttpResponse(returndata, content_type="application/json")

            else:
                return render(request, 'adminfiles/replace product/')

        else:
            return redirect('/adminsideproweb/404/')



# ================================================== Category Class ==================================================
class Category:

    # ------------------------------------------------- Categorys Function -------------------------------------------------
    @login_required(login_url="/adminsideproweb/")
    def all_categorys(request):
        employee_profile = getuser(req=request)
        emp_deparement = str(employee_profile.edeparements).lower()

        if emp_deparement == 'administrator' or emp_deparement == 'hr' or emp_deparement == 'manager':
            if request.method == "GET":
                employee_profile = getuser(req=request)
                getallcat = categorys.objects.filter(removestate__exact=0)

                allpassgat = {
                    'getallcat' : getallcat,
                    'employee_profile' : employee_profile,
                }

                return render(request, "adminfiles/categorys/categorys.html", allpassgat)

            elif request.method == "POST":
                cname = request.POST['ncatname']
                cdesc = request.POST['ncatdescription']

                if request.FILES.get('ncatimage') == None:
                    cimage = getallcat.catimage
                    newcat = categorys.objects.create(catname=cname,catimage=cimage, catdescription=cdesc)
                    newcat.save()
                    messages.success(request, "New Category Create SuccessFully.")
                    return redirect('/adminsideproweb/categorys/')

                elif request.FILES.get('ncatimage') != None:
                    cimage = request.FILES.get('ncatimage')
                    newcat = categorys.objects.create(catname=cname,catimage=cimage, catdescription=cdesc)
                    newcat.save()
                    messages.success(request, "New Category Create SuccessFully.")
                    return redirect('/adminsideproweb/categorys/')

            else:
                return redirect('/adminsideproweb/dashboard/')

        else:
            return redirect('/adminsideproweb/404/')



    # ------------------------------------------------- Category Data Set Edit Record Function -------------------------------------------------
    @login_required(login_url="/adminsideproweb/")
    def category_data_edit(request):
        employee_profile = getuser(req=request)
        emp_deparement = str(employee_profile.edeparements).lower()

        if emp_deparement == 'administrator' or emp_deparement == 'hr' or emp_deparement == 'manager':
            if request.method == "GET":
                try:
                    global gcdata
                    gcid = request.GET.get('getcid')
                    gcdata = categorys.objects.get(cid=gcid, removestate=0)

                    catdata = json.dumps  ({
                        'cname' : gcdata.catname,
                        'cdesc' : gcdata.catdescription,
                        'cimage' : gcdata.catimage.url,
                    })

                    return HttpResponse(catdata, content_type='application/json')

                except:
                    return redirect('/adminsideproweb/categorys/')

            elif request.method == "POST":
                ncatname = request.POST['ncatname']
                ncatdesc = request.POST['ncatdescription']


                if request.FILES.get('ncatimage') == None:
                    oldcatimage = gcdata.catimage

                    Category.catupdate(gcdata, ncatname, ncatdesc, oldcatimage)
                    

                elif request.FILES.get('ncatimage') != None:
                    newcatimage = request.FILES.get('ncatimage')
                    Category.catupdate(gcdata, ncatname, ncatdesc, newcatimage)


                messages.success(request, ncatname + " Category Is Update SuccessFully.")

                return redirect('/adminsideproweb/categorys/')

            else:
                return redirect('/adminsideproweb/dashboard/')

        else:
                return redirect('/adminsideproweb/404/')


    # Category Update Function
    def catupdate(*ucatdata):
        ucatdata[0].catname = ucatdata[1]
        ucatdata[0].catdescription = ucatdata[2]
        ucatdata[0].catimage = ucatdata[3]
        ucatdata[0].catdate = today
        ucatdata[0].save()
        


    # ------------------------------------------------- Category Remove Function -------------------------------------------------
    @login_required(login_url="/adminsideproweb/")
    def category_data_remove(request):
        employee_profile = getuser(req=request)
        emp_deparement = str(employee_profile.edeparements).lower()

        if emp_deparement == 'administrator' or emp_deparement == 'hr' or emp_deparement == 'manager':
            if request.method == "GET":
                try:
                    global getrcid
                    getrcid = request.GET.get('getrcid')
                    rmcatid = categorys.objects.get(cid = getrcid)

                    removecatdata = json.dumps({
                        'rmcategory' : rmcatid.catname
                    })
                    return HttpResponse(removecatdata, content_type="application/json")

                except:
                    return redirect('/adminsideproweb/categorys/')


            elif request.method == "POST":

                # category Remove
                rmcatid = categorys.objects.get(cid = getrcid)
                rmcatid.removestate = 1
                rmcatid.catrmdate = today
                rmcatid.save()

                # Brands Remove
                brands.objects.filter(cid=getrcid).update(removestate = 1, brmdate=today)

                # Product Remove
                products.objects.filter(cid=getrcid).update(removestate = 1, prormdate=today)

                rmcatnm = rmcatid.catname
                
                messages.success(request, rmcatnm + " Category Is Delete SuccessFully.")
                return redirect('/adminsideproweb/categorys/')

            else:
                return redirect('/adminsideproweb/categorys/')

        else:
            return redirect('/adminsideproweb/404/')




# ================================================== Brands Class ==================================================
class Brands:

    # ------------------------------------------------- Brands Function -------------------------------------------------
    @login_required(login_url="/adminsideproweb/")
    def all_brands(request):
        employee_profile = getuser(req=request)
        emp_deparement = str(employee_profile.edeparements).lower()

        if emp_deparement == 'administrator' or emp_deparement == 'hr' or emp_deparement == 'manager':

            if request.method == "GET":
                # Get the all categorys
                getallcat = categorys.objects.filter(removestate__exact=0).order_by('catname')

                # Get the all brands
                getallbran = brands.objects.filter(removestate__exact=0)

                allpassbrand = {
                    'getallbrands' : getallbran,
                    'getallcat' : getallcat,
                    'employee_profile' : employee_profile,
                }

                return render(request, "adminfiles/brands/brands.html", allpassbrand)

            # New Brands Create
            elif request.method == "POST":
                brcat = request.POST['brCategory']
                brname = request.POST['brName']
                brdesc = request.POST['brDescription']

                if brcat == "" or brname == "" or brdesc == "":
                    messages.error(request, "Please! Enter the values into filed")
                    return redirect('/adminsideproweb/brands/')

                else:
                    getcategory = categorys.objects.filter(catname=brcat)
                    checkcatbr = brands.objects.filter(cid = getcategory[0].cid, bname = brname)
                    if checkcatbr.exists():
                        messages.error(request, "Sorry! This Category And Brand Is Allready Exists!")
                        return redirect('/adminsideproweb/brands/')

                    else:
                        newbra = brands.objects.create(cid_id=getcategory[0].cid, bname=brname, bdescription = brdesc)
                        newbra.save()
                        messages.success(request, "Create New Brand SuccessFully")
                        return redirect('/adminsideproweb/brands/')

            else:
                return redirect('/adminsideproweb/brands/')

        else:
            return redirect('/adminsideproweb/404/')


    # ------------------------------------------------- Edit Brands Function -------------------------------------------------
    @login_required(login_url="/adminsideproweb/")
    def brands_data_edit(request):
        employee_profile = getuser(req=request)
        emp_deparement = str(employee_profile.edeparements).lower()

        if emp_deparement == 'administrator' or emp_deparement == 'hr' or emp_deparement == 'manager':

            if request.method == "GET":
                try:
                    global getbid
                    getbid = request.GET.get('getbid')

                    getcatdata = list(categorys.objects.filter(removestate__exact=0).values('catname').order_by('catname'))
                    getbranddata = brands.objects.get(bid=getbid, removestate=0)
                    getbcatname = str(getbranddata.cid)

                    brandata = json.dumps ({
                        'cname' : getcatdata,
                        'bname' : getbranddata.bname,
                        'bcatname' : getbcatname,
                        'bdesc' : getbranddata.bdescription,
                    })

                    return HttpResponse(brandata, content_type='application/json')
                except:
                    return redirect('/adminsideproweb/brands/')

            elif request.method == "POST":
                bcname = request.POST['bcatname']
                bname = request.POST['nbranname']
                bdesc = request.POST['nbranddescription']

                getcatid = categorys.objects.get(catname=bcname)

                changebrand = brands.objects.get(bid = getbid)
                changebrand.cid_id = getcatid.cid
                changebrand.bname = bname
                changebrand.bdescription = bdesc
                changebrand.bdate = today
                changebrand.save()

                messages.success(request, bname + ' Brand Is Update SuccessFully.')
                return redirect('/adminsideproweb/brands/')

            else:
                return redirect("/adminsideproweb/brands/")

        else:
            return redirect('/adminsideproweb/404/')



    # ------------------------------------------------- Remove Brands Function -------------------------------------------------
    @login_required(login_url="/adminsideproweb/")
    def brands_data_remove(request):
        employee_profile = getuser(req=request)
        emp_deparement = str(employee_profile.edeparements).lower()

        if emp_deparement == 'administrator' or emp_deparement == 'hr' or emp_deparement == 'manager':
            if request.method == "GET":
                try:
                    global getbid
                    getbid = request.GET.get('getrbid')
                    getrbrand = brands.objects.get(bid=getbid)

                    removebranddata = json.dumps({
                        'rmbrand' : getrbrand.bname
                    })
                    return HttpResponse(removebranddata, content_type="application/json")

                except:
                    return redirect('/adminsideproweb/brands/')

            elif request.method == "POST":
                # Brand Remove
                getrbrand = brands.objects.get(bid=getbid)
                getrbrand.removestate = 1
                getrbrand.brmdate = today
                getrbrand.save()

                # Product Remove
                products.objects.filter(bid=getbid).update(removestate=1, prormdate=today)
                brandname = getrbrand.bname
                messages.success(request, brandname + " Brand Is Delete SuccessFully.")
                return redirect('/adminsideproweb/brands/')

            else:
                return redirect('/adminsideproweb/brands/')

        else:
            return redirect('/adminsideproweb/404/')




# ================================================== Users Class ==================================================
class allUsers:

    # ------------------------------------------------- Users Function -------------------------------------------------
    @login_required(login_url="/adminsideproweb/")
    def users(request):
        employee_profile = getuser(req=request)
        emp_deparement = str(employee_profile.edeparements).lower()

        if emp_deparement == 'administrator' or emp_deparement == 'hr' or emp_deparement == 'manager':

            if request.method == "GET":
                allusers = userprofile.objects.raw('SELECT * FROM auth_user AS au INNER JOIN webadminsiteapp_userprofile as wu ON au.id = wu.user_id WHERE wu.removestate=0')

                alluserdata = {
                    'employee_profile' : employee_profile,
                    'allsetuser' : allusers,
                }

                return render(request, 'adminfiles/users/users.html', alluserdata)

            else:
                return redirect('/adminsideproweb/users/')

        else:
            return redirect('/adminsideproweb/404/')



    # ------------------------------------------------- Users Details Show Function -------------------------------------------------
    @login_required(login_url="/adminsideproweb/")
    def user_data_show(request):
        employee_profile = getuser(req=request)
        emp_deparement = str(employee_profile.edeparements).lower()

        if emp_deparement == 'administrator' or emp_deparement == 'hr' or emp_deparement == 'manager':
            if request.method == 'GET':
                try:
                    uid = request.GET.get('userid')

                    allusers = userprofile.objects.raw('SELECT * FROM auth_user AS au INNER JOIN webadminsiteapp_userprofile as wu ON au.id = wu.user_id WHERE wu.user_id = %s', params=[uid])

                    for guser in allusers:
                        us = guser.username
                        em = guser.email
                        fname = guser.firstname
                        lname = guser.lastname
                        phone = guser.phone
                        dob = guser.dob
                        gender = guser.gender
                        city = guser.city
                        state = guser.state
                        country = guser.country
                        uimage = guser.profileimage.url


                    data = json.dumps({
                        'username' : us,
                        'email' : em,
                        'firstname' : fname,
                        'lastname' : lname,
                        'phone' : phone,
                        'dob' : dob,
                        'gender' : gender,
                        'city' : city,
                        'state' : state,
                        'country' : country,
                        'profileimage' : uimage,
                    })

                    return HttpResponse(data, content_type='application/json')

                except:
                    return redirect('/adminsideproweb/users/')

            else:
                return redirect('/adminsideproweb/users/')

        else:
            return redirect('/adminsideproweb/404/')



    # ------------------------------------------------- Remove User Function -------------------------------------------------
    @login_required(login_url="/adminsideproweb/")
    def user_data_remove(request):
        employee_profile = getuser(req=request)
        emp_deparement = str(employee_profile.edeparements).lower()

        if emp_deparement == 'administrator' or emp_deparement == 'hr' or emp_deparement == 'manager':
            if request.method == "GET":
                try:
                    global getruserid, getusernm
                    getruserid = request.GET.get('ruserid')
                    getusernm = User.objects.get(id = getruserid)

                    rUserData = json.dumps ({
                        'rusername' : getusernm.username
                    })

                    return HttpResponse(rUserData, content_type="application/json")

                except:
                    return redirect('/adminsideproweb/users/')

            elif request.method == "POST":
                ruser = userprofile.objects.get(user=getruserid, removestate=0)
                ruser.removestate = 1
                ruser.rmuserdate = today
                ruser.save()

                messages.success(request, getusernm.username + " User Is Delete SuccessFully.")
                return redirect('/adminsideproweb/users/')

            else:
                return redirect('/adminsideproweb/users/')

        else:
            return redirect('/adminsideproweb/404/')




# ================================================== Employees Class ==================================================
class Employees:

    # ------------------------------------------------- Employees Function -------------------------------------------------
    @login_required(login_url='/adminsideproweb/')
    def employees(request):
        employee_profile = getuser(req=request)
        emp_deparement = str(employee_profile.edeparements).lower()

        if emp_deparement == 'administrator' or emp_deparement == 'hr' or emp_deparement == 'manager':
            if request.method == "GET":
                allemps = employees.objects.raw('SELECT * FROM auth_user AS au INNER JOIN webadminsiteapp_employees AS we ON au.id = we.eid_id WHERE we.removestate = 0')

                allemployeesdata = {
                    'employee_profile' : employee_profile,
                    'allsetemp' : allemps
                }

                return render(request, 'adminfiles/employees/employees.html', allemployeesdata)

            elif request.method == "POST":
                ueid = request.POST['uempid']
                getempdata = employees.objects.get(eid=ueid)
                getusertdata = User.objects.get(id=ueid) 

                uefname = request.POST['uefirstname']
                uelname = request.POST['uelastname']
                ueusername = request.POST['ueusername']
                ueemail = request.POST['ueemail']
                uephone = request.POST['uephone']
                uedob = request.POST['uedob']
                uegender = request.POST['uegender']
                uesalary = request.POST['uesalary']
                uedep = request.POST['uedeparement']
                ueaddr = request.POST['ueaddress']
                uecity = request.POST['uecity']
                uestate = request.POST['uestate']
                uecountry = request.POST['uecountry']


                if request.FILES.get('ueprofile') == None:
                    oldimage = getempdata.profileimage
                    Employees.empupchange(getempdata, getusertdata, oldimage, uefname, uelname, ueusername, ueemail, uephone, uedob, uegender, uedep, ueaddr, uecity, uestate, uecountry, uesalary)


                elif request.FILES.get('ueprofile') != None:
                    newimage = request.FILES.get('ueprofile')
                    Employees.empupchange(getempdata, getusertdata, newimage, uefname, uelname, ueusername, ueemail, uephone, uedob, uegender, uedep, ueaddr, uecity, uestate, uecountry, uesalary)

                messages.success(request, uefname + " Record Update SuccessFully.")
                return redirect('/adminsideproweb/employees/')

            else:
                return redirect('/adminsideproweb/employees/')

        else:
            return redirect('/adminsideproweb/404/')

    # Employee Record Update Function
    def empupchange(*empdata):
        empdata[0].profileimage = empdata[2]
        empdata[0].efirstname = empdata[3]
        empdata[0].elastname = empdata[4]
        empdata[0].ephone = empdata[7]
        empdata[0].edob = empdata[8]
        empdata[0].egender = empdata[9]
        empdata[0].edeparements = empdata[10]
        empdata[0].eaddress = empdata[11]
        empdata[0].city = empdata[12]
        empdata[0].state = empdata[13]
        empdata[0].country = empdata[14]
        empdata[0].salary = empdata[15]
        empdata[0].save()

        empdata[1].username = empdata[5]
        empdata[1].email = empdata[6]
        empdata[1].save()


    # ------------------------------------------------- Employee Fectch Record In AJAX Employees Function -------------------------------------------------
    @login_required(login_url="/adminsideproweb/")
    def employee_data_edit(request):
        employee_profile = getuser(req=request)
        emp_deparement = str(employee_profile.edeparements).lower()

        if emp_deparement == 'administrator' or emp_deparement == 'hr' or emp_deparement == 'manager':

            if request.method == "GET":
                try:
                    geid = request.GET.get('empid')
                    getempdata = employees.objects.raw('SELECT * FROM auth_user AS au INNER JOIN webadminsiteapp_employees AS we ON au.id = we.eid_id WHERE we.eid_id = %s', params=[geid])

                    for empdata in getempdata:
                        efname = empdata.efirstname
                        elname = empdata.elastname
                        eusername = empdata.username
                        eemail = empdata.email
                        ephone = empdata.ephone
                        edob = empdata.edob
                        egender = empdata.egender
                        esalary = empdata.salary
                        eaddr = empdata.eaddress
                        edep = empdata.edeparements
                        ecity = empdata.city
                        estate = empdata.state
                        ecountry = empdata.country
                        eimage = empdata.profileimage.url


                    empdata = json.dumps({
                        'efirstname' : efname,
                        'elastname' : elname,
                        'eusername' : eusername,
                        'eemail' : eemail,
                        'ephone' : ephone,
                        'edob' : edob,
                        'egender' : egender,
                        'esalary' : esalary,
                        'eaddr' : eaddr,
                        'edep' : edep,
                        'ecity' : ecity,
                        'estate' : estate,
                        'ecountry' : ecountry,
                        'eproimage' : eimage,
                    })

                    return HttpResponse(empdata, content_type='application/json')

                except:
                    return redirect('/adminsideproweb/employees/')

            else:
                return redirect('/adminsideproweb/employees/')

        else:
            return redirect('/adminsideproweb/404/')


    # ------------------------------------------------- Employee Remove Record In AJAX Employees Function -------------------------------------------------
    @login_required(login_url="/adminsideproweb/")
    def employee_data_remove(request):
        employee_profile = getuser(req=request)
        emp_deparement = str(employee_profile.edeparements).lower()

        if emp_deparement == 'administrator' or emp_deparement == 'hr' or emp_deparement == 'manager':

            if request.method == "GET":
                try:
                    global rmempid, rmempnm
                    rmempid = request.GET.get('rmempid')
                    rmempnm = User.objects.get(id = rmempid)

                    remployeedata = json.dumps ({
                        'rmemployeenm' : rmempnm.username
                    })

                    return HttpResponse(remployeedata, content_type="application/json")

                except:
                    return redirect('/adminsideproweb/employees/')

            elif request.method == "POST":
                rmemp = employees.objects.get(eid = rmempid)
                rmemp.removestate = 1
                rmemp.rmempdate = today
                rmemp.save()

                messages.success(request, rmempnm.username + " Employee Is Delete SuccessFully.")
                return redirect('/adminsideproweb/employees/')

            else:
                return redirect('/adminsideproweb/employees/')

        else:
            return redirect('/adminsideproweb/404/')



    # ------------------------------------------------- New Employees Function -------------------------------------------------
    @login_required(login_url='/adminsideproweb/')
    def new_employees(request):
        employee_profile = getuser(req=request)
        emp_deparement = str(employee_profile.edeparements).lower()

        if emp_deparement == 'administrator' or emp_deparement == 'hr' or emp_deparement == 'manager':

            if request.method == "GET":  
                return render(request, 'adminfiles/employees/newEmployee.html')

            elif request.method == "POST":
                empfname = request.POST['empFirstname']
                emplname = request.POST['empLastname']
                empusername = request.POST['empUsername']
                empemail = request.POST['empEmail']
                empmobile = request.POST['empMobile']
                empsalary = request.POST['empSalary']
                empaddress = request.POST['empAddress']
                empdob = request.POST['empDob']
                empcity = request.POST['empCity']
                empstate = request.POST['empState']
                empcountry = request.POST['empCountry']
                gender = request.POST['empGender']
                deparement = request.POST['empDeparement']
                emphiredate = request.POST['empJoinDate']

                if len(empusername) <= 8 :
                    messages.error(request, 'Please, Enter The 8 Characture Username')
                    return redirect('/adminsideproweb/new employee/')

                else:

                    # Auto Generate Password
                    autopassword = generatcode(12)

                    if User.objects.filter(email = empemail).exists():
                        messages.error(request, 'This Email Address Allready Exists!')
                        return redirect('/adminsideproweb/new employee/')

                    elif User.objects.filter(username = empusername).exists():
                        messages.error(request, 'This Username Allready Exists!')
                        return redirect('/adminsideproweb/new employee/')

                    else:
                        newEmpUser = User.objects.create_user(username=empusername, email=empemail, password=autopassword)
                        newEmpUser.save()

                        user_new_emp = User.objects.get(username=empusername)
                        empprofile = employees.objects.create(eid = user_new_emp, efirstname = empfname, elastname = emplname, ephone = empmobile, edob = empdob, egender = gender, eaddress = empaddress, edeparements = deparement, salary=empsalary, city = empcity, state = empstate, country = empcountry, ehiredate=emphiredate)
                        empprofile.save()

                        sendUserMail(empemail, 'common/email/newEmployeeMail.html', f'{empusername} is your joining letter from King Shopping Company', autopassword).start()

                        messages.success(request, "New Employee Create SuccessFully")

                        return redirect('/adminsideproweb/employees/')


            else:
                return redirect('/adminsideproweb/employees/')

        else:
            return redirect('/adminsideproweb/404/')




# ================================================== Orders Class ==================================================
class Orders:

    # ------------------------------------------------- Orders Function -------------------------------------------------
    @login_required(login_url='/adminsideproweb/')
    def orders(request):
        if request.method == "GET":
            employee_profile = getuser(req=request)
            orderprocess = ['conform', 'shipped', 'outofdelivery', 'delived']
            orderdata = products.objects.raw('SELECT * FROM webadminsiteapp_orders AS wo INNER JOIN webadminsiteapp_userprofile AS wu ON wo.user_id = wu.user_id INNER JOIN webadminsiteapp_products AS wp ON wo.proid_id = wp.proid INNER JOIN webadminsiteapp_useraddress AS wa ON wo.deliaddr_id = wa.addid WHERE wo.removestate=0 AND wo.returnpro = "No" AND wo.productstatus IN %s', params=[orderprocess])

            odata = {
                'orderRecords' : orderdata,
                'employee_profile' : employee_profile,
            }

            return render(request, 'adminfiles/orders/orders.html', odata)

        elif request.method == "POST":
            getoid = request.POST['orderid']
            getprostatus = request.POST['orproductstatus']

            orderchange = orders.objects.get(oid=getoid)
            useremail = User.objects.filter(id=orderchange.user_id)
            product = products.objects.filter(proid=orderchange.proid_id)
            getaddress = useraddress.objects.filter(addid=orderchange.deliaddr_id)

            totalprice = product[0].proprice * orderchange.proqty

            if orderchange.productstatus != "delived" or orderchange.returnpro != "Return":
                orderchange.productstatus = getprostatus
                orderchange.save()

                if getprostatus == "shipped":
                    productMail(
                        senduser = useremail[0].email,
                        template = 'common/email/orderProcess/shippedOrder.html',
                        mail_subject = f'{product[0].proname}.. from your order has been shipped',
                        orderid = orderchange.oid,
                        orderdate = orderchange.ordate,
                        product_name = product[0].proname,
                        delivery_address = getaddress[0].adddescription,
                        proprice = product[0].proprice,
                        product_qty = orderchange.proqty,
                        delivery_date = orderchange.deliveddate,
                        totalprice = totalprice
                    ).start()

                elif getprostatus == "outofdelivery":
                    productMail(
                        senduser = useremail[0].email,
                        template = 'common/email/orderProcess/outofdeliveryOrder.html',
                        mail_subject = f'{product[0].proname}.. from your order has been out of delivery',
                        orderid = orderchange.oid,
                        orderdate = orderchange.ordate,
                        product_name = product[0].proname,
                        delivery_address = getaddress[0].adddescription,
                        proprice = product[0].proprice,
                        product_qty = orderchange.proqty,
                        delivery_date = orderchange.deliveddate,
                        totalprice = totalprice
                    ).start()


                elif getprostatus == "delived":
                    productMail(
                        senduser = useremail[0].email,
                        template = 'common/email/orderProcess/deliveredOrder.html',
                        mail_subject = f'{product[0].proname}.. from your order has been delived',
                        orderid = orderchange.oid,
                        orderdate = orderchange.ordate,
                        product_name = product[0].proname,
                        delivery_address = getaddress[0].adddescription,
                        proprice = product[0].proprice,
                        product_qty = orderchange.proqty,
                        delivery_date = orderchange.deliveddate,
                        totalprice = totalprice
                    ).start()
                    

                else:
                    messages.warning(request, 'Sorry, Product Proccess Is Not Change.')
                    return redirect('/adminsideproweb/orders/')

                messages.success(request, 'Product Proccess Is Change SuccessFully.')
                return redirect('/adminsideproweb/orders/')

            elif orderchange.productstatus == "delived" or orderchange.returnpro == "No":
                messages.success(request, 'Your Product Is All Ready Delived.')
                return redirect('/adminsideproweb/orders/')

            elif orderchange.productstatus == "cancel" or orderchange.returnpro == "No":
                messages.success(request, 'Sorry, This Order Is Cancel.')
                return redirect('/adminsideproweb/orders/')

            else:
                messages.success(request, 'Your Product Is All Ready Delived.')
                return redirect('/adminsideproweb/orders/')

        else:
            return redirect('/adminsideproweb/orders/')


    # ------------------------------------------------- Cancel Orders Function -------------------------------------------------
    @login_required(login_url='/adminsideproweb/')
    def order_data_edit(request):
        if request.method == "GET":
            try:
                getoid = request.GET.get('soid')

                orderdata = orders.objects.get(oid=getoid)

                orderdate = orderdata.ordate.strftime('%Y-%m-%d')

                getprodata = products.objects.get(proid=orderdata.proid_id)
                getusers = userprofile.objects.get(user=orderdata.user_id)
                getaddress = useraddress.objects.get(addid=orderdata.deliaddr_id)

                product_more_details_url = f'/adminsideproweb/products/edit/?proname={getprodata.proname}&procat={getprodata.cid}&probrand={getprodata.bid}&procolor={getprodata.procolorname}'

                eodata = json.dumps({
                    'orderdate' : str(orderdate),
                    'ordercenceldate' : str(orderdata.canceldate),
                    'deliverydate' : str(orderdata.deliveddate),
                    'returndate' : str(orderdata.returndate),
                    'oid' : getoid,
                    'prostatus' : orderdata.productstatus,
                    'productid' : str(getprodata.proid),
                    'product' : getprodata.proname,
                    'productimage' : getprodata.proimage1.url,
                    'totalprice' : getprodata.proprice * orderdata.proqty,
                    'procolorname' : getprodata.procolorname,
                    'proqty' : orderdata.proqty,
                    'fullname' : getusers.firstname + " " + getusers.lastname,
                    'phone' : getusers.phone,
                    'userstate' : getusers.state,
                    'delivery' : getaddress.adddescription,
                    'prorestatus' : orderdata.returnpro,
                    'productUrl': product_more_details_url,
                })

                return HttpResponse(eodata, content_type="application/json")

            except:
                return redirect('/adminsideproweb/orders/')

        else:
            return redirect('/adminsideproweb/orders/')


    # ------------------------------------------------- Cancel Orders Function -------------------------------------------------
    @login_required(login_url="/adminsideproweb/")
    def cancel_orders(request):
        employee_profile = getuser(req=request)
        emp_deparement = str(employee_profile.edeparements).lower()

        if emp_deparement == 'administrator' or emp_deparement == 'hr' or emp_deparement == 'manager' or emp_deparement == "employee":
            if request.method == "GET":
                orderprocess = ['cancel']
                orderdata = products.objects.raw('SELECT * FROM webadminsiteapp_orders AS wo INNER JOIN webadminsiteapp_userprofile AS wu ON wo.user_id = wu.user_id INNER JOIN webadminsiteapp_products AS wp ON wo.proid_id = wp.proid INNER JOIN webadminsiteapp_useraddress AS wa ON wo.deliaddr_id = wa.addid WHERE wo.productstatus IN %s', params=[orderprocess])

                odata = {
                    'orderRecords' : orderdata,
                    'employee_profile' : employee_profile,
                }

                return render(request, 'adminfiles/orders/cancel_orders.html', odata)

            else:
                return redirect('/adminsideproweb/cancel orders/')

        else:
            return redirect('/adminsideproweb/404/')




# ================================================== Product Class ==================================================
class Others:

    # ------------------------------------------------- Banners Function -------------------------------------------------
    @login_required(login_url="/adminsideproweb/")
    def banner(request):
        employee_profile = getuser(req=request)
        emp_deparement = str(employee_profile.edeparements).lower()

        if emp_deparement == 'administrator' or emp_deparement == 'hr' or emp_deparement == 'manager':

            if request.method == "GET":
                productdata = products.objects.filter(removestate=0).order_by('proname')
                # Get all banners
                getbanners = banners.objects.filter(removestate=0)

                bannerdata = {
                    'products' : productdata,
                    'banners' : getbanners,
                    'employee_profile' : employee_profile,
                }

                return render(request, 'adminfiles/others/banners.html', bannerdata)

            elif request.method == "POST":
                productname = request.POST['productName']
                bimage = request.FILES.get('banneruploadimage')

                if productname != "":
                    getproid = products.objects.get(proname=productname, removestate=0)
                    newbanner = banners.objects.create(bannerImage=bimage, proid_id=getproid.proid)
                    newbanner.save()
                    messages.success(request, "Banner Is Saved Successfully.")
                    return redirect('/adminsideproweb/banner/')
                else:
                    messages.error(request, "Please, Select The Product Name")
                    return redirect('/adminsideproweb/banner/')

            else:
                return redirect('/adminsideproweb/banner/')

        else:
            return redirect('/adminsideproweb/404/')


    # ------------------------------------------------- Notifications Function -------------------------------------------------
    @login_required(login_url="/adminsideproweb/")
    def bannerRemove(request):
        employee_profile = getuser(req=request)
        emp_deparement = str(employee_profile.edeparements).lower()

        if emp_deparement == 'administrator' or emp_deparement == 'hr' or emp_deparement == 'manager':
            if request.method == "GET":
                try:
                    rmbannerid = request.GET.get('bannerid')
                    countbanner = banners.objects.filter(removestate=0).count()

                    if countbanner == 1: 
                        messages.warning(request, "Sorry! minimum one banner is required.")
                        return HttpResponse()

                    else:
                        getbanner = banners.objects.get(bannerid=rmbannerid, removestate=0)
                        getbanner.removestate = 1
                        getbanner.save()
                        messages.success(request, "Banner Is Removed Successfully.")
                        return HttpResponse()

                except:
                    return redirect('/adminsideproweb/banner/')

            else:
                return redirect('/adminsideproweb/banner/')

        else:
            return redirect('/adminsideproweb/404/')



    # ------------------------------------------------- Notifications Function -------------------------------------------------
    @login_required(login_url="/adminsideproweb/")
    def notifications(request):
        employee_profile = getuser(req=request)
        emp_deparement = str(employee_profile.edeparements).lower()

        if emp_deparement == 'administrator' or emp_deparement == 'hr' or emp_deparement == 'manager' or emp_deparement == "employee":

            if request.method == "GET":
                # Get User Issues
                getissues = customerissues.objects.order_by('idate')

                notificationdata = {
                    'allissues' : getissues,
                    'employee_profile' : employee_profile,
                }
                return render(request, 'adminfiles/others/notification.html', notificationdata)

            else:
                return redirect('/adminsideproweb/notification/')

        else:
            return redirect('/adminsideproweb/404/')


    # ------------------------------------------------- Notifications Function -------------------------------------------------
    @login_required(login_url="/adminsideproweb/")
    def notifications_edit(request):
        employee_profile = getuser(req=request)
        emp_deparement = str(employee_profile.edeparements).lower()

        if emp_deparement == 'administrator' or emp_deparement == 'hr' or emp_deparement == 'manager' or emp_deparement == 'employee':

            if request.method == "GET":
                try:
                    notid = request.GET.get('notid')
                    notdata = customerissues.objects.filter(issuesid=notid)
                    notedata = json.dumps({
                        'nottitle' : notdata[0].issueshort,
                        'notissues' : notdata[0].issues,
                        'notdate' : str(notdata[0].idate),
                        'notuser' : str(notdata[0].user),
                    })
                    return HttpResponse(notedata, content_type='application/json')

                except:
                    return redirect('/adminsideproweb/notification/')

            else:
                return redirect('/adminsideproweb/notification/')

        else:
            return redirect('/adminsideproweb/404/')


    # ------------------------------------------------- Notifications Function -------------------------------------------------
    @login_required(login_url="/adminsideproweb/")
    def headerbar_search(request):
        if request.method == 'POST':
            searchvalue = request.POST['searchValue']
            return redirect(f'/adminsideproweb/{searchvalue}')

        else:
            return redirect('/adminsideproweb/dashboard/')


# ================================================== Settings Class ==================================================
class Settings:

    # ------------------------------------------------- Settings Function -------------------------------------------------
    @login_required(login_url="/adminsideproweb/")
    def settings(request):
        if request.method == "GET":
            employeeprofile = getuser(req=request)
            return render(request, 'adminfiles/others/settings.html',{'employee_profile' : employeeprofile})

        else:
            return redirect('/adminsideproweb/settings/')


    # ------------------------------------------------- General Tab In Settings Function -------------------------------------------------
    @login_required(login_url="/adminsideproweb/")
    def general_settings(request):  
        if request.method == "GET":
            employee_profile = getuser(req=request)
            user_object = User.objects.get(username=request.user.username)
            getempdata = employees.objects.get(eid=user_object)

            generaldata = {
                'userob' : user_object,
                'userdata' : getempdata,
                'employee_profile' : employee_profile,
            }

            return render(request, 'adminfiles/others/settings/general.html', generaldata)

        elif request.method == "POST":
            efname = request.POST['empfirstname']
            elname = request.POST['emplastname']
            egender = request.POST['empgender']
            edob = request.POST['empdob']
            eusername = request.POST['empusername']
            eemail = request.POST['empemail']
            ephone = request.POST['empphone']
            ecity = request.POST['empcity']
            estate = request.POST['empstate']
            ecountry = request.POST['empcountry']

            # Employee profile in Change Username After Check Username
            if user_object.username != eusername:
                if User.objects.filter(username = eusername).exists():
                    messages.error(request, 'This Username Allready Exists!')

                else:
                    if request.FILES.get('empimage') == None:
                        image = getempdata.profileimage
                        Settings.employeeProfileUpdate(request=request, userobject = user_object, employeeprofile=getempdata, fname=efname, lname=elname, image=image, username=eusername, email=eemail, phone=ephone, dob=edob,  gender=egender, city=ecity, state=estate, country=ecountry)

                    
                    elif request.FILES.get('empimage') != None:
                        image = request.FILES.get('empimage')
                        Settings.employeeProfileUpdate(request=request, userobject = user_object, employeeprofile=getempdata, fname=efname, lname=elname, image=image, username=eusername, email=eemail, phone=ephone, dob=edob,  gender=egender, city=ecity, state=estate, country=ecountry)

            # Employee profile in Change Email Address After Check Email Address
            elif user_object.email != eemail:
                if User.objects.filter(email = eemail).exists():
                    messages.error(request, 'This Email Address Allready Exists!')

                else:
                    if request.FILES.get('empimage') == None:
                        image = getempdata.profileimage
                        Settings.employeeProfileUpdate(request=request, userobject = user_object, employeeprofile=getempdata, fname=efname, lname=elname, image=image, username=eusername, email=eemail, phone=ephone, dob=edob,  gender=egender, city=ecity, state=estate, country=ecountry)

                    
                    elif request.FILES.get('empimage') != None:
                        image = request.FILES.get('empimage')
                        Settings.employeeProfileUpdate(request=request, userobject = user_object, employeeprofile=getempdata, fname=efname, lname=elname, image=image, username=eusername, email=eemail, phone=ephone, dob=edob,  gender=egender, city=ecity, state=estate, country=ecountry)

            # Employee profile not changed username and email address after any other change
            else:
                if request.FILES.get('empimage') == None:
                    image = getempdata.profileimage
                    Settings.employeeProfileUpdate(request=request, userobject = user_object, employeeprofile=getempdata, fname=efname, lname=elname, image=image, username=eusername, email=eemail, phone=ephone, dob=edob,  gender=egender, city=ecity, state=estate, country=ecountry)

                    
                elif request.FILES.get('empimage') != None:
                    image = request.FILES.get('empimage')
                    Settings.employeeProfileUpdate(request=request, userobject = user_object, employeeprofile=getempdata, fname=efname, lname=elname, image=image, username=eusername, email=eemail, phone=ephone, dob=edob,  gender=egender, city=ecity, state=estate, country=ecountry)

        else:
            return redirect('/adminsideproweb/settings/general/')


    # Employee Profile Update Method
    def employeeProfileUpdate(**uppro):
        ep = uppro['employeeprofile']
        eu = uppro['userobject']


        ep.profileimage = uppro['image']
        ep.efirstname = uppro['fname']
        ep.elastname = uppro['lname']
        ep.ephone = uppro['phone']
        ep.edob = uppro['dob']
        ep.egender = uppro['gender']
        ep.city = uppro['city']
        ep.state = uppro['state']
        ep.country = uppro['country']
        ep.save()

        eu.username = uppro['username']
        eu.email = uppro['email']
        eu.save()

        messages.success(uppro['request'], "Your Profile Is Update Successfully.")
        return redirect('/adminsideproweb/settings/general/')


    # ------------------------------------------------- Restore Tab In Settings Function -------------------------------------------------
    @login_required(login_url="/adminsideproweb/")
    def restore_settings(request):
        employee_profile = getuser(req=request)
        emp_deparement = str(employee_profile.edeparements).lower()

        if emp_deparement == 'administrator' or emp_deparement == 'hr' or emp_deparement == 'manager':

            if request.method == "GET":

                # Models (Tables) Name
                modal = [categorys, brands, products, employees, banners]

                # Tables Convet after store in smodal
                smodal = []

                # remove records table name store in rmodals
                rmodals = []

                for checkmodal in modal:
                    rmmodal = checkmodal.objects.filter(removestate__exact = 1)
                    if rmmodal.exists():
                        cnstr = str(checkmodal)
                        rmodals.append(cnstr[31:-2])

                    cnstr = str(checkmodal)
                    smodal.append(cnstr[31:-2])

                bincategoryrecords = categorys.objects.filter(removestate=1)
                binbrandsrecords = brands.objects.filter(removestate=1)
                binproductsrecords = products.objects.filter(removestate=1)
                binemprecords = employees.objects.filter(removestate=1)
                binbannerecords = banners.objects.filter(removestate=1)


                removemodal = {
                    'modals' : smodal,
                    'rmodals' : rmodals,
                    'employee_profile' : employee_profile,
                    'removecategory' : bincategoryrecords,
                    'removebrands' : binbrandsrecords,
                    'removeproducts' : binproductsrecords,
                    'removeemp' : binemprecords,
                    'removebanners' : binbannerecords,
                }

                return render(request, 'adminfiles/others/settings/restore.html', removemodal)

            else:
                return redirect('/adminsideproweb/404/')

        else:
            return redirect('/adminsideproweb/404/')


    # ------------------------------------------------- Bin Featch Records In Settings Function -------------------------------------------------
    @login_required(login_url="/adminsideproweb/")
    def restore_record_settings(request):
        if request.method == "GET":
            employee_profile = getuser(req=request)
            emp_deparement = str(employee_profile.edeparements).lower()

            if emp_deparement == 'administrator' or emp_deparement == 'hr' or emp_deparement == 'manager':
                try:
                    bintable = request.GET.get('bintable')
                    restoredata = request.GET.get('restore')

                    if bintable == "categorys":
                        checkcat = categorys.objects.filter(cid=restoredata, removestate=1)
                        if checkcat.exists():
                            categorys.update(removestate=0)
                            messages.success(request, "Category Is Restore SuccessFully.")

                        else:
                            messages.error(request, "Sorry! Category Is Not Restore.")

                    elif bintable == "brands":
                        getbrandid = brands.objects.get(bid=restoredata, removestate=1)
                        checkcat = categorys.objects.filter(cid=getbrandid.cid_id, removestate=0)

                        if checkcat.exists():
                            brands.update(removestate=0)
                            messages.success(request, "Brand Is Restore SuccessFully.")

                        else:
                            messages.error(request, "Sorry! Brand Is Not Restore.")

                    elif bintable == "products":
                        getproduct = products.objects.get(proid=restoredata, removestate=1)
                        getbrand = brands.objects.filter(bid=getproduct.bid_id, removestate=0)

                        if getbrand.exists():
                            getcategory = categorys.objects.filter(cid=getbrand[0].cid_id, removestate=0)

                            if getcategory.exists():
                                getproduct.removestate = 0
                                getproduct.save()
                                messages.success(request, "Product Is Restore SuccessFully.")

                            else:
                                messages.error(request, "Sorry! Category Is Not Found.")

                        else:
                            messages.error(request, "Sorry! Brand Is Not Found.")


                    elif bintable == "employees":
                        checkemp = employees.objects.filter(eid_id=restoredata, removestate=1)
                        if checkemp.exists():
                            employees.objects.filter(eid=restoredata, removestate=1).update(removestate=0)
                            messages.success(request, "Employee Is Restore SuccessFully.")
                        else:
                            messages.error(request, "Sorry! Employee Is Not Restore.")

                    elif bintable == "banners":
                        checkbanner = banners.objects.filter(bannerid=restoredata, removestate=1)
                        if checkbanner.exists():
                            checkbanner.update(removestate=0)
                            messages.success(request, "Banner Is Restore SuccessFully.")
                        else:
                            messages.error(request, "Sorry! Banner Is Not Restore.")

                    return HttpResponse()

                except:
                    return redirect('/adminsideproweb/settings/restore/')

            else:
                return redirect('/adminsideproweb/404/')

        else:
            return redirect('/adminsideproweb/settings/restore/')



    # ------------------------------------------------- Change Password In Settings Function -------------------------------------------------
    @login_required(login_url="/adminsideproweb/")
    def security_settings(request):
        if request.user.is_authenticated:
            if request.method == "GET":
                employee_profile = getuser(req=request)
                user_object = User.objects.get(username=request.user.username)

                # Change The Email Address *****@Gmail.com
                loginuseremail = user_object.email
                res = loginuseremail[2 : loginuseremail.find('@')]
                useremail = loginuseremail.replace(res, '****')

                # Check Two Step Verification
                checktwostep = employees.objects.get(eid=user_object, removestate = 0)

                sdata = {
                    'login_user' : user_object,
                    'twostep' : checktwostep.etwostepauthonetication,
                    'useremail' : useremail,
                    'employee_profile' : employee_profile,
                }

                return render(request, 'adminfiles/others/settings/security.html', sdata)

            elif request.method == "POST":
                getoldps = request.POST['oldpassword']
                getnewps = request.POST['newpassword']
                getreps = request.POST['repassword']

                try:
                    user_object.check_password(getoldps)
                except:
                    messages.error(request, 'Please, create new password.')
                    return redirect('/adminsideproweb/settings/security/')

                if getnewps == getreps:
                    user_object.set_password(getnewps)
                    user_object.save()
                    auth.authenticate(username=user_object, password=getnewps)
                    messages.success(request, 'Password update successfully.')
                    return redirect('/adminsideproweb/settings/security/')

                else:
                    messages.error(request, 'Sorry! Password is not match!')
                    return redirect('/adminsideproweb/settings/security/')

            else:
                return redirect('/adminsideproweb/settings/security/')




    # ------------------------------------------------- Send OTP In Settings Function -------------------------------------------------
    @login_required(login_url="/adminsideproweb/")
    def securityOTP_settings(request):
        if request.user.is_authenticated:

            if request.method == "GET":
                userval = request.GET.get('uservalue')

                if userval != None:
                    user_object = User.objects.get(username=request.user.username)
                    changepscode = generatcode(6)

                    setuserotp = employees.objects.get(eid_id=user_object.id, removestate=0)
                    getempemail = user_object.email

                    sendUserMail(getempemail, 'common/email/sendcode/resetpassword.html', f'King Shopping Account {changepscode} is your verification code for secure access', changepscode).start()

                    setuserotp.eOTP = changepscode
                    setuserotp.save()

                    t = 60
                    while t: 
                        mins, secs = divmod(t, 60)
                        timer = '{:02d}:{:02d}'.format(mins, secs)
                        print(timer, end="\r")
                        time.sleep(1)
                        t -= 1
                        if(t == 0):
                            setuserotp.eOTP = 0
                            setuserotp.save()

                    return HttpResponse()
                
                else:
                    return redirect('/adminsideproweb/settings/security/')

            else:
                return redirect('/adminsideproweb/settings/security/')


    # ------------------------------------------------- User OTP Check In Settings Function -------------------------------------------------
    @login_required(login_url="/adminsideproweb/")
    def securityOTPcheck_settings(request):
        if request.user.is_authenticated:
            if request.method == "GET":
                user_object = User.objects.get(username=request.user.username)

                getuserotp = request.GET.get('getuserotp')
                gettbotp = employees.objects.get(eid_id=user_object.id, removestate=0)

                checkotp = ""
                if getuserotp == gettbotp.eOTP:
                    checkotp = 1

                else:
                    checkotp = 0

                changedata = json.dumps ({
                    'sdata' : checkotp
                })

                return HttpResponse(changedata, content_type="application/json")

            else:
                return redirect('/adminsideproweb/settings/security/')



    # ------------------------------------------------- Check Email Address In Two Step Verification In Settings Function -------------------------------------------------
    @login_required(login_url="/adminsideproweb/")
    def twostepchekemail(request):
        if request.user.is_authenticated:
            user_object = User.objects.get(username=request.user.username)
            changepscode = generatcode(6)
            
            if request.method == "GET":
                uemail = request.GET.get('uemail')

                setuserotp = employees.objects.get(eid=user_object.id, removestate=0)

                checkuseremail = 0
                if (user_object.email == uemail):
                    sendUserMail(user_object.email, 'common/email/sendcode/twostepcode.html', f'King Shopping Account {changepscode} is your verification code for secure access', changepscode).start()

                    setuserotp.eOTP = changepscode
                    setuserotp.save()
                    checkuseremail = 1

                else:
                    checkuseremail = 0

                sdata = json.dumps({
                    'checkemailstatus':checkuseremail
                })

                return HttpResponse(sdata, content_type="application/json")

            else:
                return redirect('/adminsideproweb/settings/security/')



    # ------------------------------------------------- Two Step On Verification In Settings Function -------------------------------------------------
    @login_required(login_url="/adminsideproweb/")
    def twostepcheckotp(request):
        if request.user.is_authenticated:
            user_object = User.objects.get(username=request.user.username)

            if request.method == "GET":
                getuserotp = request.GET.get('userotp')

                gettbuserotp = employees.objects.get(eid=user_object, removestate=0)

                checkotp = ""

                if getuserotp == gettbuserotp.eOTP:
                    checkotp = 1
                    gettbuserotp.etwostepauthonetication = 1
                    gettbuserotp.eOTP = 0
                    gettbuserotp.save()
                    sendUserMail(user_object.email, 'common/email/twostepon.html', 'Your account has been secured starting with two-step verification', '').start()
                    messages.success(request, "Your Two Step Authontication On Successfully.")

                else:
                    checkotp = 0

                sdata = json.dumps({
                    'status' : checkotp,
                })

                return HttpResponse(sdata, content_type="application/json")

            else:
                return redirect('/adminsideproweb/settings/security/')


    # ------------------------------------------------- Two Step off Verification In Settings Function -------------------------------------------------
    @login_required(login_url="/adminsideproweb/")
    def twosteponoff(request):
        if request.user.is_authenticated:
            user_object = User.objects.get(username=request.user.username)

            if request.method == "POST":
                userpassword = request.POST['userloginpassword']
                user = auth.authenticate(username=user_object, password=userpassword)

                if user is not None:
                    twostepoff = employees.objects.get(eid=user_object, etwostepauthonetication=1, removestate=0)
                    twostepoff.etwostepauthonetication = 0;
                    twostepoff.save()
                    messages.success(request, "Turn Off 2-Step Verification SuccessFully")
                    sendUserMail(user_object.email, 'common/email/twostepoff.html', 'Your account is locked out of secure with two-step verification enabled.', '').start()
                    return redirect('/adminsideproweb/settings/security/')

                else:
                    messages.error(request, "Please, Enter The Currect Password.")
                    return redirect('/adminsideproweb/settings/security/')

            else:
                return redirect('/adminsideproweb/settings/security/')



# ================================================== All Errors Class ==================================================
class All_Errors:

    # ------------------------------------------------- 404 Function -------------------------------------------------
    # Change The Settings.py file
    def error_404_view(request):
        employee_profile = getuser(req=request)
        return render(request, 'adminfiles/others/404.html', {'employee_profile' : employee_profile})



# ------------------------------------------------- Send Code Email Function -------------------------------------------------
class sendUserMail(threading.Thread):

    def __init__(self, sendmail, template, subject, otpnumber):
        self.receive_mail = sendmail
        self.use_template = template
        self.mail_subject = subject
        self.otp_number = otpnumber
        threading.Thread.__init__(self)

    def run(self):
        try:
            getusername = User.objects.get(email = self.receive_mail)
            if len(self.otp_number) != 0:
                html_content = render_to_string(self.use_template, {'username' : getusername, 'mailsubject' : self.mail_subject, 'code' : self.otp_number})
            else:
                html_content = render_to_string(self.use_template, {'username' : getusername, 'mailsubject' : self.mail_subject})

            text_content = strip_tags(html_content)
            email = EmailMultiAlternatives(
                self.mail_subject,
                text_content,
                'kingshopping23@gmail.com',
                [self.receive_mail]
            )
            email.attach_alternative(html_content, "text/html")
            email.send()
            print("Send main")

        except Exception as e:
            print("OTP Mail Not Send", e)

# ------------------------------------------------- Send Product Details Email Function -------------------------------------------------
class productMail(threading.Thread):

    def __init__(self, **MailInfo):
        self.send_user = MailInfo['senduser']
        self.use_template = MailInfo['template']
        self.mail_subject = MailInfo['mail_subject']
        self.order_id = MailInfo['orderid']
        self.order_date = MailInfo['orderdate']
        self.product_name = MailInfo['product_name']
        self.delivery_address = MailInfo['delivery_address']
        self.product_price = MailInfo['proprice']
        self.product_qty = MailInfo['product_qty']
        self.delivery_date = MailInfo['delivery_date']
        self.total_price = MailInfo['totalprice']
        self.today_datetime = today
        threading.Thread.__init__(self)

    def run(self):
        try:
            getusername = User.objects.get(email = self.send_user)
            html_content = render_to_string(self.use_template, {
                'username' : getusername, 
                'mailsubject' : self.mail_subject,
                'orderid': self.order_id, 
                'orderdate': self.order_date,
                'proname': self.product_name,
                'deliveryaddress': self.delivery_address,
                'proprice': self.product_price,
                'proqty': self.product_qty,
                'deliverydate': self.delivery_date,
                'totalprice': self.total_price,
                'todaydatetime': self.today_datetime,
            })

            text_content = strip_tags(html_content)
            email = EmailMultiAlternatives(
                self.mail_subject,
                text_content,
                'kingshopping23@gmail.com',
                [self.send_user]
            )
            email.attach_alternative(html_content, "text/html")
            email.send()


        except Exception as e:
            print("Product Mail is not send",e)


# ------------------------------------------------- Generate The OTP -------------------------------------------------
def generatcode(no):
    generate = [
        '1','2','3','4','5','6','7','8','9','0',
        'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
        'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'
    ]

    gotp = ""
    for x in range(no):
        gotp = gotp + random.choice(generate)[0]
    return gotp



# ------------------------------------------------- Get User Profile -------------------------------------------------
def getuser(**args):
    user_object = User.objects.get(username=args['req'].user.username)
    employee_profile = employees.objects.get(eid=user_object, removestate=0)

    return employee_profile