#!/usr/bin/env node
/**
 * @fileoverview Console Logger with Colors
 * Enterprise-grade logging with level support and formatting.
 * @module utils/logger
 */

'use strict';

/**
 * ANSI color codes for terminal output.
 * @enum {string}
 */
const Colors = {
  RESET: '\x1b[0m',
  BOLD: '\x1b[1m',
  DIM: '\x1b[2m',

  // Foreground colors
  BLACK: '\x1b[30m',
  RED: '\x1b[31m',
  GREEN: '\x1b[32m',
  YELLOW: '\x1b[33m',
  BLUE: '\x1b[34m',
  MAGENTA: '\x1b[35m',
  CYAN: '\x1b[36m',
  WHITE: '\x1b[37m',
  GRAY: '\x1b[90m',

  // Background colors
  BG_RED: '\x1b[41m',
  BG_GREEN: '\x1b[42m',
  BG_YELLOW: '\x1b[43m',
  BG_BLUE: '\x1b[44m'
};

/**
 * Log levels.
 * @enum {number}
 */
const LogLevel = {
  DEBUG: 0,
  INFO: 1,
  WARN: 2,
  ERROR: 3,
  SILENT: 4
};

/**
 * Console logger with colors and levels.
 */
class Logger {
  /**
   * Creates a new Logger instance.
   * @param {string} [name=''] - Logger name/prefix
   * @param {number} [level=LogLevel.INFO] - Minimum log level
   * @throws {TypeError} If arguments have invalid types
   */
  constructor(name = '', level = LogLevel.INFO) {
    if (typeof name !== 'string') {
      throw new TypeError('name must be a string');
    }
    if (typeof level !== 'number') {
      throw new TypeError('level must be a number');
    }

    this.name = name;
    this.level = level;
  }

  /**
   * Sets log level.
   * @param {number} level - New log level
   * @throws {TypeError} If level is not a number
   */
  setLevel(level) {
    if (typeof level !== 'number') {
      throw new TypeError('level must be a number');
    }
    this.level = level;
  }

  /**
   * Formats message with timestamp and name.
   * @private
   * @param {string} message - Message to format
   * @returns {string} Formatted message
   */
  _format(message) {
    const timestamp = new Date().toISOString();
    const prefix = this.name ? `[${this.name}]` : '';
    return `${Colors.GRAY}${timestamp}${Colors.RESET} ${prefix} ${message}`;
  }

  /**
   * Logs debug message.
   * @param {string} message - Message to log
   * @example
   * logger.debug('Processing item 1 of 10');
   */
  debug(message) {
    if (this.level <= LogLevel.DEBUG) {
      console.log(this._format(`${Colors.GRAY}[DEBUG]${Colors.RESET} ${message}`));
    }
  }

  /**
   * Logs info message.
   * @param {string} message - Message to log
   * @example
   * logger.info('Server started on port 3000');
   */
  info(message) {
    if (this.level <= LogLevel.INFO) {
      console.log(this._format(`${Colors.CYAN}[INFO]${Colors.RESET} ${message}`));
    }
  }

  /**
   * Logs warning message.
   * @param {string} message - Message to log
   * @example
   * logger.warn('Configuration file not found, using defaults');
   */
  warn(message) {
    if (this.level <= LogLevel.WARN) {
      console.warn(this._format(`${Colors.YELLOW}[WARN]${Colors.RESET} ${message}`));
    }
  }

  /**
   * Logs error message.
   * @param {string} message - Message to log
   * @param {Error} [error] - Optional error object
   * @example
   * logger.error('Failed to connect', new Error('ECONNREFUSED'));
   */
  error(message, error = null) {
    if (this.level <= LogLevel.ERROR) {
      console.error(this._format(`${Colors.RED}[ERROR]${Colors.RESET} ${message}`));
      if (error && error.stack) {
        console.error(`${Colors.GRAY}${error.stack}${Colors.RESET}`);
      }
    }
  }

  /**
   * Logs success message (green).
   * @param {string} message - Message to log
   * @example
   * logger.success('All tests passed!');
   */
  success(message) {
    if (this.level <= LogLevel.INFO) {
      console.log(this._format(`${Colors.GREEN}✓${Colors.RESET} ${message}`));
    }
  }

  /**
   * Logs failure message (red).
   * @param {string} message - Message to log
   * @example
   * logger.fail('Deployment failed');
   */
  fail(message) {
    if (this.level <= LogLevel.ERROR) {
      console.error(this._format(`${Colors.RED}✗${Colors.RESET} ${message}`));
    }
  }

  /**
   * Prints a separator line.
   * @param {number} [length=70] - Line length
   * @param {string} [char='='] - Character to repeat
   * @example
   * logger.separator(80, '-');
   */
  separator(length = 70, char = '=') {
    if (this.level <= LogLevel.INFO) {
      console.log(`${Colors.CYAN}${char.repeat(length)}${Colors.RESET}`);
    }
  }

  /**
   * Prints a header with separators.
   * @param {string} title - Header title
   * @param {number} [length=70] - Line length
   * @example
   * logger.header('MCP Server Health Check');
   */
  header(title, length = 70) {
    if (this.level <= LogLevel.INFO) {
      console.log();
      this.separator(length);
      console.log(`${Colors.CYAN}${Colors.BOLD}${title}${Colors.RESET}`);
      this.separator(length);
      console.log();
    }
  }

  /**
   * Prints JSON object with pretty formatting.
   * @param {Object} obj - Object to print
   * @param {number} [indent=2] - Indentation spaces
   * @example
   * logger.json({ status: 'healthy', uptime: 3600 });
   */
  json(obj, indent = 2) {
    if (this.level <= LogLevel.INFO) {
      console.log(JSON.stringify(obj, null, indent));
    }
  }

  /**
   * Prints a blank line.
   */
  blank() {
    if (this.level <= LogLevel.INFO) {
      console.log();
    }
  }
}

/**
 * Creates a new logger instance.
 * @param {string} [name=''] - Logger name
 * @param {number} [level=LogLevel.INFO] - Log level
 * @returns {Logger} New logger instance
 * @example
 * const logger = createLogger('MyApp', LogLevel.DEBUG);
 * logger.info('Application started');
 */
function createLogger(name = '', level = LogLevel.INFO) {
  return new Logger(name, level);
}

module.exports = {
  Logger,
  createLogger,
  Colors,
  LogLevel
};
