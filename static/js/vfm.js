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



/** File upload */
    $('#UploadFileButton').change(function(event){
        event.preventDefault();
        
        var file = this.files[0];
        var path = $(this).attr("file-path");
        var formData = new FormData();
        
        formData.append("fname", file.name);
        formData.append("fdata", file);
        formData.append("fpath", path)
        
        console.log(formData)        
        $("#UploadedFileLabel").html('<span class="glyphicon glyphicon-file"></span>' + file.name + '<span id="UploadCounter"></span>');
        $("#UploadInfo").css("display","block");        
        $.ajax({
            xhr: function(){
                    var xhr = new window.XMLHttpRequest();
                    xhr.upload.addEventListener('progress',function(e){
                        if(e.lengthComputable){
                            console.log("Bytes Loaded: " + e.loaded);
                            console.log("Total Size: " + e.total);
                            var percent = Math.round((e.loaded / e.total) * 100);
                            console.log("Percentage:" + percent + "%");
                                                       
                            $("#ProgressBar").attr("aria-valuenow", percent).css("width", percent + "%");
                            $("#UploadCounter").text(" - " + percent + "%");                                             
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