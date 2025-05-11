import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from azure.identity import ClientSecretCredential
from openai import AzureOpenAI
from utils import format_bitcoin_prompt

load_dotenv()

credential = ClientSecretCredential(
    tenant_id=os.getenv("tenant_id"),
    client_id=os.getenv("client_id"),
    client_secret=os.getenv("client_secret")
)
token = credential.get_token(os.getenv("scope")).token

client = AzureOpenAI(
    api_version=os.getenv("api_version"),
    azure_endpoint=os.getenv("azure_endpoint"),
    api_key=token,
    default_headers={
        "projectId": os.getenv("project_id"),
        "x-idp": "azuread"
    }
)

def load_bitcoin_data(path="bitcoin_history.csv") -> pd.DataFrame:
    return pd.read_csv(path, parse_dates=["Date"])

st.set_page_config("Bitcoin Price Forecast with Azure GPT", layout="wide")
st.title("₿ Bitcoin Price")

bitcoin_df = load_bitcoin_data()
st.subheader("📊 Bitcoin Monthly Price History")
st.dataframe(bitcoin_df)

question = st.text_area("Enter your question:", "What is the expected Bitcoin price trend for the next 3 months?")
if st.button("Generate Forecast"):
    with st.spinner("Analyzing Bitcoin price patterns..."):
        prompt = format_bitcoin_prompt(bitcoin_df, question)
        response = client.chat.completions.create(
            model=os.getenv("generation_model"),
            messages=[
                {"role": "system", "content": "You are a cryptocurrency analyst specializing in Bitcoin price movements."},
                {"role": "user", "content": prompt}
            ]
        )
        st.subheader("🧠 Price Prediction")
        st.markdown(response.choices[0].message.content)