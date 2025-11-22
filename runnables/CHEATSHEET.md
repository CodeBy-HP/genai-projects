# 🚀 LangChain Runnables - Quick Reference

## 📋 Core Interface

### Every Runnable Has:
```python
runnable.invoke(input, config)      # Single execution
runnable.batch([inputs], config)    # Multiple inputs
runnable.stream(input, config)      # Streaming output

# Async versions
await runnable.ainvoke(input, config)
await runnable.abatch([inputs], config)
async for chunk in runnable.astream(input, config):
    ...
```

---

## 🧩 Runnable Types

### RunnableSequence (Pipe Operator)
```python
# Created automatically with |
chain = prompt | model | parser

# All components composed sequentially
result = chain.invoke({"input": "value"})
```

### RunnableParallel (Dict Syntax)
```python
# Dict creates RunnableParallel
parallel = {
    "summary": summary_chain,
    "keywords": keyword_chain,
    "sentiment": sentiment_chain
}

# All run concurrently
result = parallel.invoke({"text": "..."})
# → {"summary": ..., "keywords": ..., "sentiment": ...}
```

### RunnableLambda
```python
# Wrap any function
from langchain_core.runnables import RunnableLambda

runnable = RunnableLambda(lambda x: x.upper())

# Now composable
chain = runnable | other_chain
```

### RunnablePassthrough
```python
# Pass input through
RunnablePassthrough()

# Add fields while preserving input
RunnablePassthrough.assign(
    new_field=lambda x: compute(x)
)
```

### RunnableGenerator
```python
# Custom streaming
from langchain_core.runnables import RunnableGenerator

def my_generator(input):
    for chunk in process(input):
        yield chunk

runnable = RunnableGenerator(my_generator)
```

---

## ⚙️ Configuration

```python
config = {
    "metadata": {"user_id": "123"},
    "tags": ["production"],
    "run_name": "important_task",
    "max_concurrency": 5
}

result = runnable.invoke(input, config=config)
```

---

## 🛠️ Method Chaining

### with_fallbacks()
```python
chain = primary_chain.with_fallbacks([
    backup_chain1,
    backup_chain2
])
# Tries primary, falls back on error
```

### with_retry()
```python
chain = unstable_chain.with_retry(
    stop_after_attempt=3,
    wait_exponential_jitter=True
)
# Automatic retry on failure
```

### with_config()
```python
chain = chain.with_config(
    tags=["production"],
    metadata={"version": "1.0"}
)
# Bind default config
```

### bind()
```python
# Bind model parameters
conservative_model = model.bind(temperature=0.1)
creative_model = model.bind(temperature=0.9)
```

---

## 🎯 Common Patterns

### Pattern 1: Sequential Pipeline
```python
pipeline = (
    step1
    | step2  
    | step3
)
```

### Pattern 2: Parallel + Sequential
```python
chain = (
    RunnableParallel(
        analysis1=chain1,
        analysis2=chain2
    )
    | synthesis_chain
)
```

### Pattern 3: Preserve Input + Add Fields
```python
chain = RunnablePassthrough.assign(
    summary=summary_chain,
    keywords=keyword_chain
)
# Input + new fields in output
```

### Pattern 4: Nested Parallel
```python
complex = {
    "stats": {
        "count": count_chain,
        "avg": avg_chain
    },
    "analysis": {
        "sentiment": sentiment_chain,
        "entities": entity_chain
    }
}
```

---

## ⚡ Performance Tips

### 1. Use Parallel for Independent Ops
```python
# Instead of
result1 = chain1.invoke(x)
result2 = chain2.invoke(x)

# Use
result = {
    "r1": chain1,
    "r2": chain2
}.invoke(x)
# 2-3x faster!
```

### 2. Batch When Possible
```python
# Instead of
for item in items:
    result = chain.invoke(item)

# Use
results = chain.batch(items)
# More efficient!
```

### 3. Stream for UX
```python
for chunk in chain.stream(input):
    display(chunk)  # Show immediately
```

### 4. Async for Concurrency
```python
tasks = [chain.ainvoke(item) for item in items]
results = await asyncio.gather(*tasks)
```

---

## 🔍 Debugging

### Add Logging
```python
chain = (
    step1
    | RunnableLambda(lambda x: print(f"After step1: {x}") or x)
    | step2
)
```

### Inspect Schemas
```python
print(chain.input_schema.schema())
print(chain.output_schema.schema())
```

### Structure
```python
print(chain)  # See composition
```

---

## ✅ Best Practices

### DO:
- ✓ Use pipe operator (|) for composition
- ✓ Use dict syntax for parallel operations
- ✓ Add error handling (fallbacks, retry)
- ✓ Use batch() for multiple inputs
- ✓ Stream for better UX
- ✓ Use type hints
- ✓ Test components individually

### DON'T:
- ✗ Mix sync/async incorrectly
- ✗ Ignore error handling
- ✗ Use parallel for dependent operations
- ✗ Forget to validate inputs
- ✗ Over-complicate simple chains

---

## 🎓 Quick Decision Tree

```
Need to compose operations?
├─ Sequential → Use | operator
├─ Parallel → Use dict {}
├─ Conditional → Use RunnableBranch
└─ Custom logic → Use RunnableLambda

Need error handling?
├─ Retry transient errors → with_retry()
├─ Fallback on failure → with_fallbacks()
└─ Both → Chain them!

Need better UX?
├─ Long responses → stream()
├─ Multiple items → batch()
└─ Async framework → ainvoke()/astream()
```

---

## 📚 Module Contents

```
runnables/
├── README.md                      # Complete guide
├── 01_runnable_interface.py      # Core interface
├── 02_runnable_sequence.py       # Sequential composition
├── 03_runnable_parallel.py       # Parallel execution
├── 04_advanced_runnables.py      # Specialized types
├── 05_practical_runnables.py     # Real projects
├── CHEATSHEET.md                 # This file
└── ROADMAP.md                    # Learning path
```

---

## 💡 Remember

> **Everything in LangChain is a Runnable**
>
> Models, prompts, chains, parsers - unified interface!
>
> **Pipe operator is your friend:** `chain = a | b | c`

---

**Made with ❤️ for LangChain learners**