import streamlit as st


class TheHomePage:
    def __init__(self) -> None:
        # TODO: Define page-specific variables here
        pass

    def display(self):
        # TODO: define the streamlit view here
        st.header("Predicting Heart Desease")
        
        st.header("We are looking for correlations in the data that may lead to heart diease")
        
        BMI = st.number_input('Insert your BMI')
        
       option = st.selectbox(
     'How would you like to be contacted?',
     ( 'Yes', 'No'))
    
    option1 = st.selectbox(
     'Do you have Heart Disease',
     ( 'Yes', 'No'))




        
        


        
        
        
