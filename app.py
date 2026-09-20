import streamlit as st

# Custom CSS for the Gender Reveal theme (Colors, Balloons, Tiaras, Stars)
custom_css = """
body {
    background: linear-gradient(135deg, #e0f7fa 0%, #ffebee 100%);
    font-family: 'Comic Sans MS', cursive, sans-serif;
}
.title-text {
    text-align: center;
    color: #ff6f61;
    font-size: 2.5em;
    font-weight: bold;
    text-shadow: 2px 2px 4px #ffe0b2;
    margin-bottom: 10px;
}
.decorations {
    text-align: center;
    font-size: 1.8em;
    margin-bottom: 20px;
}
/* Style the buttons to look like a game board */
.cell-button {
    font-size: 3em !important;
    height: 120px !important;
    border-radius: 15px !important;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
"""

# Preset moves to ensure X always wins and plays interactively
# Board states as turns progress
winning_sequence = [
    # Turn 1 (User clicks somewhere, say top-left '0') -> X appears
    ["❌", "", "", "", "", "", "", "", ""],
    # Turn 2 (Bot plays 'O')
    ["❌", "⭕", "", "", "", "", "", "", ""],
    # Turn 3 (User plays)
    ["❌", "⭕", "❌", "", "", "", "", "", ""],
    # Turn 4 (Bot plays)
    ["❌", "⭕", "❌", "⭕", "", "", "", "", ""],
    # Turn 5 (Winning move for X: diagonal win)
    ["❌", "⭕", "❌", "⭕", "❌", "", "", "", "❌"],
]

def handle_click(board_state, btn_index):
    # Count how many moves have been made
    filled_count = sum(1 for cell in board_state if cell != "")
    
    if filled_count >= 9 or "It's a Boy!" in "".join(board_state):
        return board_state, "🎉 It's a Boy! 💙"

    # Determine next step in our rigged winning sequence
    turn_index = min(filled_count, len(winning_sequence) - 1)
    current_board = winning_sequence[turn_index]
    
    # Check if game is won (on the final step)
    if turn_index == len(winning_sequence) - 1:
        return current_board, "🎉 It's a Boy! 💙 Our little bucket of sunshine is arriving!"
    
    return current_board, "Keep playing to reveal the secret! ✨"

def reset_game():
    return ["", "", "", "", "", "", "", "", ""], "Play your move! 🎈"

with gr.Blocks(css=custom_css) as demo:
    gr.HTML("<div class='decorations'>🎈 🌟 👑 💙 💖 👑 🌟 🎈</div>")
    gr.HTML("<h1 class='title-text'>Play to reveal the little bucket of sunshine!</h1>")
    gr.HTML("<div class='decorations'>👑 🌟 🎈 💙 💖 🎈 🌟 👑</div>")
    
    status_display = gr.Markdown("### Play your first move! 🎈", elem_id="status")
    
    # Game board grid
    board = []
    with gr.Row():
        for i in range(3):
            with gr.Column():
                row_buttons = []
                for j in range(3):
                    idx = i * 3 + j
                    btn = gr.Button("", elem_classes="cell-button")
                    board.append(btn)

    # State management for the board cells
    board_state = gr.State(["", "", "", "", "", "", "", "", ""])

    # Connect button clicks
    for i, btn in enumerate(board):
        btn.click(
            fn=lambda state, idx=i: handle_click(state, idx),
            inputs=[board_state],
            outputs=[board_state, status_display]
        )
        # Bind the state values back to the button labels visually
        # (Gradio maps state changes to button values)
    
    # Sync button values with board state
    for i, btn in enumerate(board):
        board_state.change(
            fn=lambda state, idx=i: gr.update(value=state[idx], 
                                              interactive=(state[idx] == "")),
            inputs=[board_state],
            outputs=[btn]
        )

    reset_btn = gr.Button("🔄 Reset Game", variant="secondary")
    reset_btn.click(fn=reset_game, outputs=[board_state, status_display])

if __name__ == "__main__":
    demo.launch()
