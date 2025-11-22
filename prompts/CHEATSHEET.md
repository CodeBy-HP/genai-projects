# 📊 LangChain Prompts - Quick Reference Cheat Sheet

## 🎯 When to Use What?

| Need | Use This | Example |
|------|----------|---------|
| Simple, one-time task | Static Prompt | "Translate to French: Hello" |
| Reusable with variables | PromptTemplate | "Translate to {lang}: {text}" |
| Conversation/Chatbot | ChatPromptTemplate | System + Human + AI messages |
| Chat with history | MessagesPlaceholder | Inject conversation history |
| Teach a pattern | Few-Shot Prompts | Show 3 examples, get similar output |
| Structured output | Output Parsers | Get JSON, lists, or custom formats |
| Complex workflows | Prompt Composition | Combine multiple templates |

---

## 🔧 Quick Code Reference

### 1. Static Prompt (Simplest)
```python
from langchain_google_genai import ChatGoogleGenerativeAI

chat = ChatGoogleGenerativeAI(model="gemini-pro")
response = chat.invoke("Explain AI in one sentence")
```

### 2. PromptTemplate (Reusable)
```python
from langchain_core.prompts import PromptTemplate

template = PromptTemplate.from_template(
    "Explain {topic} to a {audience} in {style} style"
)

prompt = template.format(
    topic="quantum physics",
    audience="10-year-old",
    style="fun"
)
```

### 3. ChatPromptTemplate (Conversations)
```python
from langchain_core.prompts import ChatPromptTemplate

template = ChatPromptTemplate.from_messages([
    ("system", "You are a {role}"),
    ("human", "{question}")
])

messages = template.format_messages(
    role="helpful tutor",
    question="What is Python?"
)
```

### 4. MessagesPlaceholder (With History)
```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

template = ChatPromptTemplate.from_messages([
    ("system", "You are helpful"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])

messages = template.format_messages(
    chat_history=[...],  # List of previous messages
    input="Continue our conversation"
)
```

### 5. Few-Shot Prompts (Learn from Examples)
```python
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate

examples = [
    {"word": "happy", "antonym": "sad"},
    {"word": "big", "antonym": "small"}
]

example_template = PromptTemplate(
    input_variables=["word", "antonym"],
    template="Word: {word}\nAntonym: {antonym}"
)

few_shot = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_template,
    prefix="Give antonyms:",
    suffix="Word: {input}\nAntonym:",
    input_variables=["input"]
)
```

### 6. JSON Output Parser
```python
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

class Person(BaseModel):
    name: str = Field(description="Person's name")
    age: int = Field(description="Person's age")

parser = JsonOutputParser(pydantic_object=Person)

template = ChatPromptTemplate.from_messages([
    ("system", "Extract person info as JSON"),
    ("human", "{text}\n\n{format_instructions}")
])

prompt = template.format_messages(
    text="John is 25 years old",
    format_instructions=parser.get_format_instructions()
)

# Parse response
parsed_data = parser.parse(response.content)
```

---

## 💡 Best Practices

### ✅ DO:
- Use `ChatPromptTemplate` for modern apps
- Add system messages to control behavior
- Use `MessagesPlaceholder` for chat history
- Parse outputs with output parsers
- Keep prompts under 2000 words for best results
- Test prompts with different inputs
- Version control your prompts

### ❌ DON'T:
- Hardcode prompts in production
- Ignore output validation
- Send entire history (manage context window)
- Use high temperature for factual tasks
- Forget to handle parsing errors

---

**Remember**: Great prompts = Great AI outputs! 🎯
