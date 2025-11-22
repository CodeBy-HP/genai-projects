# 📚 Structured Output - Quick Reference

## 🎯 When to Use What

```python
# ✅ Model supports structured output (Gemini, GPT-4, Claude)
chat.with_structured_output(PydanticModel)

# ✅ Model doesn't support it OR need more control
PydanticOutputParser + format instructions
```

## 🔧 Output Parsers Cheatsheet

### 1. PydanticOutputParser
```python
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

class User(BaseModel):
    name: str = Field(description="User name")
    age: int = Field(ge=0, le=120)

parser = PydanticOutputParser(pydantic_object=User)

template = PromptTemplate(
    template="Extract: {text}\n\n{format_instructions}",
    input_variables=["text"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

chain = template | llm | parser
```

**When to use:** Need validation, type safety, complex structures

### 2. JsonOutputParser
```python
from langchain_core.output_parsers import JsonOutputParser

class Person(BaseModel):
    name: str
    age: int

parser = JsonOutputParser(pydantic_object=Person)
chain = prompt | llm | parser  # Returns dict
```

**When to use:** Simple dict output, JSON APIs

### 3. StructuredOutputParser
```python
from langchain.output_parsers import StructuredOutputParser, ResponseSchema

schemas = [
    ResponseSchema(name="name", description="Person name"),
    ResponseSchema(name="age", description="Person age")
]

parser = StructuredOutputParser.from_response_schemas(schemas)
```

**When to use:** Quick field extraction, simple structures

### 4. StrOutputParser
```python
from langchain_core.output_parsers import StrOutputParser

parser = StrOutputParser()
chain = prompt | llm | parser  # Returns clean string
```

**When to use:** Just need clean text output

### 5. CommaSeparatedListOutputParser
```python
from langchain_core.output_parsers import CommaSeparatedListOutputParser

parser = CommaSeparatedListOutputParser()
chain = prompt | llm | parser  # Returns list
```

**When to use:** Extract lists from text

### 6. DatetimeOutputParser
```python
from langchain.output_parsers import DatetimeOutputParser

parser = DatetimeOutputParser()
chain = prompt | llm | parser  # Returns datetime object
```

**When to use:** Parse dates/times

### 7. BooleanOutputParser
```python
from langchain.output_parsers import BooleanOutputParser

parser = BooleanOutputParser()
chain = prompt | llm | parser  # Returns True/False
```

**When to use:** Yes/no questions

### 8. EnumOutputParser
```python
from langchain.output_parsers import EnumOutputParser
from enum import Enum

class Color(str, Enum):
    RED = "red"
    BLUE = "blue"

parser = EnumOutputParser(enum=Color)
```

**When to use:** Fixed set of values

## 🚀 Advanced Techniques

### OutputFixingParser (Auto-fix errors)
```python
from langchain.output_parsers import OutputFixingParser

base_parser = PydanticOutputParser(pydantic_object=Model)
fixing_parser = OutputFixingParser.from_llm(
    parser=base_parser,
    llm=chat
)

# Automatically fixes malformed output using LLM
result = fixing_parser.parse(malformed_json)
```

### RetryOutputParser (Retry with context)
```python
from langchain.output_parsers import RetryOutputParser

retry_parser = RetryOutputParser.from_llm(
    parser=base_parser,
    llm=chat,
    max_retries=2
)

# Retry with original prompt context
result = retry_parser.parse_with_prompt(
    completion,
    original_prompt
)
```

### Custom Parser
```python
from langchain_core.output_parsers.base import BaseOutputParser

class CustomParser(BaseOutputParser[YourType]):
    def parse(self, text: str) -> YourType:
        # Your parsing logic
        return parsed_result
    
    def get_format_instructions(self) -> str:
        return "Your format instructions"
```

## 📐 Common Patterns

### Pattern 1: Partial Variables (Recommended)
```python
template = PromptTemplate(
    template="Task: {task}\n\n{format_instructions}",
    input_variables=["task"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

# Clean! No need to pass format_instructions manually
chain = template | llm | parser
result = chain.invoke({"task": "Extract data"})
```

### Pattern 2: LCEL Chain
```python
chain = prompt | llm | parser
result = chain.invoke(input_data)
```

### Pattern 3: Validation Cascade
```python
try:
    result = strict_parser.parse(output)
except Exception:
    try:
        result = lenient_parser.parse(output)
    except Exception:
        result = default_value
```

### Pattern 4: Multiple Parsers
```python
# Step 1: Extract metadata
metadata = meta_parser.parse(chain1.invoke(text))

# Step 2: Extract content
content = content_parser.parse(chain2.invoke(text))
```

## 🎨 Pydantic Features

### Field Constraints
```python
from langchain_core.pydantic_v1 import BaseModel, Field

class Model(BaseModel):
    age: int = Field(ge=0, le=120)  # 0 <= age <= 120
    name: str = Field(min_length=1, max_length=100)
    score: float = Field(gt=0, le=100)  # 0 < score <= 100
    tags: List[str] = Field(max_items=10)
```

### Custom Validators
```python
from langchain_core.pydantic_v1 import validator

class User(BaseModel):
    email: str
    age: int
    
    @validator('email')
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email')
        return v.lower()
    
    @validator('age')
    def validate_age(cls, v):
        if v < 0 or v > 120:
            raise ValueError('Invalid age')
        return v
```

### Enums
```python
from enum import Enum

class Status(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"

class User(BaseModel):
    status: Status  # Only accepts valid enum values
```

### Nested Models
```python
class Address(BaseModel):
    street: str
    city: str

class Person(BaseModel):
    name: str
    address: Address  # Nested structure
```

## ⚡ Performance Tips

1. **Use with_structured_output when available** (faster, more reliable)
2. **Partial variables > manual injection** (cleaner code)
3. **OutputFixingParser for unreliable outputs** (auto-recovery)
4. **Lower temperature for structured output** (0.1-0.3)
5. **Validate early** (catch errors before processing)

## 🔍 Debugging

### Check format instructions
```python
print(parser.get_format_instructions())
```

### Test parser separately
```python
test_json = '{"name": "John", "age": 30}'
result = parser.parse(test_json)
```

### Use try-except
```python
try:
    result = parser.parse(output)
except Exception as e:
    print(f"Parse error: {e}")
    print(f"Output was: {output}")
```

## 📊 Comparison Table

| Parser | Output Type | Use Case | Complexity |
|--------|-------------|----------|------------|
| PydanticOutputParser | Pydantic object | Validation, complex structures | High |
| JsonOutputParser | dict | Simple JSON | Low |
| StructuredOutputParser | dict | Quick field extraction | Low |
| StrOutputParser | str | Clean text | Minimal |
| CommaSeparatedListOutputParser | list | List extraction | Low |
| DatetimeOutputParser | datetime | Date/time | Low |
| BooleanOutputParser | bool | Yes/no | Minimal |
| EnumOutputParser | Enum | Fixed choices | Low |

## 🎯 Decision Tree

```
Need structured output?
├─ Model supports with_structured_output?
│  ├─ Yes → Use chat.with_structured_output(Model)
│  └─ No → Continue below
├─ Need validation?
│  ├─ Yes → PydanticOutputParser
│  └─ No → Continue below
├─ Need complex structure?
│  ├─ Yes → PydanticOutputParser or JsonOutputParser
│  └─ No → Continue below
├─ Just simple fields?
│  ├─ Yes → StructuredOutputParser
│  └─ No → Continue below
├─ Just clean text?
│  ├─ Yes → StrOutputParser
│  └─ No → Use specialized parser (List, DateTime, etc.)
└─ Unreliable output?
   └─ Yes → Wrap with OutputFixingParser or RetryOutputParser
```

## 🚨 Common Mistakes

❌ **Don't:** Forget format instructions
```python
template = PromptTemplate(
    template="Extract: {text}",
    input_variables=["text"]
)
# Parser has no idea what format to expect!
```

✅ **Do:** Include format instructions
```python
template = PromptTemplate(
    template="Extract: {text}\n\n{format_instructions}",
    input_variables=["text"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)
```

❌ **Don't:** Use high temperature for structured output
```python
chat = ChatGoogleGenerativeAI(temperature=0.9)  # Too creative!
```

✅ **Do:** Use low temperature
```python
chat = ChatGoogleGenerativeAI(temperature=0.1)  # More reliable
```

❌ **Don't:** Ignore validation errors
```python
result = parser.parse(output)  # Might fail silently
```

✅ **Do:** Handle errors
```python
try:
    result = parser.parse(output)
except Exception as e:
    # Handle or log error
    result = default_value
```

## 🎓 Best Practices

1. ✅ Use `with_structured_output` for supported models
2. ✅ Use low temperature (0.1-0.3) for structured output
3. ✅ Include clear descriptions in Field()
4. ✅ Add validators for critical fields
5. ✅ Use OutputFixingParser for production
6. ✅ Test parsers with sample data
7. ✅ Handle errors gracefully
8. ✅ Use partial_variables for format instructions
9. ✅ Choose simplest parser that meets needs
10. ✅ Document your schema well

---

🎯 **Remember:** 
- Supported models → `with_structured_output`
- Unsupported models → Output parsers + format instructions
- Production → Add error handling + OutputFixingParser
