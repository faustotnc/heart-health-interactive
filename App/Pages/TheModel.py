from matplotlib.pyplot import title
from pycaret.classification import get_config
import streamlit as st
import altair as alt
import pandas as pd
from sklearn.metrics import precision_recall_fscore_support
import numpy as np
from lightgbm import LGBMClassifier

from helpers import add_space


@st.cache
def redo_lightbm_model():
    prefinal_model = LGBMClassifier(n_jobs=-1, random_state=123)
    prefinal_model.fit(get_config("X_train"), get_config("y_train"))
    prefinal_model_binary_pred = prefinal_model.predict(get_config("X_test"))
    prefinal_model_prob_pred = prefinal_model.predict_proba(
        get_config("X_test"))
    return (prefinal_model, prefinal_model_binary_pred, prefinal_model_prob_pred)


class TheModelPage:
    def __init__(self, data, model) -> None:
        self.data = data
        self.model = model

        m, bp, pp = redo_lightbm_model()
        self.pre_final_model = m
        self.prefinal_binary_pred = bp
        self.prefinal_prob_pred = pp

    def display(self):
        st.header("About the Model")

        st.write("""
            As part of this project, we also wanted to create a predictive model that would be able to
            predict heart disease in the general population based on key indicators of their health like
            age, BMI, general physical health, and wether or not they smoke or drink.
        """)

        st.write("""
            To accomplish this task, we used the publicly available data titled "Personal Key Indicators
            of Heart Disease" and can be found at https://www.kaggle.com/datasets/kamilpytlak/personal-key-indicators-of-heart-disease.
            We then used PyCaret to find the best machine learning model for this type of problem. After
            some experimentation, we found that a Light Gradient Boosting Machine (lightgbm) model
            performed the best.
        """)

        st.subheader("Model Performance Metrics:")
        c1, c2, c3, c4 = st.columns([1, 1, 1, 1])
        c1.metric("Accuracy", 0.9145, delta=None, delta_color="normal")
        c2.metric("Precision", 0.9361, delta=None, delta_color="normal")
        c3.metric("Recall", 0.8896, delta=None, delta_color="normal")
        c4.metric("F1-Score", 0.9123, delta=None, delta_color="normal")
        st.write("---")

        add_space(24)
        st.subheader("The Confusion Matrix")
        st.write("""
            The following chart is a confusion matrix, which shows the performance model when making
            predictions on the testing set. This confusion matrix was also used to compute the accuracy,
            precision, recall, and F1-score metrics shown above.
        """)
        add_space(24)

        c1, _ = st.columns([1, 0.025])
        c1.altair_chart(self.add_confusion_matrix_chart(),
                        use_container_width=True)

        add_space(24)
        st.subheader("The Report of Scores for Each Class")
        st.write("""
            The following chart is a report of the scores for each one of the prediction classes. This
            gives us an idea of the relative performance of the model compared to each class in the
            prediction set. Notice that the scores related to the "Yes" class are the same as the metrics
            reported above.
        """)
        add_space(24)

        c1, _ = st.columns([1, 0.025])
        c1.altair_chart(self.add_class_report_chart(),
                        use_container_width=True)

        add_space(24)
        st.subheader("The Report of Scores for Each Class")
        st.write("""
            One of the advantages of using an ensemble model is that data analysts can easily access
            the importance or "rank" of the features used to train the model. The following chart shows
            the relative rank of the top-10 most important features found in the dataset. While physical
            and mental health were among the three most important features when it comes to determining
            a person's risk of heath disease, the amount of time they sleep turned out to be 37% more
            important.
        """)
        add_space(24)

        c1, _ = st.columns([1, 0.025])
        c1.altair_chart(self.add_feature_importance(),
                        use_container_width=True)

    def add_confusion_matrix_chart(self):
        # Convert this grid to columnar data expected by Altair
        conf_source = pd.DataFrame({
            'predicted': ["YES", "YES", "NO", "NO"],
            'actual': ["YES", "NO", "YES", "NO"],
            'value': [78104, 5479, 9694, 82177]
        })

        conf_base = alt.Chart(conf_source).properties(
            height=500,
            title="Confusion matrix"
        ).encode(
            alt.X('predicted:O', sort=None),
            alt.Y('actual:O', sort=None),
        )

        conf = conf_base.mark_rect().encode(
            x=alt.X('predicted:O', title="Predicted", sort=None),
            y=alt.Y('actual:O', title="Actual", sort=None),
            color=alt.Color(
                'value:Q',
                scale=alt.Scale(scheme="greens"),
                legend=alt.Legend(
                    title="",
                    labelFontSize=24,
                )
            )
        )

        text = conf_base.mark_text(fontSize=24).encode(
            text='value',
            color=alt.condition(
                alt.datum.value > 10000,
                alt.value('white'),
                alt.value('black')
            ),
        )

        return alt.layer(conf, text).configure_view(
            stroke='transparent'
        ).configure_axis(
            labelFontSize=24,
            titleFontSize=24,
        ).configure_axisX(
            labelAngle=0,
        ).configure_title(
            fontSize=24,
        )

    def add_class_report_chart(self):
        # Convert this grid to columnar data expected by Altair
        scores = precision_recall_fscore_support(
            get_config("y_test"), self.prefinal_binary_pred)

        class_report_source = pd.DataFrame({
            'x': ["Precision", "Precision", "Recall", "Recall", "F1", "F1"],
            'y': ["No", "Yes", "No", "Yes", "No", "Yes"],
            'score': np.around(scores, decimals=3, out=None)[:3].ravel()
        })

        class_rep_base = alt.Chart(class_report_source).properties(
            height=360,
            title="Class Scores Report"
        ).encode(
            alt.X('x:O'),
            alt.Y('y:O'),
        )

        class_rep = class_rep_base.mark_rect().encode(
            x=alt.X('x:O', title="", sort=None),
            y=alt.Y('y:O', title="",),
            color=alt.Color(
                'score',
                scale=alt.Scale(scheme="browns"),
                legend=alt.Legend(
                    title="",
                    labelFontSize=32
                )
            )
        )

        class_rep_text = class_rep.mark_text(
            fontSize=24,
        ).encode(
            text='score',
            color=alt.condition(
                alt.datum.score > 0.91,
                alt.value('white'),
                alt.value('black')
            ),
        )

        return alt.layer(class_rep, class_rep_text).configure_view(
            stroke='transparent'
        ).configure_axis(
            labelFontSize=24,
            titleFontSize=24,
        ).configure_axisX(
            labelAngle=0,
            labelFontSize=24,
        ).configure_title(
            fontSize=24,
        )

    def add_feature_importance(self):
        importances = pd.DataFrame({
            "feature": [
                "Sleep Time", "Physical Health", "Mental Health", "BMI", "Has Asthma",
                "Race: White", "Sex: Female", "Has Had Stroke", "Exceellent Gen. Health",
                "Age: 80 or Older"
            ],
            "importance": [625, 390, 370, 240, 110, 105, 80, 80, 60, 55],
        }).sort_values(
            by=['importance'],
            ascending=False
        )

        important_features = importances.iloc[:10]

        return alt.Chart(important_features).mark_bar().encode(
            x=alt.X('feature:O', title="", sort=None),
            y=alt.Y('importance:Q', title="Importance"),
            color=alt.Color(
                'importance:Q',
                scale=alt.Scale(scheme="greens"),
                legend=None
            ),
            tooltip=["importance:Q"]
        ).properties(
            height=600,
        ).configure_axis(
            labelFontSize=18,
            titleFontSize=24,
        ).configure_axisX(
            labelAngle=-45,
        ).configure_title(
            fontSize=24,
        )
