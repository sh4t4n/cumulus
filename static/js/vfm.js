$(document).ready(function() {

/** Bootstap modal positioning */ 
    $(function() {
        function reposition() {
            var modal = $(this),
            dialog = modal.find('.modal-dialog');
            modal.css('display', 'block');        
            dialog.css("margin-top", Math.max(0, ($(window).height() - dialog.height()) / 2));
        }
        $('.modal').on('show.bs.modal', reposition);
        $(window).on('resize', function() {
            $('.modal:visible').each(reposition);
        });
    });

/** Autohide alert messages **/
    
    $(".alert").delay(3000).slideUp(200, function() {
        $(this).alert('close');
    });

/** File manager functions*/ 
    // support for csrftokens
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    var csrftoken = getCookie('csrftoken');
    
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
        
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });

    // Create directory
    $("#MkdirButton").click(function(){
        var dirname = $("#DirNameInput").val();
        var path = $("#DirNameInput").attr("dir-path");
        var formData = new FormData();
        
        formData.append("dirname", dirname);
        formData.append("path", path);

        $.ajax({
            type: 'POST',
            url: "/mkdir/",        
            data: formData,
            contentType: false,
            processData: false,
            dataType: 'json',
            success: function (data) {
                if(data.success == false){    
                    $("#CreateFolderAlert").addClass("alert alert-danger text-center").attr("role","dialog").html(data.message);    
                }else{
                    location.reload();
                }   
            },
        });
    });        
        

    // File upload
    $('#UploadFileButton').change(function(event){
        event.preventDefault();
        
        var file = this.files[0];
        var path = $(this).attr("file-path");
        var formData = new FormData();

        formData.append("fname", file.name);
        formData.append("fdata", file);
        formData.append("fpath", path)
        
              
        $("#UploadedFileLabel").html('<span class="glyphicon glyphicon-file"></span>' + file.name);
        $("#UploadInfo").css("display","block"); 
           
        $.ajax({
            xhr: function(){
                    var xhr = new window.XMLHttpRequest();
                    xhr.upload.addEventListener('progress',function(e){
                        if(e.lengthComputable){
                            var percent = Math.round((e.loaded / e.total) * 100);                                                       
                            $("#ProgressBar").attr("aria-valuenow", percent).css("width", percent + "%");                                            
                        }
                    });            
                    return xhr;
                },
            type: 'POST',
            url: "/upload/",        
            data: formData,
            contentType: false,
            processData: false,
            success: function () {
               location.reload();
            },
        });
    });
});