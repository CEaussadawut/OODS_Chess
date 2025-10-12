var board1 = Chessboard('board1', {
    position: 'start',
    pieceTheme: 'chesspieces/wikipedia/{piece}.png'
});

var board2 = Chessboard('board2', {
    position: 'start',
    pieceTheme: 'chesspieces/wikipedia/{piece}.png'
});

$('#startBtn').on('click', function () {
    board1.start();
    board2.start();
});

$('#clearBtn').on('click', function () {
    board1.clear();
    board2.clear();
});