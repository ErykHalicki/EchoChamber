document.addEventListener('DOMContentLoaded', (event) => {
    var socket = io.connect('http://' + document.domain + ':' + location.port);

    socket.on('connect', function() {
        console.log('Connected to server');
    });

    socket.on('receive_message', function(data) {
        var messages = document.getElementById('messages');
        var messageElement = document.createElement('div');
        messageElement.className = 'message ' + data.sender;
        messageElement.textContent = data.message;
        messages.appendChild(messageElement);
        messages.scrollTop = messages.scrollHeight;
    });

    window.sendMessage = function() {
        var input = document.getElementById('message-input');
        var message = input.value;
        socket.emit('send_message', {message: message, sender: 'human'});
        input.value = '';
    };
});

