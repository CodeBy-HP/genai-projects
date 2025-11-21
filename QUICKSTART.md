# 🚀 Quick Start Guide - Your LangChain Learning Journey

Welcome! This guide will help you get started with your LangChain learning adventure.

## 📋 Prerequisites

Before you begin, make sure you have:

✅ Python 3.8 or higher installed
✅ Google API Key set in your `.env` file
✅ Basic understanding of Python

## 🛠️ Installation Steps

### Step 1: Install Dependencies

Open your terminal in the project directory and run:

```bash
pip install -r requirements.txt
```

This will install:
- **langchain** - The main LangChain library
- **langchain-google-genai** - Google Gemini integration
- **python-dotenv** - For loading environment variables
- **numpy** - For numerical operations in embeddings

### Step 2: Verify Your .env File

Make sure you have a `.env` file in your project root with:

```
GOOGLE_API_KEY=your_actual_api_key_here
```

**Important:** Never commit your `.env` file to version control!

## 📚 Learning Path

Follow this order for the best learning experience:

### 1️⃣ Understand the Concepts (5 minutes)
Read the `models/README.md` file to understand:
- What are Models in LangChain
- Difference between LLMs, Chat Models, and Embeddings
- When to use each type

### 2️⃣ Try LLMs (10 minutes)
Run the first example:

```bash
cd models
python 01_llm_example.py
```

**What you'll learn:**
- Basic text completion
- Creative writing with temperature
- Batch processing
- Streaming responses

### 3️⃣ Explore Chat Models (15 minutes)
Run the chat example:

```bash
python 02_chat_model_example.py
```

**What you'll learn:**
- Multi-turn conversations
- Maintaining context
- System messages for personality
- Building interactive chatbots

### 4️⃣ Master Embeddings (15 minutes)
Run the embeddings example:

```bash
python 03_embeddings_example.py
```

**What you'll learn:**
- Converting text to vectors
- Semantic similarity
- Building a semantic search engine
- Practical FAQ matching system

## 🎯 Tips for Success

### 1. **Take Your Time**
Don't rush! Each example is designed to be interactive. Press Enter between examples to digest what you learned.

### 2. **Experiment**
After running each example:
- Modify the prompts
- Change temperature values
- Add your own test cases

### 3. **Read the Comments**
The code is heavily commented with explanations. Read them!

### 4. **Ask Questions**
The examples include comparisons and explanations. Think about:
- Why does this work?
- When would I use this?
- How can I apply this to my projects?

## 🔧 Troubleshooting

### Error: "GOOGLE_API_KEY not found"
- Check if your `.env` file exists in the project root
- Verify the variable name is exactly `GOOGLE_API_KEY`
- Make sure you're running from the correct directory

### Error: "Module not found"
- Run `pip install -r requirements.txt` again
- Check if you're using the correct Python environment

### Error: "Invalid API Key"
- Verify your Google API key is correct
- Check if the API is enabled in Google Cloud Console

## 🎓 What's Next?

After completing these examples, you'll understand:
- ✅ The three types of models in LangChain
- ✅ How to use Gemini with LangChain
- ✅ Modern best practices (streaming, batch processing)
- ✅ Real-world applications (chatbots, semantic search)

### Continue Learning:
1. **Prompts** - Learn prompt templates and engineering
2. **Chains** - Combine multiple components
3. **Memory** - Add persistent conversation memory
4. **Agents** - Build autonomous AI agents
5. **RAG** - Retrieval Augmented Generation

## 💡 Pro Tips

1. **Use streaming** for better user experience in production apps
2. **Chat Models over LLMs** for most applications
3. **Batch processing** when handling multiple requests
4. **Embeddings** are the foundation for RAG systems
5. **System messages** to control AI behavior

## 🎉 Have Fun!

Learning should be enjoyable! These examples are designed to be:
- **Interactive** - See results immediately
- **Practical** - Real-world use cases
- **Progressive** - Build on previous knowledge

Happy coding! 🚀

---

**Questions or Issues?**
- Review the code comments
- Check the LangChain documentation: https://python.langchain.com/
- Experiment with the examples
