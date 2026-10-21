from dotenv import load_dotenv

load_dotenv()

from langchain_groq import ChatGroq

model = ChatGroq(model="openai/gpt-oss-20b") 

# short term memory
messages = []

print("------------ Welcome type 0 to exit the application ----------")
while True:
    prompt = input("You : ")
    messages.append(prompt)
    if prompt == "0":
        break
    response = model.invoke(messages) # it can hit token limit, slower response
    messages.append(response.content)
    print("Bot : ", response.content)