# 🔗 LangChain Chains - Complete Guide

## 📚 What are Chains?

**Chains** are the core building blocks in LangChain that let you **compose multiple components** into sophisticated workflows. Think of chains as pipelines that connect prompts, models, parsers, and other components together.

### 🎯 Real-World Analogy

Imagine a **restaurant kitchen**:
- **Single Component**: A chef (just the LLM)
- **Chain**: Chef → Prep cook → Quality checker → Server (full pipeline)

Each step processes the output of the previous step, creating a complete workflow!

---

## 🚀 LCEL: LangChain Expression Language

**LCEL** (LangChain Expression Language) is the **modern, declarative way** to build chains in LangChain (introduced 2023, standard in 2024).

### Why LCEL?

#### ❌ Old Way (Legacy)
```python
# Old LLMChain (deprecated)
from langchain.chains import LLMChain

chain = LLMChain(llm=model, prompt=prompt)
result = chain.run(input_data)
```

#### ✅ New Way (LCEL - Modern)
```python
# Modern LCEL
chain = prompt | model | parser
result = chain.invoke(input_data)
```

### 🎨 LCEL Benefits

| Feature | Description | Example |
|---------|-------------|---------|
| **Pipe Operator** | Chain with `\|` like Unix pipes | `prompt \| llm \| parser` |
| **Streaming** | Built-in streaming support | `chain.stream(input)` |
| **Async** | Native async/await support | `await chain.ainvoke(input)` |
| **Batch** | Process multiple inputs | `chain.batch([input1, input2])` |
| **Parallel** | Run steps concurrently | `RunnableParallel` |
| **Type Safety** | Better type hints | TypeScript-like experience |
| **Debugging** | Easy to inspect each step | Clear pipeline structure |

---

## 🔗 Chain Types Overview

```
┌─────────────────────────────────────────────┐
│           CHAIN TYPES IN LCEL               │
├─────────────────────────────────────────────┤
│                                             │
│  1. Sequential Chain                        │
│     ├─ Step 1 → Step 2 → Step 3            │
│     └─ Linear pipeline                      │
│                                             │
│  2. Parallel Chain                          │
│     ├─ Step 1A ┐                           │
│     ├─ Step 1B ├→ Merge → Step 2          │
│     └─ Step 1C ┘                           │
│                                             │
│  3. Conditional Chain                       │
│     ├─ If condition A → Path 1             │
│     ├─ If condition B → Path 2             │
│     └─ Else → Default Path                 │
│                                             │
│  4. Router Chain                            │
│     ├─ Analyze input                       │
│     └─ Route to specialist chain           │
│                                             │
│  5. Map-Reduce Chain                        │
│     ├─ Map: Process items in parallel      │
│     └─ Reduce: Combine results             │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 1️⃣ Sequential Chain (Multi-Step Pipeline)

**Use case:** When steps must happen in order, each using the previous output.

### Pattern
```python
chain = step1 | step2 | step3
```

### Example: Translation Pipeline
```python
# Step 1: Extract text
# Step 2: Translate
# Step 3: Format output

extraction_prompt = PromptTemplate(...)
translation_prompt = PromptTemplate(...)

chain = (
    extraction_prompt 
    | llm 
    | StrOutputParser() 
    | translation_prompt 
    | llm 
    | parser
)
```

### Real-World Uses
- 📝 Document processing (extract → summarize → categorize)
- 🔄 Data transformation (parse → validate → format)
- 🎯 Multi-stage analysis (classify → extract → score)

---

## 2️⃣ Parallel Chain (RunnableParallel)

**Use case:** When multiple independent operations can run concurrently.

### Pattern
```python
from langchain_core.runnables import RunnableParallel

chain = RunnableParallel(
    task1=chain1,
    task2=chain2,
    task3=chain3
)
```

### Example: Multi-Aspect Analysis
```python
# Analyze product review from multiple angles simultaneously
chain = RunnableParallel(
    sentiment=sentiment_chain,
    features=feature_extraction_chain,
    rating=rating_prediction_chain
)

result = chain.invoke({"review": "Great product!"})
# Result: {
#   "sentiment": "positive",
#   "features": ["quality", "price"],
#   "rating": 5
# }
```

### Real-World Uses
- ⚡ Performance optimization (parallel API calls)
- 🔍 Multi-perspective analysis
- 📊 Batch processing different attributes

---

## 3️⃣ Conditional Chain (RunnableBranch)

**Use case:** When the execution path depends on input or intermediate results.

### Pattern
```python
from langchain_core.runnables import RunnableBranch

chain = RunnableBranch(
    (condition1, chain_for_condition1),
    (condition2, chain_for_condition2),
    default_chain  # Fallback
)
```

### Example: Smart Routing
```python
def is_technical(x):
    return "code" in x["question"].lower()

def is_general(x):
    return "how" in x["question"].lower()

chain = RunnableBranch(
    (is_technical, technical_expert_chain),
    (is_general, general_assistant_chain),
    default_chain
)
```

### Real-World Uses
- 🎯 Intent-based routing
- 🔀 Dynamic workflow selection
- 🛡️ Fallback handling

---

## 4️⃣ Router Chain

**Use case:** Intelligent routing to specialized sub-chains based on content.

### Pattern
```python
# Analyze input → Route to specialist
router = (
    {"question": RunnablePassthrough()}
    | router_prompt
    | llm
    | router_parser
)

# Then route to specialist chains
```

### Example: Customer Support Router
```python
chains = {
    "technical": technical_support_chain,
    "billing": billing_support_chain,
    "general": general_support_chain
}

# Route based on classification
final_chain = router | RunnableLambda(
    lambda x: chains[x["category"]]
)
```

### Real-World Uses
- 🎯 Multi-specialist systems
- 📞 Customer support routing
- 🔍 Domain-specific processing

---

## 5️⃣ Map-Reduce Chain

**Use case:** Process multiple items in parallel, then combine results.

### Pattern
```python
# Map: Process each item
# Reduce: Combine all results

map_chain = RunnableParallel(**{
    f"item_{i}": process_chain 
    for i in range(n)
})

reduce_chain = combine_chain

full_chain = map_chain | reduce_chain
```

### Example: Multi-Document Summarization
```python
# Map: Summarize each document
doc_chains = {
    f"doc_{i}": summarize_chain 
    for i, doc in enumerate(documents)
}

map_step = RunnableParallel(**doc_chains)

# Reduce: Combine summaries
reduce_step = final_summary_chain

chain = map_step | reduce_step
```

### Real-World Uses
- 📚 Multi-document analysis
- 📊 Aggregating multiple sources
- 🔄 Batch processing with consolidation

---

## 🧰 LCEL Core Components

### 1. RunnablePassthrough
**Pass data through unchanged** (useful for preserving original input)

```python
from langchain_core.runnables import RunnablePassthrough

chain = {
    "original": RunnablePassthrough(),
    "processed": prompt | llm
}
```

### 2. RunnableLambda
**Custom Python function** as a chain step

```python
from langchain_core.runnables import RunnableLambda

def custom_processor(x):
    return x.upper()

chain = RunnableLambda(custom_processor) | llm
```

### 3. RunnableMap
**Transform data structure** (similar to dict comprehension)

```python
chain = RunnableMap({
    "question": lambda x: x["query"],
    "context": retriever
})
```

### 4. RunnableSequence
**Explicit sequential chain** (usually created with `|`)

```python
from langchain_core.runnables import RunnableSequence

chain = RunnableSequence(
    first=prompt,
    middle=llm,
    last=parser
)
# Same as: prompt | llm | parser
```

### 5. assign() - Add to Existing Dict
**Add new fields** without replacing original

```python
chain = (
    RunnablePassthrough.assign(
        summary=summarize_chain,
        keywords=keyword_chain
    )
)

# Input: {"text": "..."}
# Output: {"text": "...", "summary": "...", "keywords": [...]}
```

### 6. pick() - Select Fields
**Extract specific fields** from dict

```python
chain = some_chain | RunnablePassthrough.pick("result")

# Input: {"result": "A", "metadata": {...}}
# Output: "A"
```

---

## ⚡ Execution Methods

### 1. invoke() - Single Input
```python
result = chain.invoke({"input": "Hello"})
```

### 2. batch() - Multiple Inputs
```python
results = chain.batch([
    {"input": "Hello"},
    {"input": "Hi"}
])
```

### 3. stream() - Streaming Output
```python
for chunk in chain.stream({"input": "Hello"}):
    print(chunk, end="", flush=True)
```

### 4. ainvoke() - Async Single
```python
result = await chain.ainvoke({"input": "Hello"})
```

### 5. abatch() - Async Multiple
```python
results = await chain.abatch([inputs...])
```

### 6. astream() - Async Streaming
```python
async for chunk in chain.astream({"input": "Hello"}):
    print(chunk, end="", flush=True)
```

---

## 🎯 When to Use What

| Need | Use This | Example |
|------|----------|---------|
| Steps in order | Sequential | Extract → Translate → Format |
| Steps independent | Parallel | Sentiment + Features + Rating |
| Different paths | Conditional | If technical → Expert A, else Expert B |
| Content-based routing | Router | Support: Tech/Billing/General |
| Process many → combine | Map-Reduce | Summarize docs → Combine |
| Pass data through | RunnablePassthrough | Preserve original input |
| Custom logic | RunnableLambda | Your Python function |
| Add to dict | assign() | Add summary to existing data |
| Extract fields | pick() | Get only the result field |

---

## 🔄 Data Flow Patterns

### Pattern 1: Linear Pipeline
```python
# Input → Step 1 → Step 2 → Step 3 → Output
chain = step1 | step2 | step3
```

### Pattern 2: Fan-Out (Parallel Processing)
```python
# Input → [Step 1A, Step 1B, Step 1C] → Merge → Output
chain = RunnableParallel(a=step1a, b=step1b, c=step1c) | merge
```

### Pattern 3: Conditional Branch
```python
# Input → Evaluate → Path A or Path B → Output
chain = RunnableBranch(
    (condition, path_a),
    path_b  # default
)
```

### Pattern 4: Preserve & Process
```python
# Input → [Keep Original, Process] → Combined Output
chain = {
    "original": RunnablePassthrough(),
    "processed": processing_chain
}
```

### Pattern 5: Map-Transform-Reduce
```python
# Input → Map to dict → Process → Pick result
chain = (
    RunnableMap({...})
    | processing_chain
    | RunnablePassthrough.pick("result")
)
```

---

## 🚨 Common Mistakes

### ❌ Mistake 1: Not preserving input
```python
# Input lost after first step!
chain = prompt | llm | parser
```

### ✅ Solution: Use RunnablePassthrough
```python
chain = {
    "original": RunnablePassthrough(),
    "processed": prompt | llm | parser
}
```

### ❌ Mistake 2: Sequential when parallel possible
```python
# Slow: Steps run one by one
chain = step1 | step2 | step3  # If independent!
```

### ✅ Solution: Use RunnableParallel
```python
# Fast: Steps run concurrently
chain = RunnableParallel(
    a=step1,
    b=step2,
    c=step3
)
```

### ❌ Mistake 3: Using old LLMChain syntax
```python
# Old, deprecated
from langchain.chains import LLMChain
chain = LLMChain(llm=model, prompt=prompt)
```

### ✅ Solution: Use LCEL
```python
# Modern LCEL
chain = prompt | model | parser
```

---

## 🎨 Advanced Patterns

### Pattern: Retry with Fallback
```python
from langchain_core.runnables import RunnableWithFallbacks

primary_chain = prompt | llm | parser

chain_with_fallback = primary_chain.with_fallbacks(
    fallbacks=[fallback_chain],
    exceptions_to_handle=(ValueError,)
)
```

### Pattern: Add Config/Metadata
```python
chain = prompt | llm.with_config(
    tags=["my-chain"],
    metadata={"version": "1.0"}
)
```

### Pattern: Batch with Concurrency
```python
results = chain.batch(
    inputs,
    config={"max_concurrency": 5}
)
```

### Pattern: Transform Input
```python
def prepare_input(x):
    return {"question": x["query"].upper()}

chain = RunnableLambda(prepare_input) | prompt | llm
```

---

## 📊 Performance Comparison

| Approach | Speed | When to Use |
|----------|-------|-------------|
| Sequential | 🐌 Slow | Steps depend on each other |
| Parallel | 🚀 Fast | Independent operations |
| Conditional | ⚡ Variable | Different complexity per path |
| Map-Reduce | 🚀 Fast (map) | Process many items |

**Example:**
- Sequential (3 steps × 1s each) = **3 seconds**
- Parallel (3 steps × 1s each) = **1 second** ⚡

---

## 🎓 Best Practices

### 1. ✅ Use LCEL (Modern Syntax)
```python
# Good
chain = prompt | llm | parser
```

### 2. ✅ Parallelize When Possible
```python
# Good: Independent operations run concurrently
chain = RunnableParallel(sentiment=..., entities=...)
```

### 3. ✅ Preserve Context
```python
# Good: Keep original input
chain = {
    "original": RunnablePassthrough(),
    "result": processing_chain
}
```

### 4. ✅ Use Type Hints
```python
from typing import Dict, Any

def my_processor(x: Dict[str, Any]) -> str:
    return x["text"].upper()
```

### 5. ✅ Handle Errors
```python
chain = primary_chain.with_fallbacks(
    fallbacks=[fallback_chain]
)
```

### 6. ✅ Name Your Chains
```python
# Good: Clear pipeline structure
summarize_chain = prompt | llm | parser
translate_chain = trans_prompt | llm | parser

full_chain = summarize_chain | translate_chain
```

### 7. ✅ Use assign() for Adding Fields
```python
chain = RunnablePassthrough.assign(
    summary=summarize_chain,
    keywords=extract_keywords_chain
)
```

### 8. ✅ Stream for Long Outputs
```python
for chunk in chain.stream(input):
    print(chunk, end="", flush=True)
```

---

## 🔍 Debugging Chains

### Inspect Chain Structure
```python
# See the chain composition
print(chain)
```

### Test Individual Steps
```python
# Test each step separately
step1_output = step1.invoke(input)
step2_output = step2.invoke(step1_output)
```

### Add Logging
```python
def log_step(x):
    print(f"Step output: {x}")
    return x

chain = step1 | RunnableLambda(log_step) | step2
```

### Use Callbacks
```python
from langchain.callbacks import StdOutCallbackHandler

chain.invoke(input, config={
    "callbacks": [StdOutCallbackHandler()]
})
```

---

## 📚 Quick Reference

### Creating Chains
```python
# Sequential
chain = step1 | step2 | step3

# Parallel
chain = RunnableParallel(a=step1, b=step2)

# Conditional
chain = RunnableBranch(
    (condition, if_true_chain),
    else_chain
)

# With passthrough
chain = {
    "original": RunnablePassthrough(),
    "processed": process_chain
}

# With assign
chain = RunnablePassthrough.assign(new_field=process_chain)

# With pick
chain = some_chain | RunnablePassthrough.pick("result")
```

### Running Chains
```python
# Single
result = chain.invoke(input)

# Multiple
results = chain.batch([input1, input2])

# Streaming
for chunk in chain.stream(input):
    print(chunk)

# Async
result = await chain.ainvoke(input)
```

---

## 🎯 Next Steps

After mastering chains, you'll learn about:
1. **Runnables** - Deep dive into Runnable interface
2. **Memory** - Add conversation history to chains
3. **Agents** - Chains that can use tools
4. **RAG** - Retrieval-Augmented Generation chains

---

## 💡 Remember

✅ **LCEL is the modern way** - Use `|` operator
✅ **Parallelize when possible** - RunnableParallel for speed
✅ **Preserve context** - RunnablePassthrough, assign()
✅ **Handle errors** - with_fallbacks()
✅ **Stream long outputs** - chain.stream()
✅ **Test incrementally** - Debug step by step

**Chains are the backbone of LangChain applications!** 🚀

---

Ready to build powerful AI pipelines? Let's dive into the examples! 🎊
