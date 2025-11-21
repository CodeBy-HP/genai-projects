# 📊 LangChain Models - Quick Reference Cheat Sheet

## 🎯 When to Use What?

| Need | Use This | Example |
|------|----------|---------|
| Simple text completion | LLM | "Complete this sentence: AI is..." |
| Conversation/Chatbot | Chat Model | Multi-turn Q&A assistant |
| Find similar content | Embeddings | Search documents by meaning |
| RAG system | Chat Model + Embeddings | Q&A over your documents |
| Creative writing | LLM (high temp) | Story generation |
| Structured responses | Chat Model (low temp) | Form filling, data extraction |

## 🔧 Quick Code Reference

### LLM - Simple Completion
```python
from langchain_google_genai import GoogleGenerativeAI

llm = GoogleGenerativeAI(model="gemini-pro", temperature=0.7)
response = llm.invoke("Your prompt here")
```

### Chat Model - Conversation
```python
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

chat = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7)
messages = [
    SystemMessage(content="You are a helpful assistant"),
    HumanMessage(content="Hello!")
]
response = chat.invoke(messages)
```

### Embeddings - Semantic Search
```python
from langchain_google_genai import GoogleGenerativeAIEmbeddings

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
query_vector = embeddings.embed_query("search query")
doc_vectors = embeddings.embed_documents(["doc1", "doc2"])
```

## 🌡️ Temperature Guide

| Value | Behavior | Use For |
|-------|----------|---------|
| 0.0 - 0.3 | Focused, deterministic | Facts, code, structured data |
| 0.4 - 0.7 | Balanced | General conversation |
| 0.8 - 1.0 | Creative, random | Stories, brainstorming |

## 🎭 Message Types (Chat Models)

| Type | Role | Purpose |
|------|------|---------|
| SystemMessage | Sets behavior | "You are a helpful coding assistant" |
| HumanMessage | User input | The user's questions/requests |
| AIMessage | AI response | Previous AI responses (for context) |

## ⚡ Performance Tips

### Streaming (Better UX)
```python
for chunk in chat.stream(messages):
    print(chunk.content, end="", flush=True)
```

### Batch Processing (Faster)
```python
responses = llm.batch(["prompt1", "prompt2", "prompt3"])
```

## 🎨 Common Patterns

### Pattern 1: Simple Q&A
```python
llm = GoogleGenerativeAI(model="gemini-pro")
answer = llm.invoke("What is Python?")
```

### Pattern 2: Conversational Bot
```python
chat = ChatGoogleGenerativeAI(model="gemini-pro")
history = [SystemMessage(content="You are helpful")]

while True:
    user_input = input("You: ")
    history.append(HumanMessage(content=user_input))
    response = chat.invoke(history)
    history.append(AIMessage(content=response.content))
    print(f"AI: {response.content}")
```

### Pattern 3: Semantic Search
```python
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Index documents
docs = ["doc1", "doc2", "doc3"]
doc_embeddings = embeddings.embed_documents(docs)

# Search
query_embedding = embeddings.embed_query("find this")
# Calculate similarity with doc_embeddings
```

## 🚨 Common Mistakes to Avoid

❌ Using LLMs when Chat Models would be better
✅ Prefer Chat Models for modern applications

❌ Not streaming long responses
✅ Use `.stream()` for better user experience

❌ Processing items one-by-one
✅ Use `.batch()` for multiple items

❌ Forgetting to set temperature
✅ Choose appropriate temperature for your use case

❌ Not using system messages
✅ Use SystemMessage to control behavior

## 💾 Environment Setup

```bash
# .env file
GOOGLE_API_KEY=your_key_here
```

```python
# In your code
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
```

## 📦 Installation

```bash
pip install langchain langchain-google-genai python-dotenv numpy
```

## 🔗 Useful Resources

- LangChain Docs: https://python.langchain.com/
- Google AI Studio: https://makersuite.google.com/
- Gemini Models: https://ai.google.dev/models/gemini

## 🎓 Learning Path

1. ✅ Understand concepts (README.md)
2. ✅ Try LLMs (01_llm_example.py)
3. ✅ Explore Chat Models (02_chat_model_example.py)
4. ✅ Master Embeddings (03_embeddings_example.py)
5. 🔜 Build your own project!

---

**Remember:** The best way to learn is by doing! Modify the examples and experiment. 🚀
