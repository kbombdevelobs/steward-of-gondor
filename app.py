from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import logging
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Set the model path to the only supported local model
MODEL_PATH = "./models/deepseek-coder-1.3b-instruct"

class DeepSeekChatbot:
    def __init__(self, device=None):
        self.model_name = MODEL_PATH
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None
        self.tokenizer = None
        self.load_model()

    def load_model(self):
        """Load the DeepSeek model and tokenizer from local storage only."""
        try:
            logger.info(f"Loading model: {self.model_name}")
            if not os.path.exists(self.model_name):
                raise FileNotFoundError(f"Local model not found: {self.model_name}. Please ensure the model is downloaded to the local models directory.")
            model_path = self.model_name
            logger.info(f"Loading from local path: {model_path}")
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_path,
                trust_remote_code=True,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
            )
            self.model = AutoModelForCausalLM.from_pretrained(
                model_path,
                trust_remote_code=True,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
            ).to(self.device)
            logger.info("Model loaded successfully.")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise

    def generate_response(self, prompt, max_length=512, temperature=0.7, top_p=0.9):
        """
        Generate a response using the DeepSeek model.
        
        Args:
            prompt (str): The input prompt
            max_length (int): Maximum length of the generated response
            temperature (float): Sampling temperature
            top_p (float): Top-p sampling parameter
            
        Returns:
            str: Generated response
        """
        if self.model is None or self.tokenizer is None:
            raise ValueError("Model not loaded. Call load_model() first.")
        
        try:
            # Format the prompt for instruction-following
            formatted_prompt = f"<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"
            
            # Tokenize input
            inputs = self.tokenizer(
                formatted_prompt,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=1024
            )
            
            if self.device == "cpu":
                inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Generate response
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=max_length,
                    temperature=temperature,
                    top_p=top_p,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                    eos_token_id=self.tokenizer.eos_token_id
                )
            
            # Decode response
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract only the assistant's response
            response = response.split("<|im_start|>assistant\n")[-1].split("<|im_end|>")[0].strip()
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise

# Initialize chatbot (model will be loaded in __init__)
chatbot = DeepSeekChatbot()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "model_loaded": chatbot.model is not None,
        "device": chatbot.device
    })

@app.route('/chat', methods=['POST'])
def chat():
    """
    Chat endpoint that accepts POST requests with JSON payload.
    
    Expected JSON format:
    {
        "message": "Your message here",
        "max_length": 512,
        "temperature": 0.7,
        "top_p": 0.9
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                "error": "Missing 'message' field in request body"
            }), 400
        
        message = data['message']
        max_length = data.get('max_length', 512)
        temperature = data.get('temperature', 0.7)
        top_p = data.get('top_p', 0.9)
        
        # Validate parameters
        if not isinstance(message, str) or not message.strip():
            return jsonify({
                "error": "Message must be a non-empty string"
            }), 400
        
        if not (0 < temperature <= 2.0):
            return jsonify({
                "error": "Temperature must be between 0 and 2.0"
            }), 400
        
        if not (0 < top_p <= 1.0):
            return jsonify({
                "error": "top_p must be between 0 and 1.0"
            }), 400
        
        # Generate response
        start_time = time.time()
        response = chatbot.generate_response(
            message, 
            max_length=max_length,
            temperature=temperature,
            top_p=top_p
        )
        generation_time = time.time() - start_time
        
        return jsonify({
            "response": response,
            "generation_time": round(generation_time, 2),
            "model": chatbot.model_name,
            "parameters": {
                "max_length": max_length,
                "temperature": temperature,
                "top_p": top_p
            }
        })
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            "error": f"Internal server error: {str(e)}"
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": "Method not allowed"}), 405

if __name__ == '__main__':
    # Model is already loaded in DeepSeekChatbot.__init__()
    # Run the Flask app
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    logger.info(f"Starting Flask server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug) 