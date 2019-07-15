// Add the class to give the effect icon
function openNav() {
    document.getElementById("mySidenav").style.width = "100%";
    
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
}

/*Nav menu top sticky */
$("document").ready(function($){
    var nav = $('#home');

    $(window).scroll(function () {
        if ($(this).scrollTop()>50) {
        	nav.addClass("f-nav");
        } else {
        	nav.removeClass("f-nav");
        }
    });
});


/* proloader */
$(document).ready(function() {
  setTimeout(function() {
    $('body').addClass('loaded');
    
  }, 1000);
});

 $(document).ready(function() {
    var owl = $('.owl-carousel');
    owl.owlCarousel({
        margin: 10,
        autoplay: true,
        loop: true,
        nav: true,
        navText: ["<img src='../static/images/icon_5.png'>","<img src='../static/images/icon_6.png'>"],
        responsive: {
                      0: {
                        items: 1
                      },
                      600: {
                        items: 2
                      },
                      1000: {
                        items: 3
                      }
        }
    })
})