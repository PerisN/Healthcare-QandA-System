import streamlit as st
import time
import uuid

from rag import rag
from db import (
    save_conversation,
    save_feedback,
    get_recent_conversations,
    get_feedback_stats,
)

def print_log(message):
    print(message, flush=True)

# Custom CSS to improve the app's appearance
st.markdown("""
<style>
    .main {
        background-color: #f0f2f6;
        padding: 2rem;
        border-radius: 10px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
    }
    .feedback-button {
        font-size: 24px;
        padding: 10px;
    }
    .conversation {
        background-color: white;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    .stats-container {
        display: flex;
        justify-content: space-around;
        margin-top: 1rem;
    }
    .stat-box {
        background-color: #e1e8f0;
        padding: 1rem;
        border-radius: 5px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

def main():
    print_log("Starting the Health Assistant application")
    st.title("🏥 Health Assistant")

    # Session state initialization
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""
    if "answer_generated" not in st.session_state:
        st.session_state.answer_generated = False

    # User input
    user_input = st.text_input("What's your health question?", 
                               value=st.session_state.user_input,
                               key="user_input_widget",
                               placeholder="e.g., What are the symptoms of flu?")

    if st.button("Ask", key="ask_button"):
        if user_input:
            st.session_state.user_input = user_input  # Store the input
            st.session_state.answer_generated = True
            st.rerun()

    if st.session_state.answer_generated:
        print_log(f"User asked: '{st.session_state.user_input}'")
        with st.spinner("Thinking... 🤔"):
            print_log("Getting answer from assistant...")
            start_time = time.time()
            answer_data = rag(st.session_state.user_input)
            end_time = time.time()
            print_log(f"Answer received in {end_time - start_time:.2f} seconds")
        
        st.success("Here's what I found:")
        st.markdown(f"**Answer:** {answer_data['answer']}")

        # Display monitoring information in an expander
        with st.expander("See details"):
            st.info(f"Response time: {answer_data['response_time']:.2f} seconds")
            st.info(f"Relevance: {answer_data['relevance']}")
            st.info(f"Total tokens: {answer_data['total_tokens']}")
            if answer_data["openai_cost"] > 0:
                st.info(f"OpenAI cost: ${answer_data['openai_cost']:.4f}")

        # Generate a new conversation ID for this Q&A pair
        conversation_id = str(uuid.uuid4())
        print_log(f"Generated new conversation ID: {conversation_id}")

        # Save conversation to database
        print_log("Saving conversation to database")
        save_conversation(conversation_id, st.session_state.user_input, answer_data)
        print_log(f"Conversation saved successfully with ID: {conversation_id}")

        # Feedback buttons
        st.write("Was this answer helpful?")
        col1, col2 = st.columns(2)

        feedback_placeholder = st.empty()  # Create a placeholder for the success message
        
        with col1:
            if st.button("👍 Yes", key="positive_feedback", help="This answer was helpful"):
                print_log(f"Positive feedback button clicked for conversation ID: {conversation_id}")
                save_feedback(conversation_id, 1)
                feedback_placeholder.success("Thank you for your feedback!")
                time.sleep(3)
                st.session_state.feedback_given = True  

        with col2:
            if st.button("👎 No", key="negative_feedback", help="This answer was not helpful"):
                print_log(f"Negative feedback button clicked for conversation ID: {conversation_id}")
                save_feedback(conversation_id, -1)
                feedback_placeholder.success("Thank you for your feedback!")
                time.sleep(3)
                st.session_state.feedback_given = True

        if st.session_state.get("feedback_given", False):
            st.session_state.answer_generated = False
            st.session_state.user_input = ""

    # Display recent conversations
    st.subheader("📚 Recent Conversations")
    relevance_filter = st.selectbox(
        "Filter by relevance:", ["All", "RELEVANT", "PARTLY_RELEVANT", "NON_RELEVANT"])
    
    recent_conversations = get_recent_conversations(
        limit=5, relevance=relevance_filter if relevance_filter != "All" else None
    )
    for conv in recent_conversations:
        with st.container():
            st.markdown(f"**Q:** {conv['question']}")
            st.markdown(f"**A:** {conv['answer']}")
            st.caption(f"Relevance: {conv['relevance']}")
            st.markdown("---")

    # Display feedback stats
    st.subheader("📊 Feedback Statistics")
    feedback_stats = get_feedback_stats()
    col1, col2 = st.columns(2)
    with col1:
        st.metric("👍 Thumbs Up", feedback_stats['thumbs_up'])
    with col2:
        st.metric("👎 Thumbs Down", feedback_stats['thumbs_down'])

    print_log("Streamlit app loop completed")

if __name__ == "__main__":
    print_log("Health Assistant application started")
    main()