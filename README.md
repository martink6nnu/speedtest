# Netspeed API

A FastAPI-based network speed testing service that provides internet speed measurements through a simple HTTP API.

## 🚀 Features

- **RESTful API**: Simple HTTP endpoints for speed testing
- **Real-time Speed Tests**: Uses `speedtest-cli` for accurate measurements
- **Structured Response**: Returns download/upload speeds in Mbps, ping, and server information
- **Docker Support**: Fully containerized for easy deployment
- **Async/Await**: Built with FastAPI for high performance
- **Clean Architecture**: Layered design with dependency injection
- **Comprehensive Testing**: Full test suite with pytest
- **Code Quality**: Linting and formatting with Ruff

## 📋 Requirements

- Python 3.12+
- Docker (optional, for containerized deployment)

## 🔧 Installation

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd speedtest
```

2. Run with Docker Compose:
```bash
docker-compose up -d
```

The API will be available at `http://localhost:8000`

### Local Development

1. Clone the repository:
```bash
git clone <repository-url>
cd speedtest
```

2. Install dependencies using uv (recommended):
```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync
```

3. Install speedtest-cli:
```bash
# On macOS
brew install speedtest-cli

# On Ubuntu/Debian
sudo apt-get install speedtest-cli
```

4. Run the application:
```bash
uv run fastapi dev src/main.py
```

## 📖 API Documentation

### Endpoints

#### `GET /`
Simple health check endpoint.

**Response:**
```json
"hiiii :3"
```

#### `GET /speed`
Performs a network speed test and returns the results.

**Response:**
```json
{
  "download_speed": 99.48,
  "upload_speed": 78.65,
  "ping": 18.482,
  "server_name": "Riga",
  "server_location": "Latvia"
}
```

**Response Fields:**
- `download_speed`: Download speed in Mbps
- `upload_speed`: Upload speed in Mbps  
- `ping`: Latency in milliseconds
- `server_name`: Name of the speed test server
- `server_location`: Country of the speed test server

**Error Response:**
```json
{
  "detail": "Failed to get speed test results: <error_message>"
}
```

### Interactive Documentation

Once the service is running, you can access the interactive API documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🏗️ Architecture

The project follows a clean layered architecture:

```
src/
├── main.py              # FastAPI application entry point
├── dependencies.py      # Dependency injection configuration
├── routers/            
│   ├── root.py         # Root endpoint
│   └── speed.py        # Speed test endpoints
├── services/
│   └── get_speed.py    # Business logic layer
├── repositories/
│   └── requester.py    # Data access layer (speedtest-cli integration)
└── models/
    └── speedresponse.py # Response data models
```

### Key Components

- **Routers**: Handle HTTP requests and responses
- **Services**: Contain business logic and data transformation
- **Repositories**: Manage external data sources (speedtest-cli)
- **Models**: Define data structures using Pydantic

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src

# Run specific test categories
uv run pytest -m unit
uv run pytest -m integration
```

Test structure:
- Unit tests for all layers
- Integration tests for API endpoints
- Mocked external dependencies
- Async test support with anyio

## 🔧 Development

### Code Quality

The project uses Ruff for linting and formatting:

```bash
# Check code style
uv run ruff check

# Format code
uv run ruff format

# Fix auto-fixable issues
uv run ruff check --fix
```

### Pre-commit Hooks

Install pre-commit hooks for automatic code quality checks:

```bash
uv run pre-commit install
```

## 🐳 Docker

### Development with Docker

```bash
# Build and run
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

