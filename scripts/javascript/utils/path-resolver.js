#!/usr/bin/env node
/**
 * @fileoverview Path Resolution Utilities
 * Enterprise-grade path resolution with environment variable substitution.
 * @module utils/path-resolver
 */

'use strict';

const path = require('path');

/**
 * Resolves environment variable placeholders in strings.
 */
class PathResolver {
  /**
   * Creates a new PathResolver instance.
   * @param {string} workspaceRoot - Root directory of the workspace
   * @throws {TypeError} If workspaceRoot is not a string
   */
  constructor(workspaceRoot) {
    if (typeof workspaceRoot !== 'string') {
      throw new TypeError('workspaceRoot must be a string');
    }

    this.workspaceRoot = workspaceRoot;
  }

  /**
   * Resolves ${workspaceFolder} placeholder in string.
   * @param {string} str - String to resolve
   * @returns {string} Resolved string
   * @throws {TypeError} If str is not a string
   * @example
   * const resolver = new PathResolver('/workspace');
   * resolver.resolveWorkspaceFolder('${workspaceFolder}/config');
   * // Returns: '/workspace/config'
   */
  resolveWorkspaceFolder(str) {
    if (typeof str !== 'string') {
      throw new TypeError('str must be a string');
    }

    return str.replace(/\$\{workspaceFolder\}/g, this.workspaceRoot);
  }

  /**
   * Resolves ${env:VAR_NAME} placeholders in string.
   * @param {string} str - String to resolve
   * @returns {string} Resolved string with environment variables substituted
   * @throws {TypeError} If str is not a string
   * @example
   * process.env.MY_VAR = 'value';
   * const resolver = new PathResolver('/workspace');
   * resolver.resolveEnvVars('${env:MY_VAR}/path');
   * // Returns: 'value/path'
   */
  resolveEnvVars(str) {
    if (typeof str !== 'string') {
      throw new TypeError('str must be a string');
    }

    return str.replace(/\$\{env:([^}]+)\}/g, (match, varName) => {
      return process.env[varName] || '';
    });
  }

  /**
   * Resolves all placeholders in string.
   * @param {string} str - String to resolve
   * @returns {string} Fully resolved string
   * @throws {TypeError} If str is not a string
   * @example
   * const resolver = new PathResolver('/workspace');
   * resolver.resolve('${workspaceFolder}/${env:CONFIG_DIR}');
   */
  resolve(str) {
    if (typeof str !== 'string') {
      throw new TypeError('str must be a string');
    }

    let resolved = this.resolveWorkspaceFolder(str);
    resolved = this.resolveEnvVars(resolved);
    return resolved;
  }

  /**
   * Resolves array of arguments with placeholder substitution.
   * @param {string[]} args - Array of argument strings
   * @returns {string[]} Array with resolved arguments
   * @throws {TypeError} If args is not an array
   * @example
   * const resolver = new PathResolver('/workspace');
   * resolver.resolveArgs(['--config', '${workspaceFolder}/config.json']);
   * // Returns: ['--config', '/workspace/config.json']
   */
  resolveArgs(args) {
    if (!Array.isArray(args)) {
      throw new TypeError('args must be an array');
    }

    return args.map(arg => {
      if (typeof arg === 'string') {
        return this.resolve(arg);
      }
      return arg;
    });
  }

  /**
   * Resolves environment variable object with ${env:VAR} substitution.
   * @param {Object.<string, string>} env - Environment variables object
   * @returns {Object.<string, string>} Object with resolved values
   * @throws {TypeError} If env is not an object
   * @example
   * const resolver = new PathResolver('/workspace');
   * resolver.resolveEnv({ PATH: '${env:PATH}:/extra' });
   */
  resolveEnv(env) {
    if (!env || typeof env !== 'object') {
      throw new TypeError('env must be an object');
    }

    const resolved = {};

    for (const [key, value] of Object.entries(env)) {
      if (typeof value === 'string') {
        // Handle ${env:VAR} pattern
        if (value.startsWith('${env:') && value.endsWith('}')) {
          const varName = value.slice(6, -1);
          resolved[key] = process.env[varName] || '';
        } else {
          resolved[key] = this.resolve(value);
        }
      } else {
        resolved[key] = value;
      }
    }

    return resolved;
  }

  /**
   * Gets workspace root directory.
   * @returns {string} Workspace root path
   */
  getWorkspaceRoot() {
    return this.workspaceRoot;
  }

  /**
   * Resolves relative path from workspace root.
   * @param {string} relativePath - Relative path
   * @returns {string} Absolute path
   * @throws {TypeError} If relativePath is not a string
   * @example
   * const resolver = new PathResolver('/workspace');
   * resolver.resolvePath('config/app.json');
   * // Returns: '/workspace/config/app.json'
   */
  resolvePath(relativePath) {
    if (typeof relativePath !== 'string') {
      throw new TypeError('relativePath must be a string');
    }

    return path.join(this.workspaceRoot, relativePath);
  }
}

/**
 * Resolves workspace folder placeholder in string.
 * @param {string} str - String to resolve
 * @param {string} workspaceRoot - Workspace root directory
 * @returns {string} Resolved string
 * @throws {TypeError} If arguments are invalid
 * @example
 * resolveWorkspaceFolder('${workspaceFolder}/config', '/workspace');
 * // Returns: '/workspace/config'
 */
function resolveWorkspaceFolder(str, workspaceRoot) {
  const resolver = new PathResolver(workspaceRoot);
  return resolver.resolveWorkspaceFolder(str);
}

/**
 * Resolves environment variable placeholders in string.
 * @param {string} str - String to resolve
 * @returns {string} Resolved string
 * @throws {TypeError} If str is not a string
 * @example
 * process.env.HOME = '/home/user';
 * resolveEnvVars('${env:HOME}/.config');
 * // Returns: '/home/user/.config'
 */
function resolveEnvVars(str) {
  const resolver = new PathResolver(process.cwd());
  return resolver.resolveEnvVars(str);
}

module.exports = {
  PathResolver,
  resolveWorkspaceFolder,
  resolveEnvVars
};
