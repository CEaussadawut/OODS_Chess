import { useEffect, useRef, useState } from 'react';

function Board({ boardId }){
    const boardRef = useRef(null);
    const boardInstance = useRef(null);
    const [fen, setFen] = useState(''); // State for FEN
    const [history, setHistory] = useState([]); // State for move history
    const historyRef = useRef(null); // Ref for the history container

    useEffect(() => {
        // Initialize chessboard after component mounts
        if (window.Chessboard && boardRef.current && !boardInstance.current) {
            const onDrop = (source, target) => {
                const newFen = boardInstance.current.fen();
                setFen(newFen);
                setHistory(prevHistory => [...prevHistory, newFen]); // Use functional update for history
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
                setFen(data.fen); // Update FEN state
                setHistory(prevHistory => [...prevHistory, data.fen]); // Optionally add to history
            	}
        	});
    	}
    };

    const handleClear = () => {
        if (boardInstance.current) {
            boardInstance.current.clear();
            setFen(''); // Reset FEN on clear
            setHistory([]); // Clear history on reset
        }
    };

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
                            <li key={index}>{fenString}</li>
                        ))}
                    </ul>
                </div>
            </div>
        </div>
    );
}
export default Board;