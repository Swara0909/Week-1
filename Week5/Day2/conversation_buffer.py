from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory()

memory.save_context(
    {"input": "My name is Swara"},
    {"output": "Hello Swara"}
)

print(memory.load_memory_variables({}))