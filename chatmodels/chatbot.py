from dotenv import load_dotenv

load_dotenv()

from langchain_groq import ChatGroq

model = ChatGroq(model="openai/gpt-oss-20b") 

print("------------ Welcome type 0 to exit the application ----------")
while True:
    prompt = input("You : ")
    if prompt == "0":
        break
    response = model.invoke(prompt)

    print("Bot : ", response.content)