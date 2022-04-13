import streamlit as st
from Pages import Home, TheData, TheModel

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
