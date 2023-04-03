function reward(action, isPositive) {
    console.log('is reward positive? '+isPositive);

    reward = isPositive == true ? 10 : -1;

    $.ajax({
    url: '/train',
    method: 'POST',
    data: {action: action, reward: reward},
    success: function(response) {
        console.log(response);
        }
    });
}