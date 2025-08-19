from flask import Flask, jsonify, request, render_template
import random

app = Flask(__name__)

# Initialize the game board
board = [[" " for _ in range(3)] for _ in range(3)]
game_over = False
winner = None

def check_win(board, player):
    for row in board:
        if all(s == player for s in row):
            return True
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)):
        return True
    if all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def check_draw(board):
    return all(board[row][col] != " " for row in range(3) for col in range(3))

def ai_move():
    empty_spaces = [(r, c) for r in range(3) for c in range(3) if board[r][c] == " "]
    if empty_spaces:
        row, col = random.choice(empty_spaces)
        board[row][col] = "O"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/reset", methods=["POST"])
def reset_game():
    global board, game_over, winner
    board = [[" " for _ in range(3)] for _ in range(3)]
    game_over = False
    winner = None
    return jsonify({"message": "Game reset!"})

@app.route("/board", methods=["GET"])
def get_board():
    return jsonify({"board": board, "game_over": game_over, "winner": winner})

@app.route("/move", methods=["POST"])
def make_move():
    global game_over, winner
    data = request.get_json()
    position = data.get("position")  # position is 1-9
    player = data.get("player", "X")  # Default player is "X"
    row, col = divmod(position - 1, 3)

    if game_over or board[row][col] != " ":
        return jsonify({"error": "Invalid move"}), 400

    # Make user move
    board[row][col] = player

    # Check if the user wins
    if check_win(board, player):
        game_over = True
        winner = player
        return jsonify({"board": board, "game_over": game_over, "winner": winner})

    # Check for a draw
    if check_draw(board):
        game_over = True
        return jsonify({"board": board, "game_over": game_over, "winner": "Draw"})

    # AI Move
    ai_move()

    # Check if the AI wins
    if check_win(board, "O"):
        game_over = True
        winner = "O"
        return jsonify({"board": board, "game_over": game_over, "winner": winner})

    # Check for a draw after AI move
    if check_draw(board):
        game_over = True
        return jsonify({"board": board, "game_over": game_over, "winner": "Draw"})

    return jsonify({"board": board, "game_over": game_over, "winner": winner})

if __name__ == "__main__":
    app.run(debug=True)
