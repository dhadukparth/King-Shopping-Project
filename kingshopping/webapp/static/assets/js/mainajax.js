// // Check your connection
// if (!navigator.onLine) {
//   $("#internetModal").addClass("d-block show");
// }

// Show the Processing modal
$(".openProcessingModal").on("click", function () {
  $("#processingModal").addClass("d-block");
});

// Addres Edit Button Click
$(".addressEditBtn").on("click", function () {
  let getaddrid = $(this).attr("data-click");

  $.ajax({
    type: "GET",
    url: "/account/address/edit/",
    data: {
      setaddrid: getaddrid,
    },
    success: function (addrdata) {
      $("#upaddressModal").modal("show");

      $("#addressTitle").val(addrdata.setaddrtitle);
      $("#addressDescription").html(addrdata.setaddrdesc);
    },
  });
});

// Address Remove Button Click
$(".addressRemoveBtn").on("click", function () {
  let getremoveaddrid = $(this).attr("data-click");

  $.ajax({
    type: "GET",
    url: "/account/address/remove/",
    data: {
      addrremoveid: getremoveaddrid,
    },
    success: function (data) {
      location.href = "/account/address/";
    },
  });
});

// Change Product QTY
$(".productqty").on("change", function () {
  let getproqty = $(this).val();
  let getproid = $(this).attr("data-click");

  $.ajax({
    type: "GET",
    url: "/cart/qty/",
    data: {
      cproqty: getproqty,
      cproid: getproid,
    },
    success: function (cdata) {
      location.href = "/cart/";
    },
  });
});

// Add Product to cart
$(".addtocartbtn").on("click", function () {
  let getaddproid = $(this).attr("data-click");

  $.ajax({
    type: "GET",
    url: "/cart/add/",
    data: {
      addcartproid: getaddproid,
    },
    success: function (cdata) {
      location.href = "/cart/";
    },
  });
});

// Add Buyproduct Directive Buy Button
$(".buyproductnow").on("click", function () {
  let getaddproid = $(this).attr("data-proid");
  location.href = "/buyproduct/?newproname=" + getaddproid;
});

// Remove Cart Product Button Click
$(".cartProductRemoveBtn").on("click", function () {
  let getremovecartproid = $(this).attr("data-click");

  $.ajax({
    type: "GET",
    url: "/cart/remove/",
    data: {
      removecartpro: getremovecartproid,
    },
    success: function (cdata) {
      location.href = "/cart/";
    },
  });
});

// Add Wishlist Button click
$(".wishlistIconAddBtn").on("click", function () {
  let getwishproid = $(this).attr("data-click");

  $.ajax({
    type: "GET",
    url: "/wishlist/add/",
    data: {
      addwishproid: getwishproid,
    },
    success: function (data) {
      location.href = "/wishlist/";
    },
  });
});

// Remove Wishlist Button Click
$(".wishlistIconRemoveBtn").on("click", function () {
  let getwishproid = $(this).attr("data-click");

  $.ajax({
    type: "GET",
    url: "/wishlist/remove/",
    data: {
      removewishproid: getwishproid,
    },
    success: function (data) {
      location.href = "/wishlist/";
    },
  });
});

// Check Buy product Out or In of Stock
$(".buyproduct").on("click", function () {
  location.href = "/buyproducts/";
});

// OTP Modal Cancel Button Click
$(".twostepbtncancel").on("click", function () {
  $("#userenteremail").val("");
  $(".twoerror").html("");
});

// Otp Submit Button In OTP Modal
$(".otpsubmitbtn").on("click", function () {
  let getuserotp = $("#userotpModal").val();

  // otpformval is declare in this file
  let otpformval = $("#otpModal").attr("data-val");

  if (getuserotp == 0) {
    $(".otperror").html("Please, Enter The Correct OTP.");
  } else {
    // Password Change OTP Submit Button CLick
    if (otpformval == "passwordchange") {
      $.ajax({
        type: "GET",
        url: "/account/security/checkotp/",
        data: {
          userotp: getuserotp,
        },
        success: function (odata) {
          if (odata.status == 1) {
            $(".otperror").html("");
            $("#userotp").val("");
            $("#otpModal").modal("toggle");
            $("#oldpassword").attr("disabled", false);
            $("#newpassword").attr("disabled", false);
            $("#newrepassword").attr("disabled", false);
            $("#otpaftercheck").removeClass("d-none");
          } else {
            $(".otperror").html("Please Enter The Currect OTP.");
          }
        },
      });
    }

    // Two Step Verfication OTP Submit Button CLick
    else if (otpformval == "twostep") {
      $.ajax({
        type: "GET",
        url: "/account/security/twocheckotp/",
        data: {
          userotp: getuserotp,
        },
        success: function (data) {
          if (data.status == 1) {
            location.href = "/account/security/";
          } else {
            $(".otperror").html("Please Enter The Currect OTP.");
          }
        },
      });
    }

    // Check Forgot Password OTP Submit
    else if (otpformval == "forgotpassword") {
      $.ajax({
        type: "GET",
        url: "/forgotpassword_otp/",
        data: {
          forgotuserotp: getuserotp,
        },
        success: function (forgototpdata) {
          if (forgototpdata.checkforgototpstate == 1) {
            $(".otperror").html("");
            $("#otpModal").modal("toggle");
            $("#forgotpassword-modal").modal("show");
            $("#forgotaction").attr("action", "/forgotpassword_username/");
          } else {
            $(".otperror").html("Please, Enter The Correct OTP.");
          }
        },
      });
    }
  }
});

// Cancel Button Click
$(".cancelbtn").on("click", function () {
  location.href = "/account/security/";
});

// Two Step Verification Send OTP
$("#twostepbtnsendotp").on("click", function () {
  let useremail = $("#userenteremail").val();

  if (useremail != "") {
    $("#twostepModal").modal("toggle");
    $("#processingModal").addClass("d-block");

    $.ajax({
      type: "GET",
      url: "/account/security/twocheckemail/",
      data: {
        useremail: useremail,
      },
      success: function (twodata) {
        if (twodata.checkemailstatus == 1) {
          $("#processingModal").removeClass("d-block");
          $("#userenteremail").val("");
          $(".twoerror").html("");
          $("#otpModal").modal("show").attr("data-val", "twostep");
        } else {
          setTimeout(() => {
            $("#processingModal").removeClass("d-block");
            $("#twostepModal").modal("show");
            $("#userenteremail").val("");
            $(".twoerror").html("Please Enter The Current Email Address");
          }, 1000);
        }
      },
    });
  } else {
    $(".twoerror").html("Please enter your email address");
  }
});

// Request OTP Sign IN
$(".requestotpsignin").on("click", function () {
  let getemailvalue = $("#requestotpemail").val();

  if (getemailvalue != "") {
    $("#otplogin-modal").modal("toggle");
    $("#processingModal").addClass("d-block");

    $.ajax({
      type: "GET",
      url: "/checkrequestemail/",
      data: {
        reqemail: getemailvalue,
      },
      success: function (checkdata) {
        if (checkdata.chemail == 1) {
          setTimeout(() => {
            $("#processingModal").removeClass("d-block");
            $(".rotpemailerror").html("");
            $("#reqotpModal").modal("show");
            $("#requestotpemail").val("");
          }, 1000);
        } else {
          setTimeout(() => {
            $("#otplogin-modal").modal("show");
            $("#processingModal").removeClass("d-block");
            $("#requestotpemail").val("");
            $(".rotpemailerror").html(
              "Please, Enter The Correct Email Address."
            );
          }, 1000);
        }
      },
    });
  } else {
    $(".rotpemailerror").html("Please, Enter The Your Email Address.");
  }
});

// Forgot Password
$(".forgotpasswordbtn").on("click", function () {
  let getusername = $("#singin-username").val();

  if (getusername != "") {
    $("#signin-modal").modal("toggle");
    $("#processingModal").addClass("d-block");

    $.ajax({
      type: "GET",
      url: "/forgotpassword_username/",
      data: {
        forgotusername: getusername,
      },
      success: function (fordata) {
        if (fordata.checkuser == 1) {
          $("#processingModal").removeClass("d-block");
          $(".forgotusererror").html("");
          $("#otpModal").modal("show").attr("data-val", "forgotpassword");
          $("#userotpform").attr("action", "/forgotpassword_otp/");
        } else {
          $("#processingModal").removeClass("d-block");
          $("#signin-modal").modal("show");
          $(".forgotusererror").html("Please, Enter The Correct Username.");
        }
        $("#userotpModal").val("");
      },
    });
  } else {
    $(".forgotusererror").html("Please, Enter Your Username.");
  }
});

// Password Change Edit Button Click
$(".passwordeditBtn").on("click", function () {
  let getminute = localStorage.getItem("webminute");
  getsecond = localStorage.getItem("websecond");

  if (parseInt(getminute) == 0 && parseInt(getsecond) == 00) {
    $("#otpModal").modal("show").attr("data-val", "passwordchange");
    $("#userotpform").attr("action", "/account/security/checkotp/");
    TimerCounter("01:20");

    $.ajax({
      type: "GET",
      url: "/account/security/sendotp/",
      data: {
        uservalue: "passwordchange",
      },
      success: function () {},
    });
  }
});

let getminute = localStorage.getItem("webminute");
getsecond = localStorage.getItem("websecond");
if (getminute === "NaN" || getsecond === "NaN") {
  localStorage.setItem("webminute", "00");
  localStorage.setItem("websecond", "00");
} else if (parseInt(getminute) != 0 || parseInt(getsecond) != 0) {
  $(".passwordeditBtn").addClass("d-none");
  $("#otpModal").modal("show").attr("data-val", "passwordchange");
  $("#userotpform").attr("action", "/account/security/checkotp/");
  let settimer = getminute + ":" + getsecond;
  TimerCounter(settimer);
}

function TimerCounter(localtimer) {
  var timer2 = localtimer;
  var interval = setInterval(function () {
    var timer = timer2.split(":");
    var minutes = parseInt(timer[0], 10);
    var seconds = parseInt(timer[1], 10);

    --seconds;
    minutes = seconds < 0 ? --minutes : minutes;
    seconds = seconds < 0 ? 59 : seconds;
    seconds = seconds < 10 ? "0" + seconds : seconds;

    $(".passwordeditBtn").addClass("d-none");
    $(".regetnewotp")
      .html(minutes + " : " + seconds)
      .removeClass("d-none");
    if (minutes < 0) clearInterval(interval);
    if (seconds <= 0 && minutes <= 0) clearInterval(interval);
    timer2 = minutes + ":" + seconds;
    localStorage.setItem("webminute", minutes);
    localStorage.setItem("websecond", seconds);

    if (minutes == 0 && seconds == 0) {
      $("#otpModal").modal("toggle").attr("data-val", "");
      $(".passwordeditBtn").removeClass("d-none");
      $(".regetnewotp").addClass("d-none");
    }
  }, 1000);
}
