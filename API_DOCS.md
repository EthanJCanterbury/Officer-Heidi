
# Officer Heidi - AI Code Detection API Documentation

## Overview

Officer Heidi is an AI code detection service that analyzes GitHub repositories to identify potentially AI-generated code. It provides both a Slack bot interface and a REST API webhook for external integrations.

## Base URL

```
https://c404sso4wc08o4wwgks4k0s8.a.selfhosted.hackclub.com/
```

## Authentication

No authentication is required for the webhook endpoints. The service is designed to be publicly accessible for integration purposes.

## API Endpoints

### 1. Service Status

**GET** `/`

Returns the service status and basic information.

**Response:**
```json
{
  "message": "Officer Heidi AI Code Detection Service",
  "status": "online",
  "info_endpoint": "/webhook/info"
}
```

### 2. Health Check

**GET** `/webhook/health`

Health check endpoint to verify service availability.

**Response:**
```json
{
  "status": "healthy",
  "service": "Officer Heidi Analysis Service",
  "timestamp": "2025-06-24T17:04:16.123456"
}
```

### 3. Service Information

**GET** `/webhook/info`

Returns detailed information about the service and available endpoints.

**Response:**
```json
{
  "service": "Officer Heidi - AI Code Detection Service",
  "version": "1.0.0",
  "description": "Webhook service for analyzing GitHub repositories for AI-generated code",
  "endpoints": {
    "analyze": {
      "method": "POST",
      "url": "/webhook/analyze",
      "description": "Analyze a GitHub repository for AI-generated code",
      "payload": {
        "repo_url": "https://github.com/username/repository"
      }
    },
    "health": {
      "method": "GET",
      "url": "/webhook/health",
      "description": "Health check endpoint"
    },
    "info": {
      "method": "GET",
      "url": "/webhook/info",
      "description": "Service information"
    }
  }
}
```

### 4. Analyze Repository

**POST** `/webhook/analyze`

Analyzes a GitHub repository for AI-generated code patterns.

**Request Body:**
```json
{
  "repo_url": "https://github.com/username/repository"
}
```

**Request Headers:**
```
Content-Type: application/json
```

**Response (Success - 200):**
```json
{
  "status": "success",
  "repository_url": "https://github.com/username/repository",
  "analysis_timestamp": "2025-06-24T17:04:16.123456",
  "owner_info": {
    "username": "username",
    "created_at": "2023-01-15T10:30:00Z",
    "account_age_days": 525,
    "public_repos": 42,
    "followers": 15
  },
  "code_analysis": {
    "files_analyzed": 25,
    "total_code_lines": 1250,
    "total_comment_lines": 312,
    "comment_to_code_ratio": 24.96,
    "languages_detected": {
      "Python": 15,
      "JavaScript/TypeScript": 8,
      "HTML": 2
    }
  },
  "ai_detection": {
    "average_ai_score": 45.2,
    "ai_likelihood": "Maybe AI",
    "commit_pattern_score": 15,
    "code_duplication_score": 8
  },
  "commits": [
    {
      "hash": "abc12345",
      "message": "Initial commit with basic functionality",
      "author": "John Doe",
      "date": "2025-06-20 14:30:22",
      "files_changed": 5
    }
  ],
  "suspicious_files": [
    {
      "file_path": "src/helper.py",
      "ai_score": 75,
      "code_lines": 120,
      "comment_lines": 45
    }
  ]
}
```

**Response (Error - 400):**
```json
{
  "error": "Invalid GitHub repository URL",
  "status": "error"
}
```

**Response (Error - 500):**
```json
{
  "error": "Analysis failed: Repository not found",
  "error_details": "Full error traceback...",
  "status": "error"
}
```

## AI Likelihood Ratings

The service provides four levels of AI likelihood:

- **"Not AI"** (Score: 0-9) - Very low probability of AI generation
- **"Maybe AI"** (Score: 10-29) - Some indicators present but inconclusive
- **"Probly AI"** (Score: 30-59) - Multiple AI indicators detected
- **"Definitly AI"** (Score: 60+) - High confidence of AI generation

## Detection Methodology

Officer Heidi analyzes repositories using multiple detection methods:

### 1. Pattern Recognition
- Direct AI attribution comments
- Emoji usage in code
- Overly explanatory comments
- Perfect step-by-step comments
- AI-typical function names

### 2. Code Structure Analysis
- Comment-to-code ratios
- Perfect formatting patterns
- Overly structured code
- Excessive error handling

### 3. Metadata Analysis
- Suspicious filenames
- File size patterns
- Commit message patterns
- Account age verification

### 4. Temporal Analysis
- Commit frequency patterns
- Repository creation timing
- Code duplication across files

## Example Usage

### cURL Example

```bash
curl -X POST https://your-repl-name.username.repl.co/webhook/analyze \
  -H "Content-Type: application/json" \
  -d '{"repo_url": "https://github.com/username/repository"}'
```

### Python Example

```python
import requests
import json

url = "https://your-repl-name.username.repl.co/webhook/analyze"
payload = {"repo_url": "https://github.com/username/repository"}
headers = {"Content-Type": "application/json"}

response = requests.post(url, json=payload, headers=headers)
result = response.json()

if response.status_code == 200:
    print(f"AI Likelihood: {result['ai_detection']['ai_likelihood']}")
    print(f"Average Score: {result['ai_detection']['average_ai_score']}")
else:
    print(f"Error: {result['error']}")
```

### JavaScript Example

```javascript
const analyzeRepository = async (repoUrl) => {
  const response = await fetch('https://your-repl-name.username.repl.co/webhook/analyze', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      repo_url: repoUrl
    })
  });

  const result = await response.json();
  
  if (response.ok) {
    console.log(`AI Likelihood: ${result.ai_detection.ai_likelihood}`);
    console.log(`Average Score: ${result.ai_detection.average_ai_score}`);
  } else {
    console.error(`Error: ${result.error}`);
  }
};

analyzeRepository('https://github.com/username/repository');
```

## Error Handling

The API returns appropriate HTTP status codes:

- **200** - Success
- **400** - Bad Request (invalid JSON, missing repo_url, invalid GitHub URL)
- **404** - Endpoint not found
- **500** - Internal Server Error (analysis failure, repository access issues)

All error responses include an `error` field with a descriptive message and a `status` field set to "error".

## Rate Limiting

Currently, there are no rate limits implemented. However, analysis requests may take 30-60 seconds to complete depending on repository size.

## Integration Use Cases

- **Hiring Verification**: Verify authenticity of candidate code submissions
- **Academic Integrity**: Monitor student code submissions for AI generation
- **Code Review**: Assist in identifying potentially AI-generated code during review
- **Contest Verification**: Ensure competition submissions are authentic
- **CI/CD Integration**: Integrate into build pipelines for automated AI detection

## Deployment

This service is designed to run on Replit with automatic scaling and 24/7 availability when deployed using Reserved VM Deployments.

## Support

For issues or questions, please refer to the repository documentation or contact the development team.
