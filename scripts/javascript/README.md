# JavaScript Utilities

Enterprise-grade JavaScript utilities for the docker_dotfiles project.

## Directory Structure

```
scripts/javascript/
├── package.json         # Root package configuration with ESLint
├── utils/               # Shared utilities (NEW)
│   ├── config-loader.js    # MCP configuration loading with validation
│   ├── path-resolver.js    # Path resolution and variable substitution
│   ├── logger.js          # Console logging with colors and levels
│   └── process-manager.js  # Process spawning with timeout management
└── mcp/                 # MCP-specific tools
    ├── client.js           # MCP client abstraction (NEW)
    ├── health-check.js     # Server health check utility
    ├── discover-tools.js   # Tool discovery utility
    ├── package.json        # MCP tools package config
    └── README.md           # MCP tools documentation
```

## Shared Utilities (`utils/`)

### config-loader.js

Loads and validates MCP configuration files with caching.

```javascript
const { ConfigLoader, loadConfig } = require('./utils/config-loader');

// Quick load
const config = await loadConfig('.vscode/mcp.json');
console.log(config.servers);

// With caching and validation
const loader = new ConfigLoader('.vscode/mcp.json');
await loader.load();

const githubConfig = loader.getServer('github');
const serverNames = loader.getServerNames();
```

**Features:**
- ✅ JSON validation with descriptive errors
- ✅ Server configuration validation
- ✅ Configuration caching
- ✅ Individual server access
- ✅ Comprehensive JSDoc with examples

### path-resolver.js

Resolves environment variables and workspace paths.

```javascript
const { PathResolver } = require('./utils/path-resolver');

const resolver = new PathResolver('/workspace');

// Resolve workspace folder
const path = resolver.resolve('${workspaceFolder}/config.json');
// Returns: '/workspace/config.json'

// Resolve environment variables
const envPath = resolver.resolve('${env:HOME}/.config');
// Returns: '/home/user/.config'

// Resolve arrays
const args = resolver.resolveArgs([
  '--config',
  '${workspaceFolder}/app.json'
]);
```

**Features:**
- ✅ `${workspaceFolder}` placeholder resolution
- ✅ `${env:VAR_NAME}` environment variable substitution
- ✅ Array argument resolution
- ✅ Environment object resolution
- ✅ Type-safe with validation

### logger.js

Console logging with colors, levels, and formatting.

```javascript
const { createLogger, LogLevel, Colors } = require('./utils/logger');

const logger = createLogger('MyApp', LogLevel.DEBUG);

logger.info('Application started');
logger.success('Configuration loaded');
logger.warn('Using default port');
logger.error('Failed to connect', new Error('ECONNREFUSED'));

logger.header('Test Results');
logger.separator(80, '-');
logger.json({ passed: 10, failed: 2 });
```

**Features:**
- ✅ Log levels: DEBUG, INFO, WARN, ERROR, SILENT
- ✅ Color-coded output with ANSI codes
- ✅ Timestamp formatting
- ✅ Stack trace support for errors
- ✅ JSON pretty-printing
- ✅ Headers and separators

### process-manager.js

Managed process spawning with timeout and event handling.

```javascript
const { ManagedProcess, execute, executeJsonRpc } = require('./utils/process-manager');

// Simple execution
const result = await execute({
  command: 'node',
  args: ['--version'],
  timeout: 5000
});
console.log(result.stdout);

// JSON-RPC communication
const response = await executeJsonRpc(
  { command: 'npx', args: ['mcp-server'] },
  { jsonrpc: '2.0', id: 1, method: 'initialize', params: {} },
  5000
);

// Advanced usage with events
const proc = new ManagedProcess({
  command: 'node',
  args: ['script.js'],
  timeout: 15000
});

proc.on('stdout', (data) => console.log(data));
proc.on('stderr', (data) => console.error(data));
proc.on('exit', (result) => console.log(`Exit code: ${result.exitCode}`));
proc.on('timeout', () => console.log('Process timed out'));

proc.start();
proc.write('input data\n');
```

**Features:**
- ✅ Timeout management with automatic cleanup
- ✅ Event-driven architecture (extends EventEmitter)
- ✅ JSON-RPC request/response handling
- ✅ Stdout/stderr capture
- ✅ Environment variable resolution
- ✅ Cross-platform shell support

## MCP Client (`mcp/client.js`)

Enterprise-grade MCP client for Model Context Protocol communication.

```javascript
const { MCPClient, createClient } = require('./mcp/client');

// Create client
const client = new MCPClient('github', {
  command: 'npx',
  args: ['-y', '@modelcontextprotocol/server-github']
}, '/workspace');

// Initialize connection
const initResult = await client.initialize();
console.log(`Server: ${initResult.serverInfo.name}`);

// List available tools
const tools = await client.listTools();
console.log(`${tools.length} tools available`);

// Health check
const health = await client.healthCheck();
console.log(`Healthy: ${health.healthy} (${health.duration}ms)`);

// Full discovery
const discovery = await client.discover();
console.log(JSON.stringify(discovery, null, 2));
```

**Features:**
- ✅ Initialize protocol connection
- ✅ List server tools
- ✅ Health check with timing
- ✅ Full discovery (initialize + tools)
- ✅ Automatic path resolution
- ✅ Timeout management
- ✅ Comprehensive error handling

## Code Quality

All modules follow enterprise-grade standards:

- ✅ **Type Safety:** JSDoc with `@param`, `@returns`, `@throws`, `@example`
- ✅ **Input Validation:** TypeError for all invalid inputs
- ✅ **Error Handling:** Descriptive error messages with context
- ✅ **No Suppressions:** Zero ESLint disables or ignores
- ✅ **Documentation:** Complete JSDoc for all public APIs
- ✅ **Modularity:** Single responsibility per module
- ✅ **Testability:** Pure functions and dependency injection

## ESLint Configuration

```bash
# Lint all JavaScript files
npm run lint

# Auto-fix linting issues
npm run lint:fix
```

**Rules:**
- ES2021+ features enabled
- Semicolons required
- Single quotes preferred
- 2-space indentation
- No trailing spaces
- No unused variables (except `_` prefix)

## Usage in Other Scripts

```javascript
// Import utilities
const { loadConfig } = require('../utils/config-loader');
const { PathResolver } = require('../utils/path-resolver');
const { createLogger } = require('../utils/logger');
const { MCPClient } = require('../mcp/client');

// Use in your scripts
const config = await loadConfig('.vscode/mcp.json');
const resolver = new PathResolver(process.cwd());
const logger = createLogger('MyScript');
const client = new MCPClient('github', config.servers.github, process.cwd());
```

## Testing

```bash
# Run all tests (when implemented)
npm test

# Test specific utility
node -e "const { loadConfig } = require('./utils/config-loader'); loadConfig('.vscode/mcp.json').then(console.log);"
```

## Migration Notes

Existing scripts (`health-check.js`, `discover-tools.js`) can now be refactored to use these shared utilities, reducing duplication and improving maintainability.

---

**Version:** 1.0.0  
**Node.js:** >= 18.0.0  
**License:** MIT  
**Last Updated:** 2025-10-26
