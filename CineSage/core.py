from dotenv import load_dotenv

load_dotenv()

from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

model = ChatGroq(model="openai/gpt-oss-20b") 

prompt = PromptTemplate.from_template("")

response = model.invoke("")

print(response.content)