import streamlit as st
import requests

from api_client import ask_backend


st.set_page_config(
    page_title="UniGuide AI"
)


st.title("UniGuide AI")

st.write(
    "Ask questions about university policies, regulations, "
    "academic procedures, and student support."
)


if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


question = st.chat_input(
    "Ask a question about university policies..."
)


if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)


    with st.chat_message("assistant"):

        with st.spinner(
            "Searching university documents and generating an answer..."
        ):

            try:

                data = ask_backend(question)

                answer = data.get(
                    "answer",
                    "No answer was returned."
                )

                sources = data.get(
                    "sources",
                    []
                )

                st.markdown(answer)


                if sources:

                    st.markdown("### Sources")

                    for source in sources:

                        st.markdown(
                            f"- {source}"
                        )


                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )


            except requests.exceptions.RequestException:

                st.error(
                    "Sorry, I couldn't connect to the UniGuide AI "
                    "backend. Please make sure the backend is running "
                    "on port 8000."
                )

            except Exception:

                st.error(
                    "Sorry, something went wrong while processing "
                    "your question. Please try again."
                )
