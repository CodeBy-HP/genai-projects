"""
⚡ RunnableParallel - Concurrent Execution

Master parallel execution patterns:
1. Basic Parallel - RunnableParallel fundamentals
2. Dict Syntax - Convenient dictionary creation
3. Performance Comparison - Parallel vs Sequential
4. Nested Parallel - Complex concurrent structures
5. Error Handling - Failures in parallel execution
6. Parallel with Passthrough - Preserving input
7. Dynamic Parallel - Runtime parallelization
8. Batch Parallel - Combining batch + parallel

Optimize for performance!
"""

import os
import asyncio
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    RunnableParallel,
    RunnableLambda,
    RunnablePassthrough
)
from typing import Dict, Any, List
import time

# Load environment variables
load_dotenv()


def basic_parallel():
    """Example 1: Basic RunnableParallel"""
    
    print("=" * 70)
    print("⚡ Example 1: Basic RunnableParallel")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.6,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    print("\n🚀 Run multiple operations concurrently")
    
    # Create parallel operations
    parallel = RunnableParallel(
        summary=PromptTemplate.from_template(
            "Summarize in one sentence: {text}"
        ) | chat | StrOutputParser(),
        
        keywords=PromptTemplate.from_template(
            "Extract 3 keywords from: {text}"
        ) | chat | StrOutputParser(),
        
        sentiment=PromptTemplate.from_template(
            "What's the sentiment (positive/negative/neutral): {text}"
        ) | chat | StrOutputParser()
    )
    
    print("\n📊 Parallel operations:")
    print("   1. Summary")
    print("   2. Keywords")
    print("   3. Sentiment")
    print("   All run concurrently!")
    
    text = "Artificial intelligence is revolutionizing healthcare with breakthrough innovations"
    
    start = time.time()
    result = parallel.invoke({"text": text})
    duration = time.time() - start
    
    print(f"\n✅ Results (completed in {duration:.2f}s):")
    print(f"   Summary: {result['summary']}")
    print(f"   Keywords: {result['keywords']}")
    print(f"   Sentiment: {result['sentiment']}")
    
    print("\n💡 RunnableParallel returns a dict with all results")
    print()


def dict_syntax():
    """Example 2: Dictionary syntax for parallel"""
    
    print("=" * 70)
    print("📝 Example 2: Dict Syntax")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.5,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    print("\n✨ Dict automatically becomes RunnableParallel")
    
    # Method 1: Explicit RunnableParallel
    parallel_explicit = RunnableParallel(
        uppercase=RunnableLambda(lambda x: x["text"].upper()),
        lowercase=RunnableLambda(lambda x: x["text"].lower()),
        length=RunnableLambda(lambda x: len(x["text"]))
    )
    
    # Method 2: Dict syntax (cleaner!)
    parallel_dict = {
        "uppercase": RunnableLambda(lambda x: x["text"].upper()),
        "lowercase": RunnableLambda(lambda x: x["text"].lower()),
        "length": RunnableLambda(lambda x: len(x["text"]))
    }
    
    print("\n1️⃣ Explicit RunnableParallel:")
    result1 = parallel_explicit.invoke({"text": "Hello World"})
    print(f"   {result1}")
    
    print("\n2️⃣ Dict syntax (recommended):")
    result2 = parallel_dict.invoke({"text": "Hello World"})
    print(f"   {result2}")
    
    # Using in a chain
    print("\n3️⃣ Dict in a chain:")
    
    analysis_chain = (
        {
            "word_count": RunnableLambda(lambda x: len(x["text"].split())),
            "char_count": RunnableLambda(lambda x: len(x["text"])),
            "analysis": PromptTemplate.from_template(
                "Analyze: {text}"
            ) | chat | StrOutputParser()
        }
        | RunnableLambda(lambda x: f"Stats: {x['word_count']} words, {x['char_count']} chars\nAnalysis: {x['analysis'][:50]}...")
    )
    
    result = analysis_chain.invoke({"text": "AI is transforming the world"})
    print(f"   {result}")
    
    print("\n💡 Dict syntax is:")
    print("   • More concise")
    print("   • More Pythonic")
    print("   • Industry standard")
    print()


def performance_comparison():
    """Example 3: Parallel vs Sequential performance"""
    
    print("=" * 70)
    print("🏎️ Example 3: Performance Comparison")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.5,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    text = "Machine learning enables computers to learn from data without explicit programming"
    
    # Define operations
    op1 = PromptTemplate.from_template("Summarize: {text}") | chat | StrOutputParser()
    op2 = PromptTemplate.from_template("Keywords: {text}") | chat | StrOutputParser()
    op3 = PromptTemplate.from_template("Category: {text}") | chat | StrOutputParser()
    
    # Sequential execution
    print("\n1️⃣ Sequential execution:")
    start = time.time()
    
    result_seq = {
        "summary": op1.invoke({"text": text}),
        "keywords": op2.invoke({"text": text}),
        "category": op3.invoke({"text": text})
    }
    
    duration_seq = time.time() - start
    print(f"   Time: {duration_seq:.2f}s")
    print(f"   Summary: {result_seq['summary'][:40]}...")
    print(f"   Keywords: {result_seq['keywords'][:40]}...")
    print(f"   Category: {result_seq['category'][:40]}...")
    
    # Parallel execution
    print("\n2️⃣ Parallel execution:")
    parallel = {
        "summary": op1,
        "keywords": op2,
        "category": op3
    }
    
    start = time.time()
    result_par = parallel.invoke({"text": text})
    duration_par = time.time() - start
    
    print(f"   Time: {duration_par:.2f}s")
    print(f"   Summary: {result_par['summary'][:40]}...")
    print(f"   Keywords: {result_par['keywords'][:40]}...")
    print(f"   Category: {result_par['category'][:40]}...")
    
    # Performance gain
    speedup = duration_seq / duration_par if duration_par > 0 else 1
    print(f"\n⚡ Performance gain: {speedup:.1f}x faster!")
    print(f"   Sequential: {duration_seq:.2f}s")
    print(f"   Parallel: {duration_par:.2f}s")
    print(f"   Saved: {duration_seq - duration_par:.2f}s")
    
    print("\n💡 Use parallel when operations are:")
    print("   • Independent (no dependencies)")
    print("   • I/O bound (API calls, database)")
    print("   • Time-consuming")
    print()


def nested_parallel():
    """Example 4: Nested parallel structures"""
    
    print("=" * 70)
    print("🏗️ Example 4: Nested Parallel")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.5,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    print("\n🔄 Parallel operations can be nested")
    
    # Nested parallel structure
    complex_analysis = {
        "text_stats": {
            "word_count": RunnableLambda(lambda x: len(x["text"].split())),
            "char_count": RunnableLambda(lambda x: len(x["text"])),
            "sentence_count": RunnableLambda(lambda x: x["text"].count('.') + x["text"].count('!'))
        },
        "ai_analysis": {
            "summary": PromptTemplate.from_template("Summarize: {text}") | chat | StrOutputParser(),
            "sentiment": PromptTemplate.from_template("Sentiment: {text}") | chat | StrOutputParser()
        }
    }
    
    text = "AI is amazing! It's transforming industries. The future is bright."
    
    print("\n📊 Nested structure:")
    print("   Level 1: text_stats || ai_analysis")
    print("   Level 2: word/char/sentence || summary/sentiment")
    print("   All run concurrently!")
    
    result = complex_analysis.invoke({"text": text})
    
    print("\n✅ Results:")
    print(f"   Text Stats:")
    print(f"      Words: {result['text_stats']['word_count']}")
    print(f"      Chars: {result['text_stats']['char_count']}")
    print(f"      Sentences: {result['text_stats']['sentence_count']}")
    print(f"   AI Analysis:")
    print(f"      Summary: {result['ai_analysis']['summary'][:40]}...")
    print(f"      Sentiment: {result['ai_analysis']['sentiment'][:40]}...")
    
    print("\n💡 Nested parallel enables:")
    print("   • Organized complex operations")
    print("   • Hierarchical result structure")
    print("   • Maximum concurrency")
    print()


def error_handling():
    """Example 5: Error handling in parallel"""
    
    print("=" * 70)
    print("❌ Example 5: Error Handling")
    print("=" * 70)
    
    print("\n🚨 Handling errors in parallel execution")
    
    def success_op(x: Dict[str, Any]) -> str:
        return "Success!"
    
    def error_op(x: Dict[str, Any]) -> str:
        raise ValueError("Intentional error!")
    
    # Parallel with one failing operation
    parallel_with_error = {
        "op1": RunnableLambda(success_op),
        "op2": RunnableLambda(error_op),
        "op3": RunnableLambda(success_op)
    }
    
    print("\n1️⃣ Without error handling:")
    try:
        result = parallel_with_error.invoke({"input": "test"})
        print(f"   Result: {result}")
    except Exception as e:
        print(f"   ✗ Error caught: {type(e).__name__}: {e}")
        print("   ✗ Entire parallel operation failed!")
    
    # Solution: Add fallbacks
    print("\n2️⃣ With fallback protection:")
    
    safe_error_op = RunnableLambda(error_op).with_fallbacks([
        RunnableLambda(lambda x: "Fallback result")
    ])
    
    parallel_safe = {
        "op1": RunnableLambda(success_op),
        "op2": safe_error_op,
        "op3": RunnableLambda(success_op)
    }
    
    result = parallel_safe.invoke({"input": "test"})
    print(f"   ✓ Result: {result}")
    print("   ✓ Fallback prevented failure!")
    
    # Solution: Try/catch in lambda
    print("\n3️⃣ Try/catch in operation:")
    
    def safe_operation(x: Dict[str, Any]) -> str:
        try:
            raise ValueError("Error!")
        except Exception as e:
            return f"Handled error: {e}"
    
    parallel_trycatch = {
        "op1": RunnableLambda(success_op),
        "op2": RunnableLambda(safe_operation),
        "op3": RunnableLambda(success_op)
    }
    
    result = parallel_trycatch.invoke({"input": "test"})
    print(f"   ✓ Result: {result}")
    
    print("\n💡 Error handling strategies:")
    print("   • Use with_fallbacks() for robustness")
    print("   • Try/catch within operations")
    print("   • Validate inputs early")
    print("   • Return partial results when possible")
    print()


def parallel_with_passthrough():
    """Example 6: Combining parallel with passthrough"""
    
    print("=" * 70)
    print("🔄 Example 6: Parallel with Passthrough")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.5,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    print("\n📦 Preserve input while adding parallel results")
    
    # Pattern: RunnablePassthrough.assign(**parallel_operations)
    chain = RunnablePassthrough.assign(
        **{
            "summary": PromptTemplate.from_template(
                "Summarize: {text}"
            ) | chat | StrOutputParser(),
            
            "keywords": PromptTemplate.from_template(
                "Keywords: {text}"
            ) | chat | StrOutputParser(),
            
            "word_count": RunnableLambda(lambda x: len(x["text"].split()))
        }
    )
    
    text = "Cloud computing enables scalable and flexible infrastructure"
    
    result = chain.invoke({"text": text})
    
    print(f"\n✅ Results:")
    print(f"   Original text: {result['text']}")
    print(f"   Summary: {result['summary']}")
    print(f"   Keywords: {result['keywords']}")
    print(f"   Word count: {result['word_count']}")
    
    # Using in a pipeline
    print("\n🔗 In a pipeline:")
    
    pipeline = (
        RunnablePassthrough.assign(
            **{
                "analysis1": RunnableLambda(lambda x: f"Analysis of: {x['topic']}"),
                "analysis2": RunnableLambda(lambda x: f"More about: {x['topic']}")
            }
        )
        | RunnableLambda(lambda x: f"Topic: {x['topic']}\n1. {x['analysis1']}\n2. {x['analysis2']}")
    )
    
    result = pipeline.invoke({"topic": "AI"})
    print(f"   {result}")
    
    print("\n💡 This pattern is perfect for:")
    print("   • Enriching data with analysis")
    print("   • Preserving context")
    print("   • Building comprehensive outputs")
    print()


def dynamic_parallel():
    """Example 7: Dynamic parallel execution"""
    
    print("=" * 70)
    print("🎯 Example 7: Dynamic Parallel")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.5,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    print("\n🔧 Build parallel operations at runtime")
    
    def create_dynamic_parallel(analyses: List[str]):
        """Create parallel operations based on list"""
        operations = {}
        
        for analysis in analyses:
            operations[analysis] = (
                PromptTemplate.from_template(f"{{text}} - {analysis} analysis:")
                | chat
                | StrOutputParser()
            )
        
        return operations
    
    # Dynamic parallel based on user choice
    print("\n1️⃣ User chooses analyses:")
    user_analyses = ["technical", "business", "user experience"]
    
    parallel_ops = create_dynamic_parallel(user_analyses)
    parallel_chain = RunnablePassthrough.assign(**parallel_ops)
    
    result = parallel_chain.invoke({
        "text": "New mobile app for productivity"
    })
    
    print(f"   Requested: {', '.join(user_analyses)}")
    for key, value in result.items():
        if key != "text":
            print(f"   {key}: {value[:40]}...")
    
    # Conditional parallel
    print("\n2️⃣ Conditional parallel execution:")
    
    def conditional_parallel(x: Dict[str, Any]):
        """Only run expensive operations if needed"""
        operations = {
            "basic": RunnableLambda(lambda x: "Basic analysis")
        }
        
        if x.get("detailed"):
            operations["summary"] = (
                PromptTemplate.from_template("Detailed summary: {text}")
                | chat
                | StrOutputParser()
            )
            operations["keywords"] = (
                PromptTemplate.from_template("Extract keywords: {text}")
                | chat
                | StrOutputParser()
            )
        
        return operations.invoke(x)
    
    # Basic request
    result1 = RunnableLambda(conditional_parallel).invoke({
        "text": "Hello world",
        "detailed": False
    })
    print(f"   Basic result: {result1}")
    
    # Detailed request
    result2 = RunnableLambda(conditional_parallel).invoke({
        "text": "AI transforms industries",
        "detailed": True
    })
    print(f"   Detailed result: {list(result2.keys())}")
    
    print("\n💡 Dynamic parallel enables:")
    print("   • User-configurable analysis")
    print("   • Cost optimization")
    print("   • Flexible workflows")
    print()


def batch_parallel():
    """Example 8: Combining batch and parallel"""
    
    print("=" * 70)
    print("📦 Example 8: Batch + Parallel")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.5,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    print("\n⚡⚡ Maximum performance: Batch + Parallel")
    
    # Parallel operations
    parallel_analysis = {
        "summary": PromptTemplate.from_template("Summarize: {text}") | chat | StrOutputParser(),
        "sentiment": PromptTemplate.from_template("Sentiment: {text}") | chat | StrOutputParser()
    }
    
    # Multiple texts to process
    texts = [
        {"text": "AI is revolutionizing healthcare"},
        {"text": "Climate change requires urgent action"},
        {"text": "Space exploration inspires humanity"}
    ]
    
    print(f"\n📊 Processing {len(texts)} texts")
    print("   Each text → parallel analysis")
    print("   All texts → batch processing")
    
    start = time.time()
    results = parallel_analysis.batch(texts)
    duration = time.time() - start
    
    print(f"\n✅ Results (completed in {duration:.2f}s):")
    for i, result in enumerate(results, 1):
        print(f"   Text {i}:")
        print(f"      Summary: {result['summary'][:40]}...")
        print(f"      Sentiment: {result['sentiment'][:40]}...")
    
    # Compare with sequential
    print("\n🐌 Sequential comparison:")
    start = time.time()
    for text in texts:
        summary = (PromptTemplate.from_template("Summarize: {text}") | chat | StrOutputParser()).invoke(text)
        sentiment = (PromptTemplate.from_template("Sentiment: {text}") | chat | StrOutputParser()).invoke(text)
    duration_sequential = time.time() - start
    
    speedup = duration_sequential / duration if duration > 0 else 1
    print(f"   Sequential time: {duration_sequential:.2f}s")
    print(f"   Batch+Parallel time: {duration:.2f}s")
    print(f"   ⚡ Speedup: {speedup:.1f}x faster!")
    
    print("\n💡 Batch + Parallel is ideal for:")
    print("   • Processing multiple documents")
    print("   • Bulk analysis workflows")
    print("   • High-throughput applications")
    print()


def main():
    """Run all RunnableParallel examples"""
    
    print("\n" + "⚡" * 35)
    print("Welcome to RunnableParallel - Concurrent Execution!")
    print("⚡" * 35 + "\n")
    
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Error: GOOGLE_API_KEY not found!")
        return
    
    try:
        basic_parallel()
        input("Press Enter to continue...")
        
        dict_syntax()
        input("Press Enter to continue...")
        
        performance_comparison()
        input("Press Enter to continue...")
        
        nested_parallel()
        input("Press Enter to continue...")
        
        error_handling()
        input("Press Enter to continue...")
        
        parallel_with_passthrough()
        input("Press Enter to continue...")
        
        dynamic_parallel()
        input("Press Enter to continue...")
        
        batch_parallel()
        
        print("=" * 70)
        print("✅ RunnableParallel examples completed!")
        print("=" * 70)
        print("\n🎯 Key Takeaways:")
        print("  ✓ RunnableParallel runs operations concurrently")
        print("  ✓ Dict syntax is clean and Pythonic")
        print("  ✓ 2-3x performance improvement typical")
        print("  ✓ Nested parallel for complex structures")
        print("  ✓ Use fallbacks for error handling")
        print("  ✓ Combine with passthrough to preserve input")
        print("  ✓ Dynamic parallel for flexibility")
        print("  ✓ Batch + parallel for maximum performance")
        print("\n💡 Next: Advanced Runnables (Generator, Binding, etc.)!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
