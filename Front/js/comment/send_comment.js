$(document).ready(function () {
    let comment = $('.comment__container');
    let page = 1;
    comment.scrollTop(comment[0].scrollHeight);

    $(".comment__form").on("submit", function (event) {
        event.preventDefault();
        let data = $(this).serialize().split("=")[1];

        $.ajax({
            url: $(this).attr("action"),
            type: $(this).attr("method"),
            dataType: "json",
            contentType: "application/json",

            data: JSON.stringify({
                comment: data
            }),

            success: function (result) {
                $(`<div class='wrapper-msg'><div class='comment comment__user'> ${result}</div></div><br>`).appendTo(".wrapper");
                $("#comment").val("");
            },

            error: function (data) {
                console.log("error", data);
            }
        });
    });

    comment.scroll(function(event){
        event.preventDefault();
        if ( $(this).scrollTop() == 0 ){

            $.ajax({
                url: "/comment",
                type: "get",
                dataType: "json",
                contentType: "application/json",

                data: JSON.stringify({
                    page: ++page
                }),

                success: function (result) {
                    console.log(result)
                },

                error: function (data) {
                    console.log("error", data);
                }
            });
        }
    });
});
