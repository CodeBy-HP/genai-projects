"""
🎨 Embeddings Example - Semantic Search with Gemini

This example shows how embeddings convert text into vectors (numbers)
that capture meaning. This enables powerful semantic search!
"""

import os
import numpy as np
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Load environment variables
load_dotenv()


def basic_embedding_example():
    """Simple example: Convert text to embeddings"""
    
    print("=" * 60)
    print("🎨 Basic Embedding Example")
    print("=" * 60)
    
    # Initialize Gemini Embeddings
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    text = "Hello, I'm learning about LangChain embeddings!"
    
    print(f"\n📝 Original Text: '{text}'")
    
    # Convert text to embedding (vector of numbers)
    embedding = embeddings.embed_query(text)
    
    print(f"\n🔢 Embedding (first 10 values): {embedding[:10]}")
    print(f"📏 Embedding dimension: {len(embedding)}")
    print("\n💡 This vector of numbers represents the meaning of the text!")
    print()


def similarity_comparison():
    """Example: Compare similarity between different texts"""
    
    print("=" * 60)
    print("🔍 Semantic Similarity Comparison")
    print("=" * 60)
    
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Different texts to compare
    texts = [
        "The dog is playing in the garden",
        "A puppy is running in the backyard",
        "I love eating pizza for dinner",
        "Python is a programming language"
    ]
    
    print("\n📝 Texts to compare:")
    for i, text in enumerate(texts, 1):
        print(f"   {i}. {text}")
    
    # Get embeddings for all texts
    print("\n⚙️  Converting texts to embeddings...")
    text_embeddings = embeddings.embed_documents(texts)
    
    # Calculate cosine similarity between first text and others
    def cosine_similarity(vec1, vec2):
        """Calculate cosine similarity between two vectors"""
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    
    print("\n🎯 Similarity scores (compared to first text):\n")
    
    base_embedding = text_embeddings[0]
    
    for i, (text, embedding) in enumerate(zip(texts, text_embeddings), 1):
        similarity = cosine_similarity(base_embedding, embedding)
        
        # Visual representation
        bar = "█" * int(similarity * 40)
        
        print(f"{i}. {text}")
        print(f"   Similarity: {similarity:.4f} {bar}\n")
    
    print("💡 Notice: Similar meanings have higher similarity scores!")
    print("   Text 1 and 2 are about dogs/puppies - HIGH similarity")
    print("   Text 3 and 4 are completely different - LOW similarity\n")


def semantic_search_example():
    """Example: Build a simple semantic search system"""
    
    print("=" * 60)
    print("🔎 Semantic Search - Finding Relevant Information")
    print("=" * 60)
    
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Our "knowledge base" - collection of documents
    documents = [
        "LangChain is a framework for developing applications powered by language models.",
        "Python is a high-level programming language known for its simplicity.",
        "Machine learning is a subset of artificial intelligence focused on learning from data.",
        "React is a JavaScript library for building user interfaces.",
        "Embeddings convert text into numerical vectors that represent meaning.",
        "Natural language processing helps computers understand human language.",
        "Git is a version control system for tracking changes in code.",
        "APIs allow different software applications to communicate with each other."
    ]
    
    print("\n📚 Knowledge Base (8 documents):")
    for i, doc in enumerate(documents, 1):
        print(f"   {i}. {doc[:60]}...")
    
    # User's query
    query = "How do computers understand text?"
    
    print(f"\n❓ User Query: '{query}'")
    print("\n⚙️  Searching for most relevant documents...\n")
    
    # Embed the query
    query_embedding = embeddings.embed_query(query)
    
    # Embed all documents
    doc_embeddings = embeddings.embed_documents(documents)
    
    # Calculate similarity with each document
    def cosine_similarity(vec1, vec2):
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    
    similarities = [
        (i, doc, cosine_similarity(query_embedding, doc_emb))
        for i, (doc, doc_emb) in enumerate(zip(documents, doc_embeddings), 1)
    ]
    
    # Sort by similarity (highest first)
    similarities.sort(key=lambda x: x[2], reverse=True)
    
    # Show top 3 results
    print("🏆 Top 3 Most Relevant Documents:\n")
    
    for rank, (i, doc, score) in enumerate(similarities[:3], 1):
        print(f"{rank}. Document #{i} (Score: {score:.4f})")
        print(f"   {doc}")
        print()
    
    print("✨ This is semantic search - it found relevant docs based on MEANING,")
    print("   not just keyword matching! 'Embeddings' and 'NLP' are semantically")
    print("   related to understanding text.\n")


def practical_use_case():
    """Example: FAQ matching system"""
    
    print("=" * 60)
    print("🎯 Practical Use Case - Smart FAQ System")
    print("=" * 60)
    
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # FAQ database
    faqs = {
        "How do I reset my password?": "Go to Settings > Security > Reset Password. You'll receive an email with instructions.",
        "What payment methods do you accept?": "We accept credit cards, debit cards, PayPal, and bank transfers.",
        "How can I contact customer support?": "Email us at support@example.com or call 1-800-SUPPORT (Mon-Fri, 9am-5pm).",
        "Do you offer refunds?": "Yes, we offer full refunds within 30 days of purchase, no questions asked.",
        "How do I update my account information?": "Log in to your account and navigate to Settings > Profile to update your information."
    }
    
    print("\n📋 Our FAQ Database:")
    for i, question in enumerate(faqs.keys(), 1):
        print(f"   {i}. {question}")
    
    # User asks a question (might not be exact match!)
    user_question = "I forgot my login credentials, what should I do?"
    
    print(f"\n👤 User Question: '{user_question}'")
    print("\n⚙️  Finding best matching FAQ...\n")
    
    # Embed user question and all FAQs
    user_embedding = embeddings.embed_query(user_question)
    faq_questions = list(faqs.keys())
    faq_embeddings = embeddings.embed_documents(faq_questions)
    
    # Find most similar FAQ
    def cosine_similarity(vec1, vec2):
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    
    similarities = [
        (question, cosine_similarity(user_embedding, faq_emb))
        for question, faq_emb in zip(faq_questions, faq_embeddings)
    ]
    
    best_match = max(similarities, key=lambda x: x[1])
    matched_question, similarity = best_match
    
    print(f"🎯 Best Match (Score: {similarity:.4f}):")
    print(f"   Question: {matched_question}")
    print(f"\n🤖 Answer:")
    print(f"   {faqs[matched_question]}")
    print("\n✨ Even though the user didn't use the exact words, embeddings")
    print("   found the right FAQ based on semantic similarity!\n")


def batch_embedding_example():
    """Example: Efficiently process multiple texts"""
    
    print("=" * 60)
    print("⚡ Batch Processing - Embedding Multiple Texts Efficiently")
    print("=" * 60)
    
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Large collection of texts
    texts = [
        "Artificial Intelligence is transforming industries",
        "Cloud computing provides on-demand resources",
        "Cybersecurity protects digital assets",
        "Data science extracts insights from data",
        "DevOps bridges development and operations"
    ]
    
    print(f"\n📝 Processing {len(texts)} texts in batch...")
    print()
    
    # Batch embed - much more efficient than one at a time!
    batch_embeddings = embeddings.embed_documents(texts)
    
    print(f"✅ Successfully created {len(batch_embeddings)} embeddings!")
    print(f"📏 Each embedding has {len(batch_embeddings[0])} dimensions")
    print("\n💡 Batch processing is faster and more efficient for multiple texts!\n")


def main():
    """Run all embedding examples"""
    
    print("\n" + "🎨" * 30)
    print("Welcome to LangChain Embeddings Examples with Gemini!")
    print("🎨" * 30 + "\n")
    
    # Check if API key is set
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Error: GOOGLE_API_KEY not found in environment variables!")
        print("Make sure you have a .env file with your API key.")
        return
    
    # Check for numpy
    try:
        import numpy
    except ImportError:
        print("❌ Error: numpy is required for this example!")
        print("Install it with: pip install numpy")
        return
    
    try:
        # Run all examples
        basic_embedding_example()
        input("Press Enter to continue...")
        
        similarity_comparison()
        input("Press Enter to continue...")
        
        semantic_search_example()
        input("Press Enter to continue...")
        
        practical_use_case()
        input("Press Enter to continue...")
        
        batch_embedding_example()
        
        print("=" * 60)
        print("✅ All Embedding examples completed!")
        print("=" * 60)
        print("\n💡 Key Takeaways:")
        print("  ✓ Embeddings convert text to numerical vectors")
        print("  ✓ Similar meanings → similar vectors")
        print("  ✓ Perfect for semantic search and recommendations")
        print("  ✓ Use embed_query() for queries, embed_documents() for docs")
        print("  ✓ Batch processing is more efficient")
        print("\n🎓 Common Use Cases:")
        print("  • Semantic search engines")
        print("  • Recommendation systems")
        print("  • Document clustering")
        print("  • Question answering systems")
        print("  • RAG (Retrieval Augmented Generation)")
        print("\n🎉 Congratulations! You've completed all LangChain Models examples!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure your GOOGLE_API_KEY is valid!")


if __name__ == "__main__":
    main()
