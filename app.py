import streamlit as st

st.set_page_config(page_title="Baby Gender Reveal Game", page_icon="🚼", layout="centered")

# Custom CSS with Super Sized & Ultra Bold Letters
custom_css = """
<style>
/* Main Background */
.stApp {
    background: linear-gradient(135deg, #181a26 0%, #222638 50%, #2a2d42 100%);
    font-family: 'Comic Sans MS', 'Chalkboard SE', cursive, sans-serif;
    color: #ffffff;
}

/* Header Styling */
.title-text {
    text-align: center;
    color: #ffb6c1;
    font-size: 2.2em;
    font-weight: 900;
    text-shadow: 2px 2px 0px #000, 4px 4px 10px rgba(255, 182, 193, 0.5);
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
}

/* Compact Grid Columns */
[data-testid="column"] {
    padding: 0px 4px !important;
}

/* Base Square Button Styling */
div[data-testid="stButton"] > button {
    width: 100% !important;
    height: 120px !important;
    max-height: 120px !important;
    border-radius: 18px !important;
    border: 3px solid #4a4e69 !important;
    background-color: #2b2e4a !important;
    color: #ffffff !important;
    box-shadow: 0 5px 0px #1a1c2e, 0 8px 15px rgba(0,0,0,0.4) !important;
    transition: all 0.15s ease-in-out !important;
    padding: 0 !important;
}

div[data-testid="stButton"] > button:hover {
    border-color: #ffb6c1 !important;
    background-color: #3b3e5e !important;
}

/* Override text element inside Streamlit button for HUGE bold display */
div[data-testid="stButton"] button p {
    font-size: 6.5rem !important;
    font-weight: 900 !important;
    line-height: 1 !important;
    margin: 0 !important;
    padding: 0 !important;
    -webkit-text-stroke: 3px black; /* Bold dark outline for maximum pop */
}

/* Pink O Tile Styling (User Selection) */
div.pink-tile > div[data-testid="stButton"] > button:disabled {
    background-color: #ffb6c1 !important;
    border-color: #ff69b4 !important;
    opacity: 1 !important;
    box-shadow: 0px 0px 20px rgba(255, 105, 180, 0.8) !important;
}
div.pink-tile > div[data-testid="stButton"] button p {
    color: #8b0046 !important;
    -webkit-text-stroke: 2px #ff1493 !important;
    text-shadow: 0px 0px 15px #ff1493 !important;
}

/* Blue X Tile Styling (Bot Selection) */
div.blue-tile > div[data-testid="stButton"] > button:disabled {
    background-color: #89cff0 !important;
    border-color: #00bfff !important;
    opacity: 1 !important;
    box-shadow: 0px 0px 20px rgba(0, 191, 255, 0.8) !important;
}
div.blue-tile > div[data-testid="stButton"] button p {
    color: #002b5c !important;
    -webkit-text-stroke: 2px #00bfff !important;
    text-shadow: 0px 0px 15px #00bfff !important;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Header Section
st.markdown("<div class='decorations'>🍼 🧸 💖 💙 🚼 ✨ 🐥 🧷</div>", unsafe_allow_html=True)
st.markdown("<h1 class='title-text'>Play to Reveal the Secret Baby! 👶</h1>", unsafe_allow_html=True)
st.markdown("<div class='sub-text'>You are <span style='color:#ffb6c1;'>Pink O</span> vs Bot <span style='color:#89cff0;'>Blue X</span></div>", unsafe_allow_html=True)

# Initialize Session State
if "board" not in st.session_state:
    st.session_state.board = [""] * 9
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "status_msg" not in st.session_state:
    st.session_state.status_msg = "Your turn! Click an empty square to place O"

# Win Combinations
WIN_COMBOS = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8], # Rows
    [0, 3, 6], [1, 4, 7], [2, 5, 8], # Columns
    [0, 4, 8], [2, 4, 6]             # Diagonals
]

def check_winner(board, mark):
    for combo in WIN_COMBOS:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] == mark:
            return True
    return False

# Rigged Bot Logic: Guarantees Blue X Wins
def get_rigged_bot_move(board):
    # 1. Take immediate winning move for X if available
    for combo in WIN_COMBOS:
        marks = [board[i] for i in combo]
        if marks.count("X") == 2 and marks.count("") == 1:
            return combo[marks.index("")]

    # 2. Block O if O is about to win (prevents O from winning)
    for combo in WIN_COMBOS:
        marks = [board[i] for i in combo]
        if marks.count("O") == 2 and marks.count("") == 1:
            return combo[marks.index("")]

    # 3. Prefer strategic spots
    for preferred in [4, 0, 2, 6, 8, 1, 3, 5, 7]:
        if board[preferred] == "":
            return preferred
    return None

# Handle Player Turn
def handle_click(idx):
    if st.session_state.board[idx] != "" or st.session_state.game_over:
        return

    # 1. Place Player's O
    st.session_state.board[idx] = "O"

    # 2. Trigger Rigged Bot Move (Blue X)
    empty_indices = [i for i, cell in enumerate(st.session_state.board) if cell == ""]
    if empty_indices:
        bot_choice = get_rigged_bot_move(st.session_state.board)
        if bot_choice is not None:
            st.session_state.board[bot_choice] = "X"

    # 3. Check if X Wins (Only X triggers the reveal)
    if check_winner(st.session_state.board, "X"):
        st.session_state.game_over = True
        st.session_state.status_msg = "🎉 It's a Boy! 💙 Our little bucket of sunshine is arriving! 🍼"

# Grid Rendering with Colored Container Wrappers
_, center_col, _ = st.columns([1, 3, 1])

with center_col:
    for row in range(3):
        cols = st.columns(3)
        for col in range(3):
            idx = row * 3 + col
            cell_val = st.session_state.board[idx]
            
            # Apply dynamic class based on selection
            tile_class = "pink-tile" if cell_val == "O" else ("blue-tile" if cell_val == "X" else "")
            
            with cols[col]:
                st.markdown(f"<div class='{tile_class}'>", unsafe_allow_html=True)
                st.button(
                    cell_val if cell_val != "" else " ",
                    key=f"btn_{idx}",
                    on_click=handle_click,
                    args=(idx,),
                    disabled=(cell_val != "" or st.session_state.game_over),
                    use_container_width=True
                )
                st.markdown("</div>", unsafe_allow_html=True)

# Status & Reveal Banner
if st.session_state.game_over:
    st.balloons()
    st.success(st.session_state.status_msg)
else:
    st.info(st.session_state.status_msg)

# Reset Button
if st.button("🔄 Play Again 🧸", type="primary"):
    st.session_state.board = [""] * 9
    st.session_state.game_over = False
    st.session_state.status_msg = "Your turn! Click an empty square to place O"
    st.rerun()
