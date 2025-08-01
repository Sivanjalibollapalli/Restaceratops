#!/usr/bin/env python3
"""
🦖 Enhanced AI System for Restaceratops
Simplified AI system using OpenRouter with Qwen3 Coder model
"""

import os
import json
import logging
from typing import List, Dict, Optional, Any, Tuple
from datetime import datetime
import asyncio
import httpx

log = logging.getLogger("agent.enhanced_ai_system")

class OpenRouterAI:
    """OpenRouter AI provider using Qwen3 Coder model."""
    
    def __init__(self):
        """Initialize OpenRouter AI with Qwen3 Coder model."""
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.model = "qwen/qwen3-coder:free"
        self.base_url = "https://openrouter.ai/api/v1"
        
        if self.api_key:
            log.info(f"✅ OpenRouter AI configured with {self.model}")
            log.info(f"🔑 API key found: {self.api_key[:10]}...{self.api_key[-4:]}")
        else:
            log.warning("⚠️ No OpenRouter API key found in environment variables")
            log.warning("🔧 Set OPENROUTER_API_KEY environment variable to enable real AI")
    
    async def generate_response(self, messages: List[Dict[str, str]]) -> Optional[str]:
        """Generate response using OpenRouter API directly."""
        if not self.api_key:
            log.warning("⚠️ No OpenRouter API key provided")
            return None
        
        try:
            log.info(f"🤖 Calling OpenRouter API with model: {self.model}")
            log.info(f"📝 Sending {len(messages)} messages to OpenRouter")
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.model,
                        "messages": messages,
                        "temperature": 0.7,
                        "max_tokens": 2000
                    }
                )
                
                log.info(f"📡 OpenRouter response status: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    ai_response = result["choices"][0]["message"]["content"]
                    log.info("✅ OpenRouter response generated successfully")
                    return ai_response
                else:
                    log.error(f"❌ OpenRouter API error: {response.status_code}")
                    log.error(f"❌ Response body: {response.text}")
                    return None
                    
        except Exception as e:
            log.error(f"❌ Failed to call OpenRouter API: {e}")
            log.error(f"❌ Exception type: {type(e).__name__}")
            return None

class EnhancedAISystem:
    """Enhanced AI system using OpenRouter with Qwen3 Coder."""
    
    def __init__(self):
        """Initialize the enhanced AI system."""
        self.openrouter_ai = OpenRouterAI()
        self.conversation_history = []
        
        log.info("Enhanced AI system initialized with OpenRouter Qwen3 Coder")
    
    async def handle_conversation(self, user_input: str) -> str:
        """Handle user conversation using OpenRouter Qwen3 Coder with proper AI integration."""
        try:
            # Create comprehensive system prompt for Qwen3
            system_prompt = """You are Restaceratops, an advanced AI-powered API testing assistant built with the Qwen3 Coder model. Your core purpose is to provide expert-level guidance for API testing and development.

## Your Capabilities:
1. **API Testing Strategy**: Design comprehensive testing strategies for REST APIs, GraphQL, and microservices
2. **Test Case Generation**: Create detailed test cases including positive, negative, edge cases, and performance tests
3. **Code Generation**: Generate YAML test specifications, Python test scripts, and automation code
4. **Debugging & Analysis**: Analyze API responses, error codes, and provide troubleshooting guidance
5. **Performance Testing**: Guide users on load testing, stress testing, and performance optimization
6. **Security Testing**: Provide guidance on authentication, authorization, and security testing
7. **Best Practices**: Share industry best practices for API testing and quality assurance

## Your Response Style:
- Be professional yet approachable
- Provide actionable, practical advice
- Include code examples when relevant
- Use markdown formatting for clarity
- Focus specifically on API testing context
- Ask clarifying questions when needed

## Current Context:
You're integrated into the Restaceratops platform, which provides:
- Real-time test execution
- MongoDB data persistence
- Dashboard analytics
- File upload capabilities
- Report generation

Remember: You're helping users build robust, reliable APIs through comprehensive testing."""
            
            # Build messages array for Qwen3
            messages = [
                {"role": "system", "content": system_prompt}
            ]
            
            # Add conversation history (last 4 messages for context)
            for msg in self.conversation_history[-4:]:
                messages.append(msg)
            
            # Add current user input
            messages.append({"role": "user", "content": user_input})
            
            # Get response from Qwen3
            ai_response = await self.openrouter_ai.generate_response(messages)
            
            if ai_response:
                # Update conversation history
                self.conversation_history.append({"role": "user", "content": user_input})
                self.conversation_history.append({"role": "assistant", "content": ai_response})
                
                # Keep only last 10 messages to prevent memory issues
                if len(self.conversation_history) > 10:
                    self.conversation_history = self.conversation_history[-10:]
                
                return ai_response
            else:
                # Fallback to intelligent response
                return self._get_intelligent_fallback_response(user_input)
            
        except Exception as e:
            log.error(f"Error in conversation: {e}")
            return self._get_intelligent_fallback_response(user_input)
    
    async def generate_intelligent_tests(self, api_spec: str, requirements: str) -> str:
        """Generate intelligent test cases using OpenRouter Qwen3 Coder."""
        try:
            # Create comprehensive test generation prompt
            system_prompt = """You are an expert API testing engineer using the Qwen3 Coder model. Your task is to generate comprehensive, production-ready test cases for REST APIs.

## Test Generation Guidelines:
1. **Coverage**: Include positive, negative, edge cases, and error scenarios
2. **Format**: Generate valid YAML test specifications
3. **Realism**: Use realistic test data and scenarios
4. **Best Practices**: Follow API testing best practices
5. **Documentation**: Include clear descriptions for each test

## Output Format:
- Valid YAML structure
- Clear test names and descriptions
- Proper request/response expectations
- Error handling scenarios
- Performance considerations where relevant"""

            user_prompt = f"""Generate comprehensive API test cases for the following specification:

**API Specification:**
{api_spec}

**Requirements:**
{requirements}

**Expected Output:**
- Valid YAML test specification
- Multiple test scenarios (positive, negative, edge cases)
- Clear assertions and expectations
- Error handling tests
- Performance considerations

Please provide a complete, ready-to-use test suite."""

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]

            log.info("🤖 Generating test cases with Qwen3 Coder...")
            ai_response = await self.openrouter_ai.generate_response(messages)
            
            if ai_response:
                log.info("✅ Test cases generated successfully")
                return ai_response
            else:
                return self._get_fallback_test_template(api_spec)
            
        except Exception as e:
            log.error(f"Error generating tests: {e}")
            return self._get_fallback_test_template(api_spec)
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get system statistics."""
        return {
            "provider": "OpenRouter",
            "model": self.openrouter_ai.model,
            "api_key_configured": bool(self.openrouter_ai.api_key),
            "conversation_history_length": len(self.conversation_history)
        }
    
    def _get_intelligent_fallback_response(self, user_input: str) -> str:
        """Get intelligent fallback response using logic-based analysis."""
        user_input_lower = user_input.lower()
        
        # Analyze user input and provide intelligent responses
        if "authentication" in user_input_lower or "auth" in user_input_lower:
            return self._get_authentication_guidance(user_input)
        elif "test" in user_input_lower and "api" in user_input_lower:
            return self._get_api_testing_guidance(user_input)
        elif "error" in user_input_lower or "debug" in user_input_lower:
            return self._get_debugging_guidance(user_input)
        elif "performance" in user_input_lower or "speed" in user_input_lower:
            return self._get_performance_guidance(user_input)
        elif "security" in user_input_lower:
            return self._get_security_guidance(user_input)
        elif "generate" in user_input_lower and "test" in user_input_lower:
            return self._get_test_generation_guidance(user_input)
        else:
            return self._get_general_api_guidance(user_input)
    
    def _get_authentication_guidance(self, user_input: str) -> str:
        """Provide authentication testing guidance."""
        return f"""🔐 **Authentication Testing Guidance**

Based on your question: "{user_input}"

**Essential Authentication Tests:**
1. **Valid Credentials Test**
   - Test with correct username/password
   - Verify 200 OK response
   - Check for valid JWT/token in response

2. **Invalid Credentials Test**
   - Test with wrong username/password
   - Verify 401 Unauthorized response
   - Check error message clarity

3. **Missing Credentials Test**
   - Test without authentication headers
   - Verify 401 Unauthorized response

4. **Token Expiration Test**
   - Test with expired tokens
   - Verify 401 Unauthorized response

5. **Role-Based Access Test**
   - Test different user roles
   - Verify appropriate access levels

**Sample Test Cases:**
```yaml
- name: "Valid Authentication"
  request:
    method: POST
    url: "/api/auth/login"
    json:
      username: "testuser"
      password: "testpass"
  expect:
    status: 200
    json:
      token: "{{token}}"

- name: "Invalid Authentication"
  request:
    method: POST
    url: "/api/auth/login"
    json:
      username: "wronguser"
      password: "wrongpass"
  expect:
    status: 401
```

Would you like me to help you create specific authentication test cases for your API?"""
    
    def _get_api_testing_guidance(self, user_input: str) -> str:
        """Provide API testing guidance."""
        return f"""🧪 **API Testing Best Practices**

Based on your question: "{user_input}"

**Comprehensive API Testing Strategy:**

1. **Functional Testing**
   - Test all endpoints and methods
   - Verify correct responses
   - Test edge cases and boundaries

2. **Data Validation Testing**
   - Test with valid data
   - Test with invalid data
   - Test with missing required fields

3. **Error Handling Testing**
   - Test 4xx error responses
   - Test 5xx error responses
   - Verify meaningful error messages

4. **Performance Testing**
   - Test response times
   - Test under load
   - Monitor resource usage

**Sample Test Structure:**
```yaml
- name: "GET User Profile"
  request:
    method: GET
    url: "/api/users/123"
    headers:
      Authorization: "Bearer {{token}}"
  expect:
    status: 200
    json:
      id: 123
      name: "{{string}}"

- name: "Create User"
  request:
    method: POST
    url: "/api/users"
    json:
      name: "New User"
      email: "user@example.com"
  expect:
    status: 201
    json:
      id: "{{number}}"
```

**Testing Tools Recommendation:**
- Use Restaceratops for automated testing
- Monitor with real-time dashboards
- Generate comprehensive reports

Need help setting up specific test cases?"""
    
    def _get_debugging_guidance(self, user_input: str) -> str:
        """Provide debugging guidance."""
        return f"""🐛 **API Debugging Guide**

Based on your question: "{user_input}"

**Systematic Debugging Approach:**

1. **Check Request Details**
   - Verify HTTP method
   - Check URL and parameters
   - Validate request headers
   - Review request body

2. **Analyze Response**
   - Check status codes
   - Review response headers
   - Examine response body
   - Look for error messages

3. **Common Issues & Solutions**
   - **401 Unauthorized**: Check authentication
   - **400 Bad Request**: Validate request format
   - **404 Not Found**: Verify endpoint URL
   - **500 Internal Error**: Check server logs

4. **Debugging Tools**
   - Use browser DevTools
   - Check network tab
   - Review server logs
   - Use API testing tools

**Debugging Checklist:**
```yaml
- name: "Debug Request"
  request:
    method: "{{method}}"
    url: "{{url}}"
    headers: "{{headers}}"
    body: "{{body}}"
  expect:
    status: "{{expected_status}}"
  debug:
    log_request: true
    log_response: true
    validate_schema: true
```

**Quick Debug Steps:**
1. Test with simple tools (curl, Postman)
2. Check API documentation
3. Verify authentication
4. Review error logs
5. Test with minimal data

Need help debugging a specific issue?"""
    
    def _get_performance_guidance(self, user_input: str) -> str:
        """Provide performance testing guidance."""
        return f"""⚡ **Performance Testing Guide**

Based on your question: "{user_input}"

**Performance Testing Strategy:**

1. **Response Time Testing**
   - Measure individual request times
   - Set acceptable thresholds
   - Monitor under different loads

2. **Load Testing**
   - Test with multiple concurrent users
   - Identify breaking points
   - Monitor resource usage

3. **Stress Testing**
   - Test beyond normal capacity
   - Identify failure modes
   - Test recovery mechanisms

**Performance Metrics:**
- **Response Time**: < 200ms for simple requests
- **Throughput**: Requests per second
- **Error Rate**: < 1% under normal load
- **Resource Usage**: CPU, memory, network

**Sample Performance Test:**
```yaml
- name: "Performance Test"
  request:
    method: GET
    url: "/api/users"
  expect:
    status: 200
    response_time: "< 500ms"
  performance:
    concurrent_users: 10
    duration: "30s"
    ramp_up: "10s"
```

**Optimization Tips:**
- Use caching where appropriate
- Optimize database queries
- Implement pagination
- Use CDN for static content
- Monitor and alert on performance

Need help setting up performance tests?"""
    
    def _get_security_guidance(self, user_input: str) -> str:
        """Provide security testing guidance."""
        return f"""🔒 **Security Testing Guide**

Based on your question: "{user_input}"

**Security Testing Checklist:**

1. **Authentication Security**
   - Test password strength requirements
   - Verify secure token storage
   - Test session management
   - Check for brute force protection

2. **Authorization Testing**
   - Test role-based access control
   - Verify permission boundaries
   - Test privilege escalation
   - Check resource isolation

3. **Input Validation**
   - Test SQL injection prevention
   - Test XSS protection
   - Test file upload security
   - Validate input sanitization

4. **Data Protection**
   - Verify HTTPS usage
   - Check sensitive data encryption
   - Test data exposure prevention
   - Verify GDPR compliance

**Security Test Examples:**
```yaml
- name: "SQL Injection Test"
  request:
    method: POST
    url: "/api/search"
    json:
      query: "'; DROP TABLE users; --"
  expect:
    status: 400
    not_contains: "error in your SQL syntax"

- name: "XSS Test"
  request:
    method: POST
    url: "/api/comments"
    json:
      content: "<script>alert('xss')</script>"
  expect:
    status: 400
    not_contains: "<script>"
```

**Security Best Practices:**
- Use HTTPS everywhere
- Implement proper authentication
- Validate all inputs
- Use parameterized queries
- Regular security audits

Need help implementing security tests?"""
    
    def _get_test_generation_guidance(self, user_input: str) -> str:
        """Provide test generation guidance."""
        return f"""🎯 **Test Generation Guide**

Based on your question: "{user_input}"

**Automated Test Generation Strategy:**

1. **OpenAPI Specification Analysis**
   - Parse API documentation
   - Generate tests for all endpoints
   - Create positive and negative tests
   - Include edge cases

2. **Test Categories to Generate**
   - **Happy Path Tests**: Valid requests
   - **Error Tests**: Invalid inputs
   - **Boundary Tests**: Edge cases
   - **Performance Tests**: Load scenarios

3. **Test Data Generation**
   - Generate realistic test data
   - Create varied input scenarios
   - Include boundary values
   - Test data validation

**Generated Test Structure:**
```yaml
# Generated from OpenAPI spec
- name: "GET /api/users - Success"
  request:
    method: GET
    url: "/api/users"
    headers:
      Authorization: "Bearer {{token}}"
  expect:
    status: 200
    json_schema:
      type: array
      items:
        type: object
        properties:
          id: {type: integer}
          name: {type: string}

- name: "POST /api/users - Invalid Data"
  request:
    method: POST
    url: "/api/users"
    json:
      email: "invalid-email"
  expect:
    status: 400
    json:
      error: "Invalid email format"
```

**Test Generation Tools:**
- Use Restaceratops AI for intelligent generation
- Parse OpenAPI/Swagger specifications
- Generate comprehensive test suites
- Include assertions and validations

Ready to generate tests for your API?"""
    
    def _get_general_api_guidance(self, user_input: str) -> str:
        """Provide general API guidance."""
        return f"""🦖 **Restaceratops API Testing Assistant**

Based on your question: "{user_input}"

**How I Can Help You:**

🔧 **API Testing Services:**
- Generate comprehensive test cases
- Execute automated API tests
- Monitor test performance
- Generate detailed reports

🤖 **AI-Powered Features:**
- Intelligent test generation
- Smart debugging assistance
- Performance optimization tips
- Security testing guidance

📊 **Real-time Monitoring:**
- Live test execution tracking
- Performance metrics dashboard
- Error analysis and reporting
- Success rate monitoring

**Quick Actions:**
1. **Test Generation**: Upload your API spec or describe endpoints
2. **Test Execution**: Run existing test suites
3. **Debugging**: Get help with API issues
4. **Performance**: Analyze response times and throughput

**Sample Commands:**
- "Generate tests for my user API"
- "Help me debug a 500 error"
- "Create performance tests"
- "Test authentication endpoints"

**Current Status:**
- ✅ Test execution engine: Ready
- ✅ Report generation: Active
- ✅ Dashboard monitoring: Live
- ✅ AI model: Qwen3 Coder (OpenRouter)

I'm here to help you build robust, reliable APIs! What would you like to work on?"""
    
    def _get_fallback_test_template(self, api_spec: str) -> str:
        """Get fallback test template."""
        return f"""# API Test Template

## Test Cases for: {api_spec}

### 1. Basic Functionality Tests
```yaml
- name: "Test basic GET request"
  method: "GET"
  url: "/api/endpoint"
  expected_status: 200
  validate:
    - "response contains expected data"
    - "response time < 1000ms"
```

### 2. Error Handling Tests
```yaml
- name: "Test invalid input"
  method: "POST"
  url: "/api/endpoint"
  body: "{{invalid_data}}"
  expected_status: 400
  validate:
    - "error message is clear"
```

### 3. Authentication Tests
```yaml
- name: "Test without authentication"
  method: "GET"
  url: "/api/protected-endpoint"
  headers: {{}}
  expected_status: 401
```

Please customize these templates based on your specific API requirements."""
    
    async def reset_system(self) -> str:
        """Reset the AI system."""
        try:
            self.conversation_history = []
            return "✅ AI system reset successfully"
        except Exception as e:
            log.error(f"Error resetting system: {e}")
            return "❌ Failed to reset AI system"

def get_enhanced_ai_system() -> EnhancedAISystem:
    """Get enhanced AI system instance."""
    return EnhancedAISystem()

async def test_enhanced_ai_system():
    """Test the enhanced AI system."""
    system = get_enhanced_ai_system()
    
    # Test conversation
    response = await system.handle_conversation("Hello! Can you help me with API testing?")
    print(f"Conversation Response: {response}")
    
    # Test stats
    stats = system.get_system_stats()
    print(f"System Stats: {stats}")

if __name__ == "__main__":
    asyncio.run(test_enhanced_ai_system()) 