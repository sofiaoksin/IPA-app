import json
import pathlib
import random

import streamlit as st


@st.cache_resource
def load_ipa_data() -> dict:
    """Load IPA symbols data from JSON file."""
    data_path = pathlib.Path(__file__).parent / "data" / "ipa_symbols.json"
    if not data_path.exists():
        st.error(f"Data file not found: {data_path}")
        return {"symbols": []}
    
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)


def initialize_session_state() -> None:
    """Initialize Streamlit session state for quiz."""
    if "quiz_started" not in st.session_state:
        st.session_state.quiz_started = False
    if "current_question" not in st.session_state:
        st.session_state.current_question = 0
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "quiz_questions" not in st.session_state:
        st.session_state.quiz_questions = []
    if "selected_answer" not in st.session_state:
        st.session_state.selected_answer = -1
    if "answer_submitted" not in st.session_state:
        st.session_state.answer_submitted = False
    if "quiz_completed" not in st.session_state:
        st.session_state.quiz_completed = False


def get_random_options(
    correct_symbol: dict, all_symbols: list[dict], num_options: int = 3
) -> tuple[list[dict], int]:
    """
    Generate random multiple choice options.
    
    Args:
        correct_symbol: The correct IPA symbol
        all_symbols: All available IPA symbols
        num_options: Number of options to generate
        
    Returns:
        Tuple of (options list, correct answer index)
    """
    # Filter out the correct symbol and get random incorrect options
    other_symbols = [s for s in all_symbols if s["id"] != correct_symbol["id"]]
    incorrect_options = random.sample(other_symbols, num_options - 1)
    
    # Combine and shuffle
    options = [correct_symbol] + incorrect_options
    random.shuffle(options)
    
    # Find correct answer index
    correct_index = options.index(correct_symbol)
    
    return options, correct_index


def setup_easy_mode(all_symbols: list[dict]) -> None:
    """Setup easy mode quiz (5 questions, 3 options)."""
    num_questions = min(5, len(all_symbols))
    selected_symbols = random.sample(all_symbols, num_questions)
    
    st.session_state.quiz_questions = []
    for symbol in selected_symbols:
        options, correct_idx = get_random_options(symbol, all_symbols, num_options=3)
        st.session_state.quiz_questions.append({
            "symbol": symbol,
            "options": options,
            "correct_index": correct_idx
        })
    
    st.session_state.quiz_started = True
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.selected_answer = -1
    st.session_state.answer_submitted = False
    st.session_state.quiz_completed = False


def select_answer(index: int) -> None:
    """Store the selected option before Streamlit reruns the page."""
    st.session_state.selected_answer = index


def display_question_content(question: dict, question_num: int, total_questions: int) -> int:
    """
    Display a quiz question with audio and options.
    
    Args:
        question: Question data dictionary
        question_num: Current question number (1-indexed)
        total_questions: Total number of questions
        
    Returns:
        Selected option index (-1 if no selection)
    """
    symbol = question["symbol"]
    options = question["options"]
    
    # Progress
    st.progress(question_num / total_questions, text=f"Question {question_num}/{total_questions}")
    
    # Symbol name and description
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader(f"IPA Symbol: {symbol['symbol']}")
    with col2:
        st.caption(f"{symbol['name']}")
    
    st.markdown(f"*{symbol['description']}*")
    
    # Audio player
    st.info("🔊 Listen to the audio below to identify the IPA symbol")
    
    if symbol.get("audio_url"):
        st.audio(symbol["audio_url"], format="audio/ogg")
    else:
        st.info("⚠️ Audio file not yet configured. Add `audio_url` to ipa_symbols.json")
    
    # Multiple choice options
    st.subheader("Choose the correct IPA symbol:")
    
    selected_index = st.session_state.selected_answer
    for idx, option in enumerate(options):
        button_label = f"{option['symbol']} - {option['name']}"
        st.button(
            button_label,
            key=f"option_{question_num}_{idx}",
            use_container_width=True,
            type="primary" if idx == selected_index else "secondary",
            disabled=st.session_state.answer_submitted,
            on_click=select_answer,
            args=(idx,),
        )
    
    return selected_index


def display_question_feedback(
    selected_index: int, correct_index: int, question: dict
) -> bool:
    """
    Display feedback for a question answer.
    
    Args:
        selected_index: Index of selected option
        correct_index: Index of correct option
        question: Question data dictionary
        
    """
    if selected_index == -1:
        return
    
    is_correct = selected_index == correct_index
    symbol = question["symbol"]
    correct_symbol = question["options"][correct_index]
    
    if is_correct:
        st.success(f"✅ Correct! The symbol is **{symbol['symbol']}** ({symbol['name']})")
    else:
        selected_symbol = question["options"][selected_index]
        st.error(
            f"❌ Incorrect. You selected **{selected_symbol['symbol']}**, "
            f"but the correct answer is **{correct_symbol['symbol']}** ({symbol['name']})"
        )
    
def display_quiz_results(score: int, total: int) -> None:
    """Display final quiz results."""
    st.markdown("---")
    st.subheader("🎉 Quiz Completed!")
    
    percentage = (score / total) * 100 if total > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Score", f"{score}/{total}")
    with col2:
        st.metric("Percentage", f"{percentage:.1f}%")
    with col3:
        if percentage == 100:
            st.metric("Grade", "🌟 Perfect!")
        elif percentage >= 80:
            st.metric("Grade", "🟢 Great!")
        elif percentage >= 60:
            st.metric("Grade", "🟡 Good")
        else:
            st.metric("Grade", "🔴 Keep practicing")
    
    st.markdown("---")
    if st.button("Start New Quiz", use_container_width=True, icon="🔄"):
        for key in [
            "quiz_started",
            "quiz_completed",
            "current_question",
            "score",
            "selected_answer",
            "answer_submitted",
        ]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()


# Main Quiz Interface
def main() -> None:
    """Main quiz page logic."""
    initialize_session_state()
    ipa_data = load_ipa_data()
    all_symbols = ipa_data.get("symbols", [])
    
    st.title("🧩 Quiz")
    
    # Quiz Selection Screen
    if not st.session_state.quiz_started:
        st.subheader("Choose your difficulty level:")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button(
                "🐣 Easy\n5 questions\n3 options",
                use_container_width=True,
                help="5 questions with 3 options each - perfect for beginners!"
            ):
                setup_easy_mode(all_symbols)
                st.rerun()
        
        with col2:
            st.button(
                "🐟 Medium\n10 questions\n5 options",
                disabled=True,
                use_container_width=True,
                help="Coming soon!"
            )
        
        with col3:
            st.button(
                "🐲 Hard\n15 questions\nOpen-ended",
                disabled=True,
                use_container_width=True,
                help="Coming soon!"
            )
        
        st.markdown("---")
        st.info("📖 **Tip**: Learn more about IPA symbols in the Interactive IPA Chart!")
    
    # Quiz Running Screen
    elif st.session_state.quiz_started and not st.session_state.quiz_completed:
        current_q_idx = st.session_state.current_question
        total_questions = len(st.session_state.quiz_questions)
        
        if current_q_idx < total_questions:
            question = st.session_state.quiz_questions[current_q_idx]
            
            # Display question
            selected_idx = display_question_content(question, current_q_idx + 1, total_questions)
            
            # Handle answer submission
            if selected_idx != -1 and not st.session_state.answer_submitted:
                col1, col2, col3 = st.columns([1, 1, 1])
                
                with col2:
                    if st.button("Submit Answer", use_container_width=True, type="primary"):
                        # Record answer
                        is_correct = selected_idx == question["correct_index"]
                        if is_correct:
                            st.session_state.score += 1

                        st.session_state.answer_submitted = True
                        st.rerun()

            if st.session_state.answer_submitted:
                display_question_feedback(
                    selected_idx, question["correct_index"], question
                )

                button_text = (
                    "Finish Quiz"
                    if current_q_idx + 1 >= total_questions
                    else "Next Question"
                )
                if st.button(button_text, use_container_width=True, type="primary"):
                    st.session_state.current_question += 1
                    st.session_state.selected_answer = -1
                    st.session_state.answer_submitted = False

                    if st.session_state.current_question >= total_questions:
                        st.session_state.quiz_completed = True

                    st.rerun()
    
    # Quiz Completed Screen
    if st.session_state.quiz_completed:
        display_quiz_results(st.session_state.score, len(st.session_state.quiz_questions))


if __name__ == "__main__":
    main()


