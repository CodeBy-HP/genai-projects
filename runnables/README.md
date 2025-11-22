# 🔧 LangChain Runnables - Complete Guide

## 📋 Table of Contents
- [What are Runnables?](#what-are-runnables)
- [Core Concepts](#core-concepts)
- [Runnable Types](#runnable-types)
- [Execution Methods](#execution-methods)
- [Composition Patterns](#composition-patterns)
- [Advanced Features](#advanced-features)
- [Best Practices](#best-practices)
- [Common Use Cases](#common-use-cases)

---

## 🎯 What are Runnables?

**Runnables** are the fundamental building blocks of LangChain. Everything you've been using—models, prompts, chains, parsers—is a Runnable!

### Key Characteristics

✨ **Unified Interface**
- Every Runnable implements the same core methods
- Consistent API across all components
- Easy to compose and combine

🔗 **Composable**
- Use pipe operator (`|`) to chain together
- Automatically creates RunnableSequence
- Type-safe composition

⚡ **Execution Modes**
- Synchronous: `invoke()`, `batch()`
- Streaming: `stream()`
- Async: `ainvoke()`, `abatch()`, `astream()`

🎨 **Flexible**
- Built-in runnables for common patterns
- Create custom runnables
- Extend and modify behavior

---

## 🔑 Core Concepts

### The Runnable Protocol

Every Runnable must implement:

```python
from langchain_core.runnables import Runnable

class MyRunnable(Runnable):
    """All runnables implement these methods"""
    
    def invoke(self, input, config=None):
        """Process single input"""
        pass
    
    def batch(self, inputs, config=None):
        """Process multiple inputs"""
        pass
    
    def stream(self, input, config=None):
        """Stream output chunks"""
        pass
    
    # Async versions
    async def ainvoke(self, input, config=None):
        """Async single input"""
        pass
    
    async def abatch(self, inputs, config=None):
        """Async batch"""
        pass
    
    async def astream(self, input, config=None):
        """Async stream"""
        pass
```

### Why Runnables Matter

1. **Consistency**: Same interface everywhere
2. **Composability**: Chain anything with anything
3. **Optimization**: Automatic batching, streaming
4. **Debugging**: Standardized introspection
5. **Testing**: Easy to mock and test

---

## 🧩 Runnable Types

### 1. RunnableSequence
**Purpose**: Sequential composition (the pipe operator creates these)

```python
# These are equivalent
chain = prompt | model | parser
chain = RunnableSequence(prompt, model, parser)

# Automatically created when using |
result = chain.invoke({"input": "value"})
```

**When to use**: Multi-step linear pipelines

---

### 2. RunnableParallel (RunnableMap)
**Purpose**: Execute multiple runnables concurrently

```python
from langchain_core.runnables import RunnableParallel

# Explicit
parallel = RunnableParallel(
    summary=summary_chain,
    keywords=keyword_chain,
    sentiment=sentiment_chain
)

# Dict syntax (creates RunnableParallel)
parallel = {
    "summary": summary_chain,
    "keywords": keyword_chain,
    "sentiment": sentiment_chain
}

# All run concurrently!
result = parallel.invoke({"text": "..."})
# Output: {
#   "summary": "...",
#   "keywords": "...",
#   "sentiment": "..."
# }
```

**When to use**: Independent operations that can run concurrently

---

### 3. RunnableBranch
**Purpose**: Conditional routing based on input

```python
from langchain_core.runnables import RunnableBranch

branch = RunnableBranch(
    # (condition_function, runnable)
    (lambda x: x["type"] == "urgent", urgent_chain),
    (lambda x: x["type"] == "question", question_chain),
    default_chain  # Fallback
)

result = branch.invoke({"type": "urgent", "text": "..."})
```

**When to use**: Dynamic routing logic

---

### 4. RunnableLambda
**Purpose**: Wrap any Python function as a Runnable

```python
from langchain_core.runnables import RunnableLambda

def my_function(x):
    return x.upper()

# Wrap as runnable
runnable = RunnableLambda(my_function)

# Now it's composable!
chain = runnable | other_chain
```

**When to use**: Custom logic, data transformation

---

### 5. RunnablePassthrough
**Purpose**: Pass input through (with optional transformations)

```python
from langchain_core.runnables import RunnablePassthrough

# Simple passthrough
passthrough = RunnablePassthrough()
# Input: {"x": 5} → Output: {"x": 5}

# With assignment
chain = RunnablePassthrough.assign(
    squared=lambda x: x["num"] ** 2
)
# Input: {"num": 5} → Output: {"num": 5, "squared": 25}
```

**When to use**: Preserve input while adding computed fields

---

### 6. RunnableGenerator
**Purpose**: Create streaming runnables from generators

```python
from langchain_core.runnables import RunnableGenerator

def my_generator(input):
    for i in range(5):
        yield f"Chunk {i}: {input['text']}"

runnable = RunnableGenerator(my_generator)

# Streaming output
for chunk in runnable.stream({"text": "hello"}):
    print(chunk)
```

**When to use**: Custom streaming logic

---

### 7. RunnableBinding
**Purpose**: Bind configuration to a runnable

```python
from langchain_core.runnables import RunnableBinding

# Bind specific config
bound = model.bind(temperature=0.9, max_tokens=100)

# Always uses these settings
result = bound.invoke("hello")
```

**When to use**: Fix certain parameters

---

### 8. RunnableWithFallbacks
**Purpose**: Error handling with backup runnables

```python
# Created with with_fallbacks()
chain = primary_chain.with_fallbacks([
    backup_chain_1,
    backup_chain_2
])

# Tries primary, falls back on error
result = chain.invoke({"input": "value"})
```

**When to use**: Robust error handling

---

### 9. RunnableRetry
**Purpose**: Automatic retry on failure

```python
# Created with with_retry()
chain = unstable_chain.with_retry(
    retry_if_exception_type=[ConnectionError],
    stop_after_attempt=3,
    wait_exponential_jitter=True
)

result = chain.invoke({"input": "value"})
```

**When to use**: Handle transient failures

---

## ⚡ Execution Methods

### invoke() - Single Input
```python
result = runnable.invoke(
    input={"key": "value"},
    config={"metadata": {"user_id": "123"}}
)
```
**Use when**: Processing single request

---

### batch() - Multiple Inputs
```python
results = runnable.batch([
    {"key": "value1"},
    {"key": "value2"},
    {"key": "value3"}
])
# Returns: [result1, result2, result3]
```
**Use when**: Bulk processing, more efficient than loops

---

### stream() - Streaming Output
```python
for chunk in runnable.stream({"key": "value"}):
    print(chunk, end="", flush=True)
```
**Use when**: Real-time output, long responses

---

### Async Methods
```python
# Async invoke
result = await runnable.ainvoke({"key": "value"})

# Async batch
results = await runnable.abatch([...])

# Async stream
async for chunk in runnable.astream({"key": "value"}):
    print(chunk, end="")
```
**Use when**: Async frameworks (FastAPI, async apps)

---

## 🎨 Composition Patterns

### Pattern 1: Sequential Pipeline
```python
# Simple linear flow
pipeline = (
    step1
    | step2
    | step3
)
```

### Pattern 2: Parallel + Sequential
```python
# Parallel analysis, then synthesis
chain = (
    RunnableParallel(
        technical=technical_chain,
        business=business_chain
    )
    | synthesis_chain
)
```

### Pattern 3: Branching
```python
# Conditional routing
chain = (
    classifier
    | RunnableBranch(
        (is_urgent, urgent_handler),
        (is_complex, complex_handler),
        standard_handler
    )
)
```

### Pattern 4: Nested Composition
```python
# Complex nested structure
chain = (
    preprocessor
    | RunnableParallel(
        analysis=RunnableSequence(
            analyzer
            | validator
        ),
        metadata=metadata_extractor
    )
    | merger
    | postprocessor
)
```

---

## 🚀 Advanced Features

### 1. Input/Output Schemas
```python
# Inspect schemas
print(runnable.input_schema.schema())
print(runnable.output_schema.schema())
```

### 2. Configuration
```python
# Runtime config
config = {
    "metadata": {"user_id": "123"},
    "tags": ["production"],
    "callbacks": [my_callback],
    "max_concurrency": 5
}

result = runnable.invoke(input, config=config)
```

### 3. Coercion
```python
# Automatic type conversion
from langchain_core.runnables import RunnableSequence

# Strings become prompts
chain = "Tell me about {topic}" | model

# Dicts become RunnableParallel
chain = {
    "a": chain_a,
    "b": chain_b
} | merger
```

### 4. Map
```python
# Apply runnable to each item in list
from langchain_core.runnables import RunnableMap

results = runnable.map().invoke([item1, item2, item3])
```

### 5. Pick/Assign
```python
# Pick specific fields
chain = runnable | RunnableLambda(lambda x: {
    "result": x["field1"]
})

# Assign new fields
chain = RunnablePassthrough.assign(
    new_field=lambda x: compute(x)
)
```

---

## 💡 Best Practices

### ✅ DO

1. **Use Type Hints**
   ```python
   def my_func(x: dict) -> str:
       return x["text"].upper()
   ```

2. **Leverage Async for I/O**
   ```python
   results = await chain.abatch(inputs)
   ```

3. **Add Error Handling**
   ```python
   chain = primary.with_fallbacks([backup])
   ```

4. **Use Streaming for UX**
   ```python
   for chunk in chain.stream(input):
       display(chunk)
   ```

5. **Batch When Possible**
   ```python
   # Instead of
   for item in items:
       result = chain.invoke(item)
   
   # Use
   results = chain.batch(items)
   ```

### ❌ DON'T

1. **Don't Block Async Code**
   ```python
   # Bad
   result = chain.invoke(...)  # In async function
   
   # Good
   result = await chain.ainvoke(...)
   ```

2. **Don't Ignore Config**
   ```python
   # Bad
   chain.invoke(input)  # No metadata
   
   # Good
   chain.invoke(input, config={"metadata": {...}})
   ```

3. **Don't Forget Fallbacks**
   ```python
   # Production chains need error handling
   chain = chain.with_fallbacks([backup])
   ```

---

## 🎯 Common Use Cases

### 1. Custom Data Processing
```python
from langchain_core.runnables import RunnableLambda

def clean_data(x: dict) -> dict:
    return {
        "text": x["text"].strip().lower(),
        "timestamp": x.get("timestamp", "unknown")
    }

pipeline = RunnableLambda(clean_data) | processing_chain
```

### 2. Conditional Logic
```python
from langchain_core.runnables import RunnableBranch

router = RunnableBranch(
    (lambda x: x["priority"] == "high", fast_track),
    (lambda x: x["priority"] == "low", batch_queue),
    standard_process
)
```

### 3. Parallel Processing
```python
from langchain_core.runnables import RunnableParallel

analyzer = RunnableParallel(
    summary=summarize_chain,
    keywords=extract_keywords,
    sentiment=analyze_sentiment,
    entities=extract_entities
)
```

### 4. Streaming Applications
```python
from langchain_core.runnables import RunnableGenerator

def stream_responses(input):
    for item in process(input):
        yield item

streaming_chain = RunnableGenerator(stream_responses)
```

### 5. Error-Resilient Pipelines
```python
robust_chain = (
    primary_chain
    .with_retry(stop_after_attempt=3)
    .with_fallbacks([backup_chain])
)
```

---

## 🔍 Introspection & Debugging

### Get Chain Structure
```python
# See the structure
print(chain)
# Output: RunnableSequence(first=..., middle=[...], last=...)
```

### Get Schemas
```python
# Input/output types
print(chain.input_schema.schema())
print(chain.output_schema.schema())
```

### Add Logging
```python
from langchain_core.runnables import RunnableLambda

def log_step(x):
    print(f"Step output: {x}")
    return x

chain = (
    step1
    | RunnableLambda(log_step)
    | step2
)
```

### Callbacks
```python
from langchain_core.callbacks import BaseCallbackHandler

class MyCallback(BaseCallbackHandler):
    def on_chain_start(self, serialized, inputs, **kwargs):
        print(f"Chain started: {inputs}")
    
    def on_chain_end(self, outputs, **kwargs):
        print(f"Chain ended: {outputs}")

result = chain.invoke(input, config={"callbacks": [MyCallback()]})
```

---

## 📊 Comparison with Chains

| Feature | Chains (Old) | Runnables (New) |
|---------|--------------|-----------------|
| Interface | Various classes | Unified Runnable |
| Composition | Limited | Pipe operator |
| Streaming | Hit or miss | Built-in |
| Async | Separate methods | Native support |
| Type Safety | Limited | Full schema support |
| **Recommendation** | Legacy only | ✅ **Use this** |

---

## 🎓 Learning Path

1. **Start Here**: `01_runnable_interface.py`
   - Core Runnable methods
   - Invoke, batch, stream
   - Config handling

2. **Sequential**: `02_runnable_sequence.py`
   - Pipe operator deep dive
   - Sequential composition
   - Error propagation

3. **Parallel**: `03_runnable_parallel.py`
   - Concurrent execution
   - Performance optimization
   - Nested parallel

4. **Advanced**: `04_advanced_runnables.py`
   - Custom runnables
   - RunnableGenerator
   - Binding, retry, fallbacks

5. **Practical**: `05_practical_runnables.py`
   - Real-world projects
   - Production patterns
   - Best practices in action

---

## 🌟 Key Takeaways

1. **Everything is a Runnable**
   - Models, prompts, chains, parsers
   - Unified interface
   - Easy composition

2. **Pipe Operator is Magic**
   ```python
   chain = a | b | c
   ```
   - Clean syntax
   - Type-safe
   - Auto-optimization

3. **Three Execution Modes**
   - Single: `invoke()`
   - Batch: `batch()`
   - Stream: `stream()`

4. **Async is First-Class**
   - All methods have async versions
   - Native async support
   - Performance benefits

5. **Composability is King**
   - Mix and match freely
   - Nest arbitrarily deep
   - Automatic optimization

---

## 🔗 Related Concepts

- **Chains**: Built on top of Runnables
- **LCEL**: Expression language using Runnables
- **Agents**: Use Runnables internally
- **Memory**: Can be composed as Runnables

---

## 📚 Module Contents

```
runnables/
├── README.md                      # This file
├── 01_runnable_interface.py      # Core interface & methods
├── 02_runnable_sequence.py       # Sequential composition
├── 03_runnable_parallel.py       # Parallel execution
├── 04_advanced_runnables.py      # Custom, generator, binding
├── 05_practical_runnables.py     # Real-world projects
├── CHEATSHEET.md                 # Quick reference
└── ROADMAP.md                    # Learning path
```

---

## 🎯 Next Steps

After mastering Runnables, you'll be ready for:
- **Agents**: Tool-using AI agents
- **Memory**: Conversation state management
- **RAG**: Retrieval-augmented generation
- **Production**: Deployment with LangServe

---

**Let's dive into the world of Runnables! 🚀**

*The foundation of modern LangChain applications.*
