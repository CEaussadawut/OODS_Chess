import { useState } from 'react';
import CreateBtn from './CreateBtn';
import Board from './Board';
import './App.css';

function App() {
	const [boards, setBoards] = useState([]);

	const addBoard = () => {
		$.ajax({
			url: '/api/create_board',
			method: 'POST',
			dataType: 'json'
		})
			.done((data) => {
				if (!data || data.error || typeof data.id === 'undefined') {
					console.error('Failed to create board', data?.error);
					return;
				}
				setBoards((prev) => [...prev, { id: data.id, initialState: data }]);
			})
			.fail((jqXHR) => {
				console.error('Failed to create board', jqXHR.responseJSON || jqXHR.responseText);
			});
	};

	return (
		<>
			<div className="create-btn-container">
				<CreateBtn onClick={addBoard} />
			</div>
			<div className="boards-container">
				{boards.map((board) => (
					<Board key={board.id} boardId={board.id} initialState={board.initialState} />
				))}
			</div>
		</>
	);
}

export default App;
