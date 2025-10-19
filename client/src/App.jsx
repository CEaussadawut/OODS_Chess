import { useState } from 'react'
import CreateBtn from './CreateBtn'
import Board from './Board'
import './App.css'

function App() {
    const [boards, setBoards] = useState([]);
    const [boardCount, setBoardCount] = useState(0); // Counter for board IDs

    const addBoard = () => {
        const newBoardId = boardCount + 1; // Increment ID
        setBoards([...boards, { id: newBoardId }]);
        setBoardCount(newBoardId); // Update the counter
        console.log(newBoardId); // Log the new board ID
		$.post('/api/create_board', {'id': newBoardId}, function(data) {
			console.log('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
		});
    }

    return (
        <>
            <div className="create-btn-container">
                <CreateBtn onClick={addBoard}/>
            </div>
            <div className="boards-container">
                {boards.map((board) => {
                    console.log(board.id); // Log each board ID
                    return <Board key={board.id} boardId={board.id} />;
                })}
            </div>
        </>
    )
}

export default App