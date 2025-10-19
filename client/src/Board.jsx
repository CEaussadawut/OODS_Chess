import { useCallback, useEffect, useRef, useState } from 'react';

function Board({ boardId, initialState }) {
	const boardRef = useRef(null);
	const boardInstance = useRef(null);
	const lastServerFen = useRef('');
	const serverHistoryRef = useRef([]);
	const [fen, setFen] = useState('');
	const [history, setHistory] = useState([]);
	const [currentHistoryIndex, setCurrentHistoryIndex] = useState(-1);
	const historyContainerRef = useRef(null);

	const syncFromServer = useCallback((payload, fallbackHistory) => {
		if (!payload || payload.error) {
			console.error('Failed to sync board state', payload?.error);
			return;
		}

		let serverHistory;
		if (Array.isArray(payload.history)) {
			serverHistory = payload.history;
		} else if (Array.isArray(fallbackHistory)) {
			serverHistory = fallbackHistory;
		} else {
			serverHistory = serverHistoryRef.current;
		}

		if (!Array.isArray(serverHistory)) {
			serverHistory = [];
		}

		const nextIndex = typeof payload.position === 'number'
			? payload.position
			: serverHistory.length - 1;
		const nextFen = payload.fen || (serverHistory[nextIndex] ?? '');

		serverHistoryRef.current = serverHistory;
		setHistory(serverHistory);
		setCurrentHistoryIndex(nextIndex);
		setFen(nextFen);
		lastServerFen.current = nextFen;

		if (boardInstance.current && nextFen) {
			boardInstance.current.position(nextFen);
		}
	}, []);

	const loadBoard = useCallback(() => {
		return $.ajax({
			url: `/api/history/${boardId}`,
			method: 'GET',
			dataType: 'json'
		})
			.done((data) => {
				syncFromServer(data);
			})
			.fail((jqXHR) => {
				console.error(`Unable to load board ${boardId}`, jqXHR.responseJSON || jqXHR.responseText);
			});
	}, [boardId, syncFromServer]);

	useEffect(() => {
		if (initialState) {
			syncFromServer(initialState);
		} else {
			loadBoard();
		}
	}, [initialState, loadBoard, syncFromServer]);

	useEffect(() => {
		if (window.Chessboard && boardRef.current && !boardInstance.current) {
			const onDrop = (source, target, piece, newPos) => {
				if (!boardInstance.current) {
					return;
				}

				const fenFromDrop = window.Chessboard && typeof window.Chessboard.objToFen === 'function'
					? window.Chessboard.objToFen(newPos)
					: boardInstance.current.fen();

				if (!fenFromDrop) {
					return;
				}

				boardInstance.current.position(fenFromDrop);

				$.ajax({
					url: '/api/make_move',
					method: 'POST',
					data: { fen: fenFromDrop, id: boardId },
					dataType: 'json'
				})
					.done((data) => {
						syncFromServer(data);
					})
					.fail((jqXHR) => {
						console.error('Failed to save move', jqXHR.responseJSON || jqXHR.responseText);
						if (boardInstance.current && lastServerFen.current) {
							boardInstance.current.position(lastServerFen.current);
						}
					});
			};

			boardInstance.current = Chessboard(boardRef.current, {
				draggable: true,
				dropOffBoard: 'trash',
				sparePieces: true,
				pieceTheme: '/pieces/{piece}.png',
				onDrop
			});

			if (lastServerFen.current) {
				boardInstance.current.position(lastServerFen.current);
			} else {
				loadBoard();
			}
		}

		return () => {
			if (boardInstance.current) {
				boardInstance.current.destroy();
				boardInstance.current = null;
			}
		};
	}, [boardId, loadBoard, syncFromServer]);

	useEffect(() => {
		if (historyContainerRef.current) {
			historyContainerRef.current.scrollTop = historyContainerRef.current.scrollHeight;
		}
	}, [history]);

	const handleStart = () => {
		$.ajax({
			url: '/api/create_board',
			method: 'POST',
			data: { id: boardId },
			dataType: 'json'
		})
			.done((data) => {
				syncFromServer(data);
			})
			.fail((jqXHR) => {
				console.error('Unable to reset board', jqXHR.responseJSON || jqXHR.responseText);
			});
	};

	const handleClear = () => {
		$.ajax({
			url: '/api/clear',
			method: 'GET',
			dataType: 'json'
		})
			.done((data) => {
				if (!data || !data.fen) {
					console.error('Missing clear FEN');
					return;
				}

				$.ajax({
					url: '/api/make_move',
					method: 'POST',
					data: { fen: data.fen, id: boardId },
					dataType: 'json'
				})
					.done((response) => {
						syncFromServer(response);
					})
					.fail((jqXHR) => {
						console.error('Unable to clear board', jqXHR.responseJSON || jqXHR.responseText);
						if (boardInstance.current && lastServerFen.current) {
							boardInstance.current.position(lastServerFen.current);
						}
					});
			})
			.fail((jqXHR) => {
				console.error('Unable to fetch clear FEN', jqXHR.responseJSON || jqXHR.responseText);
			});
	};

	const handleRewind = () => {
		$.ajax({
			url: '/api/rewind',
			method: 'POST',
			data: { id: boardId },
			dataType: 'json'
		})
			.done((data) => {
				syncFromServer(data, serverHistoryRef.current);
			})
			.fail((jqXHR) => {
				console.error('Unable to rewind', jqXHR.responseJSON || jqXHR.responseText);
			});
	};

	const handleNext = () => {
		$.ajax({
			url: '/api/forward',
			method: 'POST',
			data: { id: boardId },
			dataType: 'json'
		})
			.done((data) => {
				syncFromServer(data, serverHistoryRef.current);
			})
			.fail((jqXHR) => {
				console.error('Unable to step forward', jqXHR.responseJSON || jqXHR.responseText);
			});
	};

	const canRewind = currentHistoryIndex > 0;
	const canAdvance = currentHistoryIndex >= 0 && currentHistoryIndex < history.length - 1;

	return (
		<div style={{ display: 'flex', flexDirection: 'row', alignItems: 'flex-start', gap: '20px', marginBottom: '20px' }}>
			<div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '10px' }}>
				<div ref={boardRef} style={{ width: '400px' }}></div>
				<div style={{ display: 'flex', gap: '10px' }}>
					<button onClick={handleStart}>Start Position</button>
					<button onClick={handleClear}>Clear Board</button>
					<button id={`validBtn-${boardId}`}>Check Valid</button>
				</div>
			</div>
			<div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start' }}>
				<h3>FEN:</h3>
				<pre>{fen}</pre>
				<h4>History:</h4>
				<div ref={historyContainerRef} style={{ maxHeight: '300px', overflowY: 'auto', border: '1px solid #ccc', padding: '5px', width: '450px' }}>
					<ul>
						{history.map((fenString, index) => (
							<li
								key={index}
								style={index === currentHistoryIndex ? { backgroundColor: '#e0f7ff', fontWeight: 'bold' } : {}}
							>
								{fenString}
							</li>
						))}
					</ul>
				</div>
				<div style={{ display: 'flex', gap: '10px', marginTop: '10px' }}>
					<button onClick={handleRewind} disabled={!canRewind}>Rewind</button>
					<button onClick={handleNext} disabled={!canAdvance}>Next</button>
				</div>
			</div>
		</div>
	);
}

export default Board;
