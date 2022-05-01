import streamlit as st
from pycaret.classification import *
import pandas as pd


class TheHomePage:
    def __init__(self, data: pd.DataFrame, model) -> None:
        self.data = data
        self.model = model

    def display(self):
        # TODO: define the streamlit view here
        st.header("Predicting Heart Desease")

        st.write(
            "Please fill out the information below to find out if you are at risk for hearth disease."
        )

        st.write("---")

        col1, col2, col3 = st.columns([1, 1, 1])

        # Row #1
        weight = col1.number_input('Insert your weight (lb)')
        height = col2.number_input('Insert your height (in)')
        Smoking = col3.selectbox(
            'Do you smoke?', self.data["Smoking"].unique())

        # Row #2
        AlcoholDrinking = col1.selectbox(
            'Do you drink alcohol?', self.data["AlcoholDrinking"].unique())
        Stroke = col2.selectbox(
            'Have you ever had a stroke?', self.data["Stroke"].unique())
        PhysicalHealth = col3.slider(
            'Rate your physical health:', int(self.data["PhysicalHealth"].min()), int(self.data["PhysicalHealth"].max()))

        # Row #3
        MentalHealth = col1.slider(
            'Rate your mental health:', int(self.data["MentalHealth"].min()), int(self.data["MentalHealth"].max()))
        DiffWalking = col2.selectbox(
            'Do you have difficulty walking?', self.data["DiffWalking"].unique())
        Sex = col3.selectbox('What is your sex?', ('Male', 'Female'))

        # Row #4
        AgeCategory = col1.selectbox(
            'What is your age range?', sorted(self.data["AgeCategory"].unique()))
        Race = col2.selectbox(
            'Please spcify your race?', sorted(self.data["Race"].unique()))
        Diabetic = col3.selectbox(
            'Do you suffer from diabetes?', sorted(self.data["Diabetic"].unique()))

        # Row #5
        PhysicalActivity = col1.selectbox(
            'Have you done physical activity in the past 30 days', self.data["PhysicalActivity"].unique())
        GenHealth = col2.selectbox(
            'Would you say that your physical health is very good, good or other', self.data["GenHealth"].unique())
        SleepTime = col3.slider(
            'On average how many hours do you sleep in a 24 hour period', int(self.data["SleepTime"].min()), int(self.data["SleepTime"].max()))

        # Row #6
        Asthma = col1.selectbox(
            'Have you ever been told you have Asthma', self.data["Asthma"].unique())
        KidneyDisease = col2.selectbox(
            'Have you ever been told you have Kidney Diease', self.data["KidneyDisease"].unique())
        SkinCancer = col3.selectbox(
            'Have you ever been told you have Skin Cancer', self.data["SkinCancer"].unique())

        # Prepare the model's input data
        input_data = pd.DataFrame({
            "BMI": (weight/(height)**2) * 703,  # TODO: Compute BMI from weight and height
            "Smoking": "Yes",

            "AlcoholDrinking": AlcoholDrinking,
            "Stroke": Stroke,
            "PhysicalHealth": PhysicalHealth,

            "MentalHealth": MentalHealth,
            "DiffWalking": DiffWalking,
            "Sex": Sex,

            "AgeCategory": AgeCategory,
            "Race": Race,
            "Diabetic": Diabetic,

            "PhysicalActivity": PhysicalActivity,
            "GenHealth": GenHealth,
            "SleepTime": SleepTime,

            "Asthma": Asthma,
            "KidneyDisease": KidneyDisease,
            "SkinCancer": SkinCancer
        }, index=[0])

        # Transform the input to one-hot encode categorical variables
        prep_pipe = get_config('prep_pipe')
        transformed_input_data = prep_pipe.transform(input_data)

        # Make a Prediction
        prediction = self.model.predict_proba(transformed_input_data)[0][1]

        # Display the diagnosis
        st.write("---")
        diagnosis = "At Risk 🚑" if prediction >= 0.4 else "Not at Risk ✅"
        st.header(f"Diagnosis: {diagnosis}")
        st.subheader(
            f"You have a {round(prediction * 100, 2)}% change of developing heart disease.")
