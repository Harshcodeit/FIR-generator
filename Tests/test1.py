from langchain_ollama import ChatOllama

model_name = 'gemma4:e4b'

llm = ChatOllama(
    model = model_name,
    temperature = 0
)
print("Loaded model successfully")

response = llm.invoke("Explain theft under BNS sections only.")

print(response.content)