import { useEffect, useRef, useState } from 'react';

function Board({ boardId }){
	const boardRef = useRef(null);
	const boardInstance = useRef(null);
	const [fen, setFen] = useState(''); // State for FEN
	const [history, setHistory] = useState([]); // State for move history
	const [currentHistoryIndex, setCurrentHistoryIndex] = useState(-1); // Track current history position
	const historyRef = useRef(null); // Ref for the history container
	const historyIndexRef = useRef(-1); // Mirror of currentHistoryIndex for stale closure avoidance

	const pushHistoryEntry = (fenString) => {
		setHistory(prevHistory => {
			const cutoff = historyIndexRef.current + 1;
			const truncated = cutoff > 0 ? prevHistory.slice(0, cutoff) : [];
			const updated = [...truncated, fenString];
			historyIndexRef.current = updated.length - 1;
			setCurrentHistoryIndex(historyIndexRef.current);
			return updated;
		});
	};

	useEffect(() => {
		// Initialize chessboard after component mounts
		if (window.Chessboard && boardRef.current && !boardInstance.current) {
                        const onDrop = (source, target, piece, newPos) => {
                                if (!boardInstance.current) {
                                        return;
                                }

                                const fenFromDrop = window.Chessboard && typeof window.Chessboard.objToFen === 'function'
                                        ? window.Chessboard.objToFen(newPos)
                                        : boardInstance.current.fen();

                                if (fenFromDrop) {
                                        // Ensure the board reflects the dropped position immediately
                                        boardInstance.current.position(fenFromDrop);
                                        pushHistoryEntry(fenFromDrop);
                                        $.post('/api/make_move', { fen: fenFromDrop, id: boardId }, function() {
                                                console.log('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~');
                                        });
                                }

                                console.log('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                        };

			boardInstance.current = Chessboard(boardRef.current, {
				draggable: true,
				dropOffBoard: 'trash',
				sparePieces: true,
				pieceTheme: '/pieces/{piece}.png',
				onDrop: onDrop
			});
		}

		return () => {
			if (boardInstance.current) {
				boardInstance.current.destroy();
				boardInstance.current = null;
			}
		};
	}, [boardId]); // Removed history from dependencies

	useEffect(() => {
		if (currentHistoryIndex >= 0 && history[currentHistoryIndex]) {
			const targetFen = history[currentHistoryIndex];
			if (boardInstance.current) {
				boardInstance.current.position(targetFen);
			}
			setFen(targetFen);
		} else {
			setFen('');
		}
	}, [currentHistoryIndex, history]);

	useEffect(() => {
		// Scroll to the bottom of the history container whenever history updates
		if (historyRef.current) {
			historyRef.current.scrollTop = historyRef.current.scrollHeight;
		}
	}, [history]);

	const handleStart = () => {
		if (boardInstance.current) {
		$.get('/api/start_position', function(data) {
			// Assume your Flask backend returns { fen: "FEN_STRING" }
			if (data && data.fen) {
				boardInstance.current.position(data.fen); // Set board to FEN from backend
				pushHistoryEntry(data.fen); // Optionally add to history
				}
			});
		}
	};

	const handleClear = () => {
		if (boardInstance.current) {
		$.get('/api/clear', function(data) {
			// Assume your Flask backend returns { fen: "FEN_STRING" }
			if (data && data.fen) {
				boardInstance.current.position(data.fen); // Set board to FEN from backend
				setFen(''); // Reset FEN on clear
				setHistory([]); // Clear history on reset
				historyIndexRef.current = -1;
				setCurrentHistoryIndex(-1);
				}
			});
		}
	};

	const handleRewind = () => {
		setCurrentHistoryIndex(prevIndex => {
			if (prevIndex > 0) {
				const nextIndex = prevIndex - 1;
				historyIndexRef.current = nextIndex;
				return nextIndex;
			}
			historyIndexRef.current = prevIndex;
			return prevIndex;
		});
	};

	const handleNext = () => {
		setCurrentHistoryIndex(prevIndex => {
			if (prevIndex < history.length - 1) {
				const nextIndex = prevIndex + 1;
				historyIndexRef.current = nextIndex;
				return nextIndex;
			}
			historyIndexRef.current = prevIndex;
			return prevIndex;
		});
	};

	const canRewind = currentHistoryIndex > 0;
	const canAdvance = currentHistoryIndex >= 0 && currentHistoryIndex < history.length - 1;

	return(
		<div style={{display: 'flex', flexDirection: 'row', alignItems: 'flex-start', gap: '20px', marginBottom: '20px'}}>
			<div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '10px'}}>
				<div ref={boardRef} style={{width: '400px'}}></div>
				<div style={{display: 'flex', gap: '10px'}}>
					<button onClick={handleStart}>Start Position</button>
					<button onClick={handleClear}>Clear Board</button>
					<button id={`validBtn-${boardId}`}>Check Valid</button>
				</div>
			</div>
			<div style={{display: 'flex', flexDirection: 'column', alignItems: 'flex-start'}}>
				<h3>FEN:</h3>
				<pre>{fen}</pre> {/* Display FEN in a preformatted text block */}
				<h4>History:</h4>
				<div ref={historyRef} style={{ maxHeight: '300px', overflowY: 'auto', border: '1px solid #ccc', padding: '5px', width: '450px' }}>
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
