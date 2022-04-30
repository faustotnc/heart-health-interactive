import streamlit as st


def add_space(size, col=None):
    """
    Adds vertical space between two sections.
    """

    (col if col else st).markdown(
        body=f"<div style='margin-top: {size}px'></div>",
        unsafe_allow_html=True
    )
