// Any Modal Close
$('.btnmodalclose').on('click', function () {
    var closeModal = $(this).attr('data-dismiss')
    $(closeModal).modal('toggle');
});



// User Table Edit Button
$('.usereditmodalbtn').on('click', function () {
    var uid = $(this).attr('data-click');
    $.ajax({
        type: "GET",
        url: "/adminsideproweb/users/edit/",
        data: {
            'userid' : uid
        },
        success: function (data) {
            $('#userEditModal').modal('show');

            $('#efirstname').val(data.firstname);
            $('#elastname').val(data.lastname);
            $('#eusername').val(data.username);
            $('#eemail').val(data.email);
            $('#ephone').val(data.phone);
            $('#edob').val(data.dob);
            $('#egender').val(data.gender);
            $('#ecity').val(data.city);
            $('#estate').val(data.state);
            $('#ecountry').val(data.country);
            $('#eUserprofile').attr('src',data.profileimage)
            
        }
    });
    return false;
});


// User Remove Button Click
$('.userremovebtn').on('click', function () {
    var ruid = $(this).attr('data-click');

    $.ajax({
        type: "GET",
        url: "/adminsideproweb/users/remove/",
        data: {
            'ruserid' : ruid
        },
        success: function (rdata) {
            $('.deleteModalMessage').html('Are Your Sure ' + rdata.rusername + ' User Is Delete?');
            $('#deleteModal').modal('show');
            $('#deleteForm').attr('action','/adminsideproweb/users/remove/');
        }
    });
});



// Employee Edit Record Button Click
$('.eEmployeeEdit').on('click', function () {
    var eid = $(this).attr('data-click');
    $('#EmployeeForm').append("<input type='hidden' name='uempid' id='empid'>")
    $('#empid').val(eid);

    $.ajax({
        type: "GET",
        url: "/adminsideproweb/employees/edit/",
        data: {
            'empid' : eid
        },
        success: function (empdata) {
            $('#employeeEditModal').modal('show');
            
            $("#eEprofileimage").attr('src', empdata.eproimage);
            $("#eEfirstname").val(empdata.efirstname);
            $("#eElastname").val(empdata.elastname);
            $("#eEusername").val(empdata.eusername);
            $("#eEemail").val(empdata.eemail);
            $("#eEphone").val(empdata.ephone);
            $("#eEdob").val(empdata.edob);
            $("#eEaddress").html(empdata.eaddr);
            $("#eEsalary").val(empdata.esalary);
            $("#eEgander").val(empdata.egender);
            $("#eEdeparement").val(empdata.edep);
            $("#eEcity").val(empdata.ecity);
            $("#eEstate").val(empdata.estate);
            $("#eEcountry").val(empdata.ecountry);
            
        }
    });
    return false;
});



// Employee Remove Button Click
$('.eEmployeeRemove').on('click', function () {
    var rempid = $(this).attr('data-click');

    $.ajax({
        type: "GET",
        url: "/adminsideproweb/employees/remove/",
        data: {
            'rmempid' : rempid
        },
        success: function (rdata) {
            $('.deleteModalMessage').html('Are Your Sure ' + rdata.rmemployeenm + ' Employee Is Delete?');
            $('#deleteModal').modal('show');
            $('#deleteForm').attr('action','/adminsideproweb/employees/remove/');
        }
    });
});



// Category Edit Record Button Click
$('.ccatEditbtn').on('click', function () {
    var ecid = $(this).attr('data-click');
    
    $.ajax({
        type: "GET",
        url: "/adminsideproweb/categorys/edit/",
        data: {
            'getcid' : ecid
        },
        success: function (cdata) {
            $('#editCategoryModal').modal('show');

            $('#ucategoryName').val(cdata.cname);
            $('#ucategoryDescription').html(cdata.cdesc);
            $('#uCategoryImage').attr('src', cdata.cimage);
        }
    });
});



// Category Remove Button CLick
$('.ccatRemovebtn').on('click', function () {
    var rcid = $(this).attr('data-click');

    $.ajax({
        type: "GET",
        url: "/adminsideproweb/categorys/remove/",
        data: {
            'getrcid' : rcid
        },
        success: function (cdata) {
            $('.deleteModalMessage').html('Are Your Sure ' + cdata.rmcategory + ' Category Is Delete?');
            $('#deleteModal').modal('show');
            $('#deleteForm').attr('action','/adminsideproweb/categorys/remove/');
        }
    });

});



// Brands Edit Record Button Click
$('.brandEditBtn').on('click', function () {
    var bid = $(this).attr('data-click');

    $.ajax({
        type: "GET",
        url: "/adminsideproweb/brands/edit/",
        data: {
            'getbid' : bid
        },
        success: function (bdata) {
            $('#editBrandModal').modal('show');

            $('#uBrandName').val(bdata.bname);
            $('#uBrandDescription').val(bdata.bdesc);

            let setBrandCategoryBox = $('#setcategory');
            setBrandCategoryBox.empty();
            const bcategorydata = bdata.cname;
            $.each(bcategorydata, function(arrid, arrname) {
                let bcategorys = $("<option/>", {
                    value: arrname.catname,     // catname is tabel filed name
                    text: arrname.catname,      // catname is tabel filed name
                });
                setBrandCategoryBox.append(bcategorys);
            });

            setBrandCategoryBox.val(bdata.bcatname);
        }
    });
});




// Brands Table Remove Button
$('.brandRemoveBtn').on('click', function () {
    var rbid = $(this).attr('data-click');

    $.ajax({
        type: "GET",
        url: "/adminsideproweb/brands/remove/",
        data: {
            'getrbid' : rbid
        },
        success: function (rdata) {
            $('.deleteModalMessage').html('Are Your Sure ' + rdata.rmbrand + ' Brand Is Delete?');
            $('#deleteModal').modal('show');
            $('#deleteForm').attr('action','/adminsideproweb/brands/remove/')
        }
    });
});



// Product Edit Category Change After Set Brands
$('#eproducteditcategorys').on('change', function () {
    let setcat = $(this).val()
    alert(setcat)
    
    $.ajax({
        type: "GET",
        url: "/adminsideproweb/products/change/brands/",
        data: {
            'setcat' : setcat
        },
        success: function (sbrands) {
            let ProductEditbrandsbox = $('#eproducteditbrands');
            ProductEditbrandsbox.empty();
            const getproductbrands = sbrands.setbrands
            $.each(getproductbrands, function (arrid, arrname) {
                let setProductEditcategory = $("<option/>", {
                    value: arrname.bname,
                    text: arrname.bname,
                })
                ProductEditbrandsbox.append(setProductEditcategory);
            });
            ProductEditbrandsbox.val(sbrands.probrand);

        }
    });
});



// Product Remove Button Click
$('.ProductRemoveBtn').on('click', function () {
    let rmproid = $(this).attr('data-click');

    $.ajax({
        type: "GET",
        url: "/adminsideproweb/products/remove/",
        data: {
            'rmproid' : rmproid
        },
        success: function () {
            $('.deleteModalMessage').html('Are Your Sure This Product Is Delete?');
            $('#deleteModal').modal('show');
            $('#deleteForm').attr('action','/adminsideproweb/products/remove/')
        }
    });
});



// Setting Page Bin Record Restore Button
$('.binrestorebtn').on('click', function () {
    let restoreid = $(this).attr('data-restore');
    let bintable = $(this).attr('data-table');

    $.ajax({
        type: "GET",
        url: "/adminsideproweb/settings/restore/reback/",
        data: {
            'bintable' : bintable,
            'restore' : restoreid,
        },
        success: function (rdata) {
            location.href = "/adminsideproweb/settings/restore/";
        }
    });

});



// Password Button Close Button
$('.passwordclosebtn').on('click', function () {
    location.href = '/adminsideproweb/settings/security/';
});



// OTP Modal Submit Button Click
$('.otpModalbtn').on('click', function () {
    let userotp = $('.userotp').val();
    let otpformval = $('#otpModal').attr('data-val');

    if (userotp != 0) {

        // Password Change OTP Submit Button CLick
        if (otpformval == 'passwordchange') {
            $.ajax({
                type: "GET",
                url: "/adminsideproweb/settings/security/OTPcheck/",
                data: {
                    'getuserotp': userotp
                },
                success: function (chdata) {
                    if (chdata.sdata == 1) {
                        $('.userotp').val('');
                        $('#otpModal').modal('toggle');
                        $('#oldpassword').attr('readonly',false);
                        $('#password').attr('readonly',false);
                        $('#repassword').attr('readonly',false);
                        $('#changepasswordbtns').html("<button type='button' class='passwordclosebtn btn btn-outline-warning ms-1'>Close</button><button class='btn btn-outline-primary ms-1'>Change Password</button>");
                    }
                    else{
                        $('.otperror').html('Please, Enter The Currect OTP.')
                    }
                }
            });
        }

        // Two Step Verfication OTP Submit Button CLick
        else if (otpformval == 'twostep'){
            $.ajax({
                type: "GET",
                url: "/adminsideproweb/settings/security/twostepcheckotp/",
                data: {
                    'userotp' : userotp
                },
                success: function (data) {
                    if(data.status == 1){
                        location.href = '/adminsideproweb/settings/security/'
                    }
                    else{
                        $('.otperror').html("Please Enter The Currect OTP.")
                    }
                }
            });
        }

        // Forgot Password OTP Submit Button Click
        else if(otpformval == 'forgotpassword'){
            $.ajax({
                type: "GET",
                url: "/adminsideproweb/forgotpassword_otp/",
                data: {
                    'forgototp' : userotp,
                },
                success: function (fordata) {
                    $('.userotp').val('');
                    if(fordata.empotpstatus == 1){
                        $('.otperror').html('');
                        $('#otpModal').modal('toggle');
                        $('.forgotEmailBox').addClass('d-none');
                        $('.forgotPasswordBox').removeClass('d-none');
                        $('.forgotPasswordBox').attr('action', '/adminsideproweb/forgotpassword/');
                    }
                    else{
                        $('.otperror').html('Please, Enter The Correct OTP.');
                    }
                }
            });
        }
    }
    else{
        $('.otperror').html('Please, Enter The Currect OTP.');
    }

});

// Two Step verification on  Model open 
$('#twostepsecurityModalOpen').on('click', function(){
    let openModal = $(this).attr('data-target');
    $(openModal).modal('show');
});


// Two Step Authontication In Check Email Next Button Click
$('#adminemailid').on('click', function () {
    let getemail = $('#useremail').val();

    if (getemail != '') {

        $('#adminemailid').attr('disabled', true);
        $('#twosteponModal').modal('toggle');
        $('#adminprocessingModal').addClass('d-block');
        
        $.ajax({
            type: "GET",
            url: "/adminsideproweb/settings/security/twostepcheckemail/",
            data: {
                'uemail' : getemail
            },
            success: function (tdata) {
                setTimeout(() => {
                    $('#useremail').val("");
                    $('#adminprocessingModal').removeClass('d-block');
                    if(tdata.checkemailstatus == 1){
                        $('#otpModal').modal('show').attr('data-val','twostep');
                    }
                    else{
                        $('#twosteponModal').modal('show');
                        $('#adminemailid').attr('disabled', false);
                        $('.errormsg').html('Please Enter The Current Email Address');
                    }
                }, 1000);
            }
        });
    }
    else{
        $('.errormsg').html('Please enter your email address');
    }
});


// Two Step verification off  Model open 
$('.twostepoffModalOpen').on('click', function(){
    let openModal = $(this).attr('data-target');
    $(openModal).modal('show');
});


// Order Edit Button CLick
$('.ordereditmodalbtn').on('click', function () {
    let getoid = $(this).attr('data-click');
    let pagereq = $(this).attr('data-target');

    $.ajax({
        type: "GET",
        url: "/adminsideproweb/orders/edit/",
        data: {
            'soid' : getoid  
        },
        success: function (eodata) {
            $('#orderDeatailsModal').modal('show');
            $('#orcustname').html(eodata.fullname);
            $('#ordatedate').html(eodata.orderdate);
            $('#orderdate').val(eodata.orderdate);
            $('#deliverydate').val(eodata.deliverydate);
            $('#returndate').val(eodata.returndate);
            $('#ororderid').val(eodata.oid);
            $('#orproductimg').attr('src', eodata.productimage);
            $('#orproductname').val(eodata.product);
            $('#orproducttotalprice').val(eodata.totalprice);
            $('#orproducyQTY').val(eodata.proqty);
            $('#orproductcolor').val(eodata.procolorname);
            $('#orusername').val(eodata.fullname);
            $('#oruserphone').val(eodata.phone);
            $('#oruserstate').val(eodata.userstate);
            $('#ordeliveryaddress').html(eodata.delivery);
            $('.btnProductdetails').attr('data-val', eodata.productid);

            $('.ProductMoreDetails').attr('href', eodata.productUrl);


            if (pagereq == "cancelorder") {
                $('#orprostatus').addClass('d-none');
                $('.btnordereditsave').addClass('d-none');
                $('#orprocancel').removeClass('d-none');
                $('.ordercanceldate').removeClass('d-none');
                $('#ordercanceldate').html("Order Cancel Date : " + eodata.ordercenceldate);
            }

            if(eodata.prostatus == "conform")
            {
                $('#orproductstatus').html(
                    "<option checked class='conform' value='conform'>Conform</option>"+
                    "<option class='shipped' value='shipped'>Shipped</option>"
                );
            }
            if(eodata.prostatus == "shipped")
            {
                $('#orproductstatus').html(
                    "<option checked class='shipped' value='shipped'>Shipped</option>" +
                    "<option class='outofdelivery' value='outofdelivery'>Outofdelivery</option>"
                );
            }
            if(eodata.prostatus == "outofdelivery")
            {
                $('#orproductstatus').html(
                    "<option checked class='outofdelivery' value='outofdelivery'>Outofdelivery</option>" +
                    "<option class='delived' value='delived'>Delived</option>"
                );
            }
            if(eodata.prostatus == "delived")
            {
                $('#orproductstatus').html("<option checked class='delived' value='delived'>Delived</option>");
                $('#orproductstatus').attr('readonly',true);
                $('.btnordereditsave').addClass('d-none');
            }
        }
    });
});



// Order In Product Details Button Click
$('.btnProductdetails').on('click', function () {
    // getproid write in up function decleare
    $('#orderDeatailsModal').modal('toggle');
    let getproid = $(this).attr('data-val');
    let getproreq = $(this).attr('data-target');

    $.ajax({
        type: "GET",
        url: "/adminsideproweb/products/edit/",
        data: {
            'eproid' : getproid
        },
        success: function (edata) {
            $('#peoductEditModal input').attr('readonly', true);
            $('#peoductEditModal select').attr('disabled', true);
            $('#peoductEditModal textarea').attr('readonly', true);
            $('#peoductEditModal').modal('show');

            let ProductEditcategorybox = $('#eproducteditcategorys');
            ProductEditcategorybox.empty();
            const getproductcat = edata.setcatname

            $.each(getproductcat, function (arrid, arrname) {
                let setProductEditcategory = $("<option/>", {
                    value: arrname.catname,     // catname is tabel filed name
                    text: arrname.catname,      // catname is tabel filed name
                })
                ProductEditcategorybox.append(setProductEditcategory);
            });

            ProductEditcategorybox.val(edata.setprocat);
            $('#eproducteditbrands').empty();
            $('#eproducteditbrands').append("<option value=" + edata.setprobrand + ">" + edata.setprobrand + "</option>");

            $('#eproductname').val(edata.setproname);
            $('#eproductprice').val(edata.setproprice);
            $('#eproductstock').val(edata.setprostock);
            $('#eproductcolor').val(edata.setprocolor);
            $('#eproductdescription').html(edata.setprodesc);

            if (getproreq == "orderprodetailsbtn") {
                $('#peoductEditModal .updatebtn').addClass('d-none');
            }
        }
    });

});


// Forgot Password Check Email Address
$('.adminforgotpassbtn').on('click', function () {
    let admingetemail = $('#adminemail').val();

    if(admingetemail != ""){

        $('#adminprocessingModal').addClass('d-block');

        $.ajax({
            type: "GET",
            url: "/adminsideproweb/forgotpassword_email/",
            data: {
                'adminemail' : admingetemail
            },
            success: function (foremaildata) {
                setTimeout(() => {
                    $('#adminprocessingModal').removeClass('d-block');
                    $('#adminemail').val('');
                    if (foremaildata.forgotemail == 1) {
                        $('.forgoterror').html('');
                        $('#otpModal').modal('show').attr('data-val','forgotpassword');
                    }
                    else{
                        $('.forgoterror').html('Please, Enter The Correct Email Address.');
                    }
                }, 1000);
            }
        });
    }
    else{
        $('.forgoterror').html('Please, enter your email address.');
    }
})


// Return Product Is Edit Button
$('.returnmodalbtn').on('click', function () {
    let getoid = $(this).attr('data-click');
    $.ajax({
        type: "GET",
        url: "/adminsideproweb/return product/edit/",
        data: {
            'returnoid': getoid
        },
        success: function (rnprodata) {
            $('.returndate').removeClass('d-none');
            $('#orderDeatailsModal').modal('show');
            $('#orcustname').html(rnprodata.fullname);
            $('#ordatedate').html(rnprodata.orderdate);
            $('#orderdate').val(rnprodata.orderdate);
            $('#deliverydate').val(rnprodata.deliverydate);
            $('#returndate').val(rnprodata.returndate);
            $('#ororderid').val(rnprodata.oid);
            $('#orproductimg').attr('src', rnprodata.productimage);
            $('#orproductname').val(rnprodata.product);
            $('#orproducttotalprice').val(rnprodata.totalprice);
            $('#orproducyQTY').val(rnprodata.proqty);
            $('#orproductcolor').val(rnprodata.procolor);
            $('#orusername').val(rnprodata.fullname);
            $('#oruserphone').val(rnprodata.phone);
            $('#oruserstate').val(rnprodata.userstate);
            $('#ordeliveryaddress').html(rnprodata.delivery);
            $('.btnProductdetails').attr('data-val', rnprodata.productid);

            $('#orprostatus').addClass('d-none');
            $('#orproductcancel').val(rnprodata.prorestatus);
            $('.btnordereditsave').addClass('d-none');
            $('#orprocancel').removeClass('d-none');
            $('.ordercanceldate').removeClass('d-none');
        }
    });
});



// Banner Remove button
$('.bannerRemoveBtn').on('click', function(){
    let bannerid = $(this).attr('data-id');
    $.ajax({
        type: "GET",
        url: "/adminsideproweb/banner/remove/",
        data: {
            'bannerid': bannerid
        },
        success: function (bannerdata) {
            location.href = "/adminsideproweb/banner/";
        }
    });
});



// Security Page In Change Password OTP Button Click
$('#passchangebtnotp').on('click', function () {
    let getminute = localStorage.getItem('adminminute');
        getsecond = localStorage.getItem('adminsecond');

    if (parseInt(getminute) == 0 && parseInt(getsecond) == 00) {
        $('#adminprocessingModal').addClass('d-block');
        setTimeout(() => {
            $('#adminprocessingModal').removeClass('d-block');
            $('#otpModal').modal('show').attr('data-val','passwordchange');
            $('#otpformaction').attr('action','/adminsideproweb/settings/security/');
            TimerCounter("01:20");
        }, 1500);
        $.ajax({
            type: "GET",
            url: "/adminsideproweb/settings/security/OTP/",
            data: {
                'uservalue' : 'passwordchange',
            },
            success: function () {}
        });
    }
});


let getminute = localStorage.getItem('adminminute');
    getsecond = localStorage.getItem('adminsecond');

if (getminute === "NaN" || getsecond === "NaN") {
    localStorage.setItem('adminminute', '00');
    localStorage.setItem('adminsecond', '00');
}

else if (parseInt(getminute) != 00 || parseInt(getsecond) != 00) {
    $('#passchangebtnotp').addClass('d-none');
    $('#otpModal').modal('show').attr('data-val','passwordchange');
    let settimer = getminute + ":" + getsecond;
    TimerCounter(settimer);
}

function TimerCounter(localtimer) {
    var timer2 = localtimer;
    var interval = setInterval(function() {
        var timer = timer2.split(':');
        var minutes = parseInt(timer[0], 10);
        var seconds = parseInt(timer[1], 10);

        --seconds;
        minutes = (seconds < 0) ? --minutes : minutes;
        seconds = (seconds < 0) ? 59 : seconds;
        seconds = (seconds < 10) ? '0' + seconds : seconds;

        $('#passchangebtnotp').addClass('d-none');
        $('.regetnewotp').html(minutes + ' : ' + seconds).removeClass('d-none');
        if (minutes < 0) clearInterval(interval);
        if ((seconds <= 0) && (minutes <= 0)) clearInterval(interval);
        timer2 = minutes + ':' + seconds;

        localStorage.setItem('adminminute', minutes);
        localStorage.setItem('adminsecond', seconds);

        if (minutes == 0 && seconds == 00) {
            $('#passchangebtnotp').removeClass('d-none');
            $('.regetnewotp').addClass('d-none');
            location.href = '/adminsideproweb/settings/security/';
        }
    }, 1000);
    
}


// Notification button click
$('.shownotificationbtn').on('click', function(){
    let notid = $(this).attr('data-id');
    $.ajax({
        type: "GET",
        url: "/adminsideproweb/notification/edit/",
        data: {
            'notid': notid
        },
        success: function (notedata) {
            $('#notificationModal').modal('show');
            $('#notificationTitle').html(notedata.nottitle);
            $('#notificationIssues').html(notedata.notissues);
            $('#issuesUser').html(notedata.notuser);
            $('#issuesDate').html(notedata.notdate);
        }
    });
});