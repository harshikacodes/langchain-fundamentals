from dotenv import load_dotenv

load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

model = ChatGroq(model="openai/gpt-oss-20b") 

print("Chosse your AI mode")
print("press 1 for angry mode")
print("press 2 for funny mode")
print("press 3 for sad mode")

choice = int(input("tell your response :- "))

if choice == 1:
    mode = "You are an angry AI agent. You respond aggressively and impatiently."
elif choice == 2:
    mode = "You are a very funny AI agent. You respond with humor and jokes."
elif choice == 3:
    mode = "You are sad AI agent. You respond with disappointment."

messages = [
    SystemMessage(content=mode)
]

print("------------ Welcome type 0 to exit the application ----------")
while True:
    prompt = input("You : ")
    messages.append(HumanMessage(content=prompt))
    if prompt == "0":
        break
    response = model.invoke(messages)
    messages.append(AIMessage(content=response.content))
    print("Bot : ", response.content)