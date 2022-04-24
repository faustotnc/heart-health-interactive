import streamlit as st
import s3fs
import os

from Pages import Home, TheData, TheModel

# create connection object
# `anon=False` means not anonymous, it uses access keys to pull data
fs = s3fs.S3FileSystem(anon=False)
# retrieve file contents.
# uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def read_file(filename):
    with fs.open(filename) as f:
        return f.read().decode("utf-8")

THE_HOME_PAGE = Home.TheHomePage()
THE_DATA_PAGE = TheData.TheDataPage()
THE_MODEL_PAGE = TheModel.TheModelPage()

st.title("Heart Health Interactive")
st.write("---")

# The side bar
with st.sidebar:
    st.header("Main Menu")
    option = st.selectbox("Select a Page", ("Home", "The Data", "The Model"))

    st.write("---")
    st.header("Project Overview")
    st.markdown('''
        Heart disease is one of theleading causes of death for people in the U.S., which is why it is
        important to find potential causes and indicators that can help us detect and / or prevent
        heart-related issues. Our project attempts to help the general population find key indicators
        of heart disease in their personal life.
    ''')

# Display the correct page based on user selection
if option == "Home":
    THE_HOME_PAGE.display()
elif option == "The Data":
    THE_DATA_PAGE.display()
else:
    THE_MODEL_PAGE.display()
