$(document).ready(function () {
    $(".comment__form").on("submit", function (event) {
        event.preventDefault();
        var data = $(this).serialize().split("=")[1];

        $.ajax({
            url: $(this).attr("action"),
            type: $(this).attr("method"),
            dataType: "json",
            contentType: "application/json",

            data: JSON.stringify({
                comment: data
            }),

            success: function (result) {
                $(`<div class='comment__user'>${result}</div><br>`).appendTo(".wrapper");
                $("#comment").val("");
            },

            error: function (data) {
                console.log("error", data);
            }
        });
    });
});	