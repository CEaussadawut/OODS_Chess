from flask import Flask, jsonify, render_template, request

import engine


EMPTY_FEN = "8/8/8/8/8/8/8/8"
DEFAULT_BOARD_ID = 0

app = Flask(
    __name__, template_folder="../templates", static_folder="../static"
)

boards = {}


def _normalize_board_id(raw_id):
    if raw_id is None or raw_id == "":
        return DEFAULT_BOARD_ID

    try:
        return int(raw_id)
    except (TypeError, ValueError) as exc:
        raise ValueError("Invalid board id") from exc


def _get_board(board_id):
    if board_id not in boards:
        boards[board_id] = engine.Chessboard("start")
    return boards[board_id]


@app.route("/")
def chess_game():
    return render_template("index.html")


@app.route("/api/create_board", methods=["POST"])
def create_board():
    raw_id = request.form.get("id")

    try:
        if raw_id is None or raw_id == "":
            board_id = max(boards.keys(), default=-1) + 1
        else:
            board_id = _normalize_board_id(raw_id)
    except ValueError:
        return jsonify({"error": "Invalid board id"}), 400

    boards[board_id] = engine.Chessboard("start")
    board = boards[board_id]
    return (
        jsonify(
            {
                "id": board_id,
                "fen": board.fen,
                "history": board.get_history(),
                "position": board.current_index,
            }
        ),
        201,
    )


@app.route("/api/start_position", methods=["GET"])
def start_position():
    return jsonify({"fen": engine.START_FEN})


@app.route("/api/clear", methods=["GET"])
def clear():
    return jsonify({"fen": EMPTY_FEN})


@app.route("/api/make_move", methods=["POST"])
def make_move():
    raw_id = request.form.get("id")
    fen = request.form.get("fen", "").strip()

    try:
        board_id = _normalize_board_id(raw_id)
    except ValueError:
        return jsonify({"error": "Invalid board id"}), 400

    board = _get_board(board_id)

    if not fen:
        return jsonify({"error": "Missing FEN"}), 400

    try:
        updated_fen = board.pushHistory(fen)
        print(board.history)
        board.fenToMatrix()
        print("fen:",board.fen)
        board.displayMatrix()
        print(board.matrixToFen())
    except ValueError:
        return jsonify({"error": "Invalid FEN"}), 400
    return jsonify(
        {
            "fen": updated_fen,
            "history": board.get_history(),
            "position": board.current_index,
        }
    )


@app.route("/api/valid_check", methods=["POST"])
def valid_check():
    fen = request.form.get("fen", "").strip()
    if not fen:
        return jsonify({"error": "Missing FEN"}), 400

    try:
        engine.Chessboard(fen)
    except ValueError:
        return jsonify({"fen": fen, "valid": False}), 200

    return jsonify({"fen": fen, "valid": True})


@app.route("/api/history/<int:board_id>", methods=["GET"])
def history(board_id):
    if board_id not in boards:
        return jsonify({"error": "Board not found"}), 404

    board = boards[board_id]
    return jsonify(
        {
            "id": board_id,
            "fen": board.fen,
            "history": board.get_history(),
            "position": board.current_index,
        }
    )


@app.route("/api/rewind", methods=["POST"])
def rewind():
    raw_id = request.form.get("id")

    try:
        board_id = _normalize_board_id(raw_id)
    except ValueError:
        return jsonify({"error": "Invalid board id"}), 400

    if board_id not in boards:
        return jsonify({"error": "Board not found"}), 404

    board = boards[board_id]
    fen = board.rewind()
    return jsonify({"fen": fen, "position": board.current_index})


@app.route("/api/forward", methods=["POST"])
def forward():
    raw_id = request.form.get("id")

    try:
        board_id = _normalize_board_id(raw_id)
    except ValueError:
        return jsonify({"error": "Invalid board id"}), 400

    if board_id not in boards:
        return jsonify({"error": "Board not found"}), 404

    board = boards[board_id]
    fen = board.forward()
    return jsonify({"fen": fen, "position": board.current_index})


if __name__ == "__main__":
    app.run(debug=True, threaded=True)