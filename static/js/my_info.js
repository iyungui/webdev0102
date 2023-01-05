function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function upload_request(){
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", $("input[name='csrfmiddlewaretoken']").val());
          }
        }
    })

    var formData = new FormData();
    formData.append('file1', $("#file_input")[0].files[0])

    $.ajax({
        url: "upload_profile_img",
        data: formData,
        method: "POST",
        processData: false,
        contentType: false
    })
    .done(function(json){
        if(json.rslt_cd == "0000"){
            console.log(json);
            alert("완료!")
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