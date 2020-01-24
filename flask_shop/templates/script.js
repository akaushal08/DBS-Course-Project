var submitted = false;
$(document).ready(function() {
    $(".menu-items").slick({
        infinite: true,
        slidesToShow: 3,
        slidesToScroll: 3,
        nextArrow: $(".next"),
        prevArrow: $(".prev")
    });
    $(".menu-items1").slick({
        infinite: true,
        slidesToShow: 3,
        slidesToScroll: 3,
        nextArrow: $(".next1"),
        prevArrow: $(".prev1")
    });
    $(".menu-items2").slick({
        infinite: true,
        slidesToShow: 3,
        slidesToScroll: 3,
        nextArrow: $(".next2"),
        prevArrow: $(".prev2")
    });
});