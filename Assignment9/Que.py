import streamlit as st
import pandas as pd
from pandasql import sqldf
import os
import time
import tempfile

from langchain.chat_models import init_chat_model

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

llm = init_chat_model(
   model="google/gemma-3-4b",
    model_provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="not-needed"
)

st.set_page_config(page_title="Multi-Agent Intelligent App", layout="wide")
st.title("🤖 Multi-Agent Intelligent Application")

# SESSION STATE
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "web_df" not in st.session_state:
    st.session_state.web_df = None

st.sidebar.title("💬 Chat History")

if not st.session_state.chat_history:
    st.sidebar.info("No questions asked yet")
else:
    for agent, question in st.session_state.chat_history:
        st.sidebar.markdown(f"**{agent}:** {question}")
        st.sidebar.markdown("---")

# AGENT 1: CSV QUESTION ANSWERING AGENT
st.header("📄 CSV Question Answering Agent")

csv_file = st.file_uploader("Upload CSV File", type=["csv"])

if csv_file:
    df = pd.read_csv(csv_file)

    st.subheader("CSV Schema")
    st.write(df.dtypes)

    csv_question = st.text_input("Ask a question about the CSV data")

    if st.button("Ask CSV Agent") and csv_question.strip() != "":
        st.session_state.chat_history.append(("CSV Agent", csv_question))

        llm_prompt = f"""
        You are an SQL expert.

        Table name: data
        Columns:
        {df.dtypes}

        User Question:
        {csv_question}

        Rules:
        - Generate a valid SQLite SQL query
        - Use table name as data
        - Output ONLY the SQL query
        """

        sql_query = llm.invoke(llm_prompt).content.strip()
        sql_query = sql_query.replace("```sql", "").replace("```", "")

        st.subheader("Generated SQL Query")
        st.code(sql_query, language="sql")

        try:
            result = sqldf(sql_query, {"data": df})

            st.subheader("Query Result")
            st.dataframe(result)

            explanation = llm.invoke(
                f"""
                Explain the result in simple English.

                Question: {csv_question}
                Result:
                {result.head().to_string()}
                """
            ).content

            st.success(explanation)

        except Exception as e:
            st.error(f"SQL Execution Error: {e}")

# AGENT 2: SUNBEAM WEB SCRAPING AGENT
st.header("🌐 Web Scraping Agent (Sunbeam Internship Data)")

if st.button("Scrape Sunbeam Internship Data"):
    temp_dir = tempfile.mkdtemp()

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"--user-data-dir={temp_dir}")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    try:
        driver.get("https://www.sunbeaminfo.in/internship")
        time.sleep(3)

        rows = driver.find_elements(By.XPATH, "//table//tr[td]")
        scraped_data = []

        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) >= 3:
                scraped_data.append({
                    "Batch Name": cols[1].text.strip(),
                    "Start Date": cols[2].text.strip()
                })

        st.session_state.web_df = pd.DataFrame(scraped_data)

    finally:
        driver.quit()

# WEB DATA QUESTION ANSWERING AGENT
if st.session_state.web_df is not None:
    st.subheader("Scraped Internship Data")
    st.dataframe(st.session_state.web_df)

    web_question = st.text_input("Ask a question about Sunbeam internships")

    if st.button("Ask Web Agent") and web_question.strip() != "":
        st.session_state.chat_history.append(
            ("Web Scraping Agent", web_question)
        )

        answer = llm.invoke(
            f"""
            Data:
            {st.session_state.web_df}

            Question:
            {web_question}

            Explain the answer in simple English.
            """
        ).content

        st.success(answer)