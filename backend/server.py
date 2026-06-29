from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from Board import Board
from Player import HumanPlayer, AIPlayer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

game = Board()
ai = None
human = None

# ------ Setup Request ------
class SetupRequest(BaseModel):
    human_color: str   # "W" or "B"
    depth: int


# ------ Setup Game Endpoint ------
@app.post("/setup_game/")
def setup_game(data: SetupRequest):
    global game, ai, human

    # reset board
    game = Board()

    # Convert W or B to internal 1 / -1
    if data.human_color.upper() == "W":
        human = HumanPlayer(Board.W)
        ai = AIPlayer(Board.B, data.depth)
    else:
        human = HumanPlayer(Board.B)
        ai = AIPlayer(Board.W, data.depth)

    return {
        "message": "Το παιχνίδι ξεκίνησε!",
        "human_color": data.human_color,
        "ai_color": "B" if data.human_color.upper() == "W" else "W",
        "depth": data.depth
    }


# ------ State Endpoint ------
@app.get("/state")
def get_state():
    state = {
        "board": game.Board,
        "last_move": (
            game.last_move.row,
            game.last_move.col
        ) if game.last_move else None,
        "last_player": game.last_player,
        "available_moves": game.available_moves() if ai and game.last_player == ai.player_letter else None
    }

    if game.is_terminal():
        scores = game.get_scores()
        winner = "W" if scores["W"] > scores["B"] else ("B" if scores["B"] > scores["W"] else "Ισοπαλία")
        state["scores"] = scores
        state["message"] = "Τέλος παιχνιδιού!"

    return state


# ------ Make Move Endpoint ------
class MoveRequest(BaseModel):
    row: int
    col: int


@app.post("/make_move/")
def make_move(data: MoveRequest):
    global game, human

    # 1. Έλεγχος αν το παιχνίδι έχει τελειώσει
    if game.is_terminal():
        raise HTTPException(status_code=400, detail="Το παιχνίδι έχει ήδη τελειώσει.")

    # 2. Έλεγχος σειράς
    player_to_move = game.B if game.last_player == game.W else game.W
    if player_to_move != human.player_letter:
        raise HTTPException(status_code=403, detail="Δεν είναι η σειρά σας να παίξετε. Περιμένετε τον AI.")

    human_move = (data.row, data.col)

    # 3. Έλεγχος εγκυρότητας κίνησης
    if not game.is_valid_move(data.row, data.col):
        raise HTTPException(status_code=400, detail="Δεν είναι έγκυρη θέση.")

    human_has_moves = game.available_moves_for(human.player_letter)
    if human_has_moves:
        game.make_move(data.row, data.col, human.player_letter)
    else:
        human_move = None  # πάσο
        game.change_last_player()

    if game.is_terminal():
        scores = game.get_scores()
        return {
            "message": "Τέλος παιχνιδιού!",
            "board": game.Board,
            "human_move": human_move,
            "scores": scores,
            "next_player_is_ai": False
        }
    else:
        return {
            "message": "Η κίνηση του ανθρώπου έγινε.",
            "board": game.Board,
            "human_move": human_move,
            "next_player_is_ai": True
        }


# ------ AI Turn Endpoint ------
@app.post("/ai_turn/")
def ai_turn():
    global game, ai

    # 1. Έλεγχος σειράς
    player_to_move = game.B if game.last_player == game.W else game.W
    if player_to_move != ai.player_letter:
        raise HTTPException(status_code=403, detail="Δεν είναι η σειρά του AI να παίξει.")

    # 2. Έλεγχος αν το παιχνίδι έχει τελειώσει
    if game.is_terminal():
        raise HTTPException(status_code=400, detail="Το παιχνίδι έχει ήδη τελειώσει.")

    ai_move = None
    message = ""

    ai_has_moves = game.available_moves_for(ai.player_letter)

    if not ai_has_moves:
        message = "Ο AI έκανε πάσο."
        game.change_last_player()
    else:
        ai_move = ai.choose_move(game)
        if ai_move is not None:
            r, c = ai_move
            game.make_move(r, c, ai.player_letter)
            message = "Ο AI έπαιξε."
        else:
            message = "Ο AI έκανε πάσο (Minimax)."
            game.change_last_player()

    # 3. Έλεγχος τέλους παιχνιδιού
    if game.is_terminal():
        scores = game.get_scores()
        return {
            "message": "Τέλος παιχνιδιού!",
            "ai_move": ai_move,
            "board": game.Board,
            "scores": scores,
            "next_player_is_ai": False
        }
    else:
        human_has_moves = game.available_moves_for(human.player_letter)
        if not human_has_moves:
            game.change_last_player()
            return {
                "message": message,
                "ai_move": ai_move,
                "board": game.Board,
                "next_player_is_ai": True
            }
        else:
            return {
                "message": message,
                "ai_move": ai_move,
                "board": game.Board,
                "next_player_is_ai": False
            }


# ------ Reset Endpoint ------
@app.post("/reset")
def reset():
    global game, ai, human
    game = Board()
    return {"status": "reset"}
