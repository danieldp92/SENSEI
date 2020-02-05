// Section of function to call before that the html page is loaded
$.ajax({
    url: 'http://0.0.0.0:5000/resource/get_html_folders',
    type: 'post',
    contentType: 'application/json',
    dataType: 'json',
    cache: false,
    processData: false,
    async:false
}).done(function (response) {
    if (response.length == 0) {
        $("#resource_folders_list").css("display", "none")
        $("#add_pages_block").append($("<label>: no projects found</label>"))
    } else {
        for (var i = 0; i < response.length; i++) {
            var value = response[i]
            $('#resource_folders_list').append($("<option></option>").attr("value",value).
            attr("id", "resource_folder_id").text(value));
        }
    }

}).fail(function(XMLHttpRequest, textStatus, errorThrown) {
    alert("Status code: " + XMLHttpRequest.status + "\nStatus text: " + XMLHttpRequest.status +
    "\nOn ready state change: " + XMLHttpRequest.onreadystatechange +
    "\nReady State: " + XMLHttpRequest.readyState);
    alert(textStatus);
    alert(errorThrown);
});