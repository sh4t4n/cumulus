$(document).ready(function() {
/** Adduser form validation */
    // unique username method
    $.validator.addMethod(
        "uniqueUserName", 
        function(value, element) {
            var response;
            var formData = new FormData();     
            formData.append("username", value);
            $.ajax({
                type: "POST",
                url: "/panel/users/check/",
                data: formData,
                contentType: false,
                processData: false,
                async: false,
                dataType: 'json',
                success: function(data){
                    response = ( data.success == true ) ? true: false;
                }
            });
            return response;
        },
        "Username is Already Taken"
    );

    // validate
    $('#AddUserForm').validate({
        rules: {
            username: {
                minlength: 4,
                maxlength: 15,
                required: true,
                uniqueUserName: true
            },
            firstname: {
                minlength: 3,   
                maxlength: 15
            },
            lastname: {
                minlength: 3,
                maxlength: 15
                
            },
            password: {
                required: true,
                minlength: 6                
            },
            password2: {
                required: true,
                equalTo : "#Password1"                
            },
            email: {
                required: true,
                email: true                
            }
        },
        highlight: function(element) {
            $(element).closest('.form-group').addClass('has-error');
        },
        unhighlight: function(element) {
            $(element).closest('.form-group').removeClass('has-error');
        },
        errorElement: 'span',
        errorClass: 'help-block',
        errorPlacement: function(error, element) {
            if(element.parent('.input-group').length) {
                error.insertAfter(element.parent());
            } else {
                error.insertAfter(element);
            }
        },
        submitHandler: function(form) {
            console.log(form.username.val());
        }
    });

/** Delete user */
    $('td a.removeButton').click(function(){
        var user_id = $(this).attr("user-pk");
        var formData = new FormData();

        formData.append("user_id", user_id);
    
        $.ajax({
                type: 'POST',
                url: "/panel/users/delete/",
                data: formData,
                contentType: false,
                processData: false,
                dataType: 'json',
                success: function (data) {
                    if(data.success == true){
                        location.reload();
                    }else{
                        console.log(data.message);
                    }
                },
        });        
    
    });

/** Edit user */
    $("td a.editButton").click(function(){
        var formData = new FormData();
        var user_pk = $(this).attr("user-pk");
        var edit_row = $(this).parents().eq(1);
        var firstname = $(edit_row).find("td span.firstNameText");
        var lastname = $(edit_row).find("td span.lastNameText");
        var email = $(edit_row).find("td span.emailText");
        var edit_text = $(edit_row).find("td span.editSpan");

        $("#AddUserButton").addClass("disabled")
        $("a.button").css("display","none");
        $(edit_row).addClass("active");
        $(edit_text).hide();

        $(edit_row).find("td.editFirst").append('<input id="FirstNameInput" class="editInput form-control" type="text" name="first_name" value="' + firstname.text() + '" data-toggle="tooltip" data-placement="bottom" placeholder="Firstname" focus>');
        $(edit_row).find("td.editLast").append('<input id="LastNameInput" class="editInput  form-control" type="text" name="last_name" value="' + lastname.text() +'" data-toggle="tooltip" data-placement="bottom" placeholder="Lastname">');
        $(edit_row).find("td.editEmail").append('<input id="EmailInput" class="editInput  form-control" type="text" name="email" value="' + email.text() +'" data-toggle="tooltip" data-placement="bottom" placeholder="Email address">');
        $(this).after('<a id="CancelButton" class="icons over-black" data-toggle="tooltip" data-placement="right" title="Cancel ..."><span class="glyphicon glyphicon-ban-circle"></span></a>');        
        $(this).after('<a id="SaveButton" class="icons over-black"  data-toggle="tooltip" data-placement="right" title="Save ..."><span class="glyphicon glyphicon-floppy-disk"></span></a>');
        
        
        var firstname_input = $("#FirstNameInput");
        var lastname_input = $("#LastNameInput");
        var email_input = $("#EmailInput");

        $(firstname_input).focus().select();

        function leaveEditMode(){
            $("#AddUserButton").removeClass("disabled")
            $(".editInput").remove();
            $(".icons").remove();
            $("a.button").css("display","inline");
            $(edit_row).removeClass("active");
            $(edit_text).show();
        };

        // Cancel edit
        $("#CancelButton").on('click', function() {
            leaveEditMode();
        });

        // Save changes
        $("#SaveButton").on('click',function(){
            $(".editInput").removeClass("fieldError").attr('title',"");
            var firstname = $("#FirstNameInput").val();
            var lastname = $("#LastNameInput").val();
            var email = $("#EmailInput").val();
            formData.append("user_id", user_pk);
            formData.append("first_name", firstname);
            formData.append("last_name", lastname);
            formData.append("email", email);
            $.ajax({
                type: 'POST',
                url: "/panel/users/edit/",
                data: formData,
                contentType: false,
                processData: false,
                dataType: 'json',
                success: function (data) {
                    
                    if(data.success == true){
                        location.reload();
                    }else{
                        show_alert(data.messages)                        
                       
                        if($(data.details)){ 
                            for (var key in data.details) {
                                $("input[name='" + key + "']").addClass("fieldError");
                                $("input[name='" + key + "']").attr('title',data.details[key]);
                            }
                        }   
                    }
                },
            });
        });

    });

/** Alerts */
    function show_alert(message){
        $("#Alert").text(message);
        $("#Alert").show();
        $("#Alert").delay(3000).slideUp(200, function() {
            $(this).hide();
        });        
    }

});

