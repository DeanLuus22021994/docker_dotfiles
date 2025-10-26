#!/usr/bin/env node
/**
 * @fileoverview MCP Client for Model Context Protocol Communication
 * Enterprise-grade MCP client with initialize and tools/list support.
 * @module mcp/client
 */

'use strict';

const { PathResolver } = require('../utils/path-resolver');
const { executeJsonRpc } = require('../utils/process-manager');
const { createLogger } = require('../utils/logger');

/**
 * @typedef {Object} ServerConfig
 * @property {string} command - Command to execute
 * @property {string[]} args - Command arguments
 * @property {Object.<string, string>} [env] - Environment variables
 */

/**
 * @typedef {Object} MCPTool
 * @property {string} name - Tool name
 * @property {string} description - Tool description
 * @property {Object} inputSchema - JSON schema for tool input
 */

/**
 * @typedef {Object} ServerCapabilities
 * @property {Object} [tools] - Tool capabilities
 * @property {Object} [resources] - Resource capabilities
 * @property {Object} [prompts] - Prompt capabilities
 */

/**
 * @typedef {Object} InitializeResult
 * @property {string} protocolVersion - MCP protocol version
 * @property {ServerCapabilities} capabilities - Server capabilities
 * @property {Object} serverInfo - Server information
 */

/**
 * MCP protocol client for server communication.
 */
class MCPClient {
  /**
   * Creates a new MCPClient instance.
   * @param {string} serverName - Name of the MCP server
   * @param {ServerConfig} config - Server configuration
   * @param {string} workspaceRoot - Workspace root directory
   * @throws {TypeError} If arguments are invalid
   * @example
   * const client = new MCPClient('github', {
   *   command: 'npx',
   *   args: ['-y', '@modelcontextprotocol/server-github']
   * }, '/workspace');
   */
  constructor(serverName, config, workspaceRoot) {
    this._validate(serverName, config, workspaceRoot);

    this.serverName = serverName;
    this.config = config;
    this.workspaceRoot = workspaceRoot;
    this.pathResolver = new PathResolver(workspaceRoot);
    this.logger = createLogger(`MCP:${serverName}`);

    this.requestId = 0;
    this.initializeResult = null;
  }

  /**
   * Validates constructor arguments.
   * @private
   * @param {string} serverName - Server name
   * @param {ServerConfig} config - Server configuration
   * @param {string} workspaceRoot - Workspace root
   * @throws {TypeError} If arguments are invalid
   */
  _validate(serverName, config, workspaceRoot) {
    if (typeof serverName !== 'string') {
      throw new TypeError('serverName must be a string');
    }
    if (!config || typeof config !== 'object') {
      throw new TypeError('config must be an object');
    }
    if (typeof config.command !== 'string') {
      throw new TypeError('config.command must be a string');
    }
    if (!Array.isArray(config.args)) {
      throw new TypeError('config.args must be an array');
    }
    if (typeof workspaceRoot !== 'string') {
      throw new TypeError('workspaceRoot must be a string');
    }
  }

  /**
   * Gets next request ID.
   * @private
   * @returns {number} Next request ID
   */
  _nextRequestId() {
    return ++this.requestId;
  }

  /**
   * Prepares process options with resolved paths and environment.
   * @private
   * @param {number} [timeout=15000] - Timeout in milliseconds
   * @returns {Object} Process options
   */
  _prepareProcessOptions(timeout = 15000) {
    const resolvedArgs = this.pathResolver.resolveArgs(this.config.args);
    const resolvedEnv = this.config.env
      ? this.pathResolver.resolveEnv(this.config.env)
      : {};

    return {
      command: this.config.command,
      args: resolvedArgs,
      env: resolvedEnv,
      cwd: this.workspaceRoot,
      timeout
    };
  }

  /**
   * Initializes connection to MCP server.
   * @param {number} [timeout=5000] - Timeout in milliseconds
   * @returns {Promise<InitializeResult>} Initialize result
   * @throws {Error} If initialization fails
   * @example
   * const result = await client.initialize();
   * console.log(`Server: ${result.serverInfo.name} v${result.serverInfo.version}`);
   */
  async initialize(timeout = 5000) {
    const request = {
      jsonrpc: '2.0',
      id: this._nextRequestId(),
      method: 'initialize',
      params: {
        protocolVersion: '2024-11-05',
        capabilities: {
          roots: { listChanged: true },
          sampling: {}
        },
        clientInfo: {
          name: 'mcp-client',
          version: '1.0.0'
        }
      }
    };

    try {
      const options = this._prepareProcessOptions(timeout + 10000);
      const response = await executeJsonRpc(options, request, timeout);

      if (response.error) {
        throw new Error(`Initialize error: ${response.error.message}`);
      }

      if (!response.result) {
        throw new Error('Initialize response missing result');
      }

      this.initializeResult = response.result;
      return response.result;

    } catch (error) {
      throw new Error(`Failed to initialize ${this.serverName}: ${error.message}`);
    }
  }

  /**
   * Lists available tools from MCP server.
   * @param {number} [timeout=5000] - Timeout in milliseconds
   * @returns {Promise<MCPTool[]>} Array of tools
   * @throws {Error} If tools/list request fails
   * @example
   * const tools = await client.listTools();
   * console.log(`Server provides ${tools.length} tools`);
   * tools.forEach(tool => console.log(`  - ${tool.name}: ${tool.description}`));
   */
  async listTools(timeout = 5000) {
    const request = {
      jsonrpc: '2.0',
      id: this._nextRequestId(),
      method: 'tools/list',
      params: {}
    };

    try {
      const options = this._prepareProcessOptions(timeout + 10000);
      const response = await executeJsonRpc(options, request, timeout);

      if (response.error) {
        throw new Error(`tools/list error: ${response.error.message}`);
      }

      if (!response.result || !response.result.tools) {
        throw new Error('tools/list response missing tools array');
      }

      return response.result.tools;

    } catch (error) {
      throw new Error(`Failed to list tools from ${this.serverName}: ${error.message}`);
    }
  }

  /**
   * Performs health check on MCP server.
   * @param {number} [timeout=5000] - Timeout in milliseconds
   * @returns {Promise<Object>} Health check result
   * @property {boolean} healthy - Whether server is healthy
   * @property {number} duration - Response time in milliseconds
   * @property {string} [error] - Error message if unhealthy
   * @example
   * const health = await client.healthCheck();
   * if (health.healthy) {
   *   console.log(`Server is healthy (${health.duration}ms)`);
   * }
   */
  async healthCheck(timeout = 5000) {
    const startTime = Date.now();

    try {
      await this.initialize(timeout);

      const duration = Date.now() - startTime;

      return {
        healthy: true,
        duration,
        serverName: this.serverName
      };

    } catch (error) {
      const duration = Date.now() - startTime;

      return {
        healthy: false,
        duration,
        serverName: this.serverName,
        error: error.message
      };
    }
  }

  /**
   * Discovers server capabilities and tools.
   * @param {number} [timeout=15000] - Timeout in milliseconds
   * @returns {Promise<Object>} Discovery result
   * @property {InitializeResult} initialize - Initialize result
   * @property {MCPTool[]} tools - Available tools
   * @property {number} duration - Total discovery time in milliseconds
   * @example
   * const discovery = await client.discover();
   * console.log(`Server: ${discovery.initialize.serverInfo.name}`);
   * console.log(`Tools: ${discovery.tools.length}`);
   * console.log(`Time: ${discovery.duration}ms`);
   */
  async discover(timeout = 15000) {
    const startTime = Date.now();

    try {
      // Initialize connection
      const initResult = await this.initialize(timeout);

      // List tools
      const tools = await this.listTools(timeout);

      const duration = Date.now() - startTime;

      return {
        serverName: this.serverName,
        initialize: initResult,
        tools,
        toolCount: tools.length,
        duration
      };

    } catch (error) {
      const duration = Date.now() - startTime;

      throw new Error(`Discovery failed for ${this.serverName}: ${error.message} (${duration}ms)`);
    }
  }

  /**
   * Gets server name.
   * @returns {string} Server name
   */
  getServerName() {
    return this.serverName;
  }

  /**
   * Gets initialize result (if initialized).
   * @returns {InitializeResult|null} Initialize result or null
   */
  getInitializeResult() {
    return this.initializeResult;
  }

  /**
   * Checks if server has been initialized.
   * @returns {boolean} True if initialized
   */
  isInitialized() {
    return this.initializeResult !== null;
  }
}

/**
 * Creates an MCP client instance.
 * @param {string} serverName - Server name
 * @param {ServerConfig} config - Server configuration
 * @param {string} workspaceRoot - Workspace root directory
 * @returns {MCPClient} New client instance
 * @throws {TypeError} If arguments are invalid
 * @example
 * const client = createClient('github', {
 *   command: 'npx',
 *   args: ['-y', '@modelcontextprotocol/server-github']
 * }, '/workspace');
 */
function createClient(serverName, config, workspaceRoot) {
  return new MCPClient(serverName, config, workspaceRoot);
}

module.exports = {
  MCPClient,
  createClient
};
