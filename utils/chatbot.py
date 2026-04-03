import os

from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def chat_with_data(user_message, data, data_type):

    if data_type == 'dataframe':
        data_str = data.head(50).to_string()
        columns = ', '.join(data.columns.tolist())
        context = f"""You are a helpful data analyst assistant.
You have been given a dataset with the following columns: {columns}
Here is a sample of the data (first 50 rows):
{data_str}
Total rows in dataset: {len(data)}"""

    elif data_type == 'text':
        context = f"""You are a helpful document analyst assistant.
You have been given the following document content:
{data[:2000]}"""

    else:
        context = "You are a helpful assistant."

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": user_message}
        ]
    )

    return response.choices[0].message.content