---
applyTo: '**'
---

# MCP Project Architecture Guidelines

This document provides project context and coding guidelines that AI should follow when generating code, answering questions, or reviewing changes for this Model Context Protocol (MCP) server.

## Project Structure

This project follows a clear architectural pattern. **Always** place new files in their corresponding directories:

### **CRITICAL RULE: One File Per Feature**
- **Each tool MUST be in its own separate file**
- **Each resource MUST be in its own separate file**
- **Each service MUST be in its own separate file**
- **Each gateway client MUST be in its own separate file**
- **Never combine multiple tools, resources, services, or clients in a single file**

### 1. **Tools Directory** (`tools/`)
- **Purpose**: Contains MCP tool implementations
- **When to use**: When creating any MCP tool functionality
- **Structure**: Each tool in its own file named after the tool function
- **Naming Convention**: `{tool_name}.py` (e.g., `update_drive_file.py`, `test_server.py`)
- **Example**: User request like "create a tool to fetch weather data" → create `tools/fetch_weather.py`

### 2. **Resources Directory** (`resources/`)
- **Purpose**: Contains MCP resource definitions and handlers
- **When to use**: When creating MCP resources that expose data or state
- **Structure**: Each resource in its own file named after the resource function
- **Naming Convention**: `{resource_name}.py` (e.g., `get_drive_file.py`, `get_user_profile.py`)
- **Example**: User request like "create a resource for user profiles" → create `resources/get_user_profile.py`

### 3. **Prompts Directory** (`prompts/`)
- **Purpose**: Contains MCP prompt templates and prompt-related functionality
- **When to use**: When creating prompt templates or prompt handlers
- **Structure**: Each prompt in its own file
- **Naming Convention**: `{prompt_name}.py`
- **Example**: User request like "create a prompt for code review" → create `prompts/code_review_prompt.py`

### 4. **Services Directory** (`services/`)
- **Purpose**: Contains business logic and service layer implementations
- **When to use**: When creating service classes, business logic, or application-specific functionality
- **Structure**: Each service in its own file
- **Naming Convention**: `{domain}_service.py` (e.g., `drive_service.py`, `payment_service.py`)
- **Example**: User request like "create a service to process payments" → create `services/payment_service.py`

### 5. **Gateway Directory** (`gateway/`)
- **Purpose**: Contains integrations with external services and cloud providers
- **When to use**: When creating integrations with AWS services or other external APIs
- **Supported integrations**:
  - AWS services (S3, DynamoDB, SSM, etc.)
  - External APIs and third-party services
- **Structure**: Each gateway client in its own file
- **Naming Convention**: `{service}_client.py` (e.g., `s3_client.py`, `dynamodb_client.py`)
- **Example**: 
  - "create an S3 client" → create `gateway/s3_client.py`
  - "integrate with DynamoDB" → create `gateway/dynamodb_client.py`
  - "create SSM parameter handler" → create `gateway/ssm_client.py`

## Architectural Principles

1. **Separation of Concerns**: Each directory has a specific responsibility
2. **Consistency**: Always place files in the correct directory based on their purpose
3. **Modularity**: Keep modules focused and single-purpose
4. **Clear Boundaries**: 
   - Tools = MCP tool interface
   - Resources = MCP resource interface
   - Prompts = MCP prompt interface
   - Services = Business logic
   - Gateway = External integrations

## File Naming Conventions

- **Tools**: `{tool_function_name}.py` (e.g., `update_drive_file.py`, `fetch_weather.py`)
- **Resources**: `{resource_function_name}.py` (e.g., `get_drive_file.py`, `get_user_profile.py`)
- **Services**: `{domain}_service.py` (e.g., `drive_service.py`, `payment_service.py`)
- **Gateway**: `{service}_client.py` (e.g., `google_drive_client.py`, `s3_client.py`, `dynamodb_client.py`)
- **Prompts**: `{prompt_name}_prompt.py` (e.g., `code_review_prompt.py`)
- All files use snake_case
- File names should be descriptive and indicate the file's single purpose

## Critical Rules for File Organization

### One File Per Functionality
- ❌ **NEVER** create multiple tools in a single file
- ❌ **NEVER** create multiple resources in a single file
- ❌ **NEVER** create multiple services in a single file
- ❌ **NEVER** create multiple gateway clients in a single file
- ✅ **ALWAYS** create a separate file for each functionality
- ✅ The file name must match the main function name

### Function Naming Conventions
- **Resources**: `get_{resource_name}` (e.g., `get_drive_file`)
- **Tools**: `{action}_{object}` (e.g., `update_drive_file`, `test_server`)
- **Services**: Descriptive method names (e.g., `get_file_content`)

## Creating New Features

When a user requests a new MCP feature, follow this decision tree:

1. **Is it a tool?** → Create in `tools/`
2. **Is it a resource?** → Create in `resources/`
3. **Is it a prompt?** → Create in `prompts/`
4. **Is it business logic or a service?** → Create in `services/`
5. **Is it an AWS or external service integration?** → Create in `gateway/`

## Examples

### ✅ Correct
```
User: "Create a tool to query DynamoDB"
Action: 
  1. Create tool in tools/query_dynamodb.py (one file, one tool)
  2. Create DynamoDB client in gateway/dynamodb_client.py (if doesn't exist)

User: "Create tools to upload and download from S3"
Action:
  1. Create tools/upload_to_s3.py (one file for upload tool)
  2. Create tools/download_from_s3.py (one file for download tool)
  3. Create gateway/s3_client.py (if doesn't exist)
```

### ❌ Incorrect
```
User: "Create tools to upload and download from S3"
Action: Create tools/s3_tools.py with both upload and download functions
Reason: Multiple tools in one file violates the architecture

User: "Create a tool to query DynamoDB"
Action: Create everything in main.py or root directory
Reason: Wrong directory and violates separation of concerns
```

## Additional Guidelines

- Import gateway clients in services when needed
- Import services in tools/resources/prompts when needed
- Keep dependencies flowing in one direction: Tools/Resources/Prompts → Services → Gateway
- Never create MCP-related files outside their designated directories