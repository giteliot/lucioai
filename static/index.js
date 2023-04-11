function reward(command, action, isPositive) {
    console.log('is reward positive? '+isPositive);

    reward = isPositive == true ? 10 : -5;

    $.ajax({
    url: '/train',
    method: 'POST',
    data: {command: command, action: action, reward: reward},
    success: function(response) {
        console.log(response);
        }
    });
}


function handleKeyDown(event) {
  if (event.keyCode === 13) { // 13 is the code for "Enter" key
    event.preventDefault(); // prevent the default behavior of the "Enter" key
    $.ajax({
    url: '/command',
    method: 'POST',
    data: {command: $('.command-input').val()},
    success: function(response) {
        console.log(response);
        }
    });
  }
}