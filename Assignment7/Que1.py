import streamlit as st
import pandas as pd
import os
from langchain.chat_models import init_chat_model
from pandasql import sqldf

#Page config
st.set_page_config(page_title="CSV to SQL Generator", layout="centered")
st.title("CSV → SQL Analyzer")

#Initialize LLM
llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

#Helper: Clean SQL
def clean_sql(sql_text):
    return sql_text.replace("```sql", "").replace("```", "").strip()

#Upload CSV
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Show schema
    st.subheader("CSV Schema")
    st.write(df.dtypes)

    # User question
    st.subheader("Ask a Question")
    user_que = st.text_input("Example: Find employee with highest salary")

    if st.button("Generate & Execute SQL"):
        if user_que.strip() == "":
            st.warning("Please enter a question.")
        else:
            #Generate SQL
            sql_prompt = f"""
            Table Name: data
            Table Schema:
            {df.dtypes}

            Question:
            {user_que}

            Instruction:
            - Write an SQLite query only
            - Output ONLY raw SQL
            - No markdown
            - No explanation
            - If not possible, output 'Error'
            """

            with st.spinner("Generating SQL..."):
                sql_result = llm.invoke(sql_prompt)

            sql_query = clean_sql(sql_result.content)

            st.subheader("Generated SQL")
            st.code(sql_query, language="sql")

            #Execute SQL
            if sql_query.lower() != "error":
                pysqldf = lambda q: sqldf(q, {"data": df})
                result_df = pysqldf(sql_query)

                st.subheader("Query Result")
                st.dataframe(result_df)

                #Explain Result
                explain_prompt = f"""
                User Question:
                {user_que}

                SQL Query:
                {sql_query}

                Result:
                {result_df.head().to_string()}

                Instruction:
                Explain the result in simple English for a beginner.
                """

                with st.spinner("Explaining result..."):
                    explanation = llm.invoke(explain_prompt)

                st.subheader("Explanation (Simple English)")
                st.write(explanation.content)
            else:
                st.error("LLM could not generate a valid SQL query.")
