$(document).ready(function () {
    /*grab the window width */
    let windowWidth = $(window).width()
    if (windowWidth < 1460) {
        $("div.menu-list").removeClass('col-6');
        $("div.menu-list").addClass('col-12');
    }
    else {
        $("div.menu-list").removeClass('col-12');
        $("div.menu-list").addClass('col-6');
    }

    $(window).resize(function () {
        let windowWidth = $(window).width()
        if (windowWidth < 1460) {
            $("div.menu-list").removeClass('col-6');
            $("div.menu-list").addClass('col-12');
        }
        else {
            $("div.menu-list").removeClass('col-12');
            $("div.menu-list").addClass('col-6');
        }
    })
})