from dotenv import load_dotenv

load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

model = ChatGroq(model="openai/gpt-oss-20b") 

# short term memory
messages = [
    SystemMessage(content="you are a funny Ai agent")
]

print("------------ Welcome type 0 to exit the application ----------")
while True:
    prompt = input("You : ")
    messages.append(HumanMessage(content=prompt))
    if prompt == "0":
        break
    response = model.invoke(messages) # it can hit token limit, slower response
    messages.append(AIMessage(content=response.content))
    print("Bot : ", response.content)

print(messages)