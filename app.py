import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import base64
from PIL import Image

def add_bg(image_file):
    with open(image_file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()


    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image:
                linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)),
                url("data:image/jpeg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

st.set_page_config(page_title="Spotify Tracks Analysis", layout="wide")

add_bg("images/background.jpg")

st.title("Spotify Tracks Analysis")
st.title("Case study on Spotify Tracks")

# File uploader
file = st.sidebar.file_uploader("Upload your file", type=['csv', 'xlsx'])

if file:
    if file.name.endswith('.csv'):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    st.sidebar.success("File uploaded successfully!")


    # Sidebar navigation
    menu = st.sidebar.radio("Navigate", ["Data Overview", "Statistics", "Visualization", "Filter Data"])

    if menu == "Data Overview":
        st.subheader("📁 Dataset Preview")
        st.write("Shape of the dataset:", df.shape)
        st.dataframe(df)

    elif menu == "Statistics":
        st.subheader("📈 Statistical Summary")
        st.write(df.describe())

    elif menu == "Visualization":
        st.subheader("📊 Data Visualization")
        plot_type = st.selectbox("Select Plot Type", ["Scatter Plot", "Bar Chart", "Correlation Heatmap", "Box Plot", "Histogram", "Count Plot"])

        if plot_type == "Scatter Plot":
            x_col = st.selectbox("X-axis", df.select_dtypes(include='number').columns)
            y_col = st.selectbox("Y-axis", df.select_dtypes(include='number').columns)
            hue_col = st.selectbox("Color by (Optional)", [None] + list(df.columns))
            fig, ax = plt.subplots()
            sns.scatterplot(data=df, x=x_col, y=y_col, hue=hue_col if hue_col != "None" else None, ax=ax)
            st.pyplot(fig)

        elif plot_type == "Bar Chart":
            col = st.selectbox("Select Column for Bar Chart", df.select_dtypes(include='object').columns)
            fig, ax = plt.subplots()
            df[col].value_counts().plot(kind='bar', ax=ax)
            st.pyplot(fig)

        elif plot_type == "Correlation Heatmap":
            fig, ax = plt.subplots(figsize=(12, 6))
            sns.heatmap(df.select_dtypes(include='number').corr(), annot=True, cmap='coolwarm', ax=ax)
            st.pyplot(fig)

        elif plot_type == "Box Plot":
            num_col = st.selectbox("Select Column for Box Plot", df.select_dtypes(include='number').columns)
            fig, ax = plt.subplots()
            sns.boxplot(y=df[num_col], ax=ax)
            st.pyplot(fig)

        elif plot_type == "Histogram":
            num_col = st.selectbox("Select Column for Histogram", df.select_dtypes(include='number').columns)
            bins = st.slider("Number of Bins", min_value=5, max_value=100, value=30)
            fig, ax = plt.subplots()
            sns.histplot(df[num_col], bins=bins, kde=True, ax=ax)
            st.pyplot(fig)

        elif plot_type == "Count Plot":
            cat_col = st.selectbox("Select Column for Count Plot", df.select_dtypes(include='object').columns)
            fig, ax = plt.subplots()
            sns.countplot(y=cat_col, data=df, ax=ax)
            st.pyplot(fig)

    elif menu == "Filter Data":
        st.subheader(" Filter the Dataset")
        selected_col = st.selectbox("Select numeric column to filter", df.select_dtypes(include='number').columns)
        min_val = float(df[selected_col].min())
        max_val = float(df[selected_col].max())
        user_range = st.slider("Select range", min_val, max_val, (min_val, max_val))
        filtered_df = df[(df[selected_col] >= user_range[0]) & (df[selected_col] <= user_range[1])]
        st.write("Filtered data shape:", filtered_df.shape)
        st.dataframe(filtered_df)

        # Option to download filtered data
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Filtered Data", data=csv, file_name="filtered_spotify_tracks.csv", mime="text/csv")

else:
    st.warning("Please upload a Spotify tracks dataset to begin.")

st.sidebar.caption("Built with  using Streamlit")
