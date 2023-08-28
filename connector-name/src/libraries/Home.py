import streamlit as st

from connection import Connection

st.set_page_config(
    page_title="Connector Name",
    page_icon=":shark:",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None,
)

connection = Connection()

connection.debug("Home", "Opening app")

st.header("Connector name")

st.markdown(
    """
    This is the main page of the app. The first thing that the user will see. In
    case of a simple app, it could be the only page. For more complex stuff,
    check out in the Streamlit documentation extra stuff.

    Remember to check which version of Streamlit you are using in the
    requirements.txt file.
    """
)
