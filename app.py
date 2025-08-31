import streamlit as st
from langchain_openai import ChatOpenAI
import sqlalchemy

DEMO_MODE = True
OPENAI_MODEL = "gpt-4o-mini"
DB_URI = "mysql+pymysql://root:password@localhost/mydb"

llm = ChatOpenAI(model=OPENAI_MODEL, temperature=0)

engine = None
conn = None
if not DEMO_MODE:
    engine = sqlalchemy.create_engine(DB_URI, pool_pre_ping=True)
    conn = engine.connect()

def demo_rows_for(sql: str):
    lower = sql.lower()
    if "students" in lower and "select" in lower:
        return [{"id": 1, "name": "Alice", "age": 20}, {"id": 2, "name": "Bob", "age": 22}]
    return [{"demo": "This is demo data. Connect a DB to see real results."}]

st.title("💡 Text → SQL Executor")
st.caption("Type instructions in plain English. Demo mode enabled." if DEMO_MODE else "Connected to MySQL.")

text = st.text_area("Your request:", "show all students")

if st.button("Run"):
    prompt = f"""
    Convert the following request into a valid MySQL SQL statement.
    Return ONLY the SQL, no explanations.

    Request: {text}
    """
    sql_code = llm.predict(prompt).strip()
    st.code(sql_code, language="sql")

    if DEMO_MODE:
        if sql_code.lower().startswith("select"):
            rows = demo_rows_for(sql_code)
            st.json(rows)
        else:
            st.success("✅ DEMO mode: would execute this SQL against MySQL.")
    else:
        try:
            result = conn.execute(sqlalchemy.text(sql_code))
            if sql_code.lower().startswith("select"):
                rows = [dict(row) for row in result.mappings().all()]
                st.json(rows)
            else:
                conn.commit()
                st.success("✅ Executed successfully")
        except Exception as e:
            st.error(f"❌ Error: {e}")