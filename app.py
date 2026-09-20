import streamlit as st
import random

st.set_page_config(page_title="Gender Reveal Game", page_icon="🎈", layout="centered")

# Custom CSS for Dark Cartoon Theme
dark_cartoon_css = """
<style>
/* Main Dark Gradient Background */
.stApp {
    background: linear-gradient(135deg, #121212 0%, #1a1a2e 50%, #16213e 100%);
    font-family: 'Comic Sans MS', 'Chalkboard SE', cursive, sans-serif;
    color: #f1f1f1;
}

/* Styled Cartoon Header */
.title-text {
    text-align: center;
    color: #ff6f91;
    font-size: 2.5em;
    font-weight: 900;
    text-shadow: 3px 3px 0px #000, 5px 5px 10px rgba(0, 0, 0, 0.7);
    margin-bottom: 10px;
}

.decorations {
    text-align: center;
    font-size: 2em;
    margin-bottom: 15px;
    filter: drop-shadow(0px 4px 6px rgba(0,0,0,0.5));
}

/* Dark Theme Buttons for Game Grid */
div[data-testid="stButton"] > button {
    height: 100px !important;
    font-size: 2.8em !important;
    font-weight: bold !important;
    border-radius: 20px !important;
    border: 3px solid #ff6f91 !important;
    background-color: #1f1f38 !important;
    color: #ffffff !important;
    box-shadow: 0 6px 0px #0d0d1a, 0 10px 15px rgba(0,0,0,0.5) !important;
    transition: all 0.1s ease-in-out !important;
}

div[data-testid="stButton"] > button:hover {
    border-color: #845ec2 !important;
    background-color: #2a2a4a !important;
    transform: translateY(-2px) !important;
}

div[data-testid="stButton"] > button:disabled {
    color: #ffffff !important;
    background-color: #16162a !important;
    border-color: #4b4453 !important;
    box-shadow: none !important;
}
</style>
"""
st.markdown(dark_cartoon_css, unsafe_allow_html=True)

# Header Section
st.markdown("<div class='decorations'>🎈 ✨ 👑 💙 💖 👑 ✨ 🎈</div>", unsafe_allow_html=True)
st.markdown("<h1 class='title-text'>Play to reveal the secret! 🎮</h1>", unsafe_allow_html=True)

# Initialize Session State
if "board" not in st.session_state:
    st.session_state.board = [""] * 9
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "status_msg" not in st.session_state:
    st.session_state.status_msg = "Your turn! Click an empty box to place ❌"

# Helper Function: Check for 3-in-a-row Win
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

# Handle Player Click
def handle_click(idx):
    if st.session_state.board[idx] != "" or st.session_state.game_over:
        return

    # 1. Place Player's X where clicked
    st.session_state.board[idx] = "❌"

    # Check if Player Won
    if check_winner(st.session_state.board, "❌"):
        st.session_state.game_over = True
        st.session_state.status_msg = "🎉 It's a Boy! 💙 Our little bucket of sunshine is arriving!"
        return

    # Check for Draw
    empty_indices = [i for i, cell in enumerate(st.session_state.board) if cell == ""]
    if not empty_indices:
        st.session_state.game_over = True
        st.session_state.status_msg = "It's a draw! Reset to try again ✨"
        return

    # 2. Bot Move: Place O automatically in an empty spot
    bot_choice = random.choice(empty_indices)
    st.session_state.board[bot_choice] = "⭕"

    # Check if Bot Won
    if check_winner(st.session_state.board, "⭕"):
        st.session_state.game_over = True
        st.session_state.status_msg = "Bot won this round! Reset to play again 🎈"

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
if st.button("🔄 Reset Game", type="primary"):
    st.session_state.board = [""] * 9
    st.session_state.game_over = False
    st.session_state.status_msg = "Your turn! Click an empty box to place ❌"
    st.rerun()
