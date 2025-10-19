function onDrop (source, target, piece, newPos, oldPos, orientation) {
	console.log('Source: ' + source)
	console.log('Target: ' + target)
	console.log('Piece: ' + piece)
	console.log('New position: ' + Chessboard.objToFen(newPos))
	console.log('Old position: ' + Chessboard.objToFen(oldPos))
	console.log('Orientation: ' + orientation)
	$.post('/api/make_move', {'fen': Chessboard.objToFen(newPos)}, function(data) {
		console.log('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
	});
}

var config = {
  draggable: true,
  pieceTheme: '/pieces/{piece}.png',
  onDrop: onDrop,
  sparePieces: true
}
// var board1 = Chessboard('board1', config)
// var board2 = Chessboard('board2', config)

$('#createBtn').on('click', function (){
	board1.start();
	console.log(board1.fen());
});

$('#startBtn1').on('click', function () {
	board1.start();
	console.log(board1.fen());
});

$('#clearBtn1').on('click', function () {
	board1.clear();
	console.log(board1.fen());
});

$('#startBtn2').on('click', function () {
	board2.start();
	console.log(board1.fen());
});

$('#clearBtn2').on('click', function () {
	board2.clear();
	console.log(board1.fen());
});

$('#validBtn2').on('click', function (){
	$.post('/api/valid_check', {'fen': Chessboard.objToFen(board2)}, function(data) {
			console.log('Valid button pressed')
	});
});