import streamlit as st
import altair as alt


class TheDataPage:
    def __init__(self, data) -> None:
        self.data = data
        pass

    def display(self):
        st.header("About the Data")
        st.write("Access the original dataset at: https://www.kaggle.com/datasets/kamilpytlak/personal-key-indicators-of-heart-disease")

        st.write('''
            We used the publicly available dataset titled \"Personal Key Indicators of Heart Disease\"
            to accomplish our goal of building a predictive model for cardiovascular disease. The
            dataset was constructed from the CDC's annual survey of 400,000 adults to evaluate their
            health status and includes a collection of measurements of their general health.
        ''')

        st.write('''
            Even though there were no missing values in the dataset, we encountered a severe imbalance
            in the number of people that reported having heart disease vs. the ones that did not. As
            seen in the chart below, approximately 91% of respondents reported not having heart disease,
            while only 9% reported having heart disease.
        ''')

        self.add_heart_disease_distribution()

        st.write('''
            To overcome the imbalance of the dataset, we implemented a Synthetic Minority Oversampling
            Technique for Nominal and Continuous features (SMOTE-NC) on the data (see Figure 2), which
            created synthetic data points in the minority class based on 512 similar neighboring data
            points. After oversampling, the number of data points in the dataset increased from 319,795
            to 584,844 data points.
        ''')
        st.write("---")

        self.add_binary_charts()
        self.add_age_distribution_charts()
        self.add_distribution_charts()
        self.add_race_distribution_charts()

    def add_heart_disease_distribution(self):
        data = self.data["HeartDisease"].value_counts(
        ).to_frame().reset_index().sort_values("index")

        chart = alt.Chart(data).mark_bar().encode(
            x="index:O",
            y="HeartDisease:Q",
            color="index:O",
            tooltip=["HeartDisease:Q"],
        ).properties(
            height=400,
            title="Heart Disease Distribution"
        ).configure_axisX(
            labelAngle=0,
        )

        _, c1, _ = st.columns([0.25, 1, 0.25])
        c1.altair_chart(chart, use_container_width=True)

    def add_binary_charts(self):
        st.subheader("Binary Features")

        option = st.selectbox(
            'Select the following factors to see if they are potential causes of Heart Disease?',
            ('Stroke', 'Smoking', 'Sex', 'Smoking', 'AlcoholDrinking', 'Asthma', 'DiffWalking', 'PhysicalActivity', 'KidneyDisease', 'SkinCancer'))

        chart_data_1 = self.data[self.data['HeartDisease'] == 'Yes'][option].value_counts(
        ).to_frame().reset_index()

        chart1 = alt.Chart(chart_data_1).mark_bar().encode(
            y=f"{option}:Q",
            x="index:O",
            tooltip=[f"{option}:Q"],
            color="index:O"
        ).properties(
            title="Without Heart Disease"
        ).configure_axisX(
            labelAngle=0,
        )

        chart_data_2 = self.data[self.data['HeartDisease'] == 'No'][option].value_counts(
        ).to_frame().reset_index()

        chart2 = alt.Chart(chart_data_2).mark_bar().encode(
            y=f"{option}:Q",
            x="index:O",
            tooltip=[f"{option}:Q"],
            color="index:O"
        ).properties(
            title="Without Heart Disease"
        ).configure_axisX(
            labelAngle=0,
        )

        c1, c2 = st.columns(2)

        c1.altair_chart(chart1, use_container_width=True)
        c2.altair_chart(chart2, use_container_width=True)

    def add_age_distribution_charts(self):
        st.subheader("Age Distribution")

        data = self.data["AgeCategory"].value_counts(
        ).to_frame().reset_index().sort_values("index")

        chart = alt.Chart(data).mark_bar().encode(
            x="index:O",
            y="AgeCategory:Q",
            color="index:O"
        ).properties(
            height=400,
            title="Age Distribution"
        ).configure_axisX(
            labelAngle=0,
        )

        st.altair_chart(chart, use_container_width=True)

    def add_distribution_charts(self):
        st.subheader("BMI vs. Physical Health")

        chart = alt.Chart(self.data).mark_circle(size=60).encode(
            x="BMI",
            y="PhysicalHealth",
            color="HeartDisease"
        ).properties(
            height=400,
        ).configure_axisX(
            labelAngle=0,
        )

        st.altair_chart(chart, use_container_width=True)

    def add_race_distribution_charts(self):
        st.subheader("Race Distribution")

        data = self.data["Race"].value_counts(
        ).to_frame().reset_index().sort_values("index")

        data = data.replace("American Indian/Alaskan Native",
                            "Native American", regex=True)

        chart = alt.Chart(data).mark_bar().encode(
            x="index:O",
            y="Race:Q",
            color="index:O"
        ).properties(
            height=400,
            title="Race Distribution"
        ).configure_axisX(
            labelAngle=0,
        )

        st.altair_chart(chart, use_container_width=True)
