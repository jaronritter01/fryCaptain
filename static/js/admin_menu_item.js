$(document).ready(function () {
    /*grab the window width */
    let windowWidth = $(window).width()
    if (windowWidth < 1460) {
        $("div.column").removeClass('col-md-3');
        $("div.column").addClass('col-12');
    }
    else {
        $("div.column").removeClass('col-12');
        $("div.column").addClass('col-md-3');
    }

    $(window).resize(function () {
        let windowWidth = $(window).width()
        if (windowWidth < 1460) {
            $("div.column").removeClass('col-md-3');
            $("div.column").addClass('col-12');
        }
        else {
            $("div.column").removeClass('col-12');
            $("div.column").addClass('col-md-3');
        }
    })
})