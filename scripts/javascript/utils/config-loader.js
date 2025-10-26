#!/usr/bin/env node
/**
 * @fileoverview MCP Configuration Loader
 * Enterprise-grade configuration loading with validation and caching.
 * @module utils/config-loader
 */

'use strict';

const fs = require('fs').promises;
const path = require('path');

/**
 * @typedef {Object} ServerConfig
 * @property {string} command - Command to execute (npx, uvx, node, python)
 * @property {string[]} args - Command arguments
 * @property {Object.<string, string>} [env] - Environment variables
 */

/**
 * @typedef {Object} MCPConfig
 * @property {Object.<string, ServerConfig>} servers - Server configurations
 * @property {Object} [_metadata] - Optional metadata
 */

/**
 * Configuration loader with validation and caching.
 */
class ConfigLoader {
  /**
   * Creates a new ConfigLoader instance.
   * @param {string} configPath - Path to mcp.json configuration file
   * @throws {TypeError} If configPath is not a string
   */
  constructor(configPath) {
    if (typeof configPath !== 'string') {
      throw new TypeError('configPath must be a string');
    }
    
    this.configPath = configPath;
    this.config = null;
    this.loadTime = null;
  }

  /**
   * Loads and validates MCP configuration.
   * @returns {Promise<MCPConfig>} Parsed configuration object
   * @throws {Error} If file doesn't exist, is invalid JSON, or fails validation
   * @example
   * const loader = new ConfigLoader('.vscode/mcp.json');
   * const config = await loader.load();
   * console.log(`Loaded ${Object.keys(config.servers).length} servers`);
   */
  async load() {
    try {
      const data = await fs.readFile(this.configPath, 'utf-8');
      this.config = JSON.parse(data);
      this.loadTime = new Date();
      
      this._validate();
      
      return this.config;
    } catch (error) {
      if (error.code === 'ENOENT') {
        throw new Error(`Configuration file not found: ${this.configPath}`);
      }
      if (error instanceof SyntaxError) {
        throw new Error(`Invalid JSON in configuration: ${error.message}`);
      }
      throw error;
    }
  }

  /**
   * Validates configuration structure.
   * @private
   * @throws {Error} If configuration is invalid
   */
  _validate() {
    if (!this.config || typeof this.config !== 'object') {
      throw new Error('Configuration must be an object');
    }

    if (!this.config.servers || typeof this.config.servers !== 'object') {
      throw new Error('Configuration must contain "servers" object');
    }

    const serverNames = Object.keys(this.config.servers);
    if (serverNames.length === 0) {
      throw new Error('Configuration must contain at least one server');
    }

    // Validate each server configuration
    for (const [name, config] of Object.entries(this.config.servers)) {
      this._validateServer(name, config);
    }
  }

  /**
   * Validates a single server configuration.
   * @private
   * @param {string} name - Server name
   * @param {ServerConfig} config - Server configuration
   * @throws {Error} If server configuration is invalid
   */
  _validateServer(name, config) {
    if (!config || typeof config !== 'object') {
      throw new Error(`Server "${name}" configuration must be an object`);
    }

    if (!config.command || typeof config.command !== 'string') {
      throw new Error(`Server "${name}" must have a "command" string`);
    }

    if (!config.args || !Array.isArray(config.args)) {
      throw new Error(`Server "${name}" must have an "args" array`);
    }

    for (let i = 0; i < config.args.length; i++) {
      if (typeof config.args[i] !== 'string') {
        throw new Error(`Server "${name}" args[${i}] must be a string`);
      }
    }

    if (config.env) {
      if (typeof config.env !== 'object') {
        throw new Error(`Server "${name}" env must be an object`);
      }

      for (const [key, value] of Object.entries(config.env)) {
        if (typeof value !== 'string') {
          throw new Error(`Server "${name}" env["${key}"] must be a string`);
        }
      }
    }
  }

  /**
   * Gets cached configuration without reloading.
   * @returns {MCPConfig|null} Cached configuration or null if not loaded
   * @example
   * const config = loader.getCached();
   * if (config === null) {
   *   await loader.load();
   * }
   */
  getCached() {
    return this.config;
  }

  /**
   * Gets server configuration by name.
   * @param {string} serverName - Name of the server
   * @returns {ServerConfig|undefined} Server configuration or undefined
   * @throws {TypeError} If serverName is not a string
   * @throws {Error} If configuration not loaded
   * @example
   * const githubConfig = loader.getServer('github');
   * console.log(githubConfig.command); // 'npx'
   */
  getServer(serverName) {
    if (typeof serverName !== 'string') {
      throw new TypeError('serverName must be a string');
    }

    if (!this.config) {
      throw new Error('Configuration not loaded. Call load() first.');
    }

    return this.config.servers[serverName];
  }

  /**
   * Gets list of all server names.
   * @returns {string[]} Array of server names
   * @throws {Error} If configuration not loaded
   * @example
   * const servers = loader.getServerNames();
   * console.log(`Available servers: ${servers.join(', ')}`);
   */
  getServerNames() {
    if (!this.config) {
      throw new Error('Configuration not loaded. Call load() first.');
    }

    return Object.keys(this.config.servers);
  }

  /**
   * Checks if a server exists in configuration.
   * @param {string} serverName - Name of the server
   * @returns {boolean} True if server exists
   * @throws {TypeError} If serverName is not a string
   * @throws {Error} If configuration not loaded
   */
  hasServer(serverName) {
    if (typeof serverName !== 'string') {
      throw new TypeError('serverName must be a string');
    }

    if (!this.config) {
      throw new Error('Configuration not loaded. Call load() first.');
    }

    return serverName in this.config.servers;
  }

  /**
   * Gets configuration load time.
   * @returns {Date|null} Time configuration was loaded, or null if not loaded
   */
  getLoadTime() {
    return this.loadTime;
  }
}

/**
 * Loads MCP configuration from file.
 * @param {string} configPath - Path to mcp.json file
 * @returns {Promise<MCPConfig>} Parsed configuration
 * @throws {Error} If file doesn't exist or is invalid
 * @example
 * const config = await loadConfig('.vscode/mcp.json');
 * console.log(config.servers);
 */
async function loadConfig(configPath) {
  const loader = new ConfigLoader(configPath);
  return await loader.load();
}

module.exports = {
  ConfigLoader,
  loadConfig
};
