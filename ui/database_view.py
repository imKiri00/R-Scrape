import streamlit as st
import pandas as pd
from sqlalchemy.ext.asyncio import create_async_engine
import asyncio
from sqlalchemy import text

async def get_table_data(engine):
    async with engine.connect() as conn:
        query = text("SELECT * FROM reddit_posts LIMIT 100")
        result = await conn.execute(query)
        data = result.fetchall()
        columns = result.keys()
    return pd.DataFrame(data, columns=columns)

def show():
    st.header("Database View")
    
    # Use the provided DATABASE_URL
    database_url = "postgresql+asyncpg://kiri:1234@localhost/reddit_scraper"
    
    try:
        engine = create_async_engine(database_url)
        st.success("Connected to the database successfully!")
        
        df = asyncio.run(get_table_data(engine))
        st.write(f"Showing first 100 rows from reddit_posts table")
        st.dataframe(df)
        
        # Download as CSV
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name="reddit_posts.csv",
            mime="text/csv",
        )
    except Exception as e:
        st.error(f"Error connecting to the database: {str(e)}")