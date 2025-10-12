function onDrop (source, target, piece, newPos, oldPos, orientation) {
	console.log('Source: ' + source)
	console.log('Target: ' + target)
	console.log('Piece: ' + piece)
	console.log('New position: ' + Chessboard.objToFen(newPos))
	console.log('Old position: ' + Chessboard.objToFen(oldPos))
	console.log('Orientation: ' + orientation)
	console.log('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
	$.post('/make_move', {'fen': Chessboard.objToFen(newPos)}, function(data) {
		console.log(board.fen());
	});
}

var config = {
  draggable: true,
  position: 'start',
  pieceTheme: '/static/img/{piece}.png',
  onDrop: onDrop,
  sparePieces: true
}
var board = Chessboard('board1', config)


$('#startBtn').on('click', function () {
	board.start();
	console.log(board.fen());
});

$('#clearBtn').on('click', function () {
	board.clear();
	console.log(board.fen());
});