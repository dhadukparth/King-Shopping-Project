from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from webadminsiteapp.models import *
from django.db.models import *
from django.http import HttpResponse
from datetime import *
import json, random, time, re


# Send Mail
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


from urllib.request import urlopen
today = datetime.now()

import threading


# ================================================= User Action All Function =================================================
class useraction:

    # -------------------------------------------------- New Account Function --------------------------------------------------
    def newaccount(request):
        if request.method == "POST":
            username = request.POST['register-username']
            email = request.POST['register-email']
            password = request.POST['register-password']

            if not bool(re.match("^[A-Za-z]*$", username)):
                messages.error(request, 'Please, Enter The Username Is Only For Letter.')
                return redirect('/')

            elif User.objects.filter(email = email).exists() or email == 'kingshopping23@gmail.com':
                messages.error(request, 'This Email Address Allready Exists!')
                return redirect('/')

            elif User.objects.filter(username = username).exists():
                messages.error(request, 'This Username Allready Exists!')
                return redirect('/')

            elif len(username) <= 8:
                messages.success(request, 'Please, Enter The Username Is Minimum 8 Characture.')
                return redirect('/')

            else:

                if(len(password) >= 8):

                    if(bool(re.findall("[a-z]", password)) == False):
                        messages.error(request, 'Please, Enter Any One Lowercase.')

                    elif(bool(re.findall("[A-Z]", password)) == False):
                        messages.error(request, 'Please, Enter Any One Uppercase.')

                    elif(bool(re.findall("[!@#$%^&*-_+=<>,.?:;|]", password)) == False):
                        messages.error(request, 'Please, Enter Any One Symbol.')
                    
                    elif(bool(re.findall("[0-9]", password)) == False):
                        messages.error(request, 'Please, Enter Any One Number.')

                    else:
                        user = User.objects.create_user(username=username, email=email, password=password)
                        user.save()

                        # create automatical userprofile
                        user_modal = User.objects.get(username=username)
                        newuserprofile = userprofile.objects.create(user=user_modal)
                        newuserprofile.save()

			# automatically new user login
                        newuser = auth.authenticate(username=username, password=password)
                        auth.login(request, newuser)
                        messages.success(request, 'This User Create New Account SuccessFully.')

                        # Send Mail After New User Registration
                        sendUserMail(email, 'common/email/newaccount.html', 'Account Create Successfully', '').start()

                        userid = user_modal.id
                        setLocation(userid)
                
                else:
                    messages.success(request, 'Please, Enter The Password Is Minimum 8 Characture.')

                        
                return redirect('/')


        else:
            return redirect('/')


    # -------------------------------------------------- User Sign In Function --------------------------------------------------
    def userlogin(request):

        if request.method == 'POST':
            getusername = request.POST['singin-username']
            getpassword = request.POST['singin-password']
            global twostepuserid, floginuser

            user = auth.authenticate(username=getusername, password=getpassword)

            if user is not None:
                getuserid = User.objects.get(username=getusername)
                
                # Check Userprofile Records
                checkuser = userprofile.objects.filter(user=getuserid, removestate=0)
                if checkuser.exists():

                    # Check Two Step Verfication
                    if(checkuser[0].twostep == 1):
                        twostepuserid = getuserid.id
                        changepscode = generatcode(6)

                        setuserotp = userprofile.objects.get(user_id=getuserid.id, removestate=0)
                        getcustemail = getuserid.email
                        floginuser = user

                        sendUserMail(getcustemail, 'common/email/sendcode/twostepcode.html', f'King Shopping Account {changepscode} is your verification code for secure access', changepscode).start()

                        setuserotp.uotp = changepscode
                        setuserotp.save()

                        logininfo = {
                            'twostep' : 'on',
                            'userid' : getuserid.id,
                        }
                        return render(request, 'index.html', logininfo)

                    else:

                        auth.login(request, user)
                        getcustemail = getuserid.email

                        sendUserMail(getcustemail, 'common/email/loginaccount.html', 'New device login detected in your king shopping account', '').start()

                        userid = getuserid.id
                        setLocation(userid)

                        messages.success(request, 'User Login SuccessFully.')
                        return redirect('/')
                else:
                    messages.error(request, 'Please, Check Your Username and Password!')
                    return redirect('/')

            else:
                messages.error(request, 'Please, Check Your Username and Password!')
                return redirect('/')

        else:
            return redirect('/')


    # -------------------------------------------------- Request OTP Sign In Function --------------------------------------------------
    def otp_signin_email_check(request):
        if request.method == "GET":
            global getotpemail, getrequserid
            getotpemail = request.GET.get('reqemail')

            checkemail = 0
            if(User.objects.filter(email = getotpemail).exists()):
                getrequserid = User.objects.get(email=getotpemail)
                
                checkuser = userprofile.objects.filter(user=getrequserid, removestate=0)
                if checkuser.exists():

                    setuserotp = userprofile.objects.get(user=getrequserid, removestate=0)
                    changepscode = generatcode(6)

                    sendUserMail(getotpemail, 'common/email/sendcode/requestotplogin.html', f'King Shopping Account {changepscode} is your verification code for secure access', changepscode).start()

                    setuserotp.uotp = changepscode
                    setuserotp.save()

                    checkemail = 1
                else:
                    checkemail = 0

                
            else:
                checkemail = 0

            checkreqemaildata = json.dumps({
                'chemail' : checkemail,
            })

            return HttpResponse(checkreqemaildata, content_type="application/json")


    # -------------------------------------------------- Request OTP Check Function --------------------------------------------------
    def reqotpcheck(request):
        if request.method == "POST":
            getreqotp = request.POST['requserotp']

            reqcheckotp = userprofile.objects.filter(user=getrequserid, removestate=0)

            reqchangeotp = userprofile.objects.get(user=getrequserid, removestate=0)
            if reqcheckotp[0].uotp == getreqotp:
                user = User.objects.get(email=getotpemail)
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                auth.login(request, user)
                reqchangeotp.uotp = 0
                reqchangeotp.save()
                messages.success(request, 'User Login SuccessFully.')

                sendUserMail(getotpemail, 'common/email/loginaccount.html', 'New device login detected in your king shopping account', '').start()

                return redirect('/')

            else:
                reqchangeotp.uotp = 0
                reqchangeotp.save()
                messages.error(request, 'Sorry! User Not Login.')
                return redirect('/')

        else:
            return redirect('/')


    # -------------------------------------------------- Forgot Password Check Username Function --------------------------------------------------
    def forgot_check_username(request):
        if request.method == "GET":
            global forgotuserpass, getuser
            getforgotusername = request.GET.get('forgotusername')
            getuser = User.objects.filter(username=getforgotusername)
            checkuser = userprofile.objects.filter(user=getuser[0].id, removestate=0)

            usersuccess = 0
            if checkuser.exists():
                usersuccess = 1
                changepscode = generatcode(6)
                forgotuserpass = getuser[0].id

                sendUserMail(getuser[0].email, 'common/email/sendcode/resetpassword.html', f'King Shopping Account {changepscode} is your verification code for secure access', changepscode).start()

                setchangeotp = userprofile.objects.get(user=getuser[0].id, removestate=0)
                setchangeotp.uotp = changepscode
                setchangeotp.save()

            else:
                usersuccess = 0


        if request.method == "POST":
            password = request.POST['forgot-password']
            repassword = request.POST['forgot-repassword']
            global twostepuserid, floginuser


            if(len(password) >= 8):

                if(bool(re.findall("[a-z]", password)) == False):
                    messages.error(request, 'Please, Enter Any One Lowercase.')

                elif(bool(re.findall("[A-Z]", password)) == False):
                    messages.error(request, 'Please, Enter Any One Uppercase.')

                elif(bool(re.findall("[!@#$%^&*-_+=<>,.?:;|]", password)) == False):
                    messages.error(request, 'Please, Enter Any One Symbol.')
                
                elif(bool(re.findall("[0-9]", password)) == False):
                    messages.error(request, 'Please, Enter Any One Number.')

                else:
                    if password == repassword:
                        forgotsetpassword = User.objects.get(username=getuser[0].username)
                        forgotsetpassword.set_password(password)
                        forgotsetpassword.save()
                        messages.success(request, 'Your Password Is Forgot SuccessFully.')
                        forgotuserlogin = auth.authenticate(username=getuser[0].username, password=password)

                        # Forgotpasswword after Check Two Step Verfication
                        forgottwoset = userprofile.objects.get(user_id=getuser[0].id, removestate=0)
                        if(forgottwoset.twostep == 1):
                            changepscode = generatcode(6)
                            twostepuserid = getuser[0].id

                            setuserotp = userprofile.objects.get(user_id=getuser[0].id, removestate=0)
                            getcustemail = getuser[0].email
                            floginuser = forgotuserlogin

                            sendUserMail(getcustemail, 'common/email/sendcode/twostepcode.html', f'King Shopping Account {changepscode} is your verification code for secure access', changepscode).start()

                            setuserotp.uotp = changepscode
                            setuserotp.save()

                            logininfo = {
                                'twostep' : 'on'
                            }
                            return render(request, 'index.html', logininfo)

                        else:
                            auth.login(request, forgotuserlogin)
                            messages.success(request, 'User Login SuccessFully.')
                            return redirect('/')

                    else:
                        messages.success(request, 'Sorry! Both Password Are Not Match.')

                
            else:
                messages.error(request, 'Please, Enter The minimum 8 Characture.')
                        
            return redirect('/')

        forgotdata = json.dumps({
            'checkuser' : usersuccess,
        })


        return HttpResponse(forgotdata, content_type="application/json")


    # -------------------------------------------------- Forgot Password Check OTP Function --------------------------------------------------
    def forgot_check_otp(request):
        try:
            getforgotuserotp = request.GET.get('forgotuserotp')

            checkforgototp = userprofile.objects.get(user_id=forgotuserpass, removestate=0)
            if checkforgototp.uotp == getforgotuserotp:
                checkotpstate = 1
            else:
                checkotpstate = 0

            checkforgototp.uotp = 0
            checkforgototp.save()
            
            forgototpdata = json.dumps({
                'checkforgototpstate' : checkotpstate
            })

            return HttpResponse(forgototpdata, content_type="application/json")

        except:
            return redirect('/')


    # -------------------------------------------------- User Logout Function --------------------------------------------------
    def userlogout(request):
        auth.logout(request)
        return redirect('/')



# ================================================= All Products Class =================================================
class productsaction:

    # -------------------------------------------------- Home Function --------------------------------------------------
    def home(request):
        # Check The Two Step Varification OTP
        if request.method == "POST":
            gettwostepotp = request.POST['twostepOTP']
            gettwo_user_id = request.POST['two_user_id']

            # check Twostep Otp 
            checktwostepotp = userprofile.objects.get(user_id=gettwo_user_id, twostep=1)
            useremail = User.objects.get(id=gettwo_user_id)
            if checktwostepotp.uotp == gettwostepotp:
                checktwostepotp.uotp = 0
                checktwostepotp.save()

                auth.login(request, floginuser)

                messages.success(request, 'User Login SuccessFully')
                sendUserMail(useremail.email, 'common/email/loginaccount.html', 'New device login detected in your king shopping account', '').start()
                return redirect('/')

            else:
                checktwostepotp.uotp = 0
                checktwostepotp.save()
                messages.error(request, 'Sorry! OTP Is Not Correct.')
                return redirect('/')


        # User Login After
        if request.method == "GET":

            # Menu Bar Random Categorys
            get_categorylist = categorys.objects.filter(removestate__exact=0)
            menu_bar_category = random.sample(list(get_categorylist), k=7)

            # Set Banners
            getbanners = products.objects.raw('SELECT * FROM webadminsiteapp_banners AS wb INNER JOIN webadminsiteapp_products AS wp ON wb.proid_id=wp.proid where wb.removestate=0')

            # Random Categorys
            get_category = random.sample(list(get_categorylist), k=6)

            # Random Products
            get_productslist = products.objects.filter(removestate__exact=0)
            get_products = random.sample(list(get_productslist), k=8)

            # Get Random One Category Wise Products
            get_random_one_category = random.sample(list(get_categorylist), k=1)
            get_any_products = products.objects.filter(cid_id=get_random_one_category[0].cid, removestate__exact=0)
            if get_any_products.count() <= 5:
                anyproducts = random.sample(list(get_any_products), k=get_any_products.count())
            else:
                anyproducts = random.sample(list(get_any_products), k=5)

            # Random products
            all_products = random.sample(list(get_productslist), k=get_productslist.count())

            homedata = {
                'menus' : menu_bar_category,
                'allbanners' : getbanners,
                'get_category': get_category,
                'get_products' : get_products,
                'random_products' : anyproducts,
                'allproducts' : all_products,
                'notuser' : 0,
            }

            if request.user.is_authenticated:
                user_object = User.objects.get(username=request.user.username)
                allwishlistitems = uwishlist.objects.filter(user__exact=user_object).count()
                allcartitems = cart.objects.filter(user__exact=user_object).count()

                # Check User Profile
                uprofile = userprofile.objects.get(user=user_object, removestate=0)
                
                checkprofile = 0
                if uprofile.firstname == "" or uprofile.lastname == "" or uprofile.phone == "" or uprofile.dob == "" or uprofile.gender == "" or uprofile.city == "" or uprofile.state == "" or uprofile.country == "":
                    checkprofile = 1
                else:
                    checkprofile = 0

                uprofile.uotp = 0
                uprofile.save()

                homedata.update({
                    'login_user' : user_object,
                    'wishcount' : allwishlistitems,
                    'cartcount' : allcartitems,
                    'userprofile' : checkprofile,
                    'notuser' : 1,
                })

            return render(request, 'index.html', homedata)


    # -------------------------------------------------- Products List Function --------------------------------------------------
    def productslist(request, catname):
        # Category Wise Product
        getcatid = categorys.objects.filter(catname__exact=catname, removestate__exact=0)
        get_any_products = products.objects.filter(cid_id=getcatid[0].cid, removestate__exact=0)
        getallpro = random.sample(list(get_any_products), k=get_any_products.count())

        # Menu Bar Random Categorys
        get_categorylist = categorys.objects.filter(removestate__exact=0)
        menu_bar_category = random.sample(list(get_categorylist), k=7)


        # Filter Records
        allbrands = brands.objects.filter(cid__exact=getcatid[0].cid, removestate=0).order_by('bname')
        colors = products.objects.filter(cid__exact=getcatid[0].cid, removestate__exact=0).values('procolor', 'procolorname').distinct()


        pro_minprice = get_any_products.aggregate(Min('proprice'))['proprice__min']
        pro_maxprice = get_any_products.aggregate(Max('proprice'))['proprice__max']

        clothes_categoryid = categorys.objects.filter(catname__istartswith='clothes', removestate=0)
        device_categoryid = categorys.objects.filter(Q(catname__istartswith='laptop') | Q(catname__istartswith='mobile') | Q(catname__istartswith='watch') | Q(catname__istartswith='computer'), removestate=0)

        clothes_size = ""
        if getcatid[0].cid == clothes_categoryid[0].cid:
            clothes_size = products.objects.filter(cid_id__exact=clothes_categoryid[0].cid, removestate=0).values('clothes_size').distinct().order_by('clothes_size')

        proram = ""
        prorom = ""
        for x in range(0, len(device_categoryid)):
            if getcatid[0].cid == device_categoryid[x].cid:
                proram = products.objects.filter(cid_id__exact=device_categoryid[x].cid, removestate=0).values('ram').distinct()
                prorom = products.objects.filter(cid_id__exact=device_categoryid[x].cid, removestate=0).values('rom').distinct()

        prolistdata = {
            'menus' : menu_bar_category,
            'catname' : catname,
            'getpro' : getallpro,
            'notuser' : 0,

            'filters' : {
                'brands' : allbrands,
                'colorcount' : colors.count(),
                'colors' : colors,
                'pricemin': pro_minprice,
                'pricemax': pro_maxprice,
                'clothessize' : clothes_size,
                'proram' : proram,
                'prorom' : prorom,
            }
        }


        if request.user.is_authenticated:
            user_object = User.objects.get(username=request.user.username)
            allwishlistitems = uwishlist.objects.filter(user__exact=user_object).count()
            allcartitems = cart.objects.filter(user__exact=user_object).count()

            prolistdata.update({
                'login_user': user_object,
                'wishcount' : allwishlistitems,
                'cartcount' : allcartitems,
                'notuser' : 1,
            })

        return render(request, 'webpages/productslist.html', prolistdata)


    # -------------------------------------------------- Menu Product Specific Brands Function --------------------------------------------------
    def menu_product_search(request, catname, bname):
        # Menu Bar Random Categorys
        get_categorylist = categorys.objects.filter(removestate__exact=0)
        menu_bar_category = random.sample(list(get_categorylist), k=7)

        getcategory = categorys.objects.get(catname=catname, removestate__exact=0)
        getbrand = brands.objects.filter(cid=getcategory.cid, bname__istartswith=bname, removestate__exact=0)
        
        get_any_products = products.objects.filter(cid=getcategory.cid, bid=getbrand[0].bid, removestate__exact=0)
        getallpro = random.sample(list(get_any_products), k=get_any_products.count())

        prolistdata = {
            'notuser' : 0,
            'getpro' : getallpro,
            'menus' : menu_bar_category,
            'catname' : catname,
        }

        if request.user.is_authenticated:
            user_object = User.objects.get(username=request.user.username)
            allwishlistitems = uwishlist.objects.filter(user__exact=user_object).count()
            allcartitems = cart.objects.filter(user__exact=user_object).count()

            prolistdata.update({
                'login_user': user_object,
            'wishcount' : allwishlistitems,
            'cartcount' : allcartitems,
            })

        return render(request, 'webpages/productslist.html', prolistdata)


    # -------------------------------------------------- Product Function --------------------------------------------------
    def menu_product_filter_search(request):
        # Get All Url Records
        urlcategory = request.GET.get('cat')
        urlbrands = request.GET.get('brands')
        urlram = request.GET.get('ram')
        urlrom = request.GET.get('rom')
        urlsize = request.GET.get('size')
        urlcolors = request.GET.get('colors')
        urlminprice = request.GET.get('minprice')
        urlmaxprice = request.GET.get('maxprice')

        
        # Menu Bar Random Categorys
        get_categorylist = categorys.objects.filter(removestate__exact=0)
        menu_bar_category = random.sample(list(get_categorylist), k=7)



        # ======================================== Set The All Filter Values In Filter Panel Start ========================================

        # Get Category
        getcatid = categorys.objects.filter(catname__exact=urlcategory, removestate__exact=0)

        # Filter Panel Records
        allbrands = brands.objects.filter(cid_id__exact=getcatid[0].cid, removestate=0).order_by('bname')
        colors = products.objects.filter(cid_id__exact=getcatid[0].cid, removestate__exact=0).values('procolor','procolorname').distinct()


        pro_minprice = products.objects.filter(cid__exact=getcatid[0].cid, removestate__exact=0).aggregate(Min('proprice'))['proprice__min']
        pro_maxprice = products.objects.filter(cid__exact=getcatid[0].cid, removestate__exact=0).aggregate(Max('proprice'))['proprice__max']

        clothes_size = ""
        clothes_categoryid = categorys.objects.filter(catname__istartswith='clothes', removestate=0)

        # check page request clothes
        if getcatid[0].cid == clothes_categoryid[0].cid:
            clothes_size = products.objects.filter(cid__exact=clothes_categoryid[0].cid, removestate=0).values('clothes_size').distinct().order_by('clothes_size')


        product_ram = ""
        product_rom = ""
        device_categoryid = categorys.objects.filter(Q(catname__istartswith='laptop') | Q(catname__istartswith='mobile') | Q(catname__istartswith='watch') | Q(catname__istartswith='computer'), removestate=0)
        for x in range(0, len(device_categoryid)):
            if getcatid[0].cid == device_categoryid[x].cid:
                product_ram = products.objects.filter(cid_id__exact=device_categoryid[x].cid, removestate=0).values('ram').distinct()
                product_rom = products.objects.filter(cid_id__exact=device_categoryid[x].cid, removestate=0).values('rom').distinct()


        # ======================================== Set The All Filter Values In Filter Panel End ========================================


        allbrand = list(urlbrands.split(","))
        allram = list(urlram.split(","))
        allrom = list(urlrom.split(","))
        allsize = list(str(urlsize).split(","))
        allcolors = list(str(urlcolors).split(","))

        maxprice = 0
        if urlmaxprice == "5000" or urlmaxprice == "50000":
            maxprice = pro_maxprice

        else:
            maxprice = urlmaxprice


        # Get Filter Product
        brands_id = []
        getcatid = categorys.objects.filter(catname__exact=urlcategory, removestate__exact=0)
        getbrands = brands.objects.filter(cid_id__exact=getcatid[0].cid, bname__in=allbrand)

        for x in range(0, len(getbrands)):
            brands_id.append(getbrands[x].bid)

        if urlcategory != "Clothes" or urlcategory != "Clothes":
            get_any_products = products.objects.filter(cid_id=getcatid[0].cid, removestate__exact=0).filter(Q(bid__in=brands_id) | Q(ram__in=allram) | Q(rom__in=allrom) | Q(procolorname__in=allcolors) | Q(proprice__range=(urlminprice, maxprice)))
        else:
            get_any_products = products.objects.filter(cid_id=getcatid[0].cid, removestate__exact=0).filter(Q(bid__in=brands_id) | Q(clothes_size__in=allsize) | Q(procolorname__in=allcolors) | Q(proprice__range=(urlminprice, maxprice)))

        if len(get_any_products) != 0:
            getallpro = random.sample(list(get_any_products), k=get_any_products.count())
        else:
            messages.warning(request, "Sorry, This Product is Not Available.")
            return redirect(f'/products/{urlcategory}')


        prolistdata = {
            'menus' : menu_bar_category,
            'catname' : urlcategory,
            'getpro' : getallpro,

            'selectedValues' : {
                'brands' : getbrands,
                'ram' : allram,
                'rom' : allrom,
                'size' : allsize,
                'colors' : allcolors,
                'minprice' : urlminprice,
                'maxprice' : urlmaxprice,
            },

            'filters' : {
                'brands' : allbrands,
                'colorcount' : colors.count(),
                'colors' : colors,
                'pricemin': pro_minprice,
                'pricemax': pro_maxprice,
                'clothessize' : clothes_size,
                'proram' : product_ram,
                'prorom' : product_rom,
            }
        }

        if request.user.is_authenticated:
            user_object = User.objects.get(username=request.user.username)
            allwishlistitems = uwishlist.objects.filter(user__exact=user_object).count()
            allcartitems = cart.objects.filter(user__exact=user_object).count()

            prolistdata.update({
                'login_user': user_object,
                'wishcount' : allwishlistitems,
                'cartcount' : allcartitems,
            })



        return render(request, 'webpages/productslist.html', prolistdata)


    # -------------------------------------------------- Product Function --------------------------------------------------
    def product(request):
        geturlproid = request.GET['proid']
        geturlproname = request.GET['proname']
        geturlprocolorname = request.GET['procolor']

        # Check Same Any Other Produc But Different Color
        pro_data = products.objects.filter(proname__startswith=geturlproname[:len(geturlproname)//2])

        getclothessize = products.objects.filter(proname__startswith=geturlproname[:len(geturlproname)//2], procolorname=geturlprocolorname).values('clothes_size').distinct()

        # Sepcifice Product Record
        pro_get_data = products.objects.get(proid=geturlproid)

        # Menu Bar Random Categorys
        get_categorylist = categorys.objects.filter(removestate__exact=0)
        menu_bar_category = random.sample(list(get_categorylist), k=7)


        # Random Products
        getcatid = products.objects.get(proid=geturlproid, removestate=0)
        get_productslist = products.objects.filter(cid=getcatid.cid, removestate__exact=0)
        if len(get_productslist) >= 8:
            get_products = random.sample(list(get_productslist), k=8)
        else:
            get_products = random.sample(list(get_productslist), k=len(get_productslist))


        # Product All Details
        generaldata = products_general_details.objects.get(proid_id=geturlproid, removestate=0)
        displaydata = products_displays_details.objects.get(proid_id=geturlproid, removestate=0)
        conndata = products_connectivity_details.objects.get(proid_id=geturlproid, removestate=0)
        osprodata = products_osprocesser_details.objects.get(proid_id=geturlproid, removestate=0)
        dimwarrdata = products_dimensions_warranty_details.objects.get(proid_id=geturlproid, removestate=0)


        prosendata = {
            'notuser' : 0,
            'menus' : menu_bar_category,
            'urlprocolor' : geturlprocolorname,

            'prodata' : pro_get_data,
            'sameproduct_changecolor' : pro_data,
            'sameproduct_changecolor_count' : pro_data.count(),
            'productclothsize' : getclothessize,
            'productclothsizecount' : getclothessize.count(),
            'reletedproduct' : get_products,

            'productdetails': {
                'generaldata' : generaldata,
                'displaydata' : displaydata,
                'connectivitydata': conndata,
                'osprocesserdata' : osprodata,
                'dim_warr_data' : dimwarrdata,
            }
        }



        if request.user.is_authenticated:
            user_object = User.objects.get(username=request.user.username)
            allwishlistitems = uwishlist.objects.filter(user__exact=user_object).count()
            allcartitems = cart.objects.filter(user__exact=user_object).count()

            # Check The Wishlist In Product Add or Not Add
            checkwishlist = uwishlist.objects.filter(proid__exact=geturlproid, user__exact=user_object)
            if checkwishlist.exists():
                getwishlist = 'wishactive'

            else:
                getwishlist = 'wishnotactive'

            # Check The Cart In Product Add or Not Add
            checkcart = cart.objects.filter(proid__exact=geturlproid, user=user_object)
            if checkcart.exists():
                getprocart = 'cartactive'

            else:
                getprocart = 'cartnotactive'

            prosendata.update({
                'login_user' : user_object,
                'wishcount' : allwishlistitems,
                'cartcount' : allcartitems,
                'wishid' : getwishlist,
                'cartpro' : getprocart,
                'notuser' : 1,
            })


        return render(request, 'webpages/product.html', prosendata)


    # -------------------------------------------------- Product Function --------------------------------------------------
    def search_user(request):
        # Menu Bar Random Categorys
        get_categorylist = categorys.objects.filter(removestate__exact=0)
        menu_bar_category = random.sample(list(get_categorylist), k=7)

        search_value = request.GET['search']

        # Search Records for user
        get_all_products = []
        search_category = ""
        # try:
        search_category = categorys.objects.filter(catname__icontains=search_value)
        for x in range(0, len(search_category)):
            get_all_products = products.objects.filter(cid_id=search_category[x].cid)

        # if (len(search_category) == 0):
        search_brands = brands.objects.filter(bname__icontains=search_value)
        for x in range(0, len(search_brands)):
            get_all_products = products.objects.filter(Q(proname__icontains=search_brands[x].bname))


        if len(get_all_products) == 0:
            get_all_products = products.objects.filter(Q(proname__icontains=search_value) | Q(proname__icontains=search_value) | Q(procolorname__icontains=search_value) | Q(ram__icontains=search_value) | Q(rom__icontains=search_value))

        if len(get_all_products) == 0:
            get_all_products = products.objects.all()


        usersearchdata = {
            'notuser' : 0,
            'menus' : menu_bar_category,
            'getpro' : get_all_products,
        }

        # THis Is After User Login
        if request.user.is_authenticated:
            user_object = User.objects.get(username=request.user.username)
            allwishlistitems = uwishlist.objects.filter(user__exact=user_object).count()
            allcartitems = cart.objects.filter(user__exact=user_object).count()

            usersearchdata['login_user'] = user_object
            usersearchdata['wishcount'] = allwishlistitems
            usersearchdata['cartcount'] = allcartitems
            usersearchdata['cartcount'] = "1"

        return render(request, 'webpages/productslist.html', usersearchdata)


# ================================================= User Wishlist Class =================================================
class wishlistsaction:

    # -------------------------------------------------- Wishlist Function --------------------------------------------------
    def wishlist(request):
        # Menu Bar Random Categorys
        get_categorylist = categorys.objects.filter(removestate__exact=0)
        menu_bar_category = random.sample(list(get_categorylist), k=7)

        wishlistcontent = {
            'notuser' : 0,
            'menus' : menu_bar_category,
        }

        if request.user.is_authenticated:
            user_object = User.objects.get(username=request.user.username)
            allwishlistitems = uwishlist.objects.filter(user__exact=user_object).count()
            allcartitems = cart.objects.filter(user__exact=user_object).count()

            # All User Wishlist Records
            allwishdata = products.objects.raw('SELECT * FROM webadminsiteapp_uwishlist AS wu INNER JOIN webadminsiteapp_products AS wp ON wu.proid_id = wp.proid WHERE wu.user_id = %s', params=[user_object.id])

            wishlistcontent.update({
                'login_user' : user_object,
                'wishcount' : allwishlistitems,
                'cartcount' : allcartitems,
                'notuser' : 1,
                'allwishdata' : allwishdata,
            })

        return render(request, 'webpages/wishlist.html', wishlistcontent)

    # -------------------------------------------------- Add Wishlist Function --------------------------------------------------
    def add_wishlist_product(request):
        if request.user.is_authenticated:
            user_object = User.objects.get(username=request.user.username)

            if request.method == "GET":
                getwishproid = request.GET.get('addwishproid')

                if getwishproid != None:
                    checkwish = uwishlist.objects.filter(user=user_object, proid_id=getwishproid)
                    if checkwish.exists():
                        messages.success(request, "Added to your Wishlist")

                    else:
                        newish = uwishlist.objects.create(user=user_object, proid_id=getwishproid)
                        newish.save()
                        messages.success(request, "Added to your Wishlist")
                else:
                    return redirect('/wishlist/')
            
            return HttpResponse()

        else:
            return redirect('/wishlist/')


    # -------------------------------------------------- Remove Wishlist Function --------------------------------------------------
    def remove_wishlist_product(request):
        if request.user.is_authenticated:
            user_object = User.objects.get(username=request.user.username)

            if request.method == "GET":
                getrmwishpro = request.GET.get('removewishproid')

                if getrmwishpro != None:
                    rmwish = uwishlist.objects.get(user=user_object, proid_id=getrmwishpro)
                    rmwish.delete()
                else:
                    return redirect('/wishlist/')

                messages.success(request, "Remove to your Wishlist")

            return HttpResponse()

        else:
            return redirect('/wishlist/')



# ================================================= Cart Class =================================================
class cartaction:

    # -------------------------------------------------- Cart Function --------------------------------------------------
    def addtocart(request):
        if request.user.is_authenticated:
            user_object = User.objects.get(username=request.user.username)
            allwishlistitems = uwishlist.objects.filter(user__exact=user_object).count()
            allcartitems = cart.objects.filter(user__exact=user_object).count()

            # Menu Bar Random Categorys
            get_categorylist = categorys.objects.filter(removestate__exact=0)
            menu_bar_category = random.sample(list(get_categorylist), k=7)


            # Get Cart Items 
            getprocart = products.objects.raw("SELECT * FROM webadminsiteapp_cart AS wc INNER JOIN webadminsiteapp_products AS wp ON wc.proid_id = wp.proid WHERE wc.user_id = %s and wp.removestate=0", params=[user_object.id])
            getprocartcount = cart.objects.filter(user=user_object).count()


            # Set the change address box
            getuseraddressall = useraddress.objects.filter(user__exact = user_object)

            # Delivery Address
            getdeliaddress = useraddress.objects.raw("SELECT * FROM webadminsiteapp_cart AS wc INNER JOIN webadminsiteapp_useraddress AS wa ON wc.deliaddr_id = wa.addid WHERE wc.user_id = %s AND wa.removestate = 0", params=[user_object.id])


            if len(getdeliaddress) != 0:
                for deliveraddress in getdeliaddress:
                    deliaddrid = deliveraddress.addid
                    deliaddrtitle = deliveraddress.addtitle
                    deliaddrdesc = deliveraddress.adddescription
            else:
                deliaddrid = 0
                deliaddrtitle = 0
                deliaddrdesc = 0


            # User Cart Total Product Price
            totalproprice = 0
            totalprice = 0
            userproprice = cart.objects.filter(user = user_object)

            for i in range(0, len(userproprice)):
                totalproprice = totalproprice + userproprice[i].catproprice
                totalprice = totalprice + (userproprice[i].catproprice * userproprice[i].proqty)


            # Change The User Product Deliver Address
            if request.method == "POST":
                deliaddid = request.POST['deliveryaddress']
                cart.objects.filter(user = user_object).update(deliaddr=deliaddid)

                messages.success(request, "Change the Your Delivery Address.")

                return redirect('/cart/')


            cartdata = {
                'login_user':user_object,
                'wishcount' : allwishlistitems,
                'cartcount' : allcartitems,
                'menus' : menu_bar_category,

                'useralladdress' : getuseraddressall,

                'allcart' : getprocart,
                'itemsco' : getprocartcount,
            
                'deliveraddr' : {
                    'deliverid' : deliaddrid,
                    'delivertitle' : deliaddrtitle,
                    'deliverdesc' : deliaddrdesc,
                },


                'pricedetails' : {
                    'totalproprice' : totalproprice,
                    'totalprice' : totalprice,
                },

            }


            return render(request, 'webpages/cart.html', cartdata)

        else:
            # Menu Bar Random Categorys
            get_categorylist = categorys.objects.filter(removestate__exact=0)
            menu_bar_category = random.sample(list(get_categorylist), k=7)
            cartdata = {
                'notuser' : 0,
                'menus' : menu_bar_category,
            }
            return render(request, 'webpages/cart.html', cartdata)


    # -------------------------------------------------- Add Product QTY Product In Cart Function --------------------------------------------------
    def product_add_qty(request):
        if request.user.is_authenticated:
            user_object = User.objects.get(username=request.user.username)
            
            if request.method == "GET":
                getproqty = request.GET.get('cproqty')
                getproid = request.GET.get('cproid')

                if getproqty != None or getproid != None:
                    getproname = products.objects.get(proid=getproid, removestate=0)

                    changeqty = cart.objects.get(user=user_object, proid=getproid)
                    changeqty.proqty = getproqty
                    changeqty.save()

                    messages.success(request, "You've changed '"+getproname.proname+"' QUANTITY to " + getproqty)

                else:
                    return redirect('/cart/')
            
            return HttpResponse()

        else:
            cartdata = {
                'notuser' : 0,
            }
            return render(request, 'webpages/cart.html', cartdata)


    # -------------------------------------------------- Add Product In Cart Function --------------------------------------------------
    def product_add_cart(request):
        if request.user.is_authenticated:
            user_object = User.objects.get(username=request.user.username)
            if request.method == "GET":
                getproaddid = request.GET.get('addcartproid')

                if getproaddid != None:
                    getproprice = products.objects.get(proid=getproaddid, removestate=0)
                    getaddid = useraddress.objects.filter(user__exact = user_object, removestate__exact=0)

                    if getaddid.exists():
                        checkproid = cart.objects.filter(proid__exact=getproaddid, user__exact=user_object)
                        if checkproid.exists():
                            messages.error(request, "Added to your Cart")

                        else:
                            newcart = cart.objects.create(user=user_object, proid_id=getproaddid, catproprice=getproprice.proprice, deliaddr_id=getaddid[0].addid, proqty=1)
                            newcart.save()
                            messages.success(request, "Added to your Cart")
                            return HttpResponse()
                                                
                    else:
                        messages.warning(request, "Please, Enter the Your Address.")
                        return HttpResponse()

                else:
                    return redirect('/cart/')


        else:
            cartdata = {
                'notuser' : 0,
            }
            return render(request, 'webpages/cart.html', cartdata)


    # -------------------------------------------------- Remove Product In Cart Function --------------------------------------------------
    def product_remove_cart(request):
        if request.user.is_authenticated:
            user_object = User.objects.get(username=request.user.username)

            if request.method == "GET":
                rmcartproid = request.GET.get('removecartpro')

                if rmcartproid != None:
                    removecart = cart.objects.filter(proid__exact=rmcartproid, user__exact=user_object)
                    removecart.delete()
                    messages.success(request, "Your Product Is Remove SuccessFully")
                    return HttpResponse()
                    
                
                else:
                    return redirect('/cart/')

        else:
            cartdata = {
                'notuser' : 0,
            }
            return render(request, 'webpages/cart.html', cartdata)



# ================================================= Buy Products Class =================================================
class buyproduct:

    # -------------------------------------------------- Cart Buy Products Function --------------------------------------------------
    def cartbuyproducts(request):
        if request.user.is_authenticated:
            user_object = User.objects.get(username=request.user.username)

            if request.method == "GET":
                # Check The Product In Cart
                checkcartpro = cart.objects.filter(user=user_object)
                if checkcartpro.exists():

                    # all List Use In buyproduct function
                    global cartproid
                    cartproid = []
                    totalprice = 0

                    # Get User Cart Product Id
                    getcartproid = cart.objects.filter(user=user_object)

                    for x in range(0, len(getcartproid)):
                        cartproid.append(getcartproid[x].proid_id)
                        totalprice = totalprice + getcartproid[x].catproprice


                    # check stock
                    checkstock = products.objects.filter(proid__in=cartproid, prostock = 0, removestate=0)
                    if checkstock.exists():
                        messages.error(request, "Sorry! This Product Is Out of Stock.")
                        return redirect('/cart/')

                    else:
                        # Delivery Address
                        alladdr = useraddress.objects.filter(user=user_object, removestate=0)
                        cartaddr = cart.objects.filter(user=user_object)

                        # Products
                        getproducts = products.objects.filter(proid__in=cartproid, removestate=0)

                else:
                    return redirect('/')

            elif request.method == "POST":
                proqty = request.POST['orproductqty']
                paymentmode = request.POST['paymentmode']
                deliveryaddr = request.POST['ordeliveryaddr']
                
                getcartproid = cart.objects.filter(user=user_object)
                deliverydate = (date.today()+timedelta(days=10)).isoformat()
                returndate = (date.today()+timedelta(days=20)).isoformat()


                for x in range(0, len(getcartproid)):
                    productdata = products.objects.filter(proid=getcartproid[x].proid_id)
                    custorder = orders.objects.create(user=user_object, proid_id=getcartproid[x].proid_id, deliaddr_id=deliveryaddr, proqty=proqty, paymentmode=paymentmode, deliveddate=deliverydate, returndate=returndate)
                    custorder.save()

                    removecart = cart.objects.filter(proid__exact=getcartproid[x].proid_id, user__exact=user_object)
                    removecart.delete()

                    proupdate = products.objects.filter(proid=getcartproid[x].proid_id)
                    updatestock = proupdate[0].prostock - int(proqty)
                    proupdate.update(prostock=updatestock)

                    prototalprice = int(productdata[0].proprice) * int(proqty)
                    deliveraddress = useraddress.objects.get(addid=deliveryaddr, removestate=0)


                    productMail(
                        senduser = user_object.email,
                        template = 'common/email/orderProcess/conformOrder.html',
                        mail_subject = f'{productdata[0].proname} has been successfully conform',
                        orderid = '********************',
                        orderdate = today,
                        product_name = productdata[0].proname,
                        delivery_address = deliveraddress.adddescription,
                        proprice = productdata[0].proprice,
                        product_qty = proqty,
                        delivery_date = deliverydate,
                        totalprice = prototalprice
                    ).start()

                messages.success(request, "Your Orders Is Conform Successfully.")

                return redirect('/orders/')

            buyproductdata = {

                'userdetails' : {
                    'username' : user_object,
                    'email' : user_object.email
                },

                'address' : {
                    'alladdress' : alladdr,
                    'cartaddr' : cartaddr[0].deliaddr_id,
                },

                'products' : {
                    'userproduct' : getproducts,
                    'totalproducts' : getproducts.count(),
                    'totalprice' : totalprice,
                }

            }

            return render(request, 'webpages/buyproduct.html', buyproductdata)

        else:
            messages.error(request, "Sorry! User is not logged in")
            return redirect('/')


    # -------------------------------------------------- Buy Product Order Function --------------------------------------------------
    def buyproduct(request):
        if request.user.is_authenticated:
            user_object = User.objects.get(username=request.user.username)

            if request.method == "GET":
                global getbuyproductid
                getbuyproductid = request.GET['newproname']

                if getbuyproductid != "":
                    checkstock = products.objects.filter(proid=getbuyproductid, prostock = 0, removestate=0)
                    if checkstock.exists():
                        messages.error(request, "Sorry! This Product Is Out of Stock.")
                        return redirect('/')

                    else:
                        # Delivery Address
                        alladdr = useraddress.objects.filter(user=user_object, removestate=0)

                        # Get Buy Products
                        getproducts = products.objects.filter(proid=getbuyproductid, removestate=0)

                        

            elif request.method == "POST":
                proqty = request.POST['orproductqty']
                paymentmode = request.POST['paymentmode']
                deliveryaddr = request.POST['ordeliveryaddr']
                
                deliverydate = (date.today()+timedelta(days=10)).isoformat()
                returndate = (date.today()+timedelta(days=20)).isoformat()

                custorder = orders.objects.create(user=user_object, proid_id=getbuyproductid, deliaddr_id=deliveryaddr, proqty=proqty, paymentmode=paymentmode, deliveddate=deliverydate, returndate=returndate)
                custorder.save()

                proupdate = products.objects.filter(proid=getbuyproductid)
                updatestock = proupdate[0].prostock - int(proqty)
                proupdate.update(prostock=updatestock)

                prototalprice = int(proupdate[0].proprice) * int(proqty)
                deliveraddress = useraddress.objects.get(addid=deliveryaddr, removestate=0)

                productMail(
                    senduser = user_object.email,
                    template = 'common/email/orderProcess/conformOrder.html',
                    mail_subject = f'{proupdate[0].proname} has been successfully conform',
                    orderid = '********************',
                    orderdate = today,
                    product_name = proupdate[0].proname,
                    delivery_address = deliveraddress.adddescription,
                    proprice = proupdate[0].proprice,
                    product_qty = proqty,
                    delivery_date = deliverydate,
                    totalprice = prototalprice
                ).start()


                messages.success(request, "Your Orders Is Conform Successfully.")
                return redirect('/orders/')

            else:
                return redirect('/')

            buyproductdata = {

                'userdetails' : {
                    'username' : user_object,
                    'email' : user_object.email
                },

                'address' : {
                    'alladdress' : alladdr,
                    'cartaddr' : alladdr[0].addid,
                },

                'products' : {
                    'userproduct' : getproducts,
                    'totalproducts' : getproducts.count(),
                    'totalprice' : getproducts[0].proprice,
                }

            }

            return render(request, 'webpages/buyproduct.html', buyproductdata)

        else:
            messages.error(request, "Sorry! User is not logged in")
            return redirect('/')



# ================================================= Orders Class =================================================
class orderaction:

    # -------------------------------------------------- Order Function --------------------------------------------------
    def orders(request):
        if request.user.is_authenticated:
            user_object = User.objects.get(username=request.user.username)
            allwishlistitems = uwishlist.objects.filter(user__exact=user_object).count()
            allcartitems = cart.objects.filter(user__exact=user_object).count()

            # Menu Bar Random Categorys
            get_categorylist = categorys.objects.filter(removestate__exact=0)
            menu_bar_category = random.sample(list(get_categorylist), k=7)


            # Customer Orders
            custorders = products.objects.raw("SELECT * FROM webadminsiteapp_orders AS wo INNER JOIN webadminsiteapp_products AS wp ON wo.proid_id = wp.proid WHERE wo.user_id=%s and wp.removestate=0 and wo.removestate=0 ORDER BY wo.ordate DESC", params=[user_object.id])

            orderdata = {
                'login_user':user_object,
                'wishcount' : allwishlistitems,
                'cartcount' : allcartitems,
                'menus' : menu_bar_category,

                'allorders' : custorders,
                'totalorders' : len(custorders),
            }

            return render(request, 'webpages/orders.html', orderdata)

        else:
            messages.error(request, "Sorry! User is not logged in")
            # Menu Bar Random Categorys
            get_categorylist = categorys.objects.filter(removestate__exact=0)
            menu_bar_category = random.sample(list(get_categorylist), k=7)
            orderdata = {
                'menus' : menu_bar_category,
                'notuser' : 0,
            }
            return render(request, 'webpages/orders.html', orderdata)


    # -------------------------------------------------- Product Details In Order Page --------------------------------------------------
    def ordersdetails(request):
        if request.user.is_authenticated:
            user_object = User.objects.get(username=request.user.username)
            allwishlistitems = uwishlist.objects.filter(user__exact=user_object).count()
            allcartitems = cart.objects.filter(user__exact=user_object).count()

            # Menu Bar Random Categorys
            get_categorylist = categorys.objects.filter(removestate__exact=0)
            menu_bar_category = random.sample(list(get_categorylist), k=7)


            if request.method == "GET":
                getoid = request.GET.get('prooid')

                # Delivery Address
                getorder = orders.objects.get(user=user_object, oid=getoid)
                deliveryaddr = useraddress.objects.get(user=user_object, addid=getorder.deliaddr_id)

                # Phone Number
                userdetails = userprofile.objects.get(user=user_object, removestate=0)

                # Productdetails
                prodetails = products.objects.get(proid=getorder.proid_id)


                try:
                    getreturn = returnproduct.objects.get(oid_id=getoid, user=user_object)
                    returndate = getreturn.rndate
                except:
                    returndate = 0


            orderdetailsdata = {
                'login_user':user_object,
                'wishcount' : allwishlistitems,
                'cartcount' : allcartitems,
                'menus' : menu_bar_category,

                'orderdata' : getorder,
                'deliveryaddr' : deliveryaddr,
                'userdetails' : userdetails,
                'prodata' : prodetails,
                'todaydate' : date.today(),

                'returndate' : returndate,
                
            }

            return render(request, 'webpages/orderdetails.html', orderdetailsdata)

        else:
            return redirect('/orders/')


    # -------------------------------------------------- Product Cancel In Order Page --------------------------------------------------
    def ordercancel(request):
        if request.user.is_authenticated:
            user_object = User.objects.get(username=request.user.username)

            if request.method == "POST":
                getorderid = request.POST['canceloid']

                cancelorder = orders.objects.get(user=user_object, oid=getorderid)
                cancelorder.productstatus = 'cancel'
                cancelorder.canceldate = now()
                cancelorder.save()

                proupdate = products.objects.get(proid = cancelorder.proid_id)
                updatestock = int(cancelorder.proqty) + int(proupdate.prostock)
                proupdate.prostock = updatestock
                proupdate.save()

                getuser = User.objects.filter(id=cancelorder.user_id)

                sendUserMail(getuser[0].email, 'common/email/orderProcess/cancelOrder.html', f'{proupdate.proname} from your order have been cancelled', getorderid).start()

                messages.success(request, "Your Order Is Cancel SuccessFully.")

                return redirect('/orders/orderdetails/?&prooid='+getorderid)
            
            else:
                return redirect('/orders')
        
        else:
            messages.error(request, "Sorry! User is not logged in")
            return redirect('/')


    # -------------------------------------------------- Product Return In Order Page --------------------------------------------------
    def ordereturn(request):
        if request.user.is_authenticated:
            user_object = User.objects.get(username=request.user.username)
            allwishlistitems = uwishlist.objects.filter(user__exact=user_object).count()
            allcartitems = cart.objects.filter(user__exact=user_object).count()

            # Menu Bar Random Categorys
            get_categorylist = categorys.objects.filter(removestate__exact=0)
            menu_bar_category = random.sample(list(get_categorylist), k=7)

            if request.method == "GET":
                try:
                    global getorrnid
                    getorrnid = request.GET['prorn']
                    orders.objects.get(oid=getorrnid, productstatus="delived")

                except:
                    return redirect('/orders/')

            if request.method == "POST":
                rnproce = request.POST['rnprocess']
                rnresone = request.POST['returnresone']
                rncomment = request.POST['rncomment']

                if rnproce == "Replace":
                    try:
                        checkprostatus = orders.objects.get(oid=getorrnid, productstatus="delived", returnpro="No")

                        deliverydate = (date.today()+timedelta(days=10)).isoformat()
                        returndate = (date.today()+timedelta(days=20)).isoformat()


                        if checkprostatus != None:
                            rnprduct = returnproduct.objects.create(user=user_object, oid_id=getorrnid, rnproce=rnproce, rnresone=rnresone, rncomment=rncomment)
                            rnprduct.save()

                            custorder = orders.objects.create(user=user_object, proid_id=checkprostatus.proid_id, deliaddr_id=checkprostatus.deliaddr_id, proqty=checkprostatus.proqty, paymentmode=checkprostatus.paymentmode, returnpro="Replace", deliveddate=deliverydate, returndate=returndate)
                            custorder.save()

                            checkprostatus.removestate = 1
                            checkprostatus.save()

                            proupdate = products.objects.filter(proid=checkprostatus.proid_id)
                            prototalprice = int(proupdate[0].proprice) * int(checkprostatus.proqty)
                            deliveraddress = useraddress.objects.get(addid=checkprostatus.deliaddr_id, removestate=0)

                            productMail(
                                senduser = user_object.email,
                                template = 'common/email/orderProcess/conformOrder.html',
                                mail_subject = f'Your replace request for {proupdate[0].proname} has been accepted',
                                orderid = '********************',
                                orderdate = today,
                                product_name = proupdate[0].proname,
                                delivery_address = deliveraddress.adddescription,
                                proprice = proupdate[0].proprice,
                                product_qty = checkprostatus.proqty,
                                delivery_date = deliverydate,
                                totalprice = prototalprice
                            ).start()

                            sendUserMail(user_object.email, 'common/email/orderProcess/returnOrder.html', f'Your replace request for {proupdate[0].proname} has been accepted', '').start()

                            messages.success(request, "Your Product Is Replace Successfully.")
                            return redirect('/orders/')

                        else:
                            messages.warning(request, "Sorry! Your Order is Allredy Replace.")
                            return redirect('/orders/')

                    except:
                        return redirect('/orders/')


                elif rnproce == "Return":
                    checkprostatus = orders.objects.filter(oid=getorrnid, productstatus="delived", returnpro="No")
                    if checkprostatus.exists():
                        rnprduct = returnproduct.objects.create(user=user_object, oid_id=getorrnid, rnproce=rnproce, rnresone=rnresone, rncomment=rncomment)
                        rnprduct.save()

                        proupdate = products.objects.get(proid=checkprostatus[0].proid_id)
                        prostock = int(proupdate.prostock) + int(checkprostatus[0].proqty)
                        proupdate.prostock = prostock
                        proupdate.save()

                        changereturnpro = orders.objects.get(user=user_object, oid=getorrnid, removestate=0)
                        changereturnpro.returnpro = 'Return'
                        changereturnpro.save()

                        getaddress = useraddress.objects.filter(addid=changereturnpro.deliaddr_id)
                        getuser = User.objects.filter(id=changereturnpro.user_id)
                        totalprice = proupdate.proprice * changereturnpro.proqty

                        productMail(
                            senduser = getuser[0].email,
                            template = 'common/email/orderProcess/returnOrder.html',
                            mail_subject = f'{proupdate.proname} from your order have been return',
                            orderid = changereturnpro.oid,
                            orderdate = changereturnpro.ordate,
                            product_name = proupdate.proname,
                            delivery_address = getaddress[0].adddescription,
                            proprice = proupdate.proprice,
                            product_qty = changereturnpro.proqty,
                            delivery_date = changereturnpro.deliveddate,
                            totalprice = totalprice
                        ).start()


                        messages.success(request, "Your Order Is Return SuccessFully.")
                        return redirect('/orders/')

                    else:
                        messages.warning(request, "Sorry! Your Order is Allredy Return.")
                        return redirect('/orders/')

                else:
                    return redirect('/orders/')



            orderndata = {
                'login_user' : user_object,
                'wishcount' : allwishlistitems,
                'cartcount' : allcartitems,
                'orderid' : getorrnid,
                'menus' : menu_bar_category,
            }

            return render(request, 'webpages/returnProduct.html', orderndata)

        else:
            messages.error(request, "Sorry! User is not logged in")
            return redirect('/')



# ================================================= Setting Class =================================================
class settings:

    # -------------------------------------------------- Profile Page In Setting Page --------------------------------------------------
    def settingProfile(request):
        if request.user.is_authenticated:
            user_object = User.objects.get(username=request.user.username)
            allwishlistitems = uwishlist.objects.filter(user__exact=user_object).count()
            allcartitems = cart.objects.filter(user__exact=user_object).count()

            # Menu Bar Random Categorys
            get_categorylist = categorys.objects.filter(removestate__exact=0)
            menu_bar_category = random.sample(list(get_categorylist), k=7)

            # User Profile Records
            user_profile = userprofile.objects.get(user=user_object)


            if request.method == "POST":
                firstname = request.POST['firstname']
                lastname = request.POST['lastname']
                username = request.POST['username']
                email = request.POST['email']
                phone = request.POST['phone']
                dob = request.POST['dob']
                gender = request.POST['gender']
                city = request.POST['city']
                state = request.POST['state']
                country = request.POST['country']


                # User profile in Change Username After Check Username
                if not bool(re.match("^[A-Za-z]*$", username)):
                    messages.error(request, 'Please, Enter The Username Is Only For Letter.')
                    return redirect('/account/profile/')

                elif len(username) <= 8:
                    messages.error(request, 'Please, Enter The Username Is Minimum 8 Characture.')
                    return redirect('/account/profile/')

                elif user_object.username != username:
                    if User.objects.filter(username = username).exists():
                        messages.error(request, 'This Username Allready Exists!')

                    else:
                        if request.FILES.get('chooseimage') == None:
                            image = user_profile.profileimage
                            settings.updatepro(request=request, userobject = user_object, userprofile=user_profile, fname=firstname, lname=lastname, image=image, username=username, email=email, phone=phone, dob=dob,  gender=gender, city=city, state=state, country=country,)

                        elif request.FILES.get('chooseimage') != None:
                            upimage = request.FILES.get('chooseimage')
                            settings.updatepro(request=request, userobject = user_object, userprofile=user_profile, fname=firstname, lname=lastname, image=upimage, username=username, email=email, phone=phone, dob=dob,  gender=gender, city=city, state=state, country=country,)


                # User profile in Change Email Address After Check Email Address
                elif user_object.email != email:
                    if User.objects.filter(email = email).exists() or email == "kingshopping23@gmail.com":
                        messages.error(request, 'This Email Address Allready Exists!')

                    else:
                        if request.FILES.get('chooseimage') == None:
                            image = user_profile.profileimage
                            settings.updatepro(request=request, userobject = user_object, userprofile=user_profile, fname=firstname, lname=lastname, image=image, username=username, email=email, phone=phone, dob=dob,  gender=gender, city=city, state=state, country=country,)

                        elif request.FILES.get('chooseimage') != None:
                            upimage = request.FILES.get('chooseimage')
                            settings.updatepro(request=request, userobject = user_object, userprofile=user_profile, fname=firstname, lname=lastname, image=upimage, username=username, email=email, phone=phone, dob=dob,  gender=gender, city=city, state=state, country=country,)

                # User profile not changed username and email address after any other change
                else:

                    if request.FILES.get('chooseimage') == None:
                        image = user_profile.profileimage

                        settings.updatepro(request=request, userobject = user_object, userprofile=user_profile, fname=firstname, lname=lastname, image=image, username=username, email=email, phone=phone, dob=dob,  gender=gender, city=city, state=state, country=country,)
                    
                    elif request.FILES.get('chooseimage') != None:
                        upimage = request.FILES.get('chooseimage')

                        settings.updatepro(request=request, userobject = user_object, userprofile=user_profile, fname=firstname, lname=lastname, image=upimage, username=username, email=email, phone=phone, dob=dob,  gender=gender, city=city, state=state, country=country,)

            userdata = {
                'login_user' : user_object,
                'wishcount' : allwishlistitems,
                'cartcount' : allcartitems,
                'menus' : menu_bar_category,

                'user_profile': user_profile,
                'username': user_object,
            }

            return render(request, 'includefiles/profile.html', userdata)

        else:
            messages.error(request, "Sorry! User is not logged in")
            # Menu Bar Random Categorys
            get_categorylist = categorys.objects.filter(removestate__exact=0)
            menu_bar_category = random.sample(list(get_categorylist), k=7)
            settingdata = {
                'menus' : menu_bar_category,
                'notuser' : 0,
            }
            return render(request, 'includefiles/profile.html', settingdata)


    # User Profile Update Method
    def updatepro(**uppro):
        uo = uppro['userobject']    
        up = uppro['userprofile']    

        up.profileimage = uppro['image']
        up.firstname = uppro['fname']
        up.lastname = uppro['lname']
        up.phone = uppro['phone']
        up.dob = uppro['dob']
        up.gender = uppro['gender']
        up.city = uppro['city']
        up.state = uppro['state']
        up.country = uppro['country']
        up.save()

        uo.username = uppro['username']
        uo.email = uppro['email']
        uo.save()

        messages.success(uppro['request'], "Your Profile Is Update SuccessFully.")
        return redirect('/account/profile/')




    # -------------------------------------------------- Address Page In Setting Page --------------------------------------------------
    def settingAddress(request):
        if request.user.is_authenticated:
            user_object = User.objects.get(username=request.user.username)
            allwishlistitems = uwishlist.objects.filter(user__exact=user_object).count()
            allcartitems = cart.objects.filter(user__exact=user_object).count()

            # Menu Bar Random Categorys
            get_categorylist = categorys.objects.filter(removestate__exact=0)
            menu_bar_category = random.sample(list(get_categorylist), k=7)

            # User All Address Records
            user_addr = useraddress.objects.filter(user=user_object, removestate=0).values()

            if request.method == "POST":

                addrtitle = request.POST['addrtitle']
                addrdescription = request.POST['addrdescription']

                newaddr = useraddress(user=user_object, addtitle=addrtitle, adddescription=addrdescription)
                newaddr.save()
                messages.success(request, "Create New Address SuccessFully.")

                return redirect('/account/address/')


            else:
                useralladd = {
                    'login_user' : user_object,
                    'wishcount' : allwishlistitems,
                    'cartcount' : allcartitems,
                    'menus' : menu_bar_category,

                    'getalladd': user_addr,
                }

                return render(request, 'includefiles/address.html', useralladd)

        else:
            messages.error(request, "Sorry! User is not logged in")
            # Menu Bar Random Categorys
            get_categorylist = categorys.objects.filter(removestate__exact=0)
            menu_bar_category = random.sample(list(get_categorylist), k=7)
            settingdata = {
                'notuser' : 0,
                'menus' : menu_bar_category,
            }
            return render(request, 'includefiles/address.html', settingdata)


    # -------------------------------------------------- Edit Address Page In Setting Page --------------------------------------------------
    def address_edit(request):
        if request.user.is_authenticated:

            if request.method == "GET":
                global getaddrid
                getaddrid = request.GET.get('setaddrid')
                if getaddrid != None:
                    getaddrdata = useraddress.objects.get(addid=getaddrid, removestate=0)
                else:
                    return redirect('/account/address/')

            elif request.method == "POST":
                getuptitle = request.POST['editaddrtitle']
                getupdesc = request.POST['editaddrdescription']

                upaddress = useraddress.objects.get(addid=getaddrid, removestate=0)
                upaddress.addtitle = getuptitle
                upaddress.adddescription = getupdesc
                upaddress.save()

                messages.success(request, "Address Update SuccessFully.")
                return redirect('/account/address/')


            addressdata = json.dumps({
                'setaddrtitle' : getaddrdata.addtitle,
                'setaddrdesc' : getaddrdata.adddescription,
            })


            return HttpResponse(addressdata, content_type="application/json")
        else:
            messages.error(request, "Sorry! User is not logged in")
            return redirect('/')


    # -------------------------------------------------- Delete Address Page In Setting Page --------------------------------------------------
    def address_remove(request):
        if request.user.is_authenticated:
            if request.method == "GET":
                removeaddrid = request.GET.get('addrremoveid')

                if removeaddrid != None:
                    getaddr = useraddress.objects.get(addid=removeaddrid)
                    getaddr.removestate = 1
                    getaddr.save()
                    messages.success(request, "Address Is Remove SuccessFully.")
                    return HttpResponse()

                else:
                    return redirect('/account/address/')
        else:
            messages.error(request, "Sorry! User is not logged in")
            return redirect('/')





    # -------------------------------------------------- Security Page In Setting Page --------------------------------------------------
    def settingSecurity(request):
        if request.user.is_authenticated:
            user_object = User.objects.get(username=request.user.username)
            allwishlistitems = uwishlist.objects.filter(user__exact=user_object).count()
            allcartitems = cart.objects.filter(user__exact=user_object).count()

            # Menu Bar Random Categorys
            get_categorylist = categorys.objects.filter(removestate__exact=0)
            menu_bar_category = random.sample(list(get_categorylist), k=7)

            if request.method == "POST":
                oldpassword = request.POST['oldpassword']
                newpassword = request.POST['newpassword']
                newrepassword = request.POST['newrepassword']
                checkpass = user_object.check_password(oldpassword)

                if checkpass == True:

                    if oldpassword == newpassword:
                        messages.error(request, 'Sorry! New password is a current password')
                    
                    else:
                    
                        if newpassword == newrepassword:
                            user_object.set_password(newpassword)
                            user_object.save()
                            auth.authenticate(username=user_object, password=newpassword)
                            messages.success(request, 'Password update successfully.')


                        else:
                            messages.error(request, 'Sorry! Password is not match!')


                else:
                    messages.error(request, 'Please, enter the current password!')

            else:
                # Change The Email Address *****@Gmail.com
                loginuseremail = user_object.email
                res = loginuseremail[2 : loginuseremail.find('@')]
                useremail = loginuseremail.replace(res, '****')


                # Check Two Step Verification
                checktwostep = userprofile.objects.get(user=user_object, removestate = 0)
                
                usersecurity = {
                    'login_user' : user_object,
                    'wishcount' : allwishlistitems,
                    'cartcount' : allcartitems,
                    'menus' : menu_bar_category,

                    'loginuseremail' : useremail,
                    'twostep' : checktwostep.twostep
                }

                return render(request, 'includefiles/security.html', usersecurity)

        else:
            # Random Categorys
            get_categorylist = categorys.objects.filter(removestate__exact=0)

            # Menu Bar Random Categorys
            menu_bar_category = random.sample(list(get_categorylist), k=7)
            messages.error(request, 'Sorry! User is not logged in')
            usersecurity = {
                'notuser' : 0,
                'menus' : menu_bar_category,
            }
            return render(request, 'includefiles/security.html', usersecurity)


    # -------------------------------------------------- Password Chage Button Send OTP In Setting Page --------------------------------------------------
    def sendotpuser(request):
        if request.user.is_authenticated:

            if request.method == "GET":
                userval = request.GET.get('uservalue')

                if userval != None:
                    user_object = User.objects.get(username=request.user.username)
                    changepscode = generatcode(6)

                    setuserotp = userprofile.objects.get(user_id=user_object.id, removestate=0)
                    getcustemail = user_object.email

                    sendUserMail(getcustemail, 'common/email/sendcode/resetpassword.html', f'King Shopping Account {changepscode} is your verification code for secure access', changepscode).start()
                    setuserotp.uotp = changepscode
                    setuserotp.save()

                    t = 60
                    while t:
                        mins, secs = divmod(t, 60)
                        timer = '{:02d}:{:02d}'.format(mins, secs)
                        print(timer, end="\r")
                        time.sleep(1)
                        checktimer = 0
                        t -= 1
                        if(t == 0):
                            setuserotp.uotp = 0
                            setuserotp.save()

                    return HttpResponse()
                
                else:
                    return redirect('/account/security/')
        
        else:
            messages.error(request, "Sorry! User is not logged in")
            return redirect('/')


    # -------------------------------------------------- Check OTP In Password Change In Setting Page --------------------------------------------------
    def passwordotp(request):
        if request.user.is_authenticated:
            user_object = User.objects.get(username=request.user.username)

            if request.method == "GET":
                getuserotp = request.GET.get('userotp')

                if getuserotp != None:
                    gettbuserotp = userprofile.objects.get(user=user_object, removestate=0)
                    checkotp = ""
                    if getuserotp == gettbuserotp.uotp:
                        checkotp = 1
                        gettbuserotp.uotp = 0
                        gettbuserotp.save()
                    else:
                        checkotp = 0

                    pdata = json.dumps({
                        'status' : checkotp,
                    })

                    return HttpResponse(pdata, content_type="application/json")

                else:
                    return redirect('/account/security/')                

        else:
            messages.error(request, "Sorry! User is not logged in")
            return redirect('/')




    # -------------------------------------------------- Two Step Verification Check Email Address In Two-step Verification ON Setting Page --------------------------------------------------
    def twostepemail(request):
        if request.user.is_authenticated:
            user_object = User.objects.get(username=request.user.username)
            changepscode = generatcode(6)

            if request.method == "GET":
                userinemail = request.GET.get('useremail')

                # check the your email address is empty
                if userinemail != "":
                    checkuseremail = 0
                    getuserid = User.objects.filter(email=userinemail)

                    if getuserid.exists():
                
                        # Check Userprofile Records
                        checkuser = userprofile.objects.filter(user_id=getuserid[0].id, removestate=0)
                        if checkuser.exists():
                            if (user_object.email == userinemail):
                                checkuser.update(uotp=changepscode)
                                checkuseremail = 1

                                sendUserMail(user_object.email, 'common/email/sendcode/twostepcode.html', f'King Shopping Account {changepscode} is your verification code for secure access', changepscode).start()

                            else:
                                checkuseremail = 0

                        else:
                            checkuseremail = 0

                    else:
                        checkuseremail = 0

                    sdata = json.dumps({
                        'checkemailstatus':checkuseremail
                    })
                        
                    return HttpResponse(sdata, content_type="application/json")

                else:
                    return redirect('/account/security/')
        else:
            messages.error(request, "Sorry! User is not logged in")
            return redirect('/')


    # -------------------------------------------------- Check OTP In Two Step Verification In Two-step Verification ON Settings Page --------------------------------------------------
    def twostepcheckotp(request):
        if request.user.is_authenticated:
            user_object = User.objects.get(username=request.user.username)

            if request.method == "GET":
                getuserotp = request.GET.get('userotp')

                if getuserotp != None:
                    gettbuserotp = userprofile.objects.get(user=user_object, removestate=0)

                    checkotp = ""

                    if getuserotp == gettbuserotp.uotp:
                        checkotp = 1
                        gettbuserotp.twostep = 1
                        gettbuserotp.uotp = 0
                        gettbuserotp.save()
                        

                    else:
                        checkotp = 0
            
                    sdata = json.dumps({
                        'status' : checkotp,
                    })

                    return HttpResponse(sdata, content_type="application/json")

                else:
                    return redirect('/account/security/')

        else:
            messages.error(request, "Sorry! User is not logged in")
            return redirect('/')


    # -------------------------------------------------- Turn OFF Two Step Verification In Setting Page --------------------------------------------------
    def twostepoff(request):
        if request.user.is_authenticated:
            user_object = User.objects.get(username=request.user.username)

            if request.method == "POST":
                userpassword = request.POST['userloginpassword']
                user = auth.authenticate(username=user_object, password=userpassword)

                if user is not None:
                    twostepoff = userprofile.objects.get(user=user_object, twostep=1, removestate=0)
                    twostepoff.twostep = 0;
                    twostepoff.save()
                    messages.success(request, "Turn Off 2-Step Verification SuccessFully")
                    

                else:
                    messages.error(request, "Please, Enter The Currect Password.")

                return redirect('/account/security/')

            else:
                return redirect('/account/security/')

        else:
            messages.error(request, "Sorry! User is not logged in")
            return redirect('/')




    # -------------------------------------------------- Deactive Account --------------------------------------------------
    def lastlocation(request):
        if request.user.is_authenticated:
            user_object = User.objects.get(username=request.user.username)
            allwishlistitems = uwishlist.objects.filter(user__exact=user_object).count()
            allcartitems = cart.objects.filter(user__exact=user_object).count()

            # Menu Bar Random Categorys
            get_categorylist = categorys.objects.filter(removestate__exact=0)
            menu_bar_category = random.sample(list(get_categorylist), k=7)

            getlocation = userLocation.objects.filter(userid=user_object).order_by('-login_date')

            locationdata = {
                'login_user' : user_object,
                'wishcount' : allwishlistitems,
                'cartcount' : allcartitems,
                'menus' : menu_bar_category,

                'allLocation' : getlocation,
            }

            return render(request, 'includefiles/location.html', locationdata)

        else:
            messages.error(request, "Sorry! User is not logged in")
            # Menu Bar Random Categorys
            get_categorylist = categorys.objects.filter(removestate__exact=0)
            menu_bar_category = random.sample(list(get_categorylist), k=7)
            locationdata = {
                'notuser' : 0,
                'menus' : menu_bar_category,
            }
            return render(request, 'includefiles/location.html', locationdata)




    # -------------------------------------------------- Deactive Account --------------------------------------------------
    def deactiveAccount(request):
        if request.user.is_authenticated:
            user_object = User.objects.get(username=request.user.username)

            if request.method == "POST":
                userpassword = request.POST['userloginpassword']
                user = auth.authenticate(username=user_object, password=userpassword)

                if user is not None:
                    deactiveaccount = userprofile.objects.get(user=user_object, removestate=0)
                    deactiveaccount.removestate = 1;
                    deactiveaccount.reaccountdate = datetime.now();
                    deactiveaccount.save()

                    user_object.is_active = False
                    user_object.save()
                    auth.logout(request)
                    messages.success(request, "Your Account Is Deactive Account SuccessFully.")
                    

                else:
                    messages.error(request, "Please, Enter The Currect Password.")

                return redirect('/')

            else:
                return redirect('/account/security/')                

        
        else:
            messages.error(request, "Sorry! User is not logged in")
            return redirect('/')



# ================================================= Help Center Class =================================================
class helpcenter:
    # -------------------------------------------------- User Help Page --------------------------------------------------
    def userhelp(request):
        if request.user.is_authenticated:
            user_object = User.objects.get(username=request.user.username)
            allwishlistitems = uwishlist.objects.filter(user__exact=user_object).count()
            allcartitems = cart.objects.filter(user__exact=user_object).count()

            # Menu Bar Random Categorys
            get_categorylist = categorys.objects.filter(removestate__exact=0)
            menu_bar_category = random.sample(list(get_categorylist), k=7)
            
            # Get User Issues
            getissues = customerissues.objects.filter(user=user_object)

            helpdata = {
                'login_user' : user_object,
                'wishcount' : allwishlistitems,
                'cartcount' : allcartitems,
                'menus' : menu_bar_category,

                'allissues': getissues,
            }

            return render(request, 'webpages/userHelp.html', helpdata)

        else:
            # Menu Bar Random Categorys
            get_categorylist = categorys.objects.filter(removestate__exact=0)
            menu_bar_category = random.sample(list(get_categorylist), k=7)
            helpdata = {
                'menus' : menu_bar_category,
                'notuser' : 0,
            }
            return render(request, 'webpages/userHelp.html', helpdata)

    # -------------------------------------------------- Issues 2 In Helpcenter Page --------------------------------------------------
    def issues_two(request):
        if request.user.is_authenticated:
            user_object = User.objects.get(username=request.user.username)
            allwishlistitems = uwishlist.objects.filter(user__exact=user_object).count()
            allcartitems = cart.objects.filter(user__exact=user_object).count()

            if request.method == "POST":
                custissue = request.POST['custissues']
                custdesc = request.POST['custdescription']

                custissues = customerissues.objects.create(user=user_object, issueshort=custissue, issues=custdesc)
                custissues.save()
                messages.success(request, "Your Issues Send Successfully.")
                return redirect('/')

            # Menu Bar Random Categorys
            get_categorylist = categorys.objects.filter(removestate__exact=0)
            menu_bar_category = random.sample(list(get_categorylist), k=7)


            issuesdata = {
                'login_user' : user_object,
                'wishcount' : allwishlistitems,
                'cartcount' : allcartitems,
                'menus' : menu_bar_category,
            }

            return render(request, 'includefiles/helpCenter/issues2.html', issuesdata)

        else:
            # Menu Bar Random Categorys
            get_categorylist = categorys.objects.filter(removestate__exact=0)
            menu_bar_category = random.sample(list(get_categorylist), k=7)


            issuesdata = {
                'menus' : menu_bar_category,
                'notuser' : 0,
            }

            return render(request, 'includefiles/helpCenter/issues2.html', issuesdata)

    # -------------------------------------------------- Issues 3 In Helpcenter Page --------------------------------------------------
    def issues_three(request):# Menu Bar Random Categorys
        if request.user.is_authenticated:
            user_object = User.objects.get(username=request.user.username)
            allwishlistitems = uwishlist.objects.filter(user__exact=user_object).count()
            allcartitems = cart.objects.filter(user__exact=user_object).count()

            # Menu Bar Random Categorys
            get_categorylist = categorys.objects.filter(removestate__exact=0)
            menu_bar_category = random.sample(list(get_categorylist), k=7)

            issuesdata = {
                'login_user' : user_object,
                'wishcount' : allwishlistitems,
                'cartcount' : allcartitems,
                'menus' : menu_bar_category,
            }

            return render(request, 'includefiles/helpCenter/deactiveAccount.html', issuesdata)

        else:
            # Menu Bar Random Categorys
            get_categorylist = categorys.objects.filter(removestate__exact=0)
            menu_bar_category = random.sample(list(get_categorylist), k=7)


            issuesdata = {
                'menus' : menu_bar_category,
                'notuser' : 0,
            }

            return render(request, 'includefiles/helpCenter/deactiveaccount.html', issuesdata)

    # -------------------------------------------------- Issues 4 In Helpcenter Page --------------------------------------------------
    def issues_content(request):
        if request.user.is_authenticated:
            user_object = User.objects.get(username=request.user.username)
            allwishlistitems = uwishlist.objects.filter(user__exact=user_object).count()
            allcartitems = cart.objects.filter(user__exact=user_object).count()

            # Menu Bar Random Categorys
            get_categorylist = categorys.objects.filter(removestate__exact=0)
            menu_bar_category = random.sample(list(get_categorylist), k=7)

            issuesdata = {
                'login_user' : user_object,
                'wishcount' : allwishlistitems,
                'cartcount' : allcartitems,
                'menus' : menu_bar_category,
            }

            return render(request, 'includefiles/helpCenter/contact.html', issuesdata)

        else:
            # Menu Bar Random Categorys
            get_categorylist = categorys.objects.filter(removestate__exact=0)
            menu_bar_category = random.sample(list(get_categorylist), k=7)


            issuesdata = {
                'menus' : menu_bar_category,
                'notuser' : 0,
            }

            return render(request, 'includefiles/helpCenter/contact.html', issuesdata)




# -------------------------------------------------- 404 Page --------------------------------------------------
def pagenotfound(request):
    # Menu Bar Random Categorys
    get_categorylist = categorys.objects.filter(removestate__exact=0)
    menu_bar_category = random.sample(list(get_categorylist), k=7)
    pagedata = {
        'menus' : menu_bar_category,
    }
    return render(request, 'common/orderemail.html', pagedata)


# ------------------------------------------------- Send Default Information And OTP Mail Function -------------------------------------------------
# sendUserMail(getcustemail, template_path, mail_subject, otpnumber).start()
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
            print("Product Mail is not send", e)




# ------------------------------------------------- Generate The OTP -------------------------------------------------
def generatcode(generateno):
    generate = [
        '1','2','3','4','5','6','7','8','9','0',
        'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
        'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'
    ]

    gotp = ""
    for x in range(generateno):
        gotp = gotp + random.choice(generate)[0]
    return gotp


# -------------------------------------------------- User Set Location Function --------------------------------------------------
def setLocation(userid):
    url = "https://ipinfo.io/json"
    response = urlopen(url)
    data = json.load(response)
    loc = data['loc'].split(',')
    userLocation.objects.create(userid_id=userid, longitude=loc[0], latitude=loc[1])
