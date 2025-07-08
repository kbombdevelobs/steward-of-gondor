# DeepSeek Chatbot API

A language-focused chatbot using DeepSeek 1.3B model locally, wrapped in a Flask API for easy HTTP integration.

## Features

- 🤖 **Local DeepSeek 1.3B Model**: Run DeepSeek Coder 1.3B locally without external API calls
- 🌐 **Flask API**: RESTful API endpoints for easy integration
- ⚡ **Configurable Parameters**: Adjust temperature, top_p, and max_length for different response styles
- 📊 **Performance Metrics**: Response time tracking and model information
- 🛡️ **Error Handling**: Comprehensive error handling and validation
- 🔍 **Health Checks**: Monitor API and model status
- 🐳 **Docker Support**: Easy deployment with Docker and Docker Compose

## Prerequisites

- Python 3.8 or higher
- Docker and Docker Compose (for containerized deployment)
- At least 4GB RAM (8GB+ recommended)
- ~3GB disk space for the model

## Quick Start

### 1. Download the Model

```bash
# Install required packages
pip install transformers torch

# Download the DeepSeek 1.3B model
python utils/download_model_simple.py
```

### 2. Start the API

```bash
# Start with Docker (recommended)
./utils/docker-start.sh
```

This will:
- Build the Docker image with all dependencies
- Copy the local model into the container
- Start the API at `http://localhost:5001`

### 3. Test the API

```bash
# Run automated tests
python utils/test_client.py

# Or test manually
curl http://localhost:5001/health
```

## API Endpoints

### Health Check
**GET** `/health`

Check if the API is running and if the model is loaded.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "device": "cpu"
}
```

### Chat
**POST** `/chat`

Send a message to the chatbot and get a response.

**Request Body:**
```json
{
  "message": "Hello! How are you today?",
  "max_length": 512,
  "temperature": 0.7,
  "top_p": 0.9
}
```

**Parameters:**
- `message` (required): The input message
- `max_length` (optional): Maximum response length (default: 512)
- `temperature` (optional): Sampling temperature 0-2.0 (default: 0.7)
- `top_p` (optional): Top-p sampling 0-1.0 (default: 0.9)

**Response:**
```json
{
  "response": "Hello! I'm doing well, thank you for asking. How can I help you today?",
  "generation_time": 45.23,
  "model": "./models/deepseek-coder-1.3b-instruct",
  "parameters": {
    "max_length": 512,
    "temperature": 0.7,
    "top_p": 0.9
  }
}
```

## Example Usage

### Using curl

```bash
# Health check
curl http://localhost:5001/health

# Send a chat message
curl -X POST http://localhost:5001/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Write a Python function to calculate fibonacci numbers",
    "max_length": 256,
    "temperature": 0.5
  }'
```

### Using the Test Client

```bash
# Run automated tests
python utils/test_client.py

# Start interactive chat
python utils/test_client.py
# Then choose 'y' for interactive mode
```

## Model Information

- **Model**: `deepseek-ai/deepseek-coder-1.3b-instruct`
- **Size**: ~2.7GB
- **Parameters**: 1.3B
- **Use Case**: Coding assistance, general conversation
- **Performance**: Fast inference, good for basic coding tasks

## Configuration

### Environment Variables

Create a `.env` file to customize the application:

```env
# Server configuration
PORT=5000
FLASK_DEBUG=False
```

### Model Parameters

- **Temperature**: Controls randomness (0.0 = deterministic, 2.0 = very random)
- **Top-p**: Nucleus sampling parameter (0.0-1.0)
- **Max Length**: Maximum number of tokens in the response

## Performance Tips

1. **Use GPU**: Ensure CUDA is available for faster inference
2. **Memory**: The 1.3B model requires ~4GB RAM
3. **Response Length**: Reduce `max_length` for faster responses
4. **Temperature**: Lower values (0.1-0.5) for more focused responses

## Troubleshooting

### Common Issues

1. **Container Out of Memory**:
   - Increase Docker memory limit to 8GB
   - Check `docker-compose.yml` memory settings

2. **Model Not Found**:
   - Ensure model is downloaded: `python utils/download_model_simple.py`
   - Check `./models/deepseek-coder-1.3b-instruct/` exists

3. **Slow Response Times**:
   - Use GPU if available
   - Reduce `max_length` parameter
   - Check container logs: `docker-compose logs`

4. **API Not Responding**:
   - Check container status: `docker-compose ps`
   - View logs: `docker-compose logs --tail=20`
   - Restart: `docker-compose restart`

### Useful Commands

```bash
# View container logs
docker-compose logs -f

# Stop the API
docker-compose down

# Rebuild container
docker-compose build

# Check container status
docker-compose ps
```

## Development

### Utils Scripts

All utility scripts are organized in the `utils/` folder. See [utils/README.md](utils/README.md) for detailed documentation on:

- **Startup Scripts**: `docker-start.sh`, `start-local.sh`
- **Model Management**: `download_model_simple.py`
- **Testing Scripts**: `test_client.py`, `docker-test-client.py`

Quick reference:
```bash
# Download model
python utils/download_model_simple.py

# Start API
./utils/docker-start.sh

# Test API
python utils/test_client.py
```

### Project Structure

```
steward-of-gondor/
├── app.py                 # Main Flask application
├── utils/                 # Utility scripts
│   ├── README.md          # Scripts documentation
│   ├── download_model_simple.py  # Model downloader
│   ├── test_client.py     # Test client for local API
│   ├── docker-test-client.py  # Test client for Docker API
│   ├── start-local.sh     # Local startup script
│   └── docker-start.sh    # Docker startup script
├── models/                # Local model storage
│   └── deepseek-coder-1.3b-instruct/  # Model files
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose configuration
├── README.md             # This file
└── .env                  # Environment variables (optional)
```

### Local Development

```bash
# Install dependencies (full version with comments)
pip install -r requirements.txt

# Or install minimal dependencies only
pip install -r requirements-minimal.txt

# Run locally (requires model download first)
python app.py

# Test locally
python utils/test_client.py
```

## License

This project is open source and available under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs for error messages
3. Open an issue on GitHub 