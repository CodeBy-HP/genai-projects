# 🗺️ LangChain Runnables - Learning Roadmap

## 🎯 Learning Objectives

By completing this module, you will:
- ✅ Master the Runnable interface
- ✅ Understand all runnable types
- ✅ Build sequential and parallel pipelines
- ✅ Create custom runnables
- ✅ Implement production-ready patterns

---

## 📚 Learning Path

### **Stage 1: Runnable Interface** (1 hour)
📖 **File:** `01_runnable_interface.py`

**Topics Covered:**
1. Core methods (invoke, batch, stream)
2. Async execution (ainvoke, abatch, astream)
3. Runtime configuration
4. Input/output schemas
5. Method chaining
6. Custom Runnable classes
7. Inspection and debugging
8. Config propagation

**Learning Outcomes:**
- Understand unified Runnable interface
- Execute runnables in different modes
- Use configuration effectively
- Build custom runnables

**Practice Exercise:**
Create a custom Runnable that logs execution time

---

### **Stage 2: Sequential Composition** (1 hour)
📖 **File:** `02_runnable_sequence.py`

**Topics Covered:**
1. Pipe operator basics
2. Manual RunnableSequence
3. Automatic coercion
4. Streaming behavior
5. Error propagation
6. Nested sequences
7. Intermediate access
8. Performance optimization

**Learning Outcomes:**
- Master pipe operator (|)
- Understand type coercion
- Handle errors in sequences
- Optimize sequential pipelines

**Practice Exercise:**
Build a 5-step data transformation pipeline

---

### **Stage 3: Parallel Execution** (1 hour)
📖 **File:** `03_runnable_parallel.py`

**Topics Covered:**
1. Basic RunnableParallel
2. Dict syntax
3. Performance comparison
4. Nested parallel
5. Error handling
6. Parallel with passthrough
7. Dynamic parallel
8. Batch + parallel

**Learning Outcomes:**
- Run operations concurrently
- Measure performance gains
- Handle errors in parallel
- Combine batch and parallel

**Practice Exercise:**
Create parallel analysis system with 4+ perspectives

---

### **Stage 4: Advanced Runnables** (1-2 hours)
📖 **File:** `04_advanced_runnables.py`

**Topics Covered:**
1. RunnableGenerator (streaming)
2. RunnableBinding (config)
3. RunnableWithFallbacks
4. RunnableRetry
5. Custom runnable classes
6. Field selection
7. Advanced configuration
8. Production patterns

**Learning Outcomes:**
- Create custom streaming
- Implement retry/fallback
- Build robust systems
- Apply production patterns

**Practice Exercise:**
Build a monitored, fault-tolerant chain

---

### **Stage 5: Practical Projects** (2 hours)
📖 **File:** `05_practical_runnables.py`

**Real-World Projects:**
1. **Custom Text Processor**
   - Runnable toolkit
   - Multiple operations
   - AI integration

2. **Streaming Chat System**
   - Real-time responses
   - Conversation history
   - Context awareness

3. **Robust API Client**
   - Retry logic
   - Fallback handling
   - Metrics tracking

4. **Batch Document Processor**
   - High throughput
   - Parallel analysis
   - Performance optimization

5. **Async Pipeline**
   - Non-blocking I/O
   - Concurrent execution
   - Async streaming

6. **Monitoring Wrapper**
   - Performance tracking
   - Error monitoring
   - Comprehensive reports

**Learning Outcomes:**
- Build production systems
- Combine all runnable types
- Apply best practices
- Solve real problems

**Practice Exercise:**
Extend one project with additional features

---

## 🎓 Skill Progression

### Beginner Level
- [x] Understand Runnable interface
- [x] Use invoke/batch/stream
- [x] Compose with pipe operator
- [x] Create simple chains

### Intermediate Level
- [x] Build parallel operations
- [x] Handle errors with fallbacks
- [x] Implement retry logic
- [x] Create custom runnables

### Advanced Level
- [x] Optimize for performance
- [x] Build monitoring systems
- [x] Implement async pipelines
- [x] Deploy to production

---

## 📊 Time Investment

| Stage | Time | Difficulty | Priority |
|-------|------|------------|----------|
| Interface | 1h | ⭐ Easy | 🔴 Critical |
| Sequential | 1h | ⭐ Easy | 🔴 Critical |
| Parallel | 1h | ⭐⭐ Medium | 🟡 Important |
| Advanced | 1-2h | ⭐⭐⭐ Hard | 🟡 Important |
| Practical | 2h | ⭐⭐⭐ Hard | 🟢 Optional |

**Total:** 6-8 hours for complete mastery

---

## 🎯 Learning Strategy

### Day 1: Foundations
- Morning: Runnable Interface (01)
- Afternoon: Sequential Composition (02)
- Evening: Review and practice

### Day 2: Advanced
- Morning: Parallel Execution (03)
- Afternoon: Advanced Runnables (04)
- Evening: Review and practice

### Day 3: Application
- Morning: Practical Projects 1-3 (05)
- Afternoon: Practical Projects 4-6 (05)
- Evening: Build your own project

---

## 📝 Checkpoints

After each stage, you should be able to:

### ✅ After Stage 1
- [ ] Explain what a Runnable is
- [ ] Use invoke/batch/stream
- [ ] Pass configuration
- [ ] Create custom Runnable

### ✅ After Stage 2
- [ ] Compose with pipe operator
- [ ] Understand type coercion
- [ ] Build multi-step pipelines
- [ ] Debug sequences

### ✅ After Stage 3
- [ ] Use RunnableParallel
- [ ] Measure performance gains
- [ ] Combine batch + parallel
- [ ] Handle parallel errors

### ✅ After Stage 4
- [ ] Implement retry/fallback
- [ ] Create custom streaming
- [ ] Build robust chains
- [ ] Apply production patterns

### ✅ After Stage 5
- [ ] Build complete systems
- [ ] Combine all patterns
- [ ] Optimize performance
- [ ] Deploy to production

---

## 🔍 Self-Assessment

### Quiz Yourself

1. **What's the difference between invoke() and batch()?**
   - Answer: invoke() processes single input, batch() processes multiple inputs more efficiently

2. **When should you use RunnableParallel?**
   - Answer: When operations are independent and can run concurrently

3. **How do you handle errors in runnables?**
   - Answer: Use with_fallbacks() for backups, with_retry() for transient failures

4. **What does the pipe operator (|) create?**
   - Answer: RunnableSequence (sequential composition)

5. **What's automatic coercion?**
   - Answer: LangChain converts strings→PromptTemplate, dicts→RunnableParallel, functions→RunnableLambda

---

## 🛠️ Practice Projects

### Beginner
1. **Text Analyzer**
   - Count words, chars, sentences
   - Generate statistics
   - Format output

2. **Simple API Wrapper**
   - Wrap external API
   - Add error handling
   - Return structured data

### Intermediate
1. **Document Pipeline**
   - Clean text
   - Extract entities
   - Categorize content

2. **Multi-Step Processor**
   - Validate input
   - Transform data
   - Generate output

### Advanced
1. **Production Chat System**
   - Streaming responses
   - Context management
   - Error recovery

2. **Batch Analysis Tool**
   - Process multiple documents
   - Parallel analysis
   - Comprehensive reports

---

## 📚 Additional Resources

### Recommended Reading Order
1. README.md - Overview
2. 01_runnable_interface.py - Foundation
3. 02_runnable_sequence.py - Composition
4. 03_runnable_parallel.py - Performance
5. 04_advanced_runnables.py - Advanced patterns
6. 05_practical_runnables.py - Real projects
7. CHEATSHEET.md - Quick reference

### When You're Stuck
- Review README for concepts
- Check CHEATSHEET for syntax
- Run examples step by step
- Test components individually
- Start simple, add complexity

---

## 🎯 Next Steps

After mastering Runnables, you're ready for:

1. **Agents**
   - Tool-using AI
   - ReAct pattern
   - Agent executors

2. **Memory Systems**
   - Conversation buffers
   - Vector store memory
   - Entity memory

3. **RAG (Retrieval Augmented Generation)**
   - Vector stores
   - Retrievers
   - Document loaders

4. **Production Deployment**
   - LangServe
   - Monitoring
   - Scaling

---

## 💡 Pro Tips

1. **Start Simple**
   - Master basics first
   - Build complexity gradually
   - Test frequently

2. **Think in Pipelines**
   - Input → Transform → Output
   - Break into steps
   - Use appropriate runnable type

3. **Optimize Later**
   - Make it work first
   - Then make it fast
   - Measure before optimizing

4. **Handle Errors**
   - Always add fallbacks
   - Retry transient failures
   - Validate inputs early

5. **Monitor Everything**
   - Track performance
   - Log important events
   - Measure success rates

---

## 🌟 Success Metrics

You've mastered Runnables when you can:

- ✅ Build any type of runnable
- ✅ Compose complex pipelines
- ✅ Optimize for performance
- ✅ Handle errors gracefully
- ✅ Debug effectively
- ✅ Deploy to production

---

## 📅 30-Day Challenge

### Week 1: Foundations
- Days 1-2: Interface + Sequential
- Days 3-4: Parallel + Practice
- Days 5-7: Review + Mini-projects

### Week 2: Advanced
- Days 8-10: Advanced Runnables
- Days 11-14: Practice + Experimentation

### Week 3: Practical
- Days 15-17: Projects 1-3
- Days 18-21: Projects 4-6

### Week 4: Mastery
- Days 22-24: Build custom project
- Days 25-27: Optimize + Refine
- Days 28-30: Document + Share

---

**Happy Learning! 🚀**

*Remember: Runnables are the foundation of modern LangChain!*