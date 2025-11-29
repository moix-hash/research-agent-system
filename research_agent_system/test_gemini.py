import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load your API key from .env file
load_dotenv()

# Get your API key
api_key = os.getenv('GEMINI_API_KEY')
print(f"API Key loaded: {api_key[:10]}...")  # Show first 10 chars for security

# Configure Gemini
try:
    genai.configure(api_key=api_key)
    print("✅ Gemini configured successfully!")
    
    # List all available models
    print("\n🔍 Available models with generateContent:")
    available_models = []
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            available_models.append(model.name)
            print(f"   ✅ {model.name}")
    
    if not available_models:
        print("   ❌ No models found with generateContent capability!")
        exit(1)
    
    # Test the first available model
    test_model = available_models[0]
    print(f"\n🧪 Testing with model: {test_model}")
    
    model = genai.GenerativeModel(test_model)
    response = model.generate_content("Write one sentence about AI.")
    
    print("✅ API Test SUCCESSFUL!")
    print(f"📝 Response: {response.text}")
    
except Exception as e:
    print(f"❌ API Test FAILED: {e}")