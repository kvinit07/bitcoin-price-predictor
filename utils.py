import pandas as pd

def format_bitcoin_prompt(df: pd.DataFrame, question: str) -> str:
    context = df.to_string(index=False)
    return f"""You are a cryptocurrency analyst specializing in Bitcoin price analysis.

Here is the monthly Bitcoin price data:

{context}

{question}"""