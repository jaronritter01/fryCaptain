$(document).ready(function () {
    /*grab the window width */
    let windowWidth = $(window).width()
    if (windowWidth < 1100) {
        $("div.menu-item").removeClass('col-5');
        $("div.menu-item").addClass('col-12');
    }
    else {
        $("div.menu-item").removeClass('col-12');
        $("div.menu-item").addClass('col-5');
    }

    $(window).resize(function () {
        let windowWidth = $(window).width()
        if (windowWidth < 1460) {
            $("div.menu-item").removeClass('col-5');
            $("div.menu-item").addClass('col-12');
        }
        else {
            $("div.menu-item").removeClass('col-12');
            $("div.menu-item").addClass('col-5');
        }
    })
})