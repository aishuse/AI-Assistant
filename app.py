import streamlit as st
from core import chatbot
from langchain_core.messages import HumanMessage


st.set_page_config(page_title="Aiswarya’s AI Assistant", page_icon="🤖", layout="wide")
# Custom CSS for wider layout and better styling
st.markdown("""
    <style>
        .main {
            max-width: 1000px;
            margin: 0 auto;
            padding: 0rem;
        }
        .title {
            font-size: 34px;
            font-weight: bold;
            text-align: center;
            color: #FF4B4B;
        }
        .subtitle {
            font-size: 20px;
            text-align: center;
            color: #bbbbbb;
        }

    </style>
""", unsafe_allow_html=True)


st.markdown('<div class="title">Aiswarya’s AI Assistant 🤖</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Ask anything about Aiswarya Baby’s profile, skills, projects, or experience</div>', unsafe_allow_html=True)
st.markdown("---")
# st.session_state -> dict -> 
CONFIG = {'configurable': {'thread_id': 'thread-1'}}

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

# loading the conversation history
for msg in st.session_state['message_history']:
    with st.chat_message(msg['role']):
        st.text(msg['content'])

user_input = st.chat_input('Type here')

if user_input:

    # first add the message to message_history
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    # response = chatbot.invoke({'messages': [HumanMessage(content=user_input)]}, config=CONFIG)
    
    # ai_message = response['messages'][-1].content
    # # first add the message to message_history
    # st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
    # with st.chat_message('assistant'):
    #     st.text(ai_message)

    # Streaming

    with st.chat_message('assistant'):

        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config= {'configurable': {'thread_id': 'thread-1'}},
                stream_mode= 'messages'
            )
        )

    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})