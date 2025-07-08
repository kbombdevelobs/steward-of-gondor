# Utils Scripts

This directory contains utility scripts for managing and testing the DeepSeek Chatbot API.

## Scripts Overview

### 🚀 Startup Scripts

#### `docker-start.sh`
**Purpose**: Complete Docker setup and startup script  
**Usage**: 
```bash
./utils/docker-start.sh
```

**What it does**:
- Checks if Docker and Docker Compose are installed
- Creates logs directory
- Builds the Docker image
- Starts the container
- Shows useful commands and logs
- Makes the API available at `http://localhost:5001`

**Features**:
- Automatic error checking
- Helpful command suggestions
- Log display after startup

---

#### `start-local.sh`
**Purpose**: Local model startup script  
**Usage**: 
```bash
./utils/start-local.sh
```

**What it does**:
- Checks if local models exist in `./models/` directory
- Lists available local models
- Starts the Docker container with local models
- Provides instructions for using local models

**Prerequisites**:
- Local model files must be in `./models/deepseek-coder-1.3b-instruct/`

---

### 📥 Model Management

#### `download_model_simple.py`
**Purpose**: Download the DeepSeek 1.3B model to local storage  
**Usage**: 
```bash
python utils/download_model_simple.py
```

**What it does**:
- Downloads `deepseek-ai/deepseek-coder-1.3b-instruct` model
- Saves to `./models/deepseek-coder-1.3b-instruct/`
- Downloads both tokenizer and model weights (~2.7GB)
- Verifies all files are downloaded correctly

**Prerequisites**:
```bash
pip install transformers torch
```

**Output**:
- Creates `./models/deepseek-coder-1.3b-instruct/` directory
- Downloads: `model.safetensors`, `tokenizer.json`, `config.json`, etc.

---

### 🧪 Testing Scripts

#### `test_client.py`
**Purpose**: Test client for local API testing  
**Usage**: 
```bash
python utils/test_client.py
```

**What it does**:
- Tests `/health` endpoint
- Runs automated tests with sample messages
- Optionally starts interactive chat session
- Connects to `http://localhost:5001`

**Features**:
- Health check verification
- Automated test suite
- Interactive chat mode
- Response time tracking
- Error handling

**Test Messages**:
- General conversation
- Programming questions
- Technical explanations
- Web development topics

---

#### `docker-test-client.py`
**Purpose**: Test client specifically for Docker API  
**Usage**: 
```bash
python utils/docker-test-client.py
```

**What it does**:
- Same functionality as `test_client.py`
- Optimized for Docker container testing
- Longer timeouts for model loading
- Better error handling for container environment

**Features**:
- Extended timeouts (60s for chat, 120s for model loading)
- Docker-specific error messages
- Container health monitoring

---

## Quick Start Guide

### 1. First Time Setup

```bash
# Download the model
python utils/download_model_simple.py

# Start the API
./utils/docker-start.sh

# Test the API
python utils/test_client.py
```

### 2. Regular Usage

```bash
# Start the API
./utils/docker-start.sh

# Test with interactive chat
python utils/test_client.py
# Then choose 'y' for interactive mode
```

### 3. Development Workflow

```bash
# Make changes to app.py
# Rebuild and restart
docker-compose down
docker-compose build
docker-compose up -d

# Test changes
python utils/test_client.py
```

---

## API Endpoints

### Health Check
```bash
curl http://localhost:5001/health
```

**Response**:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "device": "cpu"
}
```

### Chat
```bash
curl -X POST http://localhost:5001/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello! How are you?",
    "max_length": 100,
    "temperature": 0.7,
    "top_p": 0.9
  }'
```

**Response**:
```json
{
  "response": "Hello! I'm doing well, thank you for asking...",
  "generation_time": 45.23,
  "model": "./models/deepseek-coder-1.3b-instruct",
  "parameters": {
    "max_length": 100,
    "temperature": 0.7,
    "top_p": 0.9
  }
}
```

---

## Troubleshooting

### Common Issues

1. **Model Download Fails**
   ```bash
   # Check internet connection
   # Ensure sufficient disk space (>3GB)
   # Try again
   python utils/download_model_simple.py
   ```

2. **Container Out of Memory**
   ```bash
   # Check Docker memory settings
   # Increase memory limit in docker-compose.yml
   # Restart container
   docker-compose down
   docker-compose up -d
   ```

3. **API Not Responding**
   ```bash
   # Check container status
   docker-compose ps
   
   # Check logs
   docker-compose logs --tail=20
   
   # Restart if needed
   docker-compose restart
   ```

4. **Test Client Connection Issues**
   ```bash
   # Verify API is running
   curl http://localhost:5001/health
   
   # Check port configuration
   # Ensure test_client.py uses port 5001
   ```

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

# Access container shell
docker-compose exec deepseek-chatbot bash
```

---

## File Structure

```
utils/
├── README.md                    # This file
├── download_model_simple.py     # Model downloader
├── test_client.py              # Local test client
├── docker-test-client.py       # Docker test client
├── start-local.sh              # Local startup script
└── docker-start.sh             # Docker startup script
```

---

## Notes

- All scripts assume the API runs on port 5001
- The model is baked into the Docker image for faster startup
- Test clients include timeouts for model loading delays
- Interactive chat mode is available in both test clients
- Scripts include error handling and helpful error messages 