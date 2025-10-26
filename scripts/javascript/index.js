#!/usr/bin/env node
/**
 * @fileoverview Main entry point for JavaScript utilities
 * Exports all utility modules for convenient importing.
 * @module javascript
 */

'use strict';

// Configuration utilities
const ConfigLoader = require('./utils/config-loader');

// Path resolution utilities
const PathResolver = require('./utils/path-resolver');

// Logging utilities
const Logger = require('./utils/logger');

// Process management utilities
const ProcessManager = require('./utils/process-manager');

// MCP client
const MCPClient = require('./mcp/client');

/**
 * @namespace Utils
 * @description Shared utility modules
 */
const Utils = {
  /**
   * Configuration loader with validation
   * @see module:utils/config-loader
   */
  ConfigLoader: ConfigLoader.ConfigLoader,
  loadConfig: ConfigLoader.loadConfig,

  /**
   * Path resolver with variable substitution
   * @see module:utils/path-resolver
   */
  PathResolver: PathResolver.PathResolver,
  resolveWorkspaceFolder: PathResolver.resolveWorkspaceFolder,
  resolveEnvVars: PathResolver.resolveEnvVars,

  /**
   * Console logger with colors and levels
   * @see module:utils/logger
   */
  Logger: Logger.Logger,
  createLogger: Logger.createLogger,
  Colors: Logger.Colors,
  LogLevel: Logger.LogLevel,

  /**
   * Process manager with timeout and events
   * @see module:utils/process-manager
   */
  ManagedProcess: ProcessManager.ManagedProcess,
  execute: ProcessManager.execute,
  executeJsonRpc: ProcessManager.executeJsonRpc
};

/**
 * @namespace MCP
 * @description MCP protocol utilities
 */
const MCP = {
  /**
   * MCP client for protocol communication
   * @see module:mcp/client
   */
  Client: MCPClient.MCPClient,
  createClient: MCPClient.createClient
};

// Export individual modules
module.exports = {
  Utils,
  MCP,
  
  // Direct exports for convenience
  ConfigLoader: ConfigLoader.ConfigLoader,
  loadConfig: ConfigLoader.loadConfig,
  
  PathResolver: PathResolver.PathResolver,
  resolveWorkspaceFolder: PathResolver.resolveWorkspaceFolder,
  resolveEnvVars: PathResolver.resolveEnvVars,
  
  Logger: Logger.Logger,
  createLogger: Logger.createLogger,
  Colors: Logger.Colors,
  LogLevel: Logger.LogLevel,
  
  ManagedProcess: ProcessManager.ManagedProcess,
  execute: ProcessManager.execute,
  executeJsonRpc: ProcessManager.executeJsonRpc,
  
  MCPClient: MCPClient.MCPClient,
  createClient: MCPClient.createClient
};
