"""
🌟 Practical Chains - Real-World Projects

Complete production-ready projects:
1. Document Processing Pipeline - Multi-stage document analysis
2. Intelligent Customer Support Router - Intent-based routing
3. Content Moderation System - Multi-check validation
4. Data Extraction Pipeline - Extract, validate, format
5. Multi-Language Translator - Detect, translate, verify
6. Smart Research Assistant - Query, search, synthesize

Production patterns and best practices!
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.runnables import (
    RunnableParallel,
    RunnablePassthrough,
    RunnableLambda,
    RunnableBranch
)
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Dict, Any, List

# Load environment variables
load_dotenv()


def document_processing_pipeline():
    """Project 1: Complete document processing pipeline"""
    
    print("=" * 70)
    print("📄 Project 1: Document Processing Pipeline")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.3,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Stage 1: Extract metadata
    def extract_metadata(x: Dict[str, Any]) -> Dict[str, Any]:
        """Extract basic metadata from document"""
        doc = x.get("document", "")
        return {
            **x,
            "word_count": len(doc.split()),
            "char_count": len(doc),
            "line_count": len(doc.split('\n'))
        }
    
    # Stage 2: Parallel analysis
    parallel_analysis = RunnableParallel(
        summary=PromptTemplate.from_template(
            "Summarize in 2 sentences: {document}"
        ) | chat | StrOutputParser(),
        
        keywords=PromptTemplate.from_template(
            "Extract 5 keywords: {document}"
        ) | chat | StrOutputParser(),
        
        category=PromptTemplate.from_template(
            "Categorize (tech/business/science/other): {document}"
        ) | chat | StrOutputParser(),
        
        sentiment=PromptTemplate.from_template(
            "Overall sentiment (positive/neutral/negative): {document}"
        ) | chat | StrOutputParser()
    )
    
    # Stage 3: Quality check
    def is_complete(x: Dict[str, Any]) -> bool:
        """Check if all analyses are complete"""
        required = ["summary", "keywords", "category", "sentiment"]
        return all(x.get(field) for field in required)
    
    # Stage 4: Format output
    def format_report(x: Dict[str, Any]) -> str:
        """Generate final report"""
        return f"""
DOCUMENT ANALYSIS REPORT
========================

Metadata:
  - Words: {x.get('word_count', 0)}
  - Characters: {x.get('char_count', 0)}
  - Lines: {x.get('line_count', 0)}

Analysis:
  - Category: {x.get('category', 'N/A')}
  - Sentiment: {x.get('sentiment', 'N/A')}
  
Summary:
  {x.get('summary', 'N/A')}
  
Keywords:
  {x.get('keywords', 'N/A')}

Status: {'✓ Complete' if is_complete(x) else '⚠ Incomplete'}
"""
    
    # Complete pipeline
    pipeline = (
        # Stage 1: Metadata extraction
        RunnableLambda(extract_metadata)
        
        # Stage 2: Parallel analysis
        | RunnablePassthrough.assign(**parallel_analysis)
        
        # Stage 3: Format report
        | RunnableLambda(format_report)
    )
    
    document = """
    Artificial Intelligence is revolutionizing healthcare through advanced diagnostics
    and personalized treatment plans. Machine learning algorithms can now detect
    diseases earlier and more accurately than traditional methods, leading to better
    patient outcomes and reduced healthcare costs.
    """
    
    print("\n📄 Processing Document:")
    print(document.strip()[:100] + "...")
    
    print("\n🔄 Pipeline Stages:")
    print("   1. Extract metadata (word count, etc.)")
    print("   2. Parallel analysis (summary, keywords, category, sentiment)")
    print("   3. Format comprehensive report")
    
    result = pipeline.invoke({"document": document.strip()})
    
    print("\n✅ Final Report:")
    print(result)
    
    print("\n💡 Use case: Document management systems, content analysis")
    print()


def intelligent_support_router():
    """Project 2: Intelligent customer support routing"""
    
    print("=" * 70)
    print("🎯 Project 2: Intelligent Customer Support Router")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.2,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Intent classification
    def classify_intent(x: Dict[str, Any]) -> str:
        """Classify customer intent"""
        query = x.get("query", "").lower()
        
        # Pattern matching
        if any(word in query for word in ["password", "login", "access", "account"]):
            return "account"
        elif any(word in query for word in ["price", "cost", "payment", "billing", "charge"]):
            return "billing"
        elif any(word in query for word in ["broken", "error", "bug", "not working", "issue"]):
            return "technical"
        elif any(word in query for word in ["feature", "how to", "tutorial", "guide"]):
            return "product"
        elif any(word in query for word in ["cancel", "refund", "return"]):
            return "cancellation"
        return "general"
    
    # Urgency detection
    def detect_urgency(x: Dict[str, Any]) -> str:
        """Detect urgency level"""
        query = x.get("query", "").lower()
        
        if any(word in query for word in ["urgent", "emergency", "critical", "immediately"]):
            return "high"
        elif any(word in query for word in ["soon", "asap", "quickly"]):
            return "medium"
        return "low"
    
    # Specialized handlers
    account_handler = (
        PromptTemplate.from_template(
            "Account Support Response:\n{query}\n\nProvide password reset steps."
        ) | chat | StrOutputParser()
    )
    
    billing_handler = (
        PromptTemplate.from_template(
            "Billing Support Response:\n{query}\n\nExplain charges clearly."
        ) | chat | StrOutputParser()
    )
    
    technical_handler = (
        PromptTemplate.from_template(
            "Technical Support Response:\n{query}\n\nProvide troubleshooting steps."
        ) | chat | StrOutputParser()
    )
    
    product_handler = (
        PromptTemplate.from_template(
            "Product Support Response:\n{query}\n\nProvide step-by-step guide."
        ) | chat | StrOutputParser()
    )
    
    cancellation_handler = (
        PromptTemplate.from_template(
            "Cancellation Support Response:\n{query}\n\nOffer retention options first."
        ) | chat | StrOutputParser()
    )
    
    general_handler = (
        PromptTemplate.from_template(
            "General Support Response:\n{query}"
        ) | chat | StrOutputParser()
    )
    
    # Routing logic
    def route_to_handler(x: Dict[str, Any]) -> Any:
        """Route to appropriate handler"""
        handlers = {
            "account": account_handler,
            "billing": billing_handler,
            "technical": technical_handler,
            "product": product_handler,
            "cancellation": cancellation_handler,
            "general": general_handler
        }
        
        intent = x.get("intent", "general")
        handler = handlers.get(intent, general_handler)
        return handler.invoke({"query": x.get("query", "")})
    
    # Complete routing system
    support_system = (
        # Stage 1: Classify
        RunnablePassthrough.assign(
            intent=RunnableLambda(classify_intent),
            urgency=RunnableLambda(detect_urgency)
        )
        
        # Stage 2: Route and respond
        | RunnablePassthrough.assign(
            response=RunnableLambda(route_to_handler)
        )
    )
    
    test_queries = [
        "I forgot my password and can't login URGENT!",
        "Why was I charged $50 this month?",
        "The app crashes when I try to export data",
        "How do I use the new collaboration feature?",
        "I want to cancel my subscription"
    ]
    
    print("\n🎯 Routing Customer Queries:")
    
    for query in test_queries:
        result = support_system.invoke({"query": query})
        
        print(f"\n   Query: {query}")
        print(f"   Intent: {result['intent']}")
        print(f"   Urgency: {result['urgency']}")
        print(f"   Response: {result['response'][:60]}...")
    
    print("\n💡 Use case: Customer support automation, ticket routing")
    print()


def content_moderation_system():
    """Project 3: Multi-stage content moderation"""
    
    print("=" * 70)
    print("🛡️ Project 3: Content Moderation System")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.1,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Check 1: Profanity filter
    def check_profanity(x: Dict[str, Any]) -> bool:
        """Basic profanity check"""
        content = x.get("content", "").lower()
        banned_words = ["spam", "scam", "hate"]  # Simplified list
        return any(word in content for word in banned_words)
    
    # Check 2: Length validation
    def check_length(x: Dict[str, Any]) -> bool:
        """Check if content meets length requirements"""
        content = x.get("content", "")
        return 10 <= len(content) <= 5000
    
    # Parallel safety checks
    safety_checks = RunnableParallel(
        toxicity=PromptTemplate.from_template(
            "Rate toxicity 0-10: {content}"
        ) | chat | StrOutputParser(),
        
        spam_score=PromptTemplate.from_template(
            "Rate spam likelihood 0-10: {content}"
        ) | chat | StrOutputParser(),
        
        relevance=PromptTemplate.from_template(
            "Rate relevance to discussion 0-10: {content}"
        ) | chat | StrOutputParser()
    )
    
    # Moderation decision
    def make_decision(x: Dict[str, Any]) -> str:
        """Make moderation decision"""
        has_profanity = check_profanity(x)
        valid_length = check_length(x)
        
        if has_profanity:
            return "REJECTED - Inappropriate language"
        elif not valid_length:
            return "REJECTED - Invalid length"
        else:
            return "APPROVED - Content is acceptable"
    
    # Complete moderation pipeline
    moderation_pipeline = (
        # Stage 1: Basic checks
        RunnablePassthrough.assign(
            has_profanity=RunnableLambda(check_profanity),
            valid_length=RunnableLambda(check_length)
        )
        
        # Stage 2: AI safety checks (parallel)
        | RunnablePassthrough.assign(**safety_checks)
        
        # Stage 3: Final decision
        | RunnablePassthrough.assign(
            decision=RunnableLambda(make_decision)
        )
    )
    
    test_content = [
        {"content": "This is a great discussion about AI! Very informative."},
        {"content": "Buy now! Limited offer! Click here!"},  # Spam
        {"content": "Too short"},  # Length issue
        {"content": "I really enjoyed reading this article about machine learning."}
    ]
    
    print("\n🛡️ Moderating Content:")
    
    for item in test_content:
        result = moderation_pipeline.invoke(item)
        
        print(f"\n   Content: {item['content'][:50]}...")
        print(f"   Profanity: {result['has_profanity']}")
        print(f"   Valid Length: {result['valid_length']}")
        print(f"   Decision: {result['decision']}")
    
    print("\n💡 Use case: Forum moderation, comment filtering")
    print()


def data_extraction_pipeline():
    """Project 4: Extract, validate, format data"""
    
    print("=" * 70)
    print("🔄 Project 4: Data Extraction Pipeline")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.2,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    class ContactInfo(BaseModel):
        """Contact information schema"""
        name: str = Field(description="Full name")
        email: str = Field(description="Email address")
        phone: str = Field(description="Phone number")
        company: str = Field(description="Company name")
    
    # Stage 1: Extract data
    parser = JsonOutputParser(pydantic_object=ContactInfo)
    
    extraction_chain = (
        PromptTemplate(
            template="Extract contact info.\n{format_instructions}\n\nText: {text}",
            input_variables=["text"],
            partial_variables={"format_instructions": parser.get_format_instructions()}
        )
        | chat
        | parser
    )
    
    # Stage 2: Validate
    def validate_email(email: str) -> bool:
        """Simple email validation"""
        return "@" in email and "." in email.split("@")[1]
    
    def validate_data(x: Dict[str, Any]) -> Dict[str, Any]:
        """Validate extracted data"""
        errors = []
        
        if not x.get("name"):
            errors.append("Missing name")
        if not validate_email(x.get("email", "")):
            errors.append("Invalid email")
        if not x.get("phone"):
            errors.append("Missing phone")
            
        return {
            **x,
            "is_valid": len(errors) == 0,
            "errors": errors
        }
    
    # Stage 3: Format
    def format_contact(x: Dict[str, Any]) -> str:
        """Format contact for CRM"""
        if not x.get("is_valid"):
            return f"❌ INVALID: {', '.join(x.get('errors', []))}"
        
        return f"""
✅ VALID CONTACT
================
Name: {x.get('name')}
Email: {x.get('email')}
Phone: {x.get('phone')}
Company: {x.get('company')}
"""
    
    # Complete pipeline
    pipeline = (
        extraction_chain
        | RunnableLambda(validate_data)
        | RunnableLambda(format_contact)
    )
    
    texts = [
        "Contact: John Smith, john.smith@company.com, +1-555-0123, TechCorp Inc.",
        "Name: Jane Doe, Email: invalid-email, Phone: missing",  # Invalid
        "Sarah Johnson, sarah.j@example.com, 555-0199, StartupXYZ"
    ]
    
    print("\n🔄 Extraction Pipeline:")
    print("   1. Extract structured data")
    print("   2. Validate fields")
    print("   3. Format for CRM")
    
    for text in texts:
        print(f"\n   Input: {text[:50]}...")
        result = pipeline.invoke({"text": text})
        print(result)
    
    print("\n💡 Use case: Lead generation, data migration")
    print()


def multi_language_translator():
    """Project 5: Multi-language translation with verification"""
    
    print("=" * 70)
    print("🌍 Project 5: Multi-Language Translator")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.3,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Stage 1: Detect language
    detect_chain = (
        PromptTemplate.from_template(
            "Detect language (one word: english/spanish/french/german/other): {text}"
        )
        | chat
        | StrOutputParser()
        | RunnableLambda(lambda x: x.strip().lower())
    )
    
    # Stage 2: Translate if needed
    def needs_translation(x: Dict[str, Any]) -> bool:
        """Check if translation needed"""
        source_lang = x.get("source_language", "english")
        target_lang = x.get("target_language", "english")
        return source_lang != target_lang
    
    translate_chain = (
        PromptTemplate.from_template(
            "Translate from {source_language} to {target_language}:\n{text}"
        )
        | chat
        | StrOutputParser()
    )
    
    no_translation_chain = RunnableLambda(lambda x: x.get("text"))
    
    # Stage 3: Quality check
    quality_check = (
        PromptTemplate.from_template(
            "Rate translation quality 1-10:\nOriginal: {text}\nTranslated: {translated}"
        )
        | chat
        | StrOutputParser()
    )
    
    # Complete pipeline
    pipeline = (
        # Detect source language
        RunnablePassthrough.assign(
            source_language=detect_chain
        )
        
        # Translate or pass through
        | RunnablePassthrough.assign(
            translated=RunnableBranch(
                (needs_translation, translate_chain),
                no_translation_chain
            )
        )
        
        # Quality check if translated
        | RunnablePassthrough.assign(
            quality_score=RunnableBranch(
                (needs_translation, quality_check),
                RunnableLambda(lambda x: "N/A - No translation")
            )
        )
    )
    
    test_cases = [
        {"text": "Hello, how are you?", "target_language": "spanish"},
        {"text": "Bonjour, comment allez-vous?", "target_language": "english"},
        {"text": "Good morning!", "target_language": "english"}  # Same language
    ]
    
    print("\n🌍 Translation Pipeline:")
    print("   1. Detect source language")
    print("   2. Translate if needed")
    print("   3. Quality check")
    
    for case in test_cases:
        result = pipeline.invoke(case)
        
        print(f"\n   Original ({result['source_language']}): {case['text']}")
        print(f"   Target: {case['target_language']}")
        print(f"   Translated: {result['translated']}")
        print(f"   Quality: {result['quality_score']}")
    
    print("\n💡 Use case: Multilingual customer support, content localization")
    print()


def smart_research_assistant():
    """Project 6: Research assistant with synthesis"""
    
    print("=" * 70)
    print("🔍 Project 6: Smart Research Assistant")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.6,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Simulate different information sources
    sources = {
        "academic": PromptTemplate.from_template(
            "Academic perspective on: {query}"
        ) | chat | StrOutputParser(),
        
        "industry": PromptTemplate.from_template(
            "Industry perspective on: {query}"
        ) | chat | StrOutputParser(),
        
        "practical": PromptTemplate.from_template(
            "Practical applications of: {query}"
        ) | chat | StrOutputParser()
    }
    
    # Stage 1: Gather from multiple sources (parallel)
    gather_chain = RunnableParallel(**sources)
    
    # Stage 2: Synthesize
    synthesize_chain = (
        PromptTemplate.from_template(
            """Synthesize these perspectives:
            
            Academic: {academic}
            
            Industry: {industry}
            
            Practical: {practical}
            
            Provide balanced synthesis:"""
        )
        | chat
        | StrOutputParser()
    )
    
    # Stage 3: Generate citations
    def add_citations(x: Dict[str, Any]) -> Dict[str, Any]:
        """Add source citations"""
        return {
            **x,
            "citations": [
                "Academic Research Database",
                "Industry Reports",
                "Practical Case Studies"
            ]
        }
    
    # Complete research pipeline
    research_pipeline = (
        # Gather from sources
        gather_chain
        
        # Synthesize
        | RunnablePassthrough.assign(
            synthesis=synthesize_chain
        )
        
        # Add citations
        | RunnableLambda(add_citations)
    )
    
    query = "impact of artificial intelligence on healthcare"
    
    print(f"\n🔍 Research Query: {query}")
    print("\n🔄 Research Pipeline:")
    print("   1. Gather from multiple sources (parallel)")
    print("   2. Synthesize perspectives")
    print("   3. Add citations")
    
    result = research_pipeline.invoke({"query": query})
    
    print("\n✅ Research Results:")
    print(f"\n   Academic View: {result['academic'][:80]}...")
    print(f"\n   Industry View: {result['industry'][:80]}...")
    print(f"\n   Practical View: {result['practical'][:80]}...")
    print(f"\n   Synthesis: {result['synthesis'][:100]}...")
    print(f"\n   Citations: {len(result['citations'])} sources")
    
    print("\n💡 Use case: Research automation, knowledge synthesis")
    print()


def main():
    """Run all practical chain projects"""
    
    print("\n" + "🌟" * 35)
    print("Welcome to Practical Chains - Real-World Projects!")
    print("🌟" * 35 + "\n")
    
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Error: GOOGLE_API_KEY not found!")
        return
    
    try:
        document_processing_pipeline()
        input("Press Enter to continue...")
        
        intelligent_support_router()
        input("Press Enter to continue...")
        
        content_moderation_system()
        input("Press Enter to continue...")
        
        data_extraction_pipeline()
        input("Press Enter to continue...")
        
        multi_language_translator()
        input("Press Enter to continue...")
        
        smart_research_assistant()
        
        print("=" * 70)
        print("✅ All Practical Chain Projects completed!")
        print("=" * 70)
        print("\n🎯 Real-World Applications:")
        print("  ✓ Document Processing → Content management")
        print("  ✓ Support Router → Customer service automation")
        print("  ✓ Content Moderation → Community management")
        print("  ✓ Data Extraction → Lead generation, CRM")
        print("  ✓ Multi-Language → Global customer support")
        print("  ✓ Research Assistant → Knowledge synthesis")
        print("\n💡 These patterns apply to:")
        print("  • Enterprise automation")
        print("  • Customer service")
        print("  • Content platforms")
        print("  • Data processing")
        print("  • International business")
        print("  • Research & analytics")
        print("\n🎓 You've mastered LangChain Chains!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
