import streamlit as st
import random

st.set_page_config(page_title="Baby Gender Reveal Game", page_icon="bb", layout="centered")

# Custom CSS for Dark Baby-Cartoon Theme
dark_baby_css = """
<style>
/* Main Dark Background with Soft Pastel Neon Accents */
.stApp {
    background: linear-gradient(135deg, #0d0e15 0%, #171926 50%, #1f1a30 100%);
    font-family: 'Comic Sans MS', 'Chalkboard SE', cursive, sans-serif;
    color: #f1f1f1;
}

/* Styled Cartoon Header */
.title-text {
    text-align: center;
    color: #ff9ebb;
    font-size: 2.3em;
    font-weight: 900;
    text-shadow: 2px 2px 0px #000, 4px 4px 8px rgba(255, 158, 187, 0.4);
    margin-bottom: 5px;
}

.sub-text {
    text-align: center;
    color: #89cff0;
    font-size: 1.2em;
    font-weight: bold;
    margin-bottom: 15px;
}

.decorations {
    text-align: center;
    font-size: 2.2em;
    margin-bottom: 10px;
    filter: drop-shadow(0px 4px 8px rgba(0,0,0,0.6));
}

/* Styled Game Buttons */
div[data-testid="stButton"] > button {
    height: 105px !important;
    font-size: 2.8em !important;
    font-weight: bold !important;
    border-radius: 25px !important;
    border: 3px solid #ffb6c1 !important;
    background-color: #191b2d !important;
    box-shadow: 0 6px 0px #0b0c16, 0 10px 20px rgba(0,0,0,0.6) !important;
    transition: all 0.15s ease-in-out !important;
}

div[data-testid="stButton"] > button:hover {
    border-color: #89cff0 !important;
    background-color: #252840 !important;
    transform: translateY(-3px) !important;
}

div[data-testid="stButton"] > button:disabled {
    background-color: #121320 !important;
    border-color: #383b56 !important;
    box-shadow: none !important;
}

/* Custom Text Colors inside game grid */
.pink-o {
    color: #ff69b4 !important;
    text-shadow: 0px 0px 10px #ff69b4;
}

.blue-x {
    color: #00bfff !important;
    text-shadow: 0px 0px 10px #00bfff;
}
</style>
"""
st.markdown(dark_baby_css, unsafe_allow_html=True)

# Header Section
st.markdown("<div class='decorations'>🍼 🧸 💖 💙 🚼 ✨ 🐥 🧷</div>", unsafe_allow_html=True)
st.markdown("<h1 class='title-text'>Play to Reveal the Secret Baby! 👶</h1>", unsafe_allow_html=True)
st.markdown("<div class='sub-text'>You are Pink 💗⭕ vs Bot Blue 💙❌</div>", unsafe_allow_html=True)

# Initialize Session State
if "board" not in st.session_state:
    st.session_state.board = [""] * 9
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "status_msg" not in st.session_state:
    st.session_state.status_msg = "Your turn! Click an empty block to place your Pink 💖⭕"

# Helper Function: Check Win
def check_winner(board, mark):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8], # Columns
        [0, 4, 8], [2, 4, 6]             # Diagonals
    ]
    for combo in win_conditions:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] == mark:
            return True
    return False

# Handle Player Click (Player is O)
def handle_click(idx):
    if st.session_state.board[idx] != "" or st.session_state.game_over:
        return

    # 1. Place Player's Pink O
    st.session_state.board[idx] = "💗⭕"

    # Check if Player Won
    if check_winner(st.session_state.board, "💗⭕"):
        st.session_state.game_over = True
        st.session_state.status_msg = "🎉 It's a Boy! 💙 Our little bucket of sunshine is arriving! 🍼"
        return

    # Check Draw
    empty_indices = [i for i, cell in enumerate(st.session_state.board) if cell == ""]
    if not empty_indices:
        st.session_state.game_over = True
        st.session_state.status_msg = "It's a tie! 🧸 Reset the board to try again! ✨"
        return

    # 2. Bot Move: Place Blue X automatically
    bot_choice = random.choice(empty_indices)
    st.session_state.board[bot_choice] = "💙❌"

    # Check if Bot Won
    if check_winner(st.session_state.board, "💙❌"):
        st.session_state.game_over = True
        st.session_state.status_msg = "🎉 It's a Boy! 💙 Our little bundle of joy is arriving! 🚼"

# Grid Display
cols = st.columns(3)
for i in range(9):
    col = cols[i % 3]
    cell_val = st.session_state.board[i]
    
    col.button(
        cell_val if cell_val != "" else " ",
        key=f"btn_{i}",
        on_click=handle_click,
        args=(i,),
        disabled=(cell_val != "" or st.session_state.game_over),
        use_container_width=True
    )

# Display Win Banner or Status
if st.session_state.game_over and "It's a Boy!" in st.session_state.status_msg:
    st.balloons()
    st.success(st.session_state.status_msg)
elif st.session_state.game_over:
    st.warning(st.session_state.status_msg)
else:
    st.info(st.session_state.status_msg)

# Reset Button
if st.button("🔄 Play Again 🧸", type="primary"):
    st.session_state.board = [""] * 9
    st.session_state.game_over = False
    st.session_state.status_msg = "Your turn! Click an empty block to place your Pink 💖⭕"
    st.rerun()
