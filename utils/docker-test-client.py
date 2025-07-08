#!/usr/bin/env python3
"""
Docker Test Client for the DeepSeek Chatbot API
This script tests the API running in a Docker container.
"""

import requests
import json
import time
import sys

# API configuration for Docker container
BASE_URL = "http://localhost:5001"

def wait_for_service(max_retries=30, delay=2):
    """Wait for the service to be ready."""
    print("⏳ Waiting for service to be ready...")
    
    for i in range(max_retries):
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=5)
            if response.status_code == 200:
                print("✅ Service is ready!")
                return True
        except requests.exceptions.RequestException:
            pass
        
        print(f"⏳ Attempt {i+1}/{max_retries} - Service not ready yet...")
        time.sleep(delay)
    
    print("❌ Service failed to start within expected time")
    return False

def test_health_check():
    """Test the health check endpoint."""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the server. Make sure the Docker container is running.")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_chat_endpoint(message, max_length=256, temperature=0.7, top_p=0.9):
    """Test the chat endpoint with a given message."""
    print(f"\n💬 Testing chat endpoint with message: '{message[:50]}...'")
    
    payload = {
        "message": message,
        "max_length": max_length,
        "temperature": temperature,
        "top_p": top_p
    }
    
    try:
        start_time = time.time()
        response = requests.post(f"{BASE_URL}/chat", json=payload, timeout=60)
        request_time = time.time() - start_time
        
        print(f"Status Code: {response.status_code}")
        print(f"Request Time: {request_time:.2f}s")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {data['response']}")
            print(f"Generation Time: {data['generation_time']}s")
            print(f"Model: {data['model']}")
            print(f"Parameters: {data['parameters']}")
        else:
            print(f"Error Response: {response.text}")
            
        return response.status_code == 200
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the server.")
        return False
    except requests.exceptions.Timeout:
        print("⏰ Request timed out (this is normal for the first request as the model loads)")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def run_interactive_chat():
    """Run an interactive chat session."""
    print("\n🎯 Starting interactive chat session...")
    print("Type 'quit' to exit, 'help' for available commands")
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() == 'quit':
                print("👋 Goodbye!")
                break
            elif user_input.lower() == 'help':
                print("Available commands:")
                print("  - Type any message to chat with the AI")
                print("  - 'quit' to exit")
                print("  - 'help' to show this message")
                continue
            elif not user_input:
                continue
            
            # Send chat request
            success = test_chat_endpoint(user_input)
            if not success:
                print("❌ Failed to get response. Check if the container is running.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def main():
    """Main function to run all tests."""
    print("🚀 DeepSeek Chatbot API Docker Test Client")
    print("=" * 50)
    
    # Wait for service to be ready
    if not wait_for_service():
        print("\n❌ Service failed to start. Please check Docker logs:")
        print("docker-compose logs deepseek-chatbot")
        return
    
    # Test health check
    if not test_health_check():
        print("\n❌ Health check failed. Make sure the Docker container is running.")
        print("Run: docker-compose up")
        return
    
    # Test chat with different types of prompts
    test_messages = [
        "Hello! How are you today?",
        "Write a Python function to calculate the factorial of a number.",
        "Explain what machine learning is in simple terms.",
        "What are the benefits of using Docker for development?"
    ]
    
    print("\n🧪 Running automated tests...")
    for message in test_messages:
        test_chat_endpoint(message, max_length=128, temperature=0.7)
        time.sleep(2)  # Small delay between requests
    
    # Ask user if they want to run interactive chat
    print("\n" + "=" * 50)
    choice = input("Would you like to start an interactive chat session? (y/n): ").strip().lower()
    
    if choice in ['y', 'yes']:
        run_interactive_chat()
    else:
        print("👋 Thanks for testing!")

if __name__ == "__main__":
    main() 