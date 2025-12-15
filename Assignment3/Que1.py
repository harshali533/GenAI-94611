import streamlit as st
import pandas as pd
import pandasql as ps

st.title("CSV SQL Query Executor")

# Upload CSV
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("CSV Data Preview")
    st.dataframe(df)

    st.subheader("Enter SQL Query")
    st.write("Use table name as: data")

    query = st.text_area(
        "SQL Query",
        "SELECT * FROM data"
    )

    if st.button("Run Query"):
        result = ps.sqldf(query, {"data": df})

        st.subheader("Query Result")
        st.dataframe(result)
