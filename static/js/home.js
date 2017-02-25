
function showPatientDetails(id, first_name, last_name, email, contact_num, profile_pic, address, date_of_birth, greeting_message){

    var patient_info = document.getElementById('patient_info');
    patient_info.style.display = 'block';

    if (contact_num == ""){
        contact_num = "Missing";
    }

    if (address == ""){
        address = "Missing";
    }

    document.getElementById('patient_name').innerHTML = last_name + " " + first_name ;
    document.getElementById('patient_email').innerHTML = email;
    document.getElementById('patient_contact').innerHTML = contact_num;
    document.getElementById('patient_birthdate').innerHTML = date_of_birth;
    document.getElementById('patient_address').innerHTML = address;
    document.getElementById('patient_img').src = profile_pic;
    document.getElementById('greet_message').value = greeting_message;
    document.getElementById('greet_email').value = email;
    document.getElementById('greet_id').value = id;

    var auto_greet_button = document.getElementById('greet_'+id);
    var submit_button = document.getElementById('greet_submit');
    var text_area = document.getElementById('greet_message');

    if (auto_greet_button.disabled == false){
        submit_button.value = "Greet";
        submit_button.disabled = false;
        text_area.disabled = false;
    }
    else{
        submit_button.value = "Greeted";
        submit_button.disabled = true;
        text_area.disabled = true;
    }
}

$(document).ready(function() {
    $('.greet_form').submit(function() { // catch the form's submit event
        var greet_id = this.greet_id.value;
        $.ajax({ // create an AJAX call...
            async: true,
            data: $(this).serialize(), // get the form data
            type: $(this).attr('method'), // GET or POST
            url: 'send_email/', // the url to call
            success: function(response) { // on success..
                var manual_form_greet_id = document.getElementById('greet_id')
                if (manual_form_greet_id  != null && manual_form_greet_id.value == greet_id){

                    var submit_button = document.getElementById('greet_submit');
                    submit_button.value = "Greeted";
                    submit_button.disabled = true;

                    var text_area = document.getElementById('greet_message');
                    text_area.disabled = true;
                }

                var auto_greet_button = document.getElementById('greet_'+greet_id);
                auto_greet_button.value = "Greeted";
                auto_greet_button.disabled = true;
            },
            error: function(e, x, r) { // on error..
            }
        });
        return false;
    });

});
