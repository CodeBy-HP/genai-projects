# 🎯 LangChain Prompts - Master the Art of Prompt Engineering

Welcome to the **Prompts** component of LangChain! After learning about Models, you're now ready to learn how to communicate effectively with them.

## 🎨 What are Prompts?

Think of prompts as **instructions** you give to AI models. Just like how you give clear instructions to a friend, prompts tell the AI what you want it to do.

**Simple analogy:**
- 🤖 **Model** = A skilled chef
- 🎯 **Prompt** = The recipe you give them
- 📝 **Output** = The delicious dish they create

Better recipes → Better dishes!  
Better prompts → Better AI responses!

---

## 📚 The Complete Prompt Ecosystem

### 1. 📄 **Static Prompts**
- **What they are**: Fixed text prompts that never change
- **Example**: "Translate this to French: Hello"
- **When to use**: Simple, one-off tasks

### 2. 🔄 **Dynamic Prompts**
- **What they are**: Prompts with variables that change
- **Example**: "Translate this to {language}: {text}"
- **When to use**: Reusable prompts with different inputs

### 3. 📋 **PromptTemplate**
- **What it is**: LangChain's way to create dynamic prompts
- **Superpowers**: Variable injection, validation, reusability
- **When to use**: Whenever you need dynamic content

### 4. 💬 **ChatPromptTemplate**
- **What it is**: Templates for chat-based conversations
- **Includes**: System, Human, and AI messages
- **When to use**: Building conversational applications

### 5. 🗨️ **MessagePlaceholder**
- **What it is**: Dynamic insertion of multiple messages
- **Superpower**: Inject conversation history anywhere
- **When to use**: Chatbots with memory

### 6. 🎓 **Few-Shot Prompts**
- **What they are**: Prompts with examples to guide the AI
- **Example**: Show 3 examples, then ask for a 4th
- **When to use**: Teaching AI a specific pattern

### 7. 🔗 **Prompt Composition**
- **What it is**: Combining multiple prompts together
- **Superpower**: Build complex prompts from simple pieces
- **When to use**: Advanced, modular applications

### 8. 📦 **Output Parsers**
- **What they are**: Convert AI text output into structured data
- **Example**: Parse JSON, lists, or custom formats
- **When to use**: When you need structured responses

---

## 🎯 Why Are Prompts Important?

### The Difference Good Prompts Make:

**❌ Bad Prompt:**
```
"Tell me about Python"
```
Result: Vague, could be about the snake or programming!

**✅ Good Prompt:**
```
You are a programming tutor. Explain Python programming language 
to a beginner in 3 sentences. Focus on its main benefits.
```
Result: Clear, specific, actionable!

### Benefits of LangChain Prompts:

✅ **Reusability** - Write once, use everywhere  
✅ **Maintainability** - Change prompts without changing code  
✅ **Validation** - Ensure all variables are provided  
✅ **Composition** - Combine prompts like building blocks  
✅ **Version Control** - Track prompt changes over time  
✅ **Testing** - Test prompts independently  

---

## 🌟 Prompt Components Explained

### PromptTemplate
```python
from langchain_core.prompts import PromptTemplate

template = PromptTemplate(
    input_variables=["topic", "language"],
    template="Explain {topic} in {language} language"
)

# Use it
prompt = template.format(topic="AI", language="simple")
```

### ChatPromptTemplate
```python
from langchain_core.prompts import ChatPromptTemplate

template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant"),
    ("human", "Tell me about {topic}")
])
```

### MessagePlaceholder
```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

template = ChatPromptTemplate.from_messages([
    ("system", "You are helpful"),
    MessagesPlaceholder(variable_name="history"),  # Inject history here!
    ("human", "{question}")
])
```

### Few-Shot Prompts
```python
from langchain_core.prompts import FewShotPromptTemplate

# Examples to teach the AI
examples = [
    {"word": "happy", "antonym": "sad"},
    {"word": "tall", "antonym": "short"}
]

# The AI learns the pattern!
```

---

## 🎓 Prompt Engineering Best Practices

### 1. **Be Specific**
❌ "Write about dogs"  
✅ "Write a 100-word article about dog training tips for puppies"

### 2. **Set the Context**
❌ "Answer this question"  
✅ "You are an expert teacher. Answer this student's question clearly"

### 3. **Use Examples**
❌ "Format this data"  
✅ "Format like this: Name: John, Age: 25. Now format: {data}"

### 4. **Define Output Format**
❌ "List programming languages"  
✅ "List 5 programming languages in JSON format with name and year"

### 5. **Be Clear About Constraints**
❌ "Summarize this"  
✅ "Summarize this in exactly 3 bullet points, max 20 words each"

---

## 🗺️ The Prompt Hierarchy

```
Simple → Complex

Static Prompt
    ↓
Dynamic Prompt (with variables)
    ↓
PromptTemplate (structured)
    ↓
ChatPromptTemplate (conversation)
    ↓
MessagePlaceholder (with history)
    ↓
Few-Shot Prompts (with examples)
    ↓
Composed Prompts (multiple templates)
    ↓
Prompts + Output Parsers (structured output)
```

---

## 🎯 Common Use Cases

| Use Case | Best Prompt Type | Why |
|----------|------------------|-----|
| Simple translation | PromptTemplate | Variables for language/text |
| Chatbot | ChatPromptTemplate | Structured messages |
| Chatbot with memory | MessagePlaceholder | Inject history |
| Teaching a format | Few-Shot | Examples guide AI |
| Structured data | Output Parsers | Parse JSON/lists |
| Complex workflows | Composed Prompts | Modular design |

---

## 📖 What You'll Learn

In this module, you'll master:

### 🎯 **Fundamentals** (01_basic_prompts.py)
- Static vs Dynamic prompts
- PromptTemplate basics
- Variable injection
- Partial variables

### 💬 **Chat Prompts** (02_chat_prompts.py)
- ChatPromptTemplate
- System/Human/AI messages
- MessagePlaceholder
- Conversation history handling

### 🎓 **Advanced Techniques** (03_advanced_prompts.py)
- Few-Shot prompting
- Output parsers (JSON, List, Custom)
- Prompt composition
- Conditional prompts

### 🚀 **Real-World Projects** (04_practical_examples.py)
- Smart FAQ bot
- Code generator
- Data extraction system
- Multi-step reasoning

---

## 💡 Key Concepts to Remember

### Variables & Placeholders
```python
template = "Hello {name}, welcome to {place}!"
# {name} and {place} are variables
```

### Message Types
- **SystemMessage**: Sets AI behavior/personality
- **HumanMessage**: User's input
- **AIMessage**: AI's previous responses

### Template Syntax
- `{variable}`: Simple variable
- `{variable:format}`: Formatted variable
- `{{literal}}`: Escape braces

---

## 🎨 Prompt Engineering Mindset

Think of prompt engineering as:

1. **Teaching** - You're teaching the AI what to do
2. **Guiding** - Provide clear direction
3. **Examples** - Show, don't just tell
4. **Iteration** - Refine until perfect
5. **Testing** - Try different approaches

---

## 🔥 Modern Best Practices (2024)

1. **Use ChatPromptTemplate** for most applications
2. **Leverage MessagePlaceholder** for conversation history
3. **Add output parsers** for structured data
4. **Use few-shot** when pattern is complex
5. **Compose prompts** for maintainability
6. **Version control** your prompts
7. **Test extensively** before production

---

## 🛠️ What We'll Build

### Project 1: Multi-Language Translator
- PromptTemplate with language variables
- Clean, reusable code

### Project 2: Intelligent Chatbot
- ChatPromptTemplate with personality
- MessagePlaceholder for history
- Remembers context

### Project 3: Code Reviewer
- Few-shot examples of good/bad code
- Structured JSON output
- Actionable feedback

### Project 4: Data Extractor
- Extract structured info from text
- Custom output parsers
- Validation

---

## 📊 Prompts vs Models

| Component | Purpose | Example |
|-----------|---------|---------|
| **Models** | The AI brain | Gemini, GPT, Claude |
| **Prompts** | Instructions to brain | "Translate X to Y" |
| **Together** | Magic happens! | Accurate translations |

You learned Models (the chef).  
Now learn Prompts (the recipes).  
Next: Chains (the full kitchen workflow)!

---

## 🎯 Success Criteria

You'll master Prompts when you can:

✅ Explain static vs dynamic prompts  
✅ Create reusable PromptTemplates  
✅ Build chat prompts with system messages  
✅ Handle conversation history  
✅ Use few-shot prompting  
✅ Parse structured output  
✅ Compose complex prompts  

---

## 🚀 Ready to Start?

Follow this order:

1. **Read this README** ✅ (You're here!)
2. **Run**: `python 01_basic_prompts.py`
3. **Run**: `python 02_chat_prompts.py`
4. **Run**: `python 03_advanced_prompts.py`
5. **Run**: `python 04_practical_examples.py`
6. **Build** your own prompt-powered app!

---

## 💬 Remember

> "A great prompt is half the solution. Master prompts, master AI!"

Let's make your AI interactions **precise**, **powerful**, and **production-ready**! 🚀

---

**Next Steps**: Check out the example files in this directory!
