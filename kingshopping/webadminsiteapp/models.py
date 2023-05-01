from datetime import datetime
from email.policy import default
from os import remove
from django.db import models
from django.contrib.auth import get_user_model
import uuid
from django.utils import timezone

from ckeditor.fields import RichTextField


User = get_user_model()


class userprofile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mainuser')
    firstname = models.CharField(max_length=50, default="")
    lastname = models.CharField(max_length=50, default="")
    phone = models.CharField(max_length=10, default="")
    dob = models.CharField(max_length=20, default="")
    gender = models.CharField(max_length=50, default="")
    city = models.CharField(max_length=50, default="",)
    state = models.CharField(max_length=50, default="")
    country = models.CharField(max_length=50, default="")
    country = models.CharField(max_length=50, default="") 
    profileimage = models.ImageField(upload_to="UsersProfile", default="blank-profile-picture.png")
    twostep = models.IntegerField(default=0)
    uotp = models.CharField(max_length=6, default="")
    rmuserdate = models.DateField(default=timezone.now)
    reaccountdate = models.DateField(default=timezone.now)
    removestate = models.IntegerField(default=0)

    def __str__(self):
        return self.firstname + ' ' + self.lastname



class useraddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    addid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    addtitle = models.CharField(max_length=100, default="address")
    adddescription = models.TextField(default="")
    removestate = models.IntegerField(default=0)

    def __str__(self):
        return self.addtitle


class userLocation(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    longitude = models.CharField(max_length=50, default="")
    latitude = models.CharField(max_length=50, default="")
    login_date = models.DateTimeField(default=timezone.now)



class categorys(models.Model):
    cid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    catname = models.CharField(max_length=50, default="", null= True)
    catdescription = models.TextField(max_length="100", default="")
    catimage = models.ImageField(upload_to="Categorys", default="noimage.jpg")
    catdate = models.DateTimeField(default=timezone.now)
    catrmdate = models.DateTimeField(default=timezone.now)
    removestate = models.IntegerField(default=0)

    def __str__(self):
        return self.catname
    


class brands(models.Model):
    bid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    cid = models.ForeignKey("webadminsiteapp.categorys", on_delete=models.CASCADE)
    bname = models.CharField(max_length=50, default="", null= True)
    bdescription = models.TextField(max_length="100", default="")
    bdate = models.DateTimeField(default=timezone.now)
    brmdate = models.DateTimeField(default=timezone.now)
    removestate = models.IntegerField(default=0)

    def __str__(self):
        return self.bname



class products(models.Model):
    proid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    bid = models.ForeignKey("webadminsiteapp.brands", on_delete=models.CASCADE)
    cid = models.ForeignKey("webadminsiteapp.categorys", on_delete=models.CASCADE, null=True)
    proname = models.CharField(max_length=500, default="")
    prodescription = RichTextField()
    proprice = models.IntegerField(default=0)
    propercentage = models.IntegerField(default=0)
    prostock = models.IntegerField(default=0)
    procolorname = models.CharField(max_length=50, default="")
    procolor = models.CharField(max_length=50, default="")
    ram = models.CharField(max_length=50, default="No")
    rom = models.CharField(max_length=50, default="No")
    clothes_gender = models.CharField(max_length=50, default="No")
    clothes_size = models.CharField(max_length=50, default="No")
    watch_type = models.CharField(max_length=50, default="No")
    proimage1 = models.ImageField(upload_to='ProductsImages', default="noimage.png")
    proimage2 = models.ImageField(upload_to='ProductsImages', default="noimage.png")
    proimage3 = models.ImageField(upload_to='ProductsImages', default="noimage.png")
    proimage4 = models.ImageField(upload_to='ProductsImages', default="noimage.png")
    proimage5 = models.ImageField(upload_to='ProductsImages', default="noimage.png")
    prodate = models.DateTimeField(default=timezone.now)
    prormdate = models.DateTimeField(default=timezone.now)
    removestate = models.IntegerField(default=0)

    def __str__(self):
        return self.proname


class products_general_details(models.Model):
    geneid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    proid = models.ForeignKey("webadminsiteapp.products", on_delete=models.CASCADE)
    general_details = RichTextField(default="")
    removestate = models.IntegerField(default=0)




class products_displays_details(models.Model):
    disid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    proid = models.ForeignKey("webadminsiteapp.products", on_delete=models.CASCADE)
    display_details = RichTextField(default="")
    show_display = models.CharField(max_length=50, default="hide")
    removestate = models.IntegerField(default=0)



class products_connectivity_details(models.Model):
    connid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    proid = models.ForeignKey("webadminsiteapp.products", on_delete=models.CASCADE)
    connectivity_details = RichTextField(default="")
    show_connectivity = models.CharField(max_length=50, default="hide")
    removestate = models.IntegerField(default=0)


class products_osprocesser_details(models.Model):
    osproid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    proid = models.ForeignKey("webadminsiteapp.products", on_delete=models.CASCADE)
    osprocesser_details = RichTextField(default="")
    show_osprocesser = models.CharField(max_length=50, default="hide")
    removestate = models.IntegerField(default=0)



class products_other_details(models.Model):
    otherid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    proid  = models.ForeignKey("webadminsiteapp.products", on_delete=models.CASCADE)
    other_details = RichTextField(default="")
    show_other = models.CharField(max_length=50, default="hide")
    removestate = models.IntegerField(default=0)




class products_dimensions_warranty_details(models.Model):
    dimenid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    proid = models.ForeignKey("webadminsiteapp.products", on_delete=models.CASCADE)
    dimension_warranty_details = RichTextField(default="")
    show_dimwarr = models.CharField(max_length=50, default="hide")
    removestate = models.IntegerField(default=0)




class cart(models.Model):
    cartid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    proid = models.ForeignKey("webadminsiteapp.products", on_delete=models.CASCADE)
    proqty = models.IntegerField(default=0)
    catproprice = models.IntegerField(default=0)
    deliaddr = models.ForeignKey("webadminsiteapp.useraddress", on_delete=models.CASCADE)
    wdate = models.DateField(default=timezone.now)



class uwishlist(models.Model):
    wid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    proid = models.ForeignKey("webadminsiteapp.products", on_delete=models.CASCADE)
    wdate = models.DateField(default=timezone.now)



class employees(models.Model):
    eid = models.ForeignKey(User, on_delete=models.CASCADE)
    efirstname = models.CharField(max_length=50, default='')
    elastname = models.CharField(max_length=50, default='')
    ephone = models.CharField(max_length=10, default='')
    edob = models.CharField(max_length=20,default='')
    egender = models.CharField(max_length=50)
    eaddress = models.TextField(default='')
    edeparements = models.CharField(max_length=50, default='')
    salary = models.IntegerField(default=3000)
    city = models.CharField(max_length=50, default='')
    state = models.CharField(max_length=50, default='')
    country = models.CharField(max_length=50, default='')
    profileimage = models.ImageField(upload_to="EmployeeProfile", default="blank-profile-picture.png")    
    ehiredate = models.DateField(default=timezone.now)
    etwostepauthonetication = models.IntegerField(default=0)
    eOTP = models.CharField(max_length=6, default="")
    rmempdate = models.DateField(default=timezone.now)
    removestate = models.IntegerField(default=0)

    def __str__(self):
        return self.efirstname +" "+ self.elastname



class orders(models.Model):
    oid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    proid = models.ForeignKey("webadminsiteapp.products", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deliaddr = models.ForeignKey("webadminsiteapp.useraddress", on_delete=models.CASCADE)
    proqty = models.IntegerField(default=1)
    productstatus = models.CharField(max_length=50, default="conform")
    paymentmode = models.CharField(max_length=50, default="")
    returnpro = models.CharField(max_length=50, default="No")
    ordate = models.DateTimeField(default=timezone.now)
    canceldate = models.DateTimeField(default=timezone.now)
    deliveddate = models.DateField(default=timezone.now)
    returndate = models.DateField(default=timezone.now)
    removestate = models.IntegerField(default=0)


class returnproduct(models.Model):
    reid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    oid = models.ForeignKey("webadminsiteapp.orders", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rnproce = models.CharField(max_length=20, default="")
    rnresone = models.CharField(max_length=500, default="")
    rncomment = models.TextField(default="")
    rndate = models.DateField(default=timezone.now)
    rncanceldate = models.DateField(default=timezone.now)


class banners(models.Model):
    bannerid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    proid = models.ForeignKey("webadminsiteapp.products", on_delete=models.CASCADE)
    bannerImage = models.ImageField(upload_to='Banners', default="noimage.jpg")
    uploadedate = models.DateTimeField(default=timezone.now)
    removestate = models.IntegerField(default=0)


class customerissues(models.Model):
    issuesid = models.UUIDField(default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issueshort = models.CharField(max_length=100, default="")
    issues = models.TextField(default="")
    idate = models.DateField(default=timezone.now)
