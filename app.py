import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import base64
import os

from PIL import Image
from dotenv import load_dotenv
from google import genai

# -----------------------------
# Load Environment Variables
# -----------------------------
load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# -----------------------------
# Background Image Function
# -----------------------------
def add_bg(image_file):

    image_path = image_file

    if not os.path.isabs(image_path):
        image_path = os.path.join(BASE_DIR, image_path)

    if not os.path.exists(image_path):
        st.warning(f"Background image not found: {image_path}")
        return

    with open(image_path, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image:
                linear-gradient(rgba(0,0,0,0.6),
                rgba(0,0,0,0.6)),
                url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Spotify Tracks Analysis",
    layout="wide"
)

add_bg(os.path.join("images", "background.png"))

st.title("🎵 Spotify Tracks Analysis")
st.subheader("Case Study on Spotify Tracks Dataset")

# -----------------------------
# File Upload
# -----------------------------
file = st.sidebar.file_uploader(
    "Upload Spotify Dataset",
    type=["csv", "xlsx"]
)

if file:

    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    st.sidebar.success("✅ File Uploaded Successfully!")

    # -----------------------------
    # Sidebar Menu
    # -----------------------------
    menu = st.sidebar.radio(
        "Navigate",
        [
            "Data Overview",
            "Statistics",
            "Visualization",
            "Filter Data",
            "AI Insights"
        ]
    )

    # -----------------------------
    # DATA OVERVIEW
    # -----------------------------
    if menu == "Data Overview":

        st.subheader("📁 Dataset Preview")

        st.write("Dataset Shape:", df.shape)

        st.dataframe(df)

    # -----------------------------
    # STATISTICS
    # -----------------------------
    elif menu == "Statistics":

        st.subheader("📈 Statistical Summary")

        st.write(df.describe())

    # -----------------------------
    # VISUALIZATION
    # -----------------------------
    elif menu == "Visualization":

        st.subheader("📊 Data Visualization")

        plot_type = st.selectbox(
            "Select Plot Type",
            [
                "Scatter Plot",
                "Bar Chart",
                "Correlation Heatmap",
                "Box Plot",
                "Histogram",
                "Count Plot"
            ]
        )

        # Scatter Plot
        if plot_type == "Scatter Plot":

            x_col = st.selectbox(
                "X-axis",
                df.select_dtypes(include="number").columns
            )

            y_col = st.selectbox(
                "Y-axis",
                df.select_dtypes(include="number").columns
            )

            hue_col = st.selectbox(
                "Color By (Optional)",
                [None] + list(df.columns)
            )

            fig, ax = plt.subplots()

            sns.scatterplot(
                data=df,
                x=x_col,
                y=y_col,
                hue=hue_col,
                ax=ax
            )

            st.pyplot(fig)

        # Bar Chart
        elif plot_type == "Bar Chart":

            col = st.selectbox(
                "Select Column",
                df.select_dtypes(include="object").columns
            )

            fig, ax = plt.subplots()

            df[col].value_counts().plot(
                kind="bar",
                ax=ax
            )

            st.pyplot(fig)

        # Correlation Heatmap
        elif plot_type == "Correlation Heatmap":

            fig, ax = plt.subplots(figsize=(12,6))

            sns.heatmap(
                df.select_dtypes(include="number").corr(),
                annot=True,
                cmap="coolwarm",
                ax=ax
            )

            st.pyplot(fig)

        # Box Plot
        elif plot_type == "Box Plot":

            num_col = st.selectbox(
                "Select Numeric Column",
                df.select_dtypes(include="number").columns
            )

            fig, ax = plt.subplots()

            sns.boxplot(
                y=df[num_col],
                ax=ax
            )

            st.pyplot(fig)

        # Histogram
        elif plot_type == "Histogram":

            num_col = st.selectbox(
                "Select Numeric Column",
                df.select_dtypes(include="number").columns
            )

            bins = st.slider(
                "Number of Bins",
                5,
                100,
                30
            )

            fig, ax = plt.subplots()

            sns.histplot(
                df[num_col],
                bins=bins,
                kde=True,
                ax=ax
            )

            st.pyplot(fig)

        # Count Plot
        elif plot_type == "Count Plot":

            cat_col = st.selectbox(
                "Select Categorical Column",
                df.select_dtypes(include="object").columns
            )

            fig, ax = plt.subplots()

            sns.countplot(
                y=cat_col,
                data=df,
                ax=ax
            )

            st.pyplot(fig)
                # -----------------------------
    # FILTER DATA
    # -----------------------------
    elif menu == "Filter Data":

        st.subheader("🔍 Filter the Dataset")

        selected_col = st.selectbox(
            "Select Numeric Column",
            df.select_dtypes(include="number").columns
        )

        min_val = float(df[selected_col].min())
        max_val = float(df[selected_col].max())

        user_range = st.slider(
            "Select Range",
            min_val,
            max_val,
            (min_val, max_val)
        )

        filtered_df = df[
            (df[selected_col] >= user_range[0]) &
            (df[selected_col] <= user_range[1])
        ]

        st.write("Filtered Dataset Shape:", filtered_df.shape)

        st.dataframe(filtered_df)

        csv = filtered_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="📥 Download Filtered Data",
            data=csv,
            file_name="filtered_spotify_tracks.csv",
            mime="text/csv"
        )

    # -----------------------------
    # AI INSIGHTS
    # -----------------------------
    elif menu == "AI Insights":

     st.markdown("""
# 🤖 AI Spotify Analyst

### Discover trends, patterns, and recommendations powered by Gemini AI.

Click the button below to generate an intelligent report.
""")

    st.info("💡 AI analyzes popularity, danceability, energy, and genres to provide actionable insights.")

    summary = f"""
Spotify Dataset Summary

Number of Songs: {len(df)}

Average Popularity: {df['popularity'].mean():.2f}

Average Danceability: {df['danceability'].mean():.2f}

Average Energy: {df['energy'].mean():.2f}

Most Common Genre: {df['track_genre'].mode()[0]}
"""

    st.subheader("📋 Dataset Summary")
    st.text(summary)

    if st.button("✨ Generate AI Insights", use_container_width=True):

        prompt = f"""
You are a music data analyst.

Explain this Spotify dataset in simple English.

Give:
- 5 insights
- 3 trends
- 1 conclusion

{summary}
"""

        with st.spinner("🧠 Gemini is analyzing your dataset..."):

            response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=prompt
            )

        st.success("✅ Analysis Complete!")

        st.balloons()

        st.markdown("## 📄 AI Report")

        st.write(response.text)