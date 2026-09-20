import streamlit as st
import random

st.set_page_config(page_title="Baby Gender Reveal Game", page_icon="🚼", layout="centered")

# Custom CSS for Dark Baby-Cartoon Theme with Square Grid and Giant Neon Colors
dark_baby_css = """
<style>
/* Main Dark Background */
.stApp {
    background: linear-gradient(135deg, #0d0e15 0%, #171926 50%, #1f1a30 100%);
    font-family: 'Comic Sans MS', 'Chalkboard SE', cursive, sans-serif;
    color: #f1f1f1;
}

/* Header Styling */
.title-text {
    text-align: center;
    color: #ff9ebb;
    font-size: 2.2em;
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

/* Force Square Buttons with Giant Fonts */
div[data-testid="stButton"] > button {
    width: 100% !important;
    aspect-ratio: 1 / 1 !important;  /* Enforces perfect square shape */
    height: auto !important;
    font-size: 4em !important;        /* Extra large X and O */
    font-weight: bold !important;
    border-radius: 20px !important;
    border: 3px solid #ffb6c1 !important;
    background-color: #191b2d !important;
    box-shadow: 0 6px 0px #0b0c16, 0 10px 20px rgba(0,0,0,0.6) !important;
    transition: all 0.15s ease-in-out !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
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
</style>
"""
st.markdown(dark_baby_css, unsafe_allow_html=True)

# Header Section
st.markdown("<div class='decorations'>🍼 🧸 💖 💙 🚼 ✨ 🐥 🧷</div>", unsafe_allow_html=True)
st.markdown("<h1 class='title-text'>Play to Reveal the Secret Baby! 👶</h1>", unsafe_allow_html=True)
st.markdown("<div class='sub-text'>You are Pink ⭕ vs Bot Blue ❌</div>", unsafe_allow_html=True)

# Initialize Session State
if "board" not in st.session_state:
    st.session_state.board = [""] * 9
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "status_msg" not in st.session_state:
    st.session_state.status_msg = "Your turn! Click an empty square to place ⭕"

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

# Handle Player Click (Player is Pink O)
def handle_click(idx):
    if st.session_state.board[idx] != "" or st.session_state.game_over:
        return

    # 1. Place Player's Pink O
    st.session_state.board[idx] = "🌸⭕"

    # Check if Player Won
    if check_winner(st.session_state.board, "🌸⭕"):
        st.session_state.game_over = True
        st.session_state.status_msg = "🎉 It's a Boy! 💙 Our little bucket of sunshine is arriving! 🍼"
        return

    # Check Draw
    empty_indices = [i for i, cell in enumerate(st.session_state.board) if cell == ""]
    if not empty_indices:
        st.session_state.game_over = True
        st.session_state.status_msg = "It's a tie! 🧸 Reset the board to try again! ✨"
        return

    # 2. Bot Move: Place Blue X
    bot_choice = random.choice(empty_indices)
    st.session_state.board[bot_choice] = "🚙❌"

    # Check if Bot Won
    if check_winner(st.session_state.board, "🚙❌"):
        st.session_state.game_over = True
        st.session_state.status_msg = "🎉 It's a Boy! 💙 Our little bundle of joy is arriving! 🚼"

# Render Square Grid
grid_container = st.container()
with grid_container:
    for row in range(3):
        cols = st.columns(3, gap="small")
        for col in range(3):
            idx = row * 3 + col
            cell_val = st.session_state.board[idx]
            
            cols[col].button(
                cell_val if cell_val != "" else " ",
                key=f"btn_{idx}",
                on_click=handle_click,
                args=(idx,),
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
    st.session_state.status_msg = "Your turn! Click an empty square to place ⭕"
    st.rerun()
