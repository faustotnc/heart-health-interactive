import streamlit as st
from Pages import Home, TheData, TheModel
from pycaret.classification import *


# @st.cache
def load_trained_model():
    load_config("./Data/model_config")
    return load_model("./Data/final_model")["trained_model"]


# @st.cache
def load_the_data():
    return pd.read_csv("./Data/heart_2020.csv")


# Load the data
DATA = load_the_data()

# Load the model
MODEL = load_trained_model()

THE_HOME_PAGE = Home.TheHomePage(DATA, MODEL)
THE_DATA_PAGE = TheData.TheDataPage()
THE_MODEL_PAGE = TheModel.TheModelPage(DATA, MODEL)

st.title("Heart Health Interactive")
st.write("---")

# The side bar
with st.sidebar:
    st.markdown('''
        <div style='margin-bottom:24px;text-align:center;'>
            <span style='font-size:96px;'>🫀</span>
            <h1>Heart Health Interactive</h1>
        </div>
    ''', unsafe_allow_html=True)

    st.header("Main Menu")
    option = st.selectbox("Select a Page", ("Home", "The Data", "The Model"))

    st.write("---")
    st.header("Project Overview")
    st.markdown('''
        Heart disease is one of the leading causes of death for people in the U.S., which is why it is
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
