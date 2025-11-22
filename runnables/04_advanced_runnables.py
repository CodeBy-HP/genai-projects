"""
🎨 Advanced Runnables - Specialized Components

Master advanced runnable types:
1. RunnableGenerator - Custom streaming
2. RunnableBinding - Bind configuration
3. RunnableWithFallbacks - Error recovery
4. RunnableRetry - Automatic retries
5. Custom Runnable Classes - Full control
6. RunnablePick - Select fields
7. RunnableConfig Deep Dive - Advanced config
8. Production Patterns - Best practices

Advanced techniques for production!
"""

import os
import asyncio
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    Runnable,
    RunnableLambda,
    RunnablePassthrough,
    RunnableConfig
)
from typing import Dict, Any, List, Iterator, AsyncIterator
import time

# Load environment variables
load_dotenv()


def runnable_generator_example():
    """Example 1: Custom streaming with generators"""
    
    print("=" * 70)
    print("🌊 Example 1: RunnableGenerator")
    print("=" * 70)
    
    print("\n📡 Create custom streaming runnables")
    
    # Custom generator function
    def custom_streamer(input: Dict[str, Any]) -> Iterator[str]:
        """Generate chunks progressively"""
        text = input.get("text", "")
        words = text.split()
        
        for i, word in enumerate(words):
            yield f"{word} "
            time.sleep(0.1)  # Simulate processing
    
    # Wrap as runnable
    from langchain_core.runnables import RunnableGenerator
    
    streaming_runnable = RunnableGenerator(custom_streamer)
    
    print("\n1️⃣ Streaming word by word:")
    print("   Output: ", end="", flush=True)
    for chunk in streaming_runnable.stream({"text": "Hello world from custom generator"}):
        print(chunk, end="", flush=True)
    print()
    
    # More complex generator
    def progress_generator(input: Dict[str, Any]) -> Iterator[Dict[str, Any]]:
        """Generator that yields progress updates"""
        total_steps = input.get("steps", 5)
        
        for step in range(1, total_steps + 1):
            yield {
                "step": step,
                "total": total_steps,
                "progress": f"{(step/total_steps)*100:.0f}%",
                "message": f"Processing step {step}/{total_steps}"
            }
            time.sleep(0.2)
    
    progress_runnable = RunnableGenerator(progress_generator)
    
    print("\n2️⃣ Progress tracking:")
    for update in progress_runnable.stream({"steps": 5}):
        print(f"   {update['progress']} - {update['message']}")
    
    print("\n💡 RunnableGenerator enables:")
    print("   • Custom streaming logic")
    print("   • Progress indicators")
    print("   • Chunked data processing")
    print()


def runnable_binding_example():
    """Example 2: Binding configuration"""
    
    print("=" * 70)
    print("🔧 Example 2: RunnableBinding")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.9,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    print("\n⚙️ Bind specific parameters to a runnable")
    
    # Original model
    print("\n1️⃣ Original model (temp=0.9):")
    result1 = chat.invoke("Say hello")
    print(f"   {result1.content[:50]}...")
    
    # Bind lower temperature
    print("\n2️⃣ Bound model (temp=0.1):")
    conservative_model = chat.bind(temperature=0.1)
    result2 = conservative_model.invoke("Say hello")
    print(f"   {result2.content[:50]}...")
    
    # Bind max tokens
    print("\n3️⃣ Bound with max_tokens:")
    short_model = chat.bind(temperature=0.5, max_tokens=20)
    result3 = short_model.invoke("Write a long story")
    print(f"   {result3.content}")
    
    # Use in chains
    print("\n4️⃣ Using bound models in chains:")
    
    creative_chain = (
        PromptTemplate.from_template("Write creatively about: {topic}")
        | chat.bind(temperature=0.9)
        | StrOutputParser()
    )
    
    formal_chain = (
        PromptTemplate.from_template("Write formally about: {topic}")
        | chat.bind(temperature=0.1)
        | StrOutputParser()
    )
    
    topic = "artificial intelligence"
    
    creative = creative_chain.invoke({"topic": topic})
    formal = formal_chain.invoke({"topic": topic})
    
    print(f"   Creative: {creative[:40]}...")
    print(f"   Formal: {formal[:40]}...")
    
    print("\n💡 RunnableBinding is useful for:")
    print("   • Different model behaviors")
    print("   • Reusable configurations")
    print("   • A/B testing")
    print()


def fallbacks_example():
    """Example 3: Error recovery with fallbacks"""
    
    print("=" * 70)
    print("🛡️ Example 3: RunnableWithFallbacks")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.5,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    print("\n🔄 Automatic fallback on errors")
    
    # Simulate failing operation
    def unreliable_operation(x: Dict[str, Any]) -> str:
        import random
        if random.random() < 0.7:  # 70% chance of failure
            raise ConnectionError("Simulated network error")
        return "Success!"
    
    # Fallback operation
    def fallback_operation(x: Dict[str, Any]) -> str:
        return "Fallback result"
    
    # Create chain with fallbacks
    print("\n1️⃣ Without fallbacks (may fail):")
    unreliable_chain = RunnableLambda(unreliable_operation)
    
    attempts = 0
    success = False
    while attempts < 3 and not success:
        try:
            result = unreliable_chain.invoke({"input": "test"})
            print(f"   ✓ {result}")
            success = True
        except Exception as e:
            attempts += 1
            print(f"   ✗ Attempt {attempts} failed: {e}")
    
    # With fallbacks
    print("\n2️⃣ With fallbacks (always succeeds):")
    safe_chain = unreliable_chain.with_fallbacks([
        RunnableLambda(fallback_operation)
    ])
    
    result = safe_chain.invoke({"input": "test"})
    print(f"   ✓ {result}")
    
    # Multiple fallbacks
    print("\n3️⃣ Multiple fallback levels:")
    
    def primary(x):
        raise ValueError("Primary failed")
    
    def fallback1(x):
        raise ValueError("Fallback 1 failed")
    
    def fallback2(x):
        return "Fallback 2 succeeded"
    
    multi_fallback = (
        RunnableLambda(primary)
        .with_fallbacks([
            RunnableLambda(fallback1),
            RunnableLambda(fallback2)
        ])
    )
    
    result = multi_fallback.invoke({"input": "test"})
    print(f"   Final result: {result}")
    
    # Real-world: Model fallback
    print("\n4️⃣ Real-world: Model fallback:")
    
    prompt = PromptTemplate.from_template("Explain {concept}")
    
    primary_chain = prompt | chat | StrOutputParser()
    simple_fallback = RunnableLambda(lambda x: f"Simple explanation: {x['concept']} is important")
    
    robust_chain = primary_chain.with_fallbacks([simple_fallback])
    
    result = robust_chain.invoke({"concept": "LCEL"})
    print(f"   Result: {result[:60]}...")
    
    print("\n💡 Fallbacks ensure:")
    print("   • High availability")
    print("   • Graceful degradation")
    print("   • Better user experience")
    print()


def retry_example():
    """Example 4: Automatic retries"""
    
    print("=" * 70)
    print("🔁 Example 4: RunnableRetry")
    print("=" * 70)
    
    print("\n🔄 Automatic retry on transient failures")
    
    # Simulate flaky operation
    attempt_count = {"value": 0}
    
    def flaky_operation(x: Dict[str, Any]) -> str:
        attempt_count["value"] += 1
        if attempt_count["value"] < 3:
            raise ConnectionError(f"Attempt {attempt_count['value']} failed")
        return f"Success on attempt {attempt_count['value']}"
    
    # With retry
    print("\n1️⃣ With automatic retry:")
    attempt_count["value"] = 0
    
    retry_chain = RunnableLambda(flaky_operation).with_retry(
        stop_after_attempt=5,
        wait_exponential_jitter=True
    )
    
    result = retry_chain.invoke({"input": "test"})
    print(f"   ✓ {result}")
    
    # Selective retry
    print("\n2️⃣ Retry specific errors only:")
    
    def selective_failure(x: Dict[str, Any]) -> str:
        import random
        error_type = random.choice(["network", "validation"])
        
        if error_type == "network":
            raise ConnectionError("Network error (retryable)")
        else:
            raise ValueError("Validation error (not retryable)")
    
    selective_retry = RunnableLambda(selective_failure).with_retry(
        retry_if_exception_type=(ConnectionError,),
        stop_after_attempt=3
    )
    
    try:
        result = selective_retry.invoke({"input": "test"})
        print(f"   ✓ {result}")
    except Exception as e:
        print(f"   ✗ {type(e).__name__}: {e}")
        print("   (ValidationError not retried)")
    
    print("\n💡 Retry is perfect for:")
    print("   • Network timeouts")
    print("   • Rate limits")
    print("   • Transient failures")
    print()


def custom_runnable_class():
    """Example 5: Building custom Runnable classes"""
    
    print("=" * 70)
    print("🎨 Example 5: Custom Runnable Class")
    print("=" * 70)
    
    print("\n🛠️ Build fully custom Runnables")
    
    class CachingRunnable(Runnable):
        """Runnable with caching"""
        
        def __init__(self, runnable: Runnable):
            self.runnable = runnable
            self.cache = {}
        
        def invoke(self, input: Dict[str, Any], config: RunnableConfig = None) -> Any:
            # Create cache key
            cache_key = str(sorted(input.items()))
            
            if cache_key in self.cache:
                print("   💾 Cache hit!")
                return self.cache[cache_key]
            
            print("   🔄 Cache miss, computing...")
            result = self.runnable.invoke(input, config)
            self.cache[cache_key] = result
            return result
        
        def clear_cache(self):
            self.cache = {}
    
    # Use caching runnable
    expensive_operation = RunnableLambda(lambda x: f"Processed: {x['data']}")
    cached_operation = CachingRunnable(expensive_operation)
    
    print("\n1️⃣ Testing cache:")
    result1 = cached_operation.invoke({"data": "hello"})
    print(f"   Result: {result1}")
    
    result2 = cached_operation.invoke({"data": "hello"})
    print(f"   Result: {result2}")
    
    result3 = cached_operation.invoke({"data": "world"})
    print(f"   Result: {result3}")
    
    # Advanced: Monitoring runnable
    class MonitoringRunnable(Runnable):
        """Runnable that tracks metrics"""
        
        def __init__(self, runnable: Runnable, name: str = "unnamed"):
            self.runnable = runnable
            self.name = name
            self.metrics = {
                "invocations": 0,
                "total_time": 0.0,
                "errors": 0
            }
        
        def invoke(self, input: Any, config: RunnableConfig = None) -> Any:
            self.metrics["invocations"] += 1
            start = time.time()
            
            try:
                result = self.runnable.invoke(input, config)
                self.metrics["total_time"] += time.time() - start
                return result
            except Exception as e:
                self.metrics["errors"] += 1
                raise
        
        def get_metrics(self) -> Dict[str, Any]:
            return {
                **self.metrics,
                "avg_time": self.metrics["total_time"] / max(self.metrics["invocations"], 1)
            }
    
    print("\n2️⃣ Monitoring runnable:")
    
    monitored = MonitoringRunnable(
        RunnableLambda(lambda x: time.sleep(0.1) or f"Result: {x}"),
        name="test_operation"
    )
    
    for i in range(3):
        monitored.invoke(f"input_{i}")
    
    metrics = monitored.get_metrics()
    print(f"   Invocations: {metrics['invocations']}")
    print(f"   Total time: {metrics['total_time']:.2f}s")
    print(f"   Avg time: {metrics['avg_time']:.3f}s")
    print(f"   Errors: {metrics['errors']}")
    
    print("\n💡 Custom Runnables enable:")
    print("   • Caching")
    print("   • Monitoring")
    print("   • Custom behaviors")
    print()


def runnable_pick_example():
    """Example 6: Selecting specific fields"""
    
    print("=" * 70)
    print("🎯 Example 6: Field Selection")
    print("=" * 70)
    
    print("\n📋 Select specific fields from output")
    
    # Create data
    full_data = {
        "user": "alice",
        "text": "Hello world",
        "timestamp": "2024-01-01",
        "metadata": {"source": "api", "version": "1.0"}
    }
    
    # Pick specific fields
    print("\n1️⃣ Using lambda to pick fields:")
    
    pick_user_text = RunnableLambda(lambda x: {
        "user": x["user"],
        "text": x["text"]
    })
    
    result = pick_user_text.invoke(full_data)
    print(f"   Picked: {result}")
    
    # Pick with transformation
    print("\n2️⃣ Pick and transform:")
    
    pick_and_format = RunnableLambda(lambda x: 
        f"User {x['user']} said: {x['text']}"
    )
    
    result = pick_and_format.invoke(full_data)
    print(f"   Formatted: {result}")
    
    # Nested picking
    print("\n3️⃣ Nested field access:")
    
    pick_nested = RunnableLambda(lambda x: {
        "user": x["user"],
        "source": x["metadata"]["source"]
    })
    
    result = pick_nested.invoke(full_data)
    print(f"   Picked nested: {result}")
    
    print("\n💡 Field selection for:")
    print("   • Data cleanup")
    print("   • Privacy (remove sensitive data)")
    print("   • API response formatting")
    print()


def config_deep_dive():
    """Example 7: Advanced configuration"""
    
    print("=" * 70)
    print("⚙️ Example 7: Config Deep Dive")
    print("=" * 70)
    
    print("\n🔧 Advanced configuration patterns")
    
    class ConfigAwareRunnable(Runnable):
        """Runnable that extensively uses config"""
        
        def invoke(self, input: Dict[str, Any], config: RunnableConfig = None) -> Dict[str, Any]:
            # Extract config components
            metadata = config.get("metadata", {}) if config else {}
            tags = config.get("tags", []) if config else []
            run_name = config.get("run_name", "unnamed") if config else "unnamed"
            
            return {
                "input": input,
                "user_id": metadata.get("user_id", "anonymous"),
                "tags": tags,
                "run_name": run_name,
                "processed": True
            }
    
    config_runnable = ConfigAwareRunnable()
    
    print("\n1️⃣ Rich configuration:")
    
    config = {
        "metadata": {
            "user_id": "user_123",
            "session_id": "sess_456",
            "ip_address": "192.168.1.1"
        },
        "tags": ["production", "urgent"],
        "run_name": "important_task",
        "max_concurrency": 5
    }
    
    result = config_runnable.invoke({"data": "test"}, config=config)
    
    for key, value in result.items():
        print(f"   {key}: {value}")
    
    # Config propagation
    print("\n2️⃣ Config propagates through chains:")
    
    chain = (
        config_runnable
        | RunnableLambda(lambda x: f"User {x['user_id']} processed {x['run_name']}")
    )
    
    result = chain.invoke({"data": "test"}, config=config)
    print(f"   Result: {result}")
    
    print("\n💡 Config is essential for:")
    print("   • User tracking")
    print("   • A/B testing")
    print("   • Monitoring")
    print("   • Debugging")
    print()


def production_patterns():
    """Example 8: Production best practices"""
    
    print("=" * 70)
    print("🏭 Example 8: Production Patterns")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.5,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    print("\n🎯 Production-ready patterns")
    
    # Pattern 1: Robust chain
    print("\n1️⃣ Fully robust chain:")
    
    def validate_input(x: Dict[str, Any]) -> Dict[str, Any]:
        if "text" not in x or len(x["text"]) < 5:
            raise ValueError("Invalid input")
        return x
    
    production_chain = (
        RunnableLambda(validate_input)
        | PromptTemplate.from_template("Process: {text}")
        | chat.bind(temperature=0.3)
        | StrOutputParser()
    ).with_retry(
        stop_after_attempt=3
    ).with_fallbacks([
        RunnableLambda(lambda x: "Fallback response due to error")
    ])
    
    result = production_chain.invoke({"text": "Hello production world"})
    print(f"   ✓ Result: {result[:50]}...")
    
    # Pattern 2: Monitored chain
    print("\n2️⃣ With monitoring:")
    
    def log_execution(label: str):
        def _log(x):
            print(f"   [LOG] {label}: {str(x)[:30]}...")
            return x
        return _log
    
    monitored_chain = (
        RunnableLambda(log_execution("INPUT"))
        | PromptTemplate.from_template("Analyze: {text}")
        | RunnableLambda(log_execution("PROMPT"))
        | chat
        | RunnableLambda(log_execution("MODEL"))
        | StrOutputParser()
        | RunnableLambda(log_execution("OUTPUT"))
    )
    
    result = monitored_chain.invoke({"text": "Monitor this"})
    
    # Pattern 3: Configurable chain
    print("\n3️⃣ Highly configurable:")
    
    def build_chain(temperature: float, max_tokens: int):
        """Factory for creating configured chains"""
        return (
            PromptTemplate.from_template("Answer: {question}")
            | chat.bind(temperature=temperature, max_tokens=max_tokens)
            | StrOutputParser()
        )
    
    creative_chain = build_chain(temperature=0.9, max_tokens=100)
    precise_chain = build_chain(temperature=0.1, max_tokens=50)
    
    question = {"question": "What is AI?"}
    
    creative = creative_chain.invoke(question)
    precise = precise_chain.invoke(question)
    
    print(f"   Creative: {creative[:40]}...")
    print(f"   Precise: {precise[:40]}...")
    
    print("\n💡 Production checklist:")
    print("   ✓ Input validation")
    print("   ✓ Error handling (retry + fallbacks)")
    print("   ✓ Logging and monitoring")
    print("   ✓ Configuration management")
    print("   ✓ Testing")
    print()


def main():
    """Run all advanced runnable examples"""
    
    print("\n" + "🎨" * 35)
    print("Welcome to Advanced Runnables!")
    print("🎨" * 35 + "\n")
    
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Error: GOOGLE_API_KEY not found!")
        return
    
    try:
        runnable_generator_example()
        input("Press Enter to continue...")
        
        runnable_binding_example()
        input("Press Enter to continue...")
        
        fallbacks_example()
        input("Press Enter to continue...")
        
        retry_example()
        input("Press Enter to continue...")
        
        custom_runnable_class()
        input("Press Enter to continue...")
        
        runnable_pick_example()
        input("Press Enter to continue...")
        
        config_deep_dive()
        input("Press Enter to continue...")
        
        production_patterns()
        
        print("=" * 70)
        print("✅ Advanced Runnables completed!")
        print("=" * 70)
        print("\n🎯 Key Takeaways:")
        print("  ✓ RunnableGenerator for custom streaming")
        print("  ✓ Binding for fixed configurations")
        print("  ✓ Fallbacks for error recovery")
        print("  ✓ Retry for transient failures")
        print("  ✓ Custom classes for special behaviors")
        print("  ✓ Field selection for data control")
        print("  ✓ Config for runtime customization")
        print("  ✓ Production patterns for robustness")
        print("\n💡 Next: Practical projects combining everything!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
