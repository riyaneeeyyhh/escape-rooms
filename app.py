import streamlit as st
import time

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="The 12 Room Escape",
    page_icon="🔐",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at top left, #18204a 0%, transparent 35%),
        radial-gradient(circle at bottom right, #24143f 0%, transparent 35%),
        #070a13;
    color: white;
}

.main-title {
    font-size: 48px;
    font-weight: 900;
    text-align: center;
    color: #8ea2ff;
    text-shadow: 0 0 25px #5967ff;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #9da8c3;
    font-size: 18px;
    margin-bottom: 30px;
}

.room-card {
    background: linear-gradient(145deg, #12182b, #0b1020);
    border: 1px solid #303b63;
    border-radius: 20px;
    padding: 25px;
    box-shadow: 0 15px 50px rgba(0,0,0,.35);
}

.lock-box {
    background: #080c16;
    border: 1px solid #303b63;
    border-radius: 15px;
    padding: 20px;
    margin-top: 20px;
}

.clue-box {
    background: linear-gradient(135deg,#171e38,#101629);
    border-left: 5px solid #7568ff;
    border-radius: 12px;
    padding: 18px;
    margin: 15px 0;
}

.inventory-item {
    display: inline-block;
    background: #202a48;
    border: 1px solid #42517d;
    border-radius: 10px;
    padding: 8px 12px;
    margin: 4px;
}

.success-box {
    background: #092d22;
    border: 1px solid #27dca2;
    border-radius: 15px;
    padding: 20px;
    text-align: center;
}

.warning-box {
    background: #351c1f;
    border: 1px solid #ff6478;
    border-radius: 15px;
    padding: 20px;
}

.final-box {
    background: linear-gradient(135deg,#25154c,#11152f);
    border: 2px solid #9a6cff;
    border-radius: 20px;
    padding: 25px;
    box-shadow: 0 0 35px #7652ff44;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# ROOM DATA
# =========================================================

ROOMS = [
    {
        "name": "The Library",
        "clue": "A book says: 2 + 7 + 4 + 1.",
        "code": "2741",
        "item": "Library Key",
        "description": "Ancient books surround a locked wooden door."
    },
    {
        "name": "The Clock Room",
        "clue": "Three clocks show 5, 8 and 3.",
        "code": "583",
        "item": "Clock Key",
        "description": "Three strange clocks tick in perfect silence."
    },
    {
        "name": "The Painting Room",
        "clue": "The paintings are numbered 9 - 1 - 6 - 2.",
        "code": "9162",
        "item": "Painting Key",
        "description": "Four mysterious paintings cover the walls."
    },
    {
        "name": "The Laboratory",
        "clue": "Red = 4, Blue = 2, Yellow = 1.",
        "code": "421",
        "item": "Lab Key",
        "description": "Colorful chemicals glow inside glass containers."
    },
    {
        "name": "The Office",
        "clue": "A hidden note reads: 7 3 5 8.",
        "code": "7358",
        "item": "Office Key",
        "description": "An old computer and locked filing cabinets fill the room."
    },
    {
        "name": "The Storage Room",
        "clue": "Boxes are marked 20, 4 and 6; enter the numbers in order.",
        "code": "2046",
        "item": "Storage Key",
        "description": "Dusty crates hide something important."
    },
    {
        "name": "The Music Room",
        "clue": "Notes play in this order: 8 - 1 - 9.",
        "code": "819",
        "item": "Music Key",
        "description": "A mysterious piano waits for the correct sequence."
    },
    {
        "name": "The Museum",
        "clue": "Ancient symbols translate to 5 6 2 4.",
        "code": "5624",
        "item": "Museum Key",
        "description": "Ancient artifacts cover the walls."
    },
    {
        "name": "The Secret Garden",
        "clue": "Stone tablets show 3 - 9 - 1.",
        "code": "391",
        "item": "Garden Key",
        "description": "An abandoned garden hides an underground entrance."
    },
    {
        "name": "The Security Room",
        "clue": "Camera labels: 7, 4, 8, 2.",
        "code": "7482",
        "item": "Security Key",
        "description": "Security cameras monitor every corridor."
    },
    {
        "name": "The Secret Vault",
        "clue": "The vault note says 6 - 1 - 5.",
        "code": "615",
        "item": "Master Key",
        "description": "A huge metal vault blocks the final passage."
    },
    {
        "name": "THE FINAL CHAMBER",
        "clue": "FINAL BOSS: Combine the discovered symbols to unlock the final door.",
        "code": "83917",
        "item": "Freedom",
        "description": "The final chamber contains the ultimate escape puzzle."
    }
]

# =========================================================
# SESSION STATE
# =========================================================

if "room" not in st.session_state:
    st.session_state.room = 0

if "inventory" not in st.session_state:
    st.session_state.inventory = []

if "solved" not in st.session_state:
    st.session_state.solved = []

if "hints" not in st.session_state:
    st.session_state.hints = 3

if "input_code" not in st.session_state:
    st.session_state.input_code = ""

if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

if "game_over" not in st.session_state:
    st.session_state.game_over = False

if "victory" not in st.session_state:
    st.session_state.victory = False

# =========================================================
# FUNCTIONS
# =========================================================

def reset_game():
    st.session_state.room = 0
    st.session_state.inventory = []
    st.session_state.solved = []
    st.session_state.hints = 3
    st.session_state.input_code = ""
    st.session_state.start_time = time.time()
    st.session_state.game_over = False
    st.session_state.victory = False


def check_code():

    current_room = ROOMS[st.session_state.room]

    if st.session_state.input_code == current_room["code"]:

        if st.session_state.room not in st.session_state.solved:

            st.session_state.solved.append(
                st.session_state.room
            )

            if current_room["item"] not in st.session_state.inventory:
                st.session_state.inventory.append(
                    current_room["item"]
                )

        st.session_state.input_code = ""

        if st.session_state.room == 11:
            st.session_state.victory = True

        st.success("🔓 Correct! The lock has opened.")

    else:
        st.session_state.input_code = ""
        st.error("❌ Wrong code! Search the room again.")


def add_digit(number):

    if len(st.session_state.input_code) < 10:
        st.session_state.input_code += str(number)


def clear_code():
    st.session_state.input_code = ""


def next_room():

    if st.session_state.room in st.session_state.solved:

        if st.session_state.room < 11:
            st.session_state.room += 1
            st.session_state.input_code = ""
            st.rerun()

    else:
        st.warning("🔒 Solve the current room first.")


# =========================================================
# TIMER
# =========================================================

TOTAL_TIME = 20 * 60

elapsed = int(time.time() - st.session_state.start_time)
remaining = max(0, TOTAL_TIME - elapsed)

minutes = remaining // 60
seconds = remaining % 60

if remaining == 0 and not st.session_state.victory:
    st.session_state.game_over = True

# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🔐 THE 12 ROOM ESCAPE</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Solve the puzzles • Find the clues • Escape before time runs out</div>',
    unsafe_allow_html=True
)

# =========================================================
# TOP STATS
# =========================================================

a, b, c, d = st.columns(4)

with a:
    st.metric(
        "🏠 ROOM",
        f"{st.session_state.room + 1} / 12"
    )

with b:
    timer_color = "🔴" if remaining < 120 else "⏱️"

    st.metric(
        "TIME",
        f"{timer_color} {minutes:02d}:{seconds:02d}"
    )

with c:
    st.metric(
        "💡 HINTS",
        st.session_state.hints
    )

with d:
    st.metric(
        "🔓 SOLVED",
        f"{len(st.session_state.solved)} / 12"
    )

st.progress(
    (st.session_state.room + 1) / 12
)

# =========================================================
# GAME OVER
# =========================================================

if st.session_state.game_over:

    st.markdown(
        """
        <div class="warning-box">
        <h1>⏰ TIME'S UP!</h1>
        <p>The building remains locked.</p>
        <p>Can you escape faster next time?</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("🔄 TRY AGAIN", use_container_width=True):
        reset_game()
        st.rerun()

    st.stop()

# =========================================================
# VICTORY
# =========================================================

if st.session_state.victory:

    st.markdown(
        f"""
        <div class="final-box">
        <h1>🏆 YOU ESCAPED!</h1>
        <h2>CONGRATULATIONS!</h2>
        <p>You solved all 12 rooms.</p>
        <p>⏱️ Time remaining: {minutes:02d}:{seconds:02d}</p>
        <p>💡 Hints remaining: {st.session_state.hints}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("🎮 PLAY AGAIN", use_container_width=True):
        reset_game()
        st.rerun()

    st.stop()

# =========================================================
# MAIN GAME
# =========================================================

current = ROOMS[st.session_state.room]

left, right = st.columns([2, 1])

# =========================================================
# LEFT SIDE
# =========================================================

with left:

    st.markdown(
        f"""
        <div class="room-card">
        <h1>🚪 Room {st.session_state.room + 1}: {current["name"]}</h1>
        <p>{current["description"]}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 🔍 CLUE")

    st.markdown(
        f"""
        <div class="clue-box">
        <b>Hidden clue:</b><br><br>
        {current["clue"]}
        </div>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # FINAL BOSS
    # =====================================================

    if st.session_state.room == 11:

        st.markdown(
            """
            <div class="final-box">
            <h2>👑 FINAL BOSS PUZZLE</h2>
            <p>Three symbols appear on the walls.</p>
            <p>🔺 Triangle = 8</p>
            <p>⭕ Circle = 3</p>
            <p>⬛ Square = 9</p>
            <p>Two final symbols complete the sequence.</p>
            <p><b>The final code is hidden in the chamber.</b></p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # =====================================================
    # LOCK
    # =====================================================

    st.markdown("### 🔢 NUMBER LOCK")

    st.markdown(
        f"""
        <div class="lock-box">
        <h2 style="text-align:center;color:#72f6c0;">
        {st.session_state.input_code or "— — — —"}
        </h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    # keypad

    rows = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
        ["CLEAR", 0, "ENTER"]
    ]

    for row in rows:

        cols = st.columns(3)

        for col, key in zip(cols, row):

            with col:

                if key == "CLEAR":

                    if st.button(
                        "⌫ CLEAR",
                        use_container_width=True
                    ):
                        clear_code()
                        st.rerun()

                elif key == "ENTER":

                    if st.button(
                        "🔓 ENTER",
                        use_container_width=True
                    ):
                        check_code()

                else:

                    if st.button(
                        str(key),
                        use_container_width=True
                    ):
                        add_digit(key)
                        st.rerun()

# =========================================================
# RIGHT SIDE
# =========================================================

with right:

    st.markdown("## 🎒 INVENTORY")

    if st.session_state.inventory:

        for item in st.session_state.inventory:

            st.markdown(
                f"""
                <div class="inventory-item">
                🔑 {item}
                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.info("Your inventory is empty.")

    st.markdown("---")

    # HINT

    if st.button(
        "💡 USE HINT",
        use_container_width=True
    ):

        if st.session_state.hints > 0:

            st.session_state.hints -= 1

            st.info(
                "Hint: " + current["clue"]
            )

        else:

            st.error(
                "You have no hints left!"
            )

    # NEXT ROOM

    if st.button(
        "🚪 NEXT ROOM",
        use_container_width=True
    ):

        next_room()

    # RESET

    if st.button(
        "🔄 RESTART GAME",
        use_container_width=True
    ):

        reset_game()
        st.rerun()

    st.markdown("---")

    st.markdown("### 📜 MISSION")

    st.write(
        "Solve every lock, collect every key, "
        "and reach the Final Chamber."
    )

    st.markdown("### 🎯 CONTROLS")

    st.write(
        """
        🖱️ Click buttons  
        🔢 Enter numbers using keypad  
        💡 Use hints carefully  
        🎒 Collect keys  
        🚪 Unlock every room
        """
    )

# =========================================================
# AUTO REFRESH TIMER
# =========================================================

# Refresh the Streamlit page every second.
# This keeps the countdown moving.

st.markdown(
    """
    <script>
    setTimeout(function(){
        window.parent.location.reload();
    }, 1000);
    </script>
    """,
    unsafe_allow_html=True
)
