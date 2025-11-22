"""
🎯 with_structured_output - Native Structured Output

This example covers:
- with_structured_output() method (MODERN WAY!)
- Pydantic models (recommended)
- TypedDict (Python native)
- JSON schemas
- Field validation and constraints
- Complex nested structures
- Enums and literal types

For models that support native structured output (Gemini, GPT-4, Claude 3+)
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from typing import TypedDict, List, Optional, Literal
from enum import Enum

# Load environment variables
load_dotenv()


def basic_pydantic_example():
    """Example 1: Basic structured output with Pydantic"""
    
    print("=" * 70)
    print("🎯 Basic with_structured_output - Pydantic Model")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.3,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Define the structure we want
    class Person(BaseModel):
        """Information about a person"""
        name: str = Field(description="Person's full name")
        age: int = Field(description="Person's age in years")
        email: str = Field(description="Email address")
    
    # Create structured LLM - THIS IS THE MAGIC! ✨
    structured_llm = chat.with_structured_output(Person)
    
    print("\n📋 Expected Structure (Pydantic Model):")
    print(f"   - name: str")
    print(f"   - age: int")
    print(f"   - email: str")
    
    # Use it like normal, but get structured output!
    prompt = "Create a profile for John Smith, 28 years old, email: john.smith@email.com"
    
    print(f"\n👤 Input: {prompt}")
    print("\n🤖 Structured Output:")
    
    result = structured_llm.invoke(prompt)
    
    # Result is a Person object!
    print(f"   Type: {type(result)}")
    print(f"   Name: {result.name}")
    print(f"   Age: {result.age}")
    print(f"   Email: {result.email}")
    
    # Can access as dict too
    print(f"\n📦 As Dictionary:")
    print(f"   {result.dict()}")
    
    print("\n✨ No parsing needed! Direct object access!")
    print()


def pydantic_with_validation():
    """Example 2: Pydantic with field validation"""
    
    print("=" * 70)
    print("🛡️ Pydantic with Validation Constraints")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.3,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Define model with validation
    class Product(BaseModel):
        """Product information with validation"""
        name: str = Field(description="Product name", min_length=3, max_length=100)
        price: float = Field(description="Price in USD", gt=0, le=10000)
        quantity: int = Field(description="Quantity in stock", ge=0)
        category: str = Field(description="Product category")
        in_stock: bool = Field(description="Whether product is in stock")
    
    structured_llm = chat.with_structured_output(Product)
    
    print("\n📋 Product Model with Constraints:")
    print("   - name: 3-100 characters")
    print("   - price: $0-$10,000")
    print("   - quantity: >= 0")
    print("   - in_stock: boolean")
    
    prompt = "Extract product info: MacBook Pro laptop, priced at $1299, 15 units available"
    
    print(f"\n👤 Input: {prompt}")
    print("\n🤖 Validated Output:")
    
    result = structured_llm.invoke(prompt)
    
    print(f"   Name: {result.name}")
    print(f"   Price: ${result.price}")
    print(f"   Quantity: {result.quantity}")
    print(f"   Category: {result.category}")
    print(f"   In Stock: {result.in_stock}")
    
    print("\n✅ All validations passed automatically!")
    print()


def using_enums():
    """Example 3: Using Enums for fixed choices"""
    
    print("=" * 70)
    print("🎨 Using Enums for Fixed Choices")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.3,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Define enums
    class Priority(str, Enum):
        LOW = "low"
        MEDIUM = "medium"
        HIGH = "high"
        URGENT = "urgent"
    
    class TaskStatus(str, Enum):
        TODO = "todo"
        IN_PROGRESS = "in_progress"
        DONE = "done"
    
    class Task(BaseModel):
        """A task with enum fields"""
        title: str = Field(description="Task title")
        description: str = Field(description="Detailed description")
        priority: Priority = Field(description="Task priority level")
        status: TaskStatus = Field(description="Current status")
        estimated_hours: int = Field(description="Estimated hours to complete", ge=1, le=40)
    
    structured_llm = chat.with_structured_output(Task)
    
    print("\n📋 Task Model with Enums:")
    print("   Priority: low | medium | high | urgent")
    print("   Status: todo | in_progress | done")
    
    prompt = "Create a task: Implement user authentication, high priority, not started yet, will take about 8 hours"
    
    print(f"\n👤 Input: {prompt}")
    print("\n🤖 Structured Output:")
    
    result = structured_llm.invoke(prompt)
    
    print(f"   Title: {result.title}")
    print(f"   Description: {result.description}")
    print(f"   Priority: {result.priority.value} ⭐")
    print(f"   Status: {result.status.value}")
    print(f"   Estimated Hours: {result.estimated_hours}h")
    
    print("\n✨ Enums ensure only valid values!")
    print()


def complex_nested_structure():
    """Example 4: Complex nested Pydantic models"""
    
    print("=" * 70)
    print("🏗️ Complex Nested Structures")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.3,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Nested models
    class Address(BaseModel):
        """Address information"""
        street: str
        city: str
        state: str
        zip_code: str
        country: str = "USA"
    
    class ContactInfo(BaseModel):
        """Contact information"""
        email: str
        phone: Optional[str] = None
        preferred_contact: Literal["email", "phone", "both"] = "email"
    
    class Employee(BaseModel):
        """Complete employee record"""
        name: str = Field(description="Full name")
        employee_id: str = Field(description="Unique employee ID")
        department: str = Field(description="Department name")
        position: str = Field(description="Job title")
        salary: float = Field(description="Annual salary", gt=0)
        address: Address = Field(description="Home address")
        contact: ContactInfo = Field(description="Contact details")
        skills: List[str] = Field(description="List of skills")
    
    structured_llm = chat.with_structured_output(Employee)
    
    print("\n📋 Nested Employee Model:")
    print("   Employee")
    print("   ├── Basic Info (name, id, dept, position, salary)")
    print("   ├── Address (nested object)")
    print("   ├── Contact (nested object)")
    print("   └── Skills (list)")
    
    prompt = """Extract employee information:
    Sarah Johnson, ID: EMP-2024-001
    Senior Software Engineer in Engineering Department
    Salary: $120,000/year
    Lives at 123 Main St, San Francisco, CA 94102
    Email: sarah.j@company.com, Phone: 555-0123
    Skills: Python, JavaScript, React, Node.js, AWS"""
    
    print(f"\n👤 Input:\n{prompt}")
    print("\n🤖 Structured Output:")
    
    result = structured_llm.invoke(prompt)
    
    print(f"\n📝 Employee: {result.name}")
    print(f"   ID: {result.employee_id}")
    print(f"   Position: {result.position}")
    print(f"   Department: {result.department}")
    print(f"   Salary: ${result.salary:,.0f}")
    print(f"\n📍 Address:")
    print(f"   {result.address.street}")
    print(f"   {result.address.city}, {result.address.state} {result.address.zip_code}")
    print(f"\n📞 Contact:")
    print(f"   Email: {result.contact.email}")
    print(f"   Phone: {result.contact.phone}")
    print(f"\n💼 Skills ({len(result.skills)}):")
    for skill in result.skills:
        print(f"   • {skill}")
    
    print("\n✨ Complex nested structures work perfectly!")
    print()


def using_typeddict():
    """Example 5: Using TypedDict (Python native)"""
    
    print("=" * 70)
    print("📘 Using TypedDict (Python Native)")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.3,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # TypedDict - simpler than Pydantic
    class Movie(TypedDict):
        title: str
        year: int
        director: str
        genre: str
        rating: float
    
    structured_llm = chat.with_structured_output(Movie)
    
    print("\n📋 TypedDict Structure:")
    print("   Simple Python dict with type hints")
    print("   No validation, just type information")
    
    prompt = "Extract movie info: The Shawshank Redemption, 1994, directed by Frank Darabont, Drama, rated 9.3/10"
    
    print(f"\n👤 Input: {prompt}")
    print("\n🤖 Structured Output:")
    
    result = structured_llm.invoke(prompt)
    
    print(f"   Type: {type(result)}")  # dict
    print(f"   Title: {result['title']}")
    print(f"   Year: {result['year']}")
    print(f"   Director: {result['director']}")
    print(f"   Genre: {result['genre']}")
    print(f"   Rating: {result['rating']}/10")
    
    print("\n💡 TypedDict is simpler but lacks validation!")
    print("   Use Pydantic when you need validation.")
    print()


def using_json_schema():
    """Example 6: Using JSON Schema"""
    
    print("=" * 70)
    print("📜 Using JSON Schema")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.3,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Define JSON Schema
    book_schema = {
        "title": "Book",
        "description": "Information about a book",
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "Book title"
            },
            "author": {
                "type": "string",
                "description": "Author name"
            },
            "pages": {
                "type": "integer",
                "description": "Number of pages",
                "minimum": 1
            },
            "published_year": {
                "type": "integer",
                "description": "Year of publication"
            },
            "isbn": {
                "type": "string",
                "description": "ISBN number"
            },
            "genres": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of genres"
            }
        },
        "required": ["title", "author", "pages"]
    }
    
    structured_llm = chat.with_structured_output(book_schema)
    
    print("\n📋 JSON Schema:")
    print("   Direct schema definition")
    print("   Good for API integration")
    print("   Required: title, author, pages")
    
    prompt = "Book info: '1984' by George Orwell, 328 pages, published 1949, ISBN 978-0451524935, genres: dystopian, political fiction"
    
    print(f"\n👤 Input: {prompt}")
    print("\n🤖 Structured Output:")
    
    result = structured_llm.invoke(prompt)
    
    print(f"   Title: {result['title']}")
    print(f"   Author: {result['author']}")
    print(f"   Pages: {result['pages']}")
    print(f"   Published: {result['published_year']}")
    print(f"   ISBN: {result['isbn']}")
    print(f"   Genres: {', '.join(result['genres'])}")
    
    print("\n💡 JSON Schema: Most flexible for API work!")
    print()


def custom_validators():
    """Example 7: Custom Pydantic validators"""
    
    print("=" * 70)
    print("🔐 Custom Pydantic Validators")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.3,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    class UserRegistration(BaseModel):
        """User registration with custom validation"""
        username: str = Field(description="Username (alphanumeric only)")
        email: str = Field(description="Valid email address")
        age: int = Field(description="User age", ge=18, le=120)
        password_strength: Literal["weak", "medium", "strong"] = Field(
            description="Password strength assessment"
        )
        
        @validator('username')
        def username_alphanumeric(cls, v):
            if not v.replace('_', '').isalnum():
                raise ValueError('Username must be alphanumeric')
            return v
        
        @validator('email')
        def email_valid(cls, v):
            if '@' not in v or '.' not in v:
                raise ValueError('Invalid email format')
            return v.lower()
    
    structured_llm = chat.with_structured_output(UserRegistration)
    
    print("\n📋 UserRegistration with Validators:")
    print("   - Username: alphanumeric + underscore")
    print("   - Email: must contain @ and .")
    print("   - Age: 18-120")
    print("   - Password strength: weak/medium/strong")
    
    prompt = "Register user: john_doe123, email JOHN@EMAIL.COM, age 25, strong password"
    
    print(f"\n👤 Input: {prompt}")
    print("\n🤖 Validated Output:")
    
    result = structured_llm.invoke(prompt)
    
    print(f"   Username: {result.username}")
    print(f"   Email: {result.email} (normalized to lowercase)")
    print(f"   Age: {result.age}")
    print(f"   Password Strength: {result.password_strength}")
    
    print("\n✅ Custom validators ensure data quality!")
    print()


def list_extraction():
    """Example 8: Extracting lists of structured data"""
    
    print("=" * 70)
    print("📝 Extracting Lists of Structured Objects")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.3,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    class Ingredient(BaseModel):
        """Recipe ingredient"""
        name: str
        amount: str
        unit: str
    
    class Recipe(BaseModel):
        """Complete recipe"""
        dish_name: str = Field(description="Name of the dish")
        cuisine: str = Field(description="Type of cuisine")
        prep_time: int = Field(description="Preparation time in minutes")
        cook_time: int = Field(description="Cooking time in minutes")
        servings: int = Field(description="Number of servings")
        ingredients: List[Ingredient] = Field(description="List of ingredients")
        instructions: List[str] = Field(description="Step-by-step instructions")
    
    structured_llm = chat.with_structured_output(Recipe)
    
    print("\n📋 Recipe Model with Lists:")
    print("   - List of Ingredient objects")
    print("   - List of instruction strings")
    
    prompt = """Create a simple pasta recipe:
    Dish: Spaghetti Aglio e Olio (Italian cuisine)
    Takes 10 min prep, 15 min cooking, serves 4
    Ingredients: 400g spaghetti, 6 cloves garlic, 1/2 cup olive oil, 1 tsp red pepper flakes
    Steps: 
    1. Cook spaghetti
    2. Sauté garlic in oil
    3. Add pepper flakes
    4. Toss pasta with oil
    5. Serve hot"""
    
    print(f"\n👤 Input: Pasta recipe request")
    print("\n🤖 Structured Output:")
    
    result = structured_llm.invoke(prompt)
    
    print(f"\n🍝 {result.dish_name}")
    print(f"   Cuisine: {result.cuisine}")
    print(f"   Time: {result.prep_time} min prep + {result.cook_time} min cook")
    print(f"   Servings: {result.servings}")
    
    print(f"\n📦 Ingredients ({len(result.ingredients)}):")
    for ing in result.ingredients:
        print(f"   • {ing.amount} {ing.unit} {ing.name}")
    
    print(f"\n👨‍🍳 Instructions ({len(result.instructions)} steps):")
    for i, step in enumerate(result.instructions, 1):
        print(f"   {i}. {step}")
    
    print("\n✨ Lists of structured objects work perfectly!")
    print()


def main():
    """Run all with_structured_output examples"""
    
    print("\n" + "🎯" * 35)
    print("Welcome to with_structured_output - Native Structured Output!")
    print("🎯" * 35 + "\n")
    
    # Check API key
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Error: GOOGLE_API_KEY not found!")
        return
    
    try:
        basic_pydantic_example()
        input("Press Enter to continue...")
        
        pydantic_with_validation()
        input("Press Enter to continue...")
        
        using_enums()
        input("Press Enter to continue...")
        
        complex_nested_structure()
        input("Press Enter to continue...")
        
        using_typeddict()
        input("Press Enter to continue...")
        
        using_json_schema()
        input("Press Enter to continue...")
        
        custom_validators()
        input("Press Enter to continue...")
        
        list_extraction()
        
        print("=" * 70)
        print("✅ All with_structured_output examples completed!")
        print("=" * 70)
        print("\n💡 Key Takeaways:")
        print("  ✓ with_structured_output is the MODERN way")
        print("  ✓ Pydantic provides type safety + validation")
        print("  ✓ TypedDict is simpler but no validation")
        print("  ✓ JSON Schema is most flexible")
        print("  ✓ Enums ensure fixed choices")
        print("  ✓ Custom validators add business logic")
        print("  ✓ Lists and nested structures work great")
        print("  ✓ NO MANUAL PARSING NEEDED!")
        print("\n📚 Next: Try 02_output_parsers.py for universal parsing!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
