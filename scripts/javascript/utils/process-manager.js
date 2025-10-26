#!/usr/bin/env node
/**
 * @fileoverview Process Manager for MCP Servers
 * Enterprise-grade process spawning with timeout and error handling.
 * @module utils/process-manager
 */

'use strict';

const { spawn } = require('child_process');
const EventEmitter = require('events');

/**
 * @typedef {Object} ProcessOptions
 * @property {string} command - Command to execute
 * @property {string[]} args - Command arguments
 * @property {Object.<string, string>} [env] - Environment variables
 * @property {string} [cwd] - Working directory
 * @property {number} [timeout=15000] - Timeout in milliseconds
 */

/**
 * @typedef {Object} ProcessResult
 * @property {number} exitCode - Process exit code
 * @property {string} stdout - Standard output
 * @property {string} stderr - Standard error
 * @property {number} duration - Execution duration in ms
 * @property {boolean} timedOut - Whether process timed out
 */

/**
 * Managed process with timeout and event handling.
 * @extends EventEmitter
 */
class ManagedProcess extends EventEmitter {
  /**
   * Creates a new ManagedProcess.
   * @param {ProcessOptions} options - Process options
   * @throws {TypeError} If options are invalid
   */
  constructor(options) {
    super();

    this._validateOptions(options);

    this.command = options.command;
    this.args = options.args;
    this.env = options.env || {};
    this.cwd = options.cwd || process.cwd();
    this.timeout = options.timeout || 15000;

    this.process = null;
    this.startTime = null;
    this.exitCode = null;
    this.stdout = '';
    this.stderr = '';
    this.timedOut = false;
    this.timeoutHandle = null;
  }

  /**
   * Validates process options.
   * @private
   * @param {ProcessOptions} options - Options to validate
   * @throws {TypeError} If options are invalid
   */
  _validateOptions(options) {
    if (!options || typeof options !== 'object') {
      throw new TypeError('options must be an object');
    }
    if (typeof options.command !== 'string') {
      throw new TypeError('options.command must be a string');
    }
    if (!Array.isArray(options.args)) {
      throw new TypeError('options.args must be an array');
    }
    if (options.env && typeof options.env !== 'object') {
      throw new TypeError('options.env must be an object');
    }
    if (options.timeout && typeof options.timeout !== 'number') {
      throw new TypeError('options.timeout must be a number');
    }
  }

  /**
   * Starts the process.
   * @returns {ManagedProcess} This instance for chaining
   * @throws {Error} If process is already running
   * @example
   * const proc = new ManagedProcess({ command: 'node', args: ['script.js'] });
   * proc.start();
   * proc.on('exit', (code) => console.log(`Exited with code ${code}`));
   */
  start() {
    if (this.process) {
      throw new Error('Process is already running');
    }

    this.startTime = Date.now();

    // Merge environment variables
    const env = { ...process.env, ...this.env };

    // Spawn process
    this.process = spawn(this.command, this.args, {
      env,
      cwd: this.cwd,
      stdio: ['pipe', 'pipe', 'pipe'],
      shell: true  // Use shell for proper command resolution
    });

    // Setup stdout handler
    this.process.stdout.on('data', (data) => {
      this.stdout += data.toString();
      this.emit('stdout', data.toString());
    });

    // Setup stderr handler
    this.process.stderr.on('data', (data) => {
      this.stderr += data.toString();
      this.emit('stderr', data.toString());
    });

    // Setup error handler
    this.process.on('error', (error) => {
      this.emit('error', error);
    });

    // Setup exit handler
    this.process.on('close', (code) => {
      this.exitCode = code;
      this._clearTimeout();

      const duration = Date.now() - this.startTime;

      this.emit('exit', {
        exitCode: code,
        duration,
        timedOut: this.timedOut
      });
    });

    // Setup timeout
    this.timeoutHandle = setTimeout(() => {
      if (this.process && !this.exitCode) {
        this.timedOut = true;
        this.kill();
        this.emit('timeout', {
          duration: this.timeout,
          stdout: this.stdout,
          stderr: this.stderr
        });
      }
    }, this.timeout);

    return this;
  }

  /**
   * Writes to process stdin.
   * @param {string} data - Data to write
   * @throws {Error} If process is not running
   * @example
   * proc.write(JSON.stringify({ method: 'initialize' }) + '\n');
   */
  write(data) {
    if (!this.process || !this.process.stdin) {
      throw new Error('Process is not running or stdin is not available');
    }

    this.process.stdin.write(data);
  }

  /**
   * Kills the process.
   * @param {string} [signal='SIGTERM'] - Signal to send
   * @example
   * proc.kill('SIGKILL');
   */
  kill(signal = 'SIGTERM') {
    if (this.process) {
      this.process.kill(signal);
      this._clearTimeout();
    }
  }

  /**
   * Clears timeout handle.
   * @private
   */
  _clearTimeout() {
    if (this.timeoutHandle) {
      clearTimeout(this.timeoutHandle);
      this.timeoutHandle = null;
    }
  }

  /**
   * Gets execution duration.
   * @returns {number|null} Duration in milliseconds, or null if not started
   */
  getDuration() {
    if (!this.startTime) {
      return null;
    }

    const endTime = this.exitCode !== null ? Date.now() : Date.now();
    return endTime - this.startTime;
  }

  /**
   * Gets process result.
   * @returns {ProcessResult|null} Result object, or null if not finished
   */
  getResult() {
    if (this.exitCode === null) {
      return null;
    }

    return {
      exitCode: this.exitCode,
      stdout: this.stdout,
      stderr: this.stderr,
      duration: this.getDuration(),
      timedOut: this.timedOut
    };
  }

  /**
   * Checks if process is running.
   * @returns {boolean} True if process is running
   */
  isRunning() {
    return this.process !== null && this.exitCode === null;
  }
}

/**
 * Executes a process and returns result.
 * @param {ProcessOptions} options - Process options
 * @returns {Promise<ProcessResult>} Process result
 * @throws {Error} If process execution fails
 * @example
 * const result = await execute({
 *   command: 'node',
 *   args: ['--version'],
 *   timeout: 5000
 * });
 * console.log(result.stdout);
 */
async function execute(options) {
  return new Promise((resolve, reject) => {
    const proc = new ManagedProcess(options);

    proc.on('exit', (exitInfo) => {
      const result = proc.getResult();
      resolve(result);
    });

    proc.on('error', (error) => {
      reject(new Error(`Process error: ${error.message}`));
    });

    proc.start();
  });
}

/**
 * Executes process with JSON-RPC request/response handling.
 * @param {ProcessOptions} options - Process options
 * @param {Object} request - JSON-RPC request object
 * @param {number} [responseTimeout=5000] - Response timeout in ms
 * @returns {Promise<Object>} JSON-RPC response
 * @throws {Error} If execution fails or times out
 * @example
 * const response = await executeJsonRpc(
 *   { command: 'npx', args: ['mcp-server'] },
 *   { jsonrpc: '2.0', id: 1, method: 'initialize', params: {} }
 * );
 */
async function executeJsonRpc(options, request, responseTimeout = 5000) {
  return new Promise((resolve, reject) => {
    const proc = new ManagedProcess(options);
    let responseReceived = false;
    let responseTimer = null;

    proc.on('stdout', (data) => {
      const lines = data.split('\n');

      for (const line of lines) {
        if (!line.trim()) continue;

        try {
          const response = JSON.parse(line);

          if (response.id === request.id) {
            responseReceived = true;
            clearTimeout(responseTimer);
            proc.kill();
            resolve(response);
          }
        } catch (e) {
          // Not valid JSON, continue
        }
      }
    });

    proc.on('error', (error) => {
      clearTimeout(responseTimer);
      reject(new Error(`Process error: ${error.message}`));
    });

    proc.on('exit', () => {
      clearTimeout(responseTimer);
      if (!responseReceived) {
        reject(new Error('Process exited without sending response'));
      }
    });

    proc.start();

    // Send request after small delay
    setTimeout(() => {
      try {
        proc.write(JSON.stringify(request) + '\n');
      } catch (error) {
        clearTimeout(responseTimer);
        reject(error);
      }
    }, 100);

    // Response timeout
    responseTimer = setTimeout(() => {
      if (!responseReceived) {
        proc.kill();
        reject(new Error(`No response received within ${responseTimeout}ms`));
      }
    }, responseTimeout);
  });
}

module.exports = {
  ManagedProcess,
  execute,
  executeJsonRpc
};
