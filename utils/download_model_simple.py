#!/usr/bin/env python3
"""
Simple script to download DeepSeek 1.3B model for local use.
"""

import os
import sys

def download_model():
    """Download the DeepSeek 1.3B model."""
    
    try:
        from transformers import AutoTokenizer, AutoModelForCausalLM
        import torch
    except ImportError as e:
        print(f"❌ Missing required packages: {e}")
        print("Please install: pip install transformers torch")
        sys.exit(1)
    
    model_name = "deepseek-ai/deepseek-coder-1.3b-instruct"
    local_path = "./models/deepseek-coder-1.3b-instruct"
    
    print(f"🚀 Downloading {model_name}")
    print(f"📁 Saving to: {local_path}")
    print("⏳ This may take several minutes...")
    
    # Create directory
    os.makedirs(local_path, exist_ok=True)
    
    try:
        # Download tokenizer
        print("📝 Downloading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        tokenizer.save_pretrained(local_path)
        print("✅ Tokenizer downloaded")
        
        # Download model
        print("🤖 Downloading model weights (this may take a while)...")
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            trust_remote_code=True,
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True
        )
        model.save_pretrained(local_path)
        print("✅ Model weights downloaded")
        
        # Verify files
        files = os.listdir(local_path)
        print(f"\n📁 Files in {local_path}:")
        for file in files:
            size = os.path.getsize(os.path.join(local_path, file))
            print(f"  - {file} ({size:,} bytes)")
        
        print(f"\n🎉 Model downloaded successfully!")
        print(f"📁 Location: {os.path.abspath(local_path)}")
        
    except Exception as e:
        print(f"❌ Error downloading model: {e}")
        sys.exit(1)

if __name__ == "__main__":
    download_model() 