import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('my_data.csv', encoding='latin1')

st.title("Professor Search App")

# Country filter
if st.checkbox("Do you want to select the country?"):
    countries = st.multiselect("Select countries:", sorted(df["Country"].dropna().unique()))
    if countries:
        df = df[df["Country"].isin(countries)]

# Institution filter
if st.checkbox("Do you want to select the Institution?"):
    institutions = st.multiselect("Select institutions:", sorted(df["Institution"].dropna().unique()))
    if institutions:
        df = df[df["Institution"].isin(institutions)]

# World Rank filter
if st.checkbox("Do you want to select the World Rank range?"):
    df["World Rank"] = pd.to_numeric(df["World Rank"], errors="coerce")
    min_rank, max_rank = st.slider("Select World Rank range:", 1, 1000, (1, 100))
    df = df[(df["World Rank"] >= min_rank) & (df["World Rank"] <= max_rank)]

# Country Ranking filter
if st.checkbox("Do you want to select the Country Ranking range?"):
    df["Country Ranking"] = pd.to_numeric(df["Country Ranking"], errors="coerce")
    min_c_rank, max_c_rank = st.slider("Select Country Ranking range:", 1, 1000, (1, 100))
    df = df[(df["Country Ranking"] >= min_c_rank) & (df["Country Ranking"] <= max_c_rank)]

# Display top professors
count = st.number_input("How many professors can be displayed at most?", min_value=1, max_value=100, value=10)
st.write(df["name"].head(count))

# Select specific professors
selected_professors = st.multiselect("Select specific professor(s) to view:", df["name"].dropna().unique())
if selected_professors:
    df = df[df["name"].isin(selected_professors)]

# Select specific attributes
if st.checkbox("Do you want to see specific attributes of the professors?"):
    cols = list(df.columns)
    chosen_cols = st.multiselect("Select attributes:", cols)
    st.dataframe(df[chosen_cols].head(count))
else:
    st.dataframe(df.head(count))

# Summary statistics
if st.checkbox("Do you want to see summary statistics of the numeric columns?"):
    numeric_cols = df.select_dtypes(include="number").columns
    for col in numeric_cols:
        mean_val = df[col].mean()
        max_val = df[col].max()
        min_val = df[col].min()
        st.write(f"{col}: mean={mean_val:.2f}, min={min_val}, max={max_val}")

# Save filtered results
if st.checkbox("Do you want to save the filtered results?"):
    file_type = st.selectbox("Enter file type:", ["csv", "excel"])
    if file_type == "csv":
        df.to_csv("filtered_results.csv", index=False)
        st.success("Results saved as filtered_results.csv")
    elif file_type == "excel":
        df.to_excel("filtered_results.xlsx", index=False)
        st.success("Results saved as filtered_results.xlsx")

# Histogram
if st.checkbox("Do you want to see a histogram of a numeric column?"):
    numeric_cols = df.select_dtypes(include="number").columns
    col_chart = st.selectbox("Which column do you want to plot?", numeric_cols)
    fig, ax = plt.subplots()
    df[col_chart].dropna().head(20).plot(kind="hist", edgecolor="black", ax=ax)
    ax.set_title(f"Distribution of {col_chart}")
    ax.set_xlabel(col_chart)
    ax.set_ylabel("Frequency")
    st.pyplot(fig)