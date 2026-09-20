import streamlit as st

st.set_page_config(page_title="Gender Reveal", page_icon="🎈")

# Inject Custom CSS
custom_css = """
<style>
.stApp {
    background: linear-gradient(135deg, #e0f7fa 0%, #ffebee 100%);
    font-family: 'Comic Sans MS', cursive, sans-serif;
}
.title-text {
    text-align: center;
    color: #ff6f61;
    font-size: 2.2em;
    font-weight: bold;
    text-shadow: 2px 2px 4px #ffe0b2;
    margin-bottom: 10px;
}
.decorations {
    text-align: center;
    font-size: 1.8em;
    margin-bottom: 20px;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Application Header
st.markdown("<div class='decorations'>🎈 🌟 👑 💙 💖 👑 🌟 🎈</div>", unsafe_allow_html=True)
st.markdown("<h1 class='title-text'>Play to reveal the little bucket of sunshine!</h1>", unsafe_allow_html=True)
st.markdown("<div class='decorations'>👑 🌟 🎈 💙 💖 🎈 🌟 👑</div>", unsafe_allow_html=True)

# State Management
if "board_state" not in st.session_state:
    st.session_state.board_state = [""] * 9
if "move_count" not in st.session_state:
    st.session_state.move_count = 0

winning_sequence = [
    ["❌", "", "", "", "", "", "", "", ""],
    ["❌", "⭕", "", "", "", "", "", "", ""],
    ["❌", "⭕", "❌", "", "", "", "", "", ""],
    ["❌", "⭕", "❌", "⭕", "", "", "", "", ""],
    ["❌", "⭕", "❌", "⭕", "❌", "", "", "", "❌"],
]

def make_move():
    if st.session_state.move_count < len(winning_sequence) - 1:
        st.session_state.move_count += 1
        st.session_state.board_state = winning_sequence[st.session_state.move_count]
    else:
        st.session_state.board_state = winning_sequence[-1]

# Board Grid
cols = st.columns(3)
for i in range(9):
    col = cols[i % 3]
    cell_val = st.session_state.board_state[i]
    display_label = cell_val if cell_val != "" else " "
    
    col.button(
        display_label, 
        key=f"cell_{i}", 
        on_click=make_move, 
        disabled=(cell_val != ""),
        use_container_width=True
    )

# Status Message & Win Trigger
if st.session_state.board_state == winning_sequence[-1]:
    st.balloons()
    st.success("🎉 It's a Boy! 💙 Our little bucket of sunshine is arriving!")
else:
    st.info("Keep playing to reveal the secret! ✨")

# Reset Action
if st.button("🔄 Reset Game", type="secondary"):
    st.session_state.board_state = [""] * 9
    st.session_state.move_count = 0
    st.rerun()
