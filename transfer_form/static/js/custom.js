$(document).ready(function () {
    // Counter for textarea
    $("textarea[name='recipients_list']").after("<p id='characterLeft'></p>");
    $("#characterLeft").text("1024 символов осталось");
    $("#id_recipients_list").keydown(function () {
        var max = 1024;
        var len = $(this).val().length;
        if (len >= max) {
            $("#characterLeft").text("Вы превысили лимит в " + max + "символов");
            $("#characterLeft").addClass("red");
            $("#btnSubmit").addClass("disabled");
        }
        else {
            var ch = max - len;
            $("#characterLeft").text(ch + " символов осталось").removeClass("red");
            $("#btnSubmit").removeClass("disabled");
        }
    });
    // CSRF token for AJAX
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    // Button Send handler
    $("button#btnSubmit").click(function (event) {
        var sender = $("select[name='sender']").val();
        var recipients_list = $("textarea[name='recipients_list']").val();
        var amount = $("input[name='amount']").val();
        if (sender === "" || recipients_list === "" || amount === "")
        {
            $.Zebra_Dialog(
                "<p>Поля формы не заполнены</p>",
                {"title": "Ошибка заполнения",
                 "type": "error",
                 "custom_class": "popup"
                });
            return false;
        }

        var csrftoken = Cookies.get('csrftoken');
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
        // AJAX POST
        $.post(
            "/transfer_form/",
            {
                sender: sender,
                recipients_list: recipients_list,
                amount: amount
            },
            function(data, status) {
                $.Zebra_Dialog(
                    "<p>" + data.message + "</p>",
                    {"title": data.title,
                    "type": data.status,
                    "custom_class": "popup"
                    });
            }
        );
        event.preventDefault();
    });


});
