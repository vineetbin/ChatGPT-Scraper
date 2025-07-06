# Brand Mentions Analysis System

A full-stack system that analyzes brand mentions from ChatGPT responses and provides a clean API for retrieving brand mention metrics. This project demonstrates web scraping, data processing, and API development using modern Python technologies.

## 🎯 Project Overview

This project consists of two main stages:

### Stage 1: Web Scraping
- Actually scrapes ChatGPT website with 10 different sportswear-related prompts
- Uses undetected-chromedriver to interact with ChatGPT's web interface
- Extracts and counts brand mentions (Nike, Adidas, Hoka, New Balance, Jordan)
- Stores results in PostgreSQL database

### Stage 2: Mentions API
- Lightweight FastAPI server exposing brand mention metrics
- Clean RESTful endpoints for querying mention data
- Auto-port detection for seamless deployment

## 🚀 Quick Start

### Prerequisites
- Python 3.9+ (recommended: 3.11)
- PostgreSQL
- Git

## ⚠️ PostgreSQL Setup Notes

- **PostgreSQL Service:**
  - Make sure PostgreSQL is running before initializing the database or running the app.
  - On macOS with Homebrew, start it with:
    ```bash
    brew services start postgresql@14
    ```
  - To check status:
    ```bash
    brew services list
    ```

- **Database User:**
  - The system automatically detects the correct database user for your system.
  - On macOS/Homebrew: Uses your system username
  - On Linux/Windows: Uses `postgres` user
  - You can override this by setting the `DB_USER` environment variable.

- **Troubleshooting:**
  - **Connection refused:** PostgreSQL is not running. Start it as shown above.
  - **Password authentication failed:** Make sure you use the correct password for your database user.

### Setup Instructions

**Option 1: Automated Setup (Recommended)**
```bash
# Run the setup script - it will handle everything automatically
./setup.sh
```

**Option 2: Manual Setup**
```bash
# 1. Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt
```

### What the Setup Script Does

The `setup.sh` script performs the following steps automatically:

1. **✅ Python Version Check** - Verifies Python 3.9+ is installed
2. **📦 Virtual Environment** - Creates and activates a new virtual environment
3. **⬆️ Pip Upgrade** - Upgrades pip to the latest version
4. **📚 Dependencies** - Installs all required packages from `requirements.txt`
5. **🔧 Permissions** - Makes all scripts executable
6. **📋 Instructions** - Shows next steps to run the project

### Next Steps After Setup

After running either setup option, follow these steps:

1. **Initialize the database**
   ```bash
   python scripts/database_setup.py --db-password your_password
   ```

  2. **Run Stage 1 (scraping)**
     ```bash
     python scraper.py --db-password your_password
     ```

  3. **Run Stage 2 (API)**
     ```bash
     python api_server.py --db-password your_password
     ```

## 📋 Running the Project

### Stage 1: Web Scraping
```bash
# Basic usage
python scraper.py --db-password your_password

# Custom delay between requests
python scraper.py --db-password your_password --delay 5
```

This will:
- Open browser and navigate to ChatGPT
- Send 10 sportswear-related prompts to ChatGPT
- Extract real responses from ChatGPT interface
- Count brand mentions in responses
- Store results in the database

### Stage 2: API Server
```bash
python api_server.py --db-password your_password
```

The API will be available at `http://localhost:8000`

## 🔌 API Endpoints

### GET /mentions
Returns total mentions for all brands:
```json
{
  "nike": 15,
  "adidas": 12,
  "hoka": 8,
  "new balance": 6,
  "jordan": 4
}
```

### GET /mentions/{brand}
Returns mentions for a specific brand:
```json
{
  "brand": "nike",
  "mentions": 15
}
```

## 📊 Sample Output

### Stage 1 Output
```
Processing prompt 1/10: "What are the best running shoes in 2025?"
Brand mentions found:
- Nike: 3
- Adidas: 2
- Hoka: 1
- New Balance: 1
- Jordan: 0

Processing prompt 2/10: "Top performance sneakers for athletes"
...
```

### Stage 2 API Response
```bash
curl http://localhost:8000/mentions
```

## 🛠️ Project Structure

```
Bear/
├── README.md
├── requirements.txt
├── config.py
├── scraper.py              # Main entry point for scraper
├── api_server.py
├── setup.sh
├── scraper/                # Scraper package
│   ├── __init__.py         # Package initialization
│   ├── main.py             # Main scraper entry point
│   ├── chatgpt_scraper.py  # ChatGPTScraper class
│   ├── browser_manager.py  # Browser setup & navigation
│   ├── response_handler.py # Response handling & extraction
│   ├── prompt_sender.py    # Prompt sending logic
│   ├── retry_handler.py    # Retry logic with popup handling
│   ├── data_processor.py   # Data processing & database operations
│   ├── brand_analyzer.py   # Brand mention extraction
│   └── utils.py            # Utility functions & configuration
├── scripts/
│   └── database_setup.py
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── database.py
│   └── api.py
└── data/
    └── sample_prompts.json
```

## 🔧 Configuration

All configuration is in `config.py` with sensible defaults. 

The database password must be provided as a command line argument for security.

## 🧪 Testing

Run the test suite:
```bash
python -m pytest tests/
```

## 🚀 Deployment Suggestions

### Scaling Improvements
1. **Caching**: Implement Redis for API response caching
2. **Rate Limiting**: Add rate limiting to prevent API abuse
3. **Authentication**: Implement JWT-based authentication
4. **Monitoring**: Add logging and metrics collection
5. **Containerization**: Dockerize the application
6. **CI/CD**: Set up automated testing and deployment

### Performance Optimizations
1. **Database Indexing**: Add indexes on frequently queried columns
2. **Connection Pooling**: Implement database connection pooling
3. **Async Processing**: Use background tasks for data processing
4. **CDN**: Serve static content through a CDN

## 🚀 Suggestions for Improvements & Scaling

### 🔄 **Scraping Enhancements**

#### **Multi-Platform Support**
- **Bard/Gemini Integration**: Extend scraping to Google's AI platforms
- **Claude Integration**: Add Anthropic's Claude for comparison
- **Multi-AI Comparison**: Compare brand mentions across different AI models
- **API-Based Scraping**: Use official APIs where available (OpenAI API, etc.)

#### **Advanced Scraping Features**
- **Dynamic Prompt Generation**: Use AI to generate contextually relevant prompts
- **Sentiment Analysis**: Analyze sentiment of brand mentions (positive/negative/neutral)
- **Context Extraction**: Extract surrounding context of brand mentions
- **Image Analysis**: Analyze brand logos and visual mentions in AI responses
- **Real-time Monitoring**: Set up continuous monitoring with alerts

#### **Scalability Improvements**
- **Distributed Scraping**: Use multiple browser instances for parallel processing
- **Queue System**: Implement Redis/Celery for job queuing and distribution
- **Proxy Rotation**: Rotate IP addresses to avoid rate limiting
- **Session Management**: Implement intelligent session handling and reuse
- **Headless Browser Support**: Add headless mode for server deployment and automation
  - **Server Deployment**: Enable running on servers without display
  - **Automation**: Schedule scraping jobs without user interaction
  - **Resource Efficiency**: Reduce memory and CPU usage
  - **Docker Support**: Containerized deployment capabilities
- **Headless Clustering**: Run multiple headless browsers across different machines

#### **Data Visualization**
- **Interactive Dashboards**: Real-time dashboards with Grafana/PowerBI
- **Time Series Charts**: Visualize mention trends over time
- **Heat Maps**: Geographic and temporal heat maps
- **Network Graphs**: Show relationships between brands and topics
- **Export Capabilities**: PDF reports, Excel exports, API integrations

### 🏗️ **Architecture & Infrastructure**

#### **Microservices Architecture**
- **Scraper Service**: Dedicated service for web scraping
- **API Gateway**: Centralized API management with Kong/Apache
- **Data Processing Service**: Separate service for data analysis
- **Notification Service**: Real-time alerts and notifications
- **Storage Service**: Dedicated data storage and retrieval service

#### **Cloud Deployment**
- **AWS/GCP/Azure**: Deploy on cloud platforms with auto-scaling
- **Kubernetes**: Container orchestration for high availability
- **Serverless**: Use AWS Lambda for event-driven processing
- **CDN Integration**: Global content delivery for better performance
- **Load Balancing**: Distribute traffic across multiple instances

#### **Database Optimization**
- **Read Replicas**: Separate read/write databases for better performance
- **Sharding**: Distribute data across multiple database instances
- **Caching Layers**: Redis for session and data caching
- **Data Warehousing**: Use BigQuery/Snowflake for analytics
- **Backup & Recovery**: Automated backup and disaster recovery

### 🔐 **Security & Compliance**

#### **Enhanced Security**
- **API Authentication**: OAuth2, API keys, or JWT tokens
- **Rate Limiting**: Prevent abuse with intelligent rate limiting
- **Data Encryption**: Encrypt data at rest and in transit
- **Audit Logging**: Comprehensive audit trails for compliance
- **Vulnerability Scanning**: Regular security assessments

#### **Compliance Features**
- **GDPR Compliance**: Data privacy and right to be forgotten
- **SOC 2 Compliance**: Security and availability controls
- **Data Retention Policies**: Automated data lifecycle management
- **Access Controls**: Role-based access control (RBAC)
- **Data Masking**: Sensitive data protection

### 🧪 **Testing & Quality Assurance**

#### **Comprehensive Testing**
- **Unit Tests**: 90%+ code coverage for all modules
- **Integration Tests**: End-to-end testing of all workflows
- **Performance Tests**: Load testing and stress testing
- **Security Tests**: Penetration testing and vulnerability assessment
- **UI/UX Testing**: User experience testing and optimization

#### **Monitoring & Observability**
- **Application Monitoring**: APM tools like New Relic, Datadog
- **Log Aggregation**: Centralized logging with ELK stack
- **Metrics Collection**: Custom metrics and KPIs
- **Health Checks**: Automated health monitoring and alerting
- **Performance Profiling**: Identify and fix performance bottlenecks

### 🚀 **Performance & Optimization**

#### **High-Performance Features**
- **Async Processing**: Non-blocking operations for better responsiveness
- **Database Optimization**: Query optimization and indexing strategies
- **Memory Management**: Efficient memory usage and garbage collection
- **Caching Strategies**: Multi-level caching for optimal performance
- **CDN Integration**: Global content delivery for faster access

#### **Scalability Features**
- **Horizontal Scaling**: Add more instances as demand grows
- **Vertical Scaling**: Optimize resource usage per instance
- **Auto-scaling**: Automatic scaling based on demand
- **Load Distribution**: Intelligent load balancing across instances
- **Resource Optimization**: Efficient use of CPU, memory, and storage
