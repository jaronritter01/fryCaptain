$(document).ready(function () {
    /*grab the window width */
    let nameWidth = $("#nav-bar-name").width()
    if (nameWidth != "0") {
        console.log(typeof nameWidth)
        let setWidth = nameWidth + 80;
        console.log(setWidth)
        $('#cart-icon').attr('margin-right', '400px');

        $(window).resize(function () {
            let nameWidth = $("#nav-bar-name").width()
            console.log(nameWidth)
        })
    }
})