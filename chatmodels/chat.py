from dotenv import load_dotenv

load_dotenv()

# from langchain.chat_models import init_chat_model
from langchain_groq import ChatGroq # model class

# model = init_chat_model(
#     "openai/gpt-oss-20b", 
#     model_provider="groq"
# )
model = ChatGroq(model="openai/gpt-oss-20b") 

# model = ChatGroq(model="openai/gpt-oss-20b", temperature=0.7) 
# for logical task we keep less temperature (0)
# for creative task we keep high temperature (0.8, 0.9)

# max_tokens=20

response = model.invoke("write a paragraph on Machine Learning in 50 words")

print(response.content)