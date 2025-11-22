"""
🚀 Practical Runnables - Real-World Projects

Production-ready implementations:
1. Custom Text Processor - Runnable toolkit
2. Streaming Chat System - Real-time responses
3. Robust API Client - Retry + fallback
4. Batch Document Processor - High throughput
5. Async Pipeline - Non-blocking workflows
6. Monitoring Wrapper - Track everything

Build production systems!
"""

import os
import asyncio
import time
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    Runnable,
    RunnableLambda,
    RunnablePassthrough,
    RunnableParallel,
    RunnableConfig
)
from typing import Dict, Any, List, Iterator, Optional
import json

load_dotenv()


def custom_text_processor():
    """Project 1: Complete text processing toolkit"""
    
    print("=" * 70)
    print("🔧 Project 1: Custom Text Processor Toolkit")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.5,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    class TextProcessor(Runnable):
        """Comprehensive text processing runnable"""
        
        def __init__(self, operations: Optional[List[str]] = None):
            self.operations = operations or ["clean", "analyze", "enhance"]
        
        def invoke(self, input: Dict[str, Any], config: Optional[RunnableConfig] = None) -> Dict[str, Any]:
            text = input.get("text", "")
            results = {"original": text}
            
            if "clean" in self.operations:
                results["cleaned"] = text.strip().lower()
            
            if "analyze" in self.operations:
                results["stats"] = {
                    "words": len(text.split()),
                    "chars": len(text),
                    "sentences": text.count('.') + text.count('!') + text.count('?')
                }
            
            if "enhance" in self.operations:
                results["enhanced"] = text.title()
            
            return results
    
    # Basic usage
    processor = TextProcessor()
    result = processor.invoke({"text": "  hello world. this is AI!  "})
    
    print("\n✅ Processing Results:")
    print(f"   Original: '{result['original']}'")
    print(f"   Cleaned: '{result['cleaned']}'")
    print(f"   Stats: {result['stats']}")
    print(f"   Enhanced: '{result['enhanced']}'")
    
    # Compose with AI
    ai_processor = (
        TextProcessor(["clean", "analyze"])
        | RunnablePassthrough.assign(
            ai_summary=PromptTemplate.from_template(
                "Summarize: {cleaned}"
            ) | chat | StrOutputParser()
        )
    )
    
    result = ai_processor.invoke({"text": "Artificial Intelligence transforms industries"})
    print(f"\n   AI Summary: {result['ai_summary']}")
    
    print("\n💡 Use case: Content management, data preprocessing")
    print()


def streaming_chat_system():
    """Project 2: Real-time streaming chat"""
    
    print("=" * 70)
    print("💬 Project 2: Streaming Chat System")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.7,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    class StreamingChat(Runnable):
        """Chat system with streaming and history"""
        
        def __init__(self):
            self.history = []
        
        def invoke(self, input: Dict[str, Any], config: Optional[RunnableConfig] = None) -> str:
            message = input.get("message", "")
            
            # Build context
            context = "\n".join([
                f"{'User' if i % 2 == 0 else 'Assistant'}: {msg}"
                for i, msg in enumerate(self.history[-4:])  # Last 2 exchanges
            ])
            
            # Create prompt
            prompt = f"{context}\nUser: {message}\nAssistant:"
            
            # Get response
            response = chat.invoke(prompt).content
            
            # Update history
            self.history.append(message)
            self.history.append(response)
            
            return response
        
        def stream(self, input: Dict[str, Any], config: Optional[RunnableConfig] = None) -> Iterator[str]:
            message = input.get("message", "")
            
            # Build context
            context = "\n".join([
                f"{'User' if i % 2 == 0 else 'Assistant'}: {msg}"
                for i, msg in enumerate(self.history[-4:])
            ])
            
            prompt = f"{context}\nUser: {message}\nAssistant:"
            
            # Stream response
            full_response = ""
            for chunk in chat.stream(prompt):
                content = chunk.content
                full_response += content
                yield content
            
            # Update history
            self.history.append(message)
            self.history.append(full_response)
    
    print("\n💬 Interactive Chat (streaming):")
    
    chat_system = StreamingChat()
    
    messages = [
        "Hi, what's your name?",
        "Tell me about AI",
        "That's interesting!"
    ]
    
    for msg in messages:
        print(f"\n   User: {msg}")
        print("   Assistant: ", end="", flush=True)
        
        for chunk in chat_system.stream({"message": msg}):
            print(chunk, end="", flush=True)
        print()
    
    print("\n💡 Use case: Chatbots, customer support, virtual assistants")
    print()


def robust_api_client():
    """Project 3: Robust API client with retry/fallback"""
    
    print("=" * 70)
    print("🛡️ Project 3: Robust API Client")
    print("=" * 70)
    
    class RobustAPIClient(Runnable):
        """API client with built-in resilience"""
        
        def __init__(self, max_retries: int = 3):
            self.max_retries = max_retries
            self.metrics = {"calls": 0, "failures": 0, "retries": 0}
        
        def invoke(self, input: Dict[str, Any], config: Optional[RunnableConfig] = None) -> Dict[str, Any]:
            self.metrics["calls"] += 1
            
            for attempt in range(self.max_retries):
                try:
                    # Simulate API call
                    import random
                    if random.random() < 0.3:  # 30% failure rate
                        raise ConnectionError("Network timeout")
                    
                    return {
                        "status": "success",
                        "data": f"Processed: {input.get('data')}",
                        "attempt": attempt + 1
                    }
                
                except ConnectionError as e:
                    self.metrics["retries"] += 1
                    if attempt == self.max_retries - 1:
                        self.metrics["failures"] += 1
                        return {
                            "status": "error",
                            "error": str(e),
                            "fallback": "Using cached data"
                        }
                    time.sleep(0.1 * (2 ** attempt))  # Exponential backoff
            
            return {"status": "error", "error": "Max retries exceeded"}
    
    print("\n🔄 Testing robust API client:")
    
    client = RobustAPIClient(max_retries=3)
    
    # Make multiple requests
    for i in range(5):
        result = client.invoke({"data": f"request_{i}"})
        status = result["status"]
        emoji = "✓" if status == "success" else "✗"
        print(f"   {emoji} Request {i+1}: {status} (attempt: {result.get('attempt', 'N/A')})")
    
    print(f"\n📊 Metrics:")
    print(f"   Total calls: {client.metrics['calls']}")
    print(f"   Retries: {client.metrics['retries']}")
    print(f"   Failures: {client.metrics['failures']}")
    
    print("\n💡 Use case: External APIs, microservices, unreliable networks")
    print()


def batch_document_processor():
    """Project 4: High-throughput batch processor"""
    
    print("=" * 70)
    print("📦 Project 4: Batch Document Processor")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.5,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Batch processor
    processor = RunnableParallel(
        summary=PromptTemplate.from_template("Summarize: {text}") | chat | StrOutputParser(),
        keywords=PromptTemplate.from_template("Extract keywords: {text}") | chat | StrOutputParser(),
        category=PromptTemplate.from_template("Categorize: {text}") | chat | StrOutputParser()
    )
    
    # Sample documents
    documents = [
        {"text": "AI is revolutionizing healthcare with advanced diagnostics"},
        {"text": "Climate change requires urgent global action and cooperation"},
        {"text": "Blockchain technology enables secure decentralized transactions"},
        {"text": "Quantum computing promises exponential computational power"},
        {"text": "Renewable energy sources are becoming increasingly affordable"}
    ]
    
    print(f"\n📚 Processing {len(documents)} documents in batch...")
    print("   Each document → parallel analysis (summary, keywords, category)")
    
    start = time.time()
    results = processor.batch(documents)
    duration = time.time() - start
    
    print(f"\n✅ Completed in {duration:.2f}s")
    
    for i, result in enumerate(results, 1):
        print(f"\n   Document {i}:")
        print(f"      Summary: {result['summary'][:50]}...")
        print(f"      Keywords: {result['keywords'][:50]}...")
        print(f"      Category: {result['category'][:30]}...")
    
    throughput = len(documents) / duration
    print(f"\n⚡ Throughput: {throughput:.1f} documents/second")
    
    print("\n💡 Use case: Document processing, content analysis, ETL")
    print()


def async_pipeline():
    """Project 5: Async non-blocking pipeline"""
    
    print("=" * 70)
    print("⚡ Project 5: Async Pipeline")
    print("=" * 70)
    
    async def async_demo():
        chat = ChatGoogleGenerativeAI(
            model="gemini-pro",
            temperature=0.5,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        
        # Async pipeline
        pipeline = (
            PromptTemplate.from_template("Analyze: {text}")
            | chat
            | StrOutputParser()
        )
        
        print("\n🚀 Async concurrent processing:")
        
        inputs = [
            {"text": "AI in healthcare"},
            {"text": "Cloud computing"},
            {"text": "Cybersecurity"}
        ]
        
        # Concurrent async execution
        start = time.time()
        
        tasks = [pipeline.ainvoke(inp) for inp in inputs]
        results = await asyncio.gather(*tasks)
        
        duration = time.time() - start
        
        print(f"\n✅ Processed {len(inputs)} items concurrently in {duration:.2f}s")
        
        for i, result in enumerate(results, 1):
            print(f"   {i}. {result[:50]}...")
        
        # Async streaming
        print("\n🌊 Async streaming:")
        print("   Output: ", end="", flush=True)
        
        async for chunk in pipeline.astream({"text": "Machine learning"}):
            print(chunk, end="", flush=True)
        print()
    
    asyncio.run(async_demo())
    
    print("\n💡 Use case: Web servers, async frameworks, high concurrency")
    print()


def monitoring_wrapper():
    """Project 6: Complete monitoring system"""
    
    print("=" * 70)
    print("📊 Project 6: Monitoring Wrapper")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.5,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    class MonitoredRunnable(Runnable):
        """Comprehensive monitoring wrapper"""
        
        def __init__(self, runnable: Runnable, name: str = "unnamed"):
            self.runnable = runnable
            self.name = name
            self.metrics = {
                "total_calls": 0,
                "successes": 0,
                "failures": 0,
                "total_time": 0.0,
                "min_time": float('inf'),
                "max_time": 0.0,
                "errors": []
            }
        
        def invoke(self, input: Any, config: Optional[RunnableConfig] = None) -> Any:
            self.metrics["total_calls"] += 1
            start = time.time()
            
            try:
                result = self.runnable.invoke(input, config)
                duration = time.time() - start
                
                self.metrics["successes"] += 1
                self.metrics["total_time"] += duration
                self.metrics["min_time"] = min(self.metrics["min_time"], duration)
                self.metrics["max_time"] = max(self.metrics["max_time"], duration)
                
                return result
            
            except Exception as e:
                self.metrics["failures"] += 1
                self.metrics["errors"].append({
                    "error": str(e),
                    "type": type(e).__name__,
                    "timestamp": time.time()
                })
                raise
        
        def get_report(self) -> str:
            avg_time = self.metrics["total_time"] / max(self.metrics["total_calls"], 1)
            success_rate = (self.metrics["successes"] / max(self.metrics["total_calls"], 1)) * 100
            
            return f"""
Monitoring Report: {self.name}
{'=' * 40}
Calls: {self.metrics['total_calls']}
Successes: {self.metrics['successes']}
Failures: {self.metrics['failures']}
Success Rate: {success_rate:.1f}%

Performance:
  Total Time: {self.metrics['total_time']:.2f}s
  Avg Time: {avg_time:.3f}s
  Min Time: {self.metrics['min_time']:.3f}s
  Max Time: {self.metrics['max_time']:.3f}s

Errors: {len(self.metrics['errors'])}
"""
    
    # Create monitored chain
    base_chain = (
        PromptTemplate.from_template("Explain: {concept}")
        | chat
        | StrOutputParser()
    )
    
    monitored_chain = MonitoredRunnable(base_chain, name="explanation_chain")
    
    print("\n📊 Running monitored chain:")
    
    concepts = ["AI", "ML", "DL", "NLP", "CV"]
    
    for concept in concepts:
        result = monitored_chain.invoke({"concept": concept})
        print(f"   ✓ Explained {concept}: {result[:30]}...")
    
    # Get report
    print(monitored_chain.get_report())
    
    print("💡 Use case: Production monitoring, performance tuning, debugging")
    print()


def main():
    """Run all practical runnable projects"""
    
    print("\n" + "🚀" * 35)
    print("Welcome to Practical Runnables - Real-World Projects!")
    print("🚀" * 35 + "\n")
    
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Error: GOOGLE_API_KEY not found!")
        return
    
    try:
        custom_text_processor()
        input("Press Enter to continue...")
        
        streaming_chat_system()
        input("Press Enter to continue...")
        
        robust_api_client()
        input("Press Enter to continue...")
        
        batch_document_processor()
        input("Press Enter to continue...")
        
        async_pipeline()
        input("Press Enter to continue...")
        
        monitoring_wrapper()
        
        print("=" * 70)
        print("✅ All Practical Runnable Projects completed!")
        print("=" * 70)
        print("\n🎯 Production Patterns Mastered:")
        print("  ✓ Custom runnables for domain logic")
        print("  ✓ Streaming for real-time UX")
        print("  ✓ Retry/fallback for resilience")
        print("  ✓ Batch processing for throughput")
        print("  ✓ Async for concurrency")
        print("  ✓ Monitoring for observability")
        print("\n💡 You're ready for production LangChain!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
