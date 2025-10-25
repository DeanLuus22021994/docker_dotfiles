---
applyTo: "**/agent_app.py,**/*agent*/**/*.py"
---

## Agent Code Guidelines

When working with AI agent code in this repository:

### Async Patterns
- Use `async def` for all agent functions and methods
- Implement proper `await` calls for asynchronous operations
- Use `asyncio.run()` for entry points when needed

### Error Handling
- Wrap all agent operations in try/except blocks
- Log errors appropriately using the logging framework
- Provide meaningful error messages for debugging

### Tool Integration
- Follow established tool calling patterns using MCP protocol
- Validate tool inputs and outputs
- Handle tool failures gracefully

### Code Structure
- Keep agent logic modular and testable
- Use type hints for better code clarity
- Document complex logic with clear comments

### Testing
- Write unit tests for agent functions
- Use pytest-asyncio for async test functions
- Mock external dependencies in tests

### Environment Variables
- Use environment variables for configuration
- Validate required environment variables on startup
- Document required environment variables in docstrings