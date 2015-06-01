/**
 * scripts.js
 *
 * Harvard cs50x
 * Problem Set 7 - Python Edition
 *
 *
 */

function displayError(msg, error){

    if (error) {
        msg += (typeof error == "string" ? " (" + error + ")" : " (" + error.status + ": " + error.statusText + ")");
        console.log(error);
    }

    $("#msg-container").html(
        '<div class="alert alert-error alert-danger">'
        + '<a href="#" class="close" data-dismiss="alert">&times;</a>'
        + '<strong>Error!</strong> ' + msg
    + '</div>'
    );
}

function displayInfo(msg){

    $("#msg-container").html(
        '<div class="alert alert-info">'
        + '<a href="#" class="close" data-dismiss="alert">&times;</a>'
        + msg
    + '</div>'
    );
}
