var socket = io();
$(document).ready(function() {
    console.log( "ready!" );
    $('body').fadeIn(1000);
});

socket.on('connect', function() {
    console.log("connected")
    socket.emit('send', {data: 'I\'m connected!'});
});

socket.on("message", function(msg){
    msg = msg.replace(/(\r\n|\n|\r)/gm, "");
    $('#history').append(msg + '<br/>');
});


function  sendSerialCommand(message){
    socket.emit("serial_message", message);
}

$('.terminal').on('click', function() {
    $('#input').focus();
});

$('#input').on('keydown', function search(e) {
    if (e.keyCode == 13) {
        $('#history').append($(this).val() + '<br/>');
        if($(this).val() == "clear"){
            $('#history').html('');
            $('#input').val('');
            return
        }
        sendSerialCommand($(this).val());
        
        $('#input').val('');
    
        
    }
});