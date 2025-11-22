"""
🚀 Advanced Structured Output Techniques

This example covers:
- Output parsers in chains & pipelines
- OutputFixingParser (auto-fix errors)
- RetryOutputParser (retry on failure)
- Custom output parsers
- Error handling strategies
- Pattern injection techniques
- Combining multiple parsers
- Validation & fallbacks

Advanced techniques for production!
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser, PydanticOutputParser
from langchain.output_parsers import (
    OutputFixingParser,
    RetryOutputParser,
    StructuredOutputParser,
    ResponseSchema
)
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from langchain_core.output_parsers.base import BaseOutputParser
from typing import List, Dict, Any
import json
import re

# Load environment variables
load_dotenv()


def parser_in_chain():
    """Example 1: Output parsers in LCEL chains"""
    
    print("=" * 70)
    print("⛓️  Output Parsers in LCEL Chains")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.3,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    class Recipe(BaseModel):
        """Recipe information"""
        name: str = Field(description="Recipe name")
        cuisine: str = Field(description="Type of cuisine")
        ingredients: List[str] = Field(description="List of ingredients")
        prep_time: int = Field(description="Preparation time in minutes")
        difficulty: str = Field(description="easy, medium, or hard")
    
    parser = PydanticOutputParser(pydantic_object=Recipe)
    
    # Chain: prompt → llm → parser
    template = """Extract recipe information.

{format_instructions}

Recipe: {text}

Output:"""
    
    prompt = PromptTemplate(
        template=template,
        input_variables=["text"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    
    # LCEL chain
    chain = prompt | chat | parser
    
    recipe_text = """
    Quick Pasta Carbonara
    
    This classic Italian pasta takes just 20 minutes. You'll need:
    spaghetti, eggs, bacon, parmesan cheese, black pepper, and salt.
    It's an easy recipe perfect for beginners.
    """
    
    print("\n👤 Input: Recipe text")
    print("\n🤖 Chain execution:")
    print("   prompt → llm → parser")
    
    result = chain.invoke({"text": recipe_text})
    
    print(f"\n✨ Result type: {type(result)}")
    print(f"   Name: {result.name}")
    print(f"   Cuisine: {result.cuisine}")
    print(f"   Ingredients: {', '.join(result.ingredients[:3])}...")
    print(f"   Prep time: {result.prep_time} mins")
    print(f"   Difficulty: {result.difficulty}")
    
    print("\n💡 LCEL chains: Clean & composable!")
    print()


def output_fixing_parser():
    """Example 2: OutputFixingParser - Auto-fix malformed output"""
    
    print("=" * 70)
    print("🔧 OutputFixingParser - Auto-Fix Errors")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.3,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    class Product(BaseModel):
        """Product information"""
        name: str = Field(description="Product name")
        price: float = Field(description="Price in USD")
        in_stock: bool = Field(description="Availability")
        rating: float = Field(description="Rating 0-5", ge=0, le=5)
    
    base_parser = PydanticOutputParser(pydantic_object=Product)
    
    # Wrap with OutputFixingParser
    fixing_parser = OutputFixingParser.from_llm(
        parser=base_parser,
        llm=chat
    )
    
    # Simulate malformed JSON (missing quote, wrong type)
    malformed_output = """{
        "name": "Wireless Mouse,
        "price": "29.99",
        "in_stock": "yes",
        "rating": 4.5
    }"""
    
    print("\n❌ Malformed output (missing quote, wrong types):")
    print(malformed_output)
    
    print("\n🔧 Trying base parser...")
    try:
        base_parser.parse(malformed_output)
        print("   ✓ Parsed successfully")
    except Exception as e:
        print(f"   ✗ Failed: {str(e)[:60]}...")
    
    print("\n🔧 Trying OutputFixingParser...")
    try:
        result = fixing_parser.parse(malformed_output)
        print("   ✓ Auto-fixed and parsed!")
        print(f"\n   Name: {result.name}")
        print(f"   Price: ${result.price}")
        print(f"   In stock: {result.in_stock}")
        print(f"   Rating: {result.rating}")
    except Exception as e:
        print(f"   ✗ Failed: {e}")
    
    print("\n💡 OutputFixingParser uses LLM to fix errors!")
    print()


def retry_output_parser():
    """Example 3: RetryOutputParser - Retry with original prompt"""
    
    print("=" * 70)
    print("🔄 RetryOutputParser - Retry on Failure")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.3,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    class Contact(BaseModel):
        """Contact information"""
        name: str = Field(description="Full name")
        email: str = Field(description="Email address")
        phone: str = Field(description="Phone number", regex=r'^\+?[\d\s\-\(\)]+$')
    
    base_parser = PydanticOutputParser(pydantic_object=Contact)
    
    # Wrap with RetryOutputParser
    retry_parser = RetryOutputParser.from_llm(
        parser=base_parser,
        llm=chat,
        max_retries=2
    )
    
    prompt = PromptTemplate(
        template="""Extract contact info.

{format_instructions}

Text: {text}

Output:""",
        input_variables=["text"],
        partial_variables={"format_instructions": base_parser.get_format_instructions()}
    )
    
    text = "Contact: Jane Doe, jane.doe@email.com, +1-555-0123"
    
    # First get the LLM output
    chain = prompt | chat
    completion = chain.invoke({"text": text})
    
    print("\n📝 Original prompt input:")
    print(f"   {text}")
    
    print("\n🤖 LLM output:")
    print(f"   {str(completion)[:100]}...")
    
    print("\n🔄 RetryParser with prompt context...")
    
    try:
        # RetryParser needs the original prompt to retry
        result = retry_parser.parse_with_prompt(
            completion.content,
            prompt.format(text=text)
        )
        print("   ✓ Parsed successfully!")
        print(f"\n   Name: {result.name}")
        print(f"   Email: {result.email}")
        print(f"   Phone: {result.phone}")
    except Exception as e:
        print(f"   ✗ Failed: {e}")
    
    print("\n💡 RetryParser re-prompts with error context!")
    print()


def custom_output_parser():
    """Example 4: Create custom output parser"""
    
    print("=" * 70)
    print("🎨 Custom Output Parser")
    print("=" * 70)
    
    class KeyValueParser(BaseOutputParser[Dict[str, str]]):
        """Custom parser for key:value format"""
        
        def parse(self, text: str) -> Dict[str, str]:
            """Parse key:value pairs"""
            result = {}
            lines = text.strip().split('\n')
            
            for line in lines:
                if ':' in line:
                    key, value = line.split(':', 1)
                    result[key.strip()] = value.strip()
            
            return result
        
        def get_format_instructions(self) -> str:
            return """Format your response as key:value pairs, one per line.
Example:
name: John Doe
age: 30
city: New York"""
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.3,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    parser = KeyValueParser()
    
    template = PromptTemplate(
        template="""Extract person information.

{format_instructions}

Text: {text}

Output:""",
        input_variables=["text"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    
    chain = template | chat | parser
    
    text = "Sarah Johnson is 28 years old and lives in Seattle, Washington"
    
    print("\n👤 Input:")
    print(f"   {text}")
    
    result = chain.invoke({"text": text})
    
    print("\n🤖 Parsed output:")
    for key, value in result.items():
        print(f"   {key}: {value}")
    
    print(f"\n✨ Result type: {type(result)}")
    
    print("\n💡 Custom parsers for unique formats!")
    print()


def error_handling_strategies():
    """Example 5: Different error handling approaches"""
    
    print("=" * 70)
    print("🛡️  Error Handling Strategies")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.3,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    class Score(BaseModel):
        """Test score"""
        subject: str
        score: int = Field(ge=0, le=100)
    
    parser = PydanticOutputParser(pydantic_object=Score)
    
    malformed_outputs = [
        '{"subject": "Math", "score": 150}',  # Invalid score
        '{"subject": "English"}',  # Missing field
        'This is not JSON',  # Not JSON
    ]
    
    print("\n🛡️  Strategy 1: Try-except with fallback")
    
    for i, output in enumerate(malformed_outputs, 1):
        print(f"\n   Test {i}: {output[:50]}...")
        try:
            result = parser.parse(output)
            print(f"      ✓ Success: {result}")
        except Exception as e:
            print(f"      ✗ Error: {str(e)[:50]}...")
            print(f"      → Fallback: Return default value")
            result = {"subject": "Unknown", "score": 0}
            print(f"      → Default: {result}")
    
    print("\n🛡️  Strategy 2: OutputFixingParser")
    print("   → Automatically fixes errors using LLM")
    
    print("\n🛡️  Strategy 3: RetryOutputParser")
    print("   → Retries with error context")
    
    print("\n🛡️  Strategy 4: Multiple parser cascade")
    print("   → Try strict parser, fall back to lenient")
    
    print("\n💡 Choose strategy based on requirements!")
    print()


def pattern_injection():
    """Example 6: Pattern injection techniques"""
    
    print("=" * 70)
    print("💉 Pattern Injection Techniques")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.3,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    class Task(BaseModel):
        """Task item"""
        title: str
        priority: str = Field(description="low, medium, or high")
    
    parser = PydanticOutputParser(pydantic_object=Task)
    
    print("\n💉 Technique 1: Partial variables (recommended)")
    
    template1 = PromptTemplate(
        template="Extract task.\n\n{format_instructions}\n\nText: {text}",
        input_variables=["text"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    
    print("   ✓ Instructions injected automatically")
    print(f"   ✓ Input variables: {template1.input_variables}")
    
    print("\n💉 Technique 2: Direct formatting")
    
    template2 = PromptTemplate(
        template="Extract task.\n\n{format_instructions}\n\nText: {text}",
        input_variables=["format_instructions", "text"]
    )
    
    print("   ✓ Manual control over instructions")
    print("   ⚠️  Must pass format_instructions manually")
    
    print("\n💉 Technique 3: System message injection")
    
    chat_template = ChatPromptTemplate.from_messages([
        ("system", "{format_instructions}"),
        ("human", "Extract task: {text}")
    ])
    
    print("   ✓ Instructions in system message")
    print("   ✓ Cleaner user message")
    
    # Test all techniques
    text = "Fix critical bug in payment system ASAP"
    
    print(f"\n📝 Test input: {text}")
    print("\n🧪 Testing techniques...")
    
    # Technique 1
    chain1 = template1 | chat | parser
    result1 = chain1.invoke({"text": text})
    print(f"\n   Technique 1: {result1.title} ({result1.priority})")
    
    # Technique 3
    chain3 = chat_template | chat | parser
    result3 = chain3.invoke({
        "text": text,
        "format_instructions": parser.get_format_instructions()
    })
    print(f"   Technique 3: {result3.title} ({result3.priority})")
    
    print("\n💡 Partial variables = cleanest approach!")
    print()


def combining_parsers():
    """Example 7: Combine multiple parsers"""
    
    print("=" * 70)
    print("🔀 Combining Multiple Parsers")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.3,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Parser 1: Extract metadata
    class Metadata(BaseModel):
        """Document metadata"""
        title: str
        author: str
        category: str
    
    metadata_parser = PydanticOutputParser(pydantic_object=Metadata)
    
    # Parser 2: Extract content
    content_schemas = [
        ResponseSchema(name="summary", description="Brief summary"),
        ResponseSchema(name="key_points", description="Main points")
    ]
    content_parser = StructuredOutputParser.from_response_schemas(content_schemas)
    
    document = """
    Title: Introduction to Machine Learning
    Author: Dr. Sarah Chen
    Category: Technology
    
    Machine learning is transforming industries through automated pattern recognition.
    Key applications include image recognition, natural language processing,
    and predictive analytics.
    """
    
    print("\n📄 Processing document with two parsers:")
    
    # Step 1: Extract metadata
    meta_template = PromptTemplate(
        template="Extract metadata.\n\n{format_instructions}\n\nDoc: {doc}",
        input_variables=["doc"],
        partial_variables={"format_instructions": metadata_parser.get_format_instructions()}
    )
    
    meta_chain = meta_template | chat | metadata_parser
    metadata = meta_chain.invoke({"doc": document})
    
    print(f"\n   📋 Metadata (Parser 1):")
    print(f"      Title: {metadata.title}")
    print(f"      Author: {metadata.author}")
    print(f"      Category: {metadata.category}")
    
    # Step 2: Extract content
    content_template = PromptTemplate(
        template="Extract content.\n\n{format_instructions}\n\nDoc: {doc}",
        input_variables=["doc"],
        partial_variables={"format_instructions": content_parser.get_format_instructions()}
    )
    
    content_chain = content_template | chat | content_parser
    content = content_chain.invoke({"doc": document})
    
    print(f"\n   📝 Content (Parser 2):")
    print(f"      Summary: {content['summary']}")
    print(f"      Key points: {content['key_points']}")
    
    print("\n💡 Use multiple parsers for complex extraction!")
    print()


def validation_and_fallbacks():
    """Example 8: Advanced validation with fallbacks"""
    
    print("=" * 70)
    print("✅ Advanced Validation & Fallbacks")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.3,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    class UserProfile(BaseModel):
        """User profile with validation"""
        username: str = Field(min_length=3, max_length=20)
        email: str
        age: int = Field(ge=13, le=120)
        bio: str = Field(max_length=200)
        
        @validator('email')
        def validate_email(cls, v):
            if '@' not in v:
                raise ValueError('Invalid email')
            return v.lower()
        
        @validator('username')
        def validate_username(cls, v):
            if not v.isalnum():
                raise ValueError('Username must be alphanumeric')
            return v
    
    # Strict parser
    strict_parser = PydanticOutputParser(pydantic_object=UserProfile)
    
    # Lenient fallback
    class BasicProfile(BaseModel):
        """Basic profile without strict validation"""
        username: str
        email: str
        age: int
        bio: str
    
    lenient_parser = PydanticOutputParser(pydantic_object=BasicProfile)
    
    template = PromptTemplate(
        template="Extract profile.\n\n{format_instructions}\n\nText: {text}",
        input_variables=["text"],
        partial_variables={"format_instructions": strict_parser.get_format_instructions()}
    )
    
    chain = template | chat
    
    test_cases = [
        "User: john123, email john@email.com, age 25, bio: Software developer",
        "User: ab, email invalid-email, age 150, bio: Test user"
    ]
    
    print("\n✅ Testing validation cascade:")
    
    for i, text in enumerate(test_cases, 1):
        print(f"\n   Test {i}: {text[:50]}...")
        
        completion = chain.invoke({"text": text})
        
        # Try strict parser first
        try:
            result = strict_parser.parse(completion.content)
            print(f"      ✓ Strict validation passed")
            print(f"      → Username: {result.username}")
            print(f"      → Email: {result.email}")
        except Exception as e:
            print(f"      ✗ Strict validation failed: {str(e)[:40]}...")
            
            # Fallback to lenient
            try:
                result = lenient_parser.parse(completion.content)
                print(f"      ⚠️  Using lenient parser")
                print(f"      → Username: {result.username}")
                print(f"      → Email: {result.email}")
            except Exception as e2:
                print(f"      ✗ Lenient also failed: {str(e2)[:40]}...")
    
    print("\n💡 Validation cascade: Strict → Lenient → Default")
    print()


def main():
    """Run all advanced structured output examples"""
    
    print("\n" + "🚀" * 35)
    print("Welcome to Advanced Structured Output Techniques!")
    print("🚀" * 35 + "\n")
    
    # Check API key
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Error: GOOGLE_API_KEY not found!")
        return
    
    try:
        parser_in_chain()
        input("Press Enter to continue...")
        
        output_fixing_parser()
        input("Press Enter to continue...")
        
        retry_output_parser()
        input("Press Enter to continue...")
        
        custom_output_parser()
        input("Press Enter to continue...")
        
        error_handling_strategies()
        input("Press Enter to continue...")
        
        pattern_injection()
        input("Press Enter to continue...")
        
        combining_parsers()
        input("Press Enter to continue...")
        
        validation_and_fallbacks()
        
        print("=" * 70)
        print("✅ All Advanced examples completed!")
        print("=" * 70)
        print("\n💡 Key Takeaways:")
        print("  ✓ LCEL chains: prompt | llm | parser")
        print("  ✓ OutputFixingParser: Auto-fix with LLM")
        print("  ✓ RetryOutputParser: Retry with context")
        print("  ✓ Custom parsers: Full control")
        print("  ✓ Error strategies: Try-except, fixing, retry")
        print("  ✓ Pattern injection: Partial variables best")
        print("  ✓ Multiple parsers: Complex extraction")
        print("  ✓ Validation cascade: Strict → Lenient → Default")
        print("\n📚 Next: Try 04_practical_structured.py for real projects!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
