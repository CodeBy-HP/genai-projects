# 🚀 LangChain Chains - Quick Reference

## 📋 Core Concepts

### LCEL (LangChain Expression Language)
```python
# Pipe operator for chain composition
chain = prompt | model | parser

# Execute
result = chain.invoke({"input": "value"})
```

### Chain Types Comparison

| Type | Use When | Performance | Complexity |
|------|----------|-------------|------------|
| **Sequential** | Linear multi-step pipeline | ⚡ Fast | ⭐ Simple |
| **Parallel** | Independent operations | ⚡⚡⚡ Fastest | ⭐⭐ Medium |
| **Conditional** | Dynamic routing needed | ⚡⚡ Moderate | ⭐⭐⭐ Complex |

---

## 🔧 Essential Components

### RunnablePassthrough
```python
# Pass input through unchanged
from langchain_core.runnables import RunnablePassthrough

chain = RunnablePassthrough()
# Input: {"x": 5} → Output: {"x": 5}

# Add new fields while preserving original
chain = RunnablePassthrough.assign(
    squared=lambda x: x["num"] ** 2
)
# Input: {"num": 5} → Output: {"num": 5, "squared": 25}
```

### RunnableLambda
```python
# Custom transformation
from langchain_core.runnables import RunnableLambda

def process(x):
    return x.upper()

chain = RunnableLambda(process)
# Input: "hello" → Output: "HELLO"
```

### RunnableParallel
```python
# Execute multiple chains in parallel
from langchain_core.runnables import RunnableParallel

parallel = RunnableParallel(
    summary=summary_chain,
    keywords=keyword_chain,
    sentiment=sentiment_chain
)
# All three chains run concurrently!
```

### RunnableBranch
```python
# Conditional routing
from langchain_core.runnables import RunnableBranch

branch = RunnableBranch(
    (lambda x: x["urgent"], urgent_handler),
    (lambda x: x["question"], question_handler),
    default_handler  # Fallback
)
```

---

## 📊 Quick Decision Tree

```
Need multiple steps in order?
├─ YES → Sequential Chain
│   └─ RunnablePassthrough.assign() for context
└─ NO
    │
    ├─ Independent operations?
    │   └─ YES → Parallel Chain
    │       └─ RunnableParallel()
    │
    └─ Dynamic routing?
        └─ YES → Conditional Chain
            ├─ Simple if/else → RunnableBranch
            ├─ Error handling → with_fallbacks()
            └─ Runtime selection → dict + RunnableLambda
```

---

## 🎯 Common Patterns

### Pattern 1: Multi-Step Processing
```python
# Extract → Transform → Load
pipeline = (
    extract_chain
    | RunnablePassthrough.assign(transformed=transform_chain)
    | load_chain
)
```

### Pattern 2: Parallel Analysis
```python
# Get multiple perspectives simultaneously
analysis = RunnableParallel(
    technical=technical_chain,
    business=business_chain,
    user=user_chain
)
```

### Pattern 3: Intent-Based Routing
```python
# Classify then route
system = (
    RunnablePassthrough.assign(intent=classify_chain)
    | RunnableBranch(
        (lambda x: x["intent"] == "tech", tech_handler),
        (lambda x: x["intent"] == "sales", sales_handler),
        general_handler
    )
)
```

### Pattern 4: Conditional Processing
```python
# Process differently based on conditions
chain = RunnableBranch(
    (is_urgent, fast_track_chain),
    (is_complex, detailed_chain),
    standard_chain
)
```

---

## ⚡ Execution Methods

```python
# Single execution
result = chain.invoke({"input": "value"})

# Batch processing
results = chain.batch([
    {"input": "value1"},
    {"input": "value2"}
])

# Streaming
for chunk in chain.stream({"input": "value"}):
    print(chunk, end="")

# Async execution
result = await chain.ainvoke({"input": "value"})
```

---

## 🛠️ Useful Operators

### assign()
```python
# Add new fields
chain = RunnablePassthrough.assign(
    new_field=lambda x: process(x["input"])
)
```

### pick()
```python
# Select specific fields
from langchain_core.runnables import RunnablePassthrough

chain = RunnablePassthrough() | RunnableLambda(
    lambda x: {k: x[k] for k in ["field1", "field2"]}
)
```

### with_fallbacks()
```python
# Error handling
chain = primary_chain.with_fallbacks([
    backup_chain1,
    backup_chain2
])
```

---

## 🎓 Best Practices

### ✅ DO
- Use `|` operator for clean chain composition
- Preserve context with `RunnablePassthrough.assign()`
- Use `RunnableParallel` for independent operations
- Add error handling with `with_fallbacks()`
- Use type hints for better IDE support
- Test chains with simple inputs first

### ❌ DON'T
- Don't use parallel for dependent operations
- Don't mutate input dictionaries
- Don't ignore error handling in production
- Don't over-complicate simple chains
- Don't forget to validate outputs

---

## 📈 Performance Tips

1. **Use Parallel When Possible**
   ```python
   # Instead of sequential
   a = chain1.invoke(x)
   b = chain2.invoke(x)
   
   # Use parallel
   result = RunnableParallel(a=chain1, b=chain2).invoke(x)
   # 2-3x faster!
   ```

2. **Batch Processing**
   ```python
   # Instead of loops
   for item in items:
       result = chain.invoke(item)
   
   # Use batch
   results = chain.batch(items)
   # More efficient!
   ```

3. **Streaming for UX**
   ```python
   # For long responses
   for chunk in chain.stream(input):
       display(chunk)  # Show progress immediately
   ```

---

## 🔍 Debugging

```python
# Add logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Print intermediate steps
chain = (
    step1
    | RunnableLambda(lambda x: print(f"After step1: {x}") or x)
    | step2
    | RunnableLambda(lambda x: print(f"After step2: {x}") or x)
    | step3
)

# Inspect chain structure
print(chain)
```

---

## 🎯 Real-World Examples

### Document Processing
```python
pipeline = (
    extract_metadata
    | RunnablePassthrough.assign(**parallel_analysis)
    | format_report
)
```

### Customer Support Router
```python
router = (
    RunnablePassthrough.assign(
        intent=classify_intent,
        urgency=detect_urgency
    )
    | RunnableBranch(
        (is_urgent, priority_handler),
        (is_technical, tech_handler),
        general_handler
    )
)
```

### Multi-Language Translation
```python
translator = (
    RunnablePassthrough.assign(source_lang=detect_chain)
    | RunnableBranch(
        (needs_translation, translate_chain),
        passthrough_chain
    )
    | RunnablePassthrough.assign(quality=quality_check)
)
```

---

## 📚 Module Structure

```
chains/
├── README.md                    # Complete guide
├── 01_lcel_basics.py           # LCEL fundamentals
├── 02_sequential_chains.py      # Multi-step pipelines
├── 03_parallel_chains.py        # Concurrent execution
├── 04_conditional_chains.py     # Dynamic routing
├── 05_practical_chains.py       # Real-world projects
├── CHEATSHEET.md               # This file
└── ROADMAP.md                  # Learning path
```

---

## 🔗 Quick Links

- **LCEL Basics** → Start here for pipe operator
- **Sequential** → Linear multi-step workflows
- **Parallel** → Speed up independent operations
- **Conditional** → Dynamic routing and branching
- **Practical** → Production-ready projects

---

## 💡 Remember

> **LCEL = Declarative + Composable + Optimized**
> 
> The pipe operator (`|`) is your friend!
> 
> Think: Input → Transform → Output

---

**Made with ❤️ for LangChain learners**
