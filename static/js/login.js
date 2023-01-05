function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


function login_request(){
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", $("input[name='csrfmiddlewaretoken']").val());
          }
        }
    })

    var url_href = window.location.href;

    var url = new URL(url_href);
    var next_url = url.searchParams.get("next");


    $.ajax({
        url: "login_req",
        data: {"user_id":$("#user_id").val(), 'user_pw':$("#user_pw").val()},
        method: "POST",
        dataType: "json"
    })
    .done(function(json){
        if(json.rslt_cd == "0000"){
            if (next_url == null){
                location.href = "/"
            } else {
                location.href = next_url
            }
        }
    })
    .fail(function(xhr, status, error){
        console.log(xhr)
        console.log(status)
        console.log(error)
    })
    .always(function(xhr, status){
        console.log("Finished")
    });
}