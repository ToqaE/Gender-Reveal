import streamlit as st
import random

st.set_page_config(page_title="Baby Gender Reveal Game", page_icon="🚼", layout="centered")

# Custom CSS for Dark Theme, Smaller Centered Grid & Giant Styled Letters
custom_css = """
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
    font-size: 1.3em;
    font-weight: bold;
    margin-bottom: 20px;
}

.decorations {
    text-align: center;
    font-size: 2.2em;
    margin-bottom: 10px;
    filter: drop-shadow(0px 4px 8px rgba(0,0,0,0.6));
}

/* Restrain overall grid width so squares aren't massive */
[data-testid="column"] {
    padding: 0px 4px !important;
}

/* Button Styling: Compact Square Fields & Massive Text */
div[data-testid="stButton"] > button {
    width: 100% !important;
    height: 110px !important;            /* Smaller, compact height */
    max-height: 110px !important;
    font-size: 3.5em !important;          /* Enormous letter sizing */
    font-weight: 900 !important;
    border-radius: 18px !important;
    border: 3px solid #ffb6c1 !important;
    background-color: #191b2d !important;
    box-shadow: 0 5px 0px #0b0c16, 0 8px 15px rgba(0,0,0,0.6) !important;
    transition: all 0.15s ease-in-out !important;
    line-height: 1 !important;
}

div[data-testid="stButton"] > button:hover {
    border-color: #89cff0 !important;
    background-color: #252840 !important;
    transform: translateY(-2px) !important;
}

div[data-testid="stButton"] > button:disabled {
    background-color: #121320 !important;
    border-color: #383b56 !important;
    box-shadow: none !important;
}

/* Pink O Color */
.pink-o {
    color: #FF69B4 !important;
    font-weight: 900;
}

/* Blue X Color */
.blue-x {
    color: #00BFFF !important;
    font-weight: 900;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Header Section
st.markdown("<div class='decorations'>🍼 🧸 💖 💙 🚼 ✨ 🐥 🧷</div>", unsafe_allow_html=True)
st.markdown("<h1 class='title-text'>Play to Reveal the Secret Baby! 👶</h1>", unsafe_allow_html=True)
st.markdown("<div class='sub-text'>You are <span style='color:#FF69B4;'>Pink O</span> vs Bot <span style='color:#00BFFF;'>Blue X</span></div>", unsafe_allow_html=True)

# Initialize Session State
if "board" not in st.session_state:
    st.session_state.board = [""] * 9
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "status_msg" not in st.session_state:
    st.session_state.status_msg = "Your turn! Click an empty box to place O"

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

    # 1. Place Player's O
    st.session_state.board[idx] = "O"

    # Check if Player Won
    if check_winner(st.session_state.board, "O"):
        st.session_state.game_over = True
        st.session_state.status_msg = "🎉 It's a Boy! 💙 Our little bucket of sunshine is arriving! 🍼"
        return

    # Check Draw
    empty_indices = [i for i, cell in enumerate(st.session_state.board) if cell == ""]
    if not empty_indices:
        st.session_state.game_over = True
        st.session_state.status_msg = "It's a tie! 🧸 Reset the board to try again! ✨"
        return

    # 2. Bot Move: Place X
    bot_choice = random.choice(empty_indices)
    st.session_state.board[bot_choice] = "X"

    # Check if Bot Won
    if check_winner(st.session_state.board, "X"):
        st.session_state.game_over = True
        st.session_state.status_msg = "🎉 It's a Boy! 💙 Our little bundle of joy is arriving! 🚼"

# Center and constrain grid width
_, center_col, _ = st.columns([1, 3, 1])

with center_col:
    for row in range(3):
        cols = st.columns(3)
        for col in range(3):
            idx = row * 3 + col
            cell_val = st.session_state.board[idx]
            
            # Display plain X or O without surrounding emojis
            display_char = cell_val if cell_val != "" else " "
            
            cols[col].button(
                display_char,
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
    st.session_state.status_msg = "Your turn! Click an empty box to place O"
    st.rerun()
