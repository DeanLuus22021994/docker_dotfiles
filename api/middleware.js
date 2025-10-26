/**
 * Middleware Module
 * Provides rate limiting, validation, and security middleware
 */

const rateLimit = require('express-rate-limit');
const { body, param, validationResult } = require('express-validator');

/**
 * Rate limiter for general API endpoints
 * 100 requests per 15 minutes
 */
const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // 100 requests per window
  message: {
    error: 'Too Many Requests',
    message: 'Too many requests from this IP, please try again later.',
    retryAfter: '15 minutes',
  },
  standardHeaders: true, // Return rate limit info in `RateLimit-*` headers
  legacyHeaders: false, // Disable `X-RateLimit-*` headers
  handler: (req, res) => {
    res.status(429).json({
      error: 'Too Many Requests',
      message: 'Rate limit exceeded. Please try again later.',
      retryAfter: Math.ceil(req.rateLimit.resetTime / 1000),
    });
  },
});

/**
 * Stricter rate limiter for resource-intensive endpoints (stats)
 * 10 requests per 15 minutes
 */
const statsLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 10, // 10 requests per window
  message: {
    error: 'Too Many Requests',
    message: 'Too many stats requests from this IP, please try again later.',
    retryAfter: '15 minutes',
  },
  standardHeaders: true,
  legacyHeaders: false,
  handler: (req, res) => {
    res.status(429).json({
      error: 'Too Many Requests',
      message: 'Stats rate limit exceeded. Please try again later.',
      retryAfter: Math.ceil(req.rateLimit.resetTime / 1000),
    });
  },
});

/**
 * Rate limiter for authentication endpoints
 * 5 requests per 15 minutes (prevent brute force)
 */
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // 5 attempts per window
  message: {
    error: 'Too Many Requests',
    message: 'Too many login attempts, please try again later.',
    retryAfter: '15 minutes',
  },
  standardHeaders: true,
  legacyHeaders: false,
  skipSuccessfulRequests: true, // Don't count successful logins
  handler: (req, res) => {
    res.status(429).json({
      error: 'Too Many Requests',
      message: 'Too many login attempts. Please try again later.',
      retryAfter: Math.ceil(req.rateLimit.resetTime / 1000),
    });
  },
});

/**
 * Validation rules for container ID
 * Docker container IDs are 12-64 character hexadecimal strings
 */
const validateContainerId = [
  param('id')
    .matches(/^[a-f0-9]{12,64}$/)
    .withMessage('Invalid container ID format. Must be 12-64 character hex string.'),
];

/**
 * Validation rules for login request
 */
const validateLogin = [
  body('username')
    .trim()
    .isLength({ min: 3, max: 50 })
    .withMessage('Username must be between 3 and 50 characters')
    .matches(/^[a-zA-Z0-9_-]+$/)
    .withMessage('Username can only contain alphanumeric characters, underscores, and hyphens'),
  body('password')
    .isLength({ min: 4 })
    .withMessage('Password must be at least 4 characters'),
];

/**
 * Validation rules for refresh token request
 */
const validateRefreshToken = [
  body('refreshToken')
    .notEmpty()
    .withMessage('Refresh token is required')
    .isJWT()
    .withMessage('Invalid refresh token format'),
];

/**
 * Validation error handler middleware
 * Checks for validation errors and returns 400 if any found
 */
function handleValidationErrors(req, res, next) {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({
      error: 'Validation Error',
      message: 'Invalid request data',
      details: errors.array().map((err) => ({
        field: err.path,
        message: err.msg,
        value: err.value,
      })),
    });
  }
  next();
}

/**
 * Sanitize error messages for production
 * Removes stack traces and sensitive information
 */
function sanitizeError(err, req, res, next) {
  const isProduction = process.env.NODE_ENV === 'production';

  // Log full error for debugging
  console.error('Error occurred:', {
    message: err.message,
    stack: err.stack,
    path: req.path,
    method: req.method,
  });

  // Send sanitized error to client
  const statusCode = err.statusCode || 500;
  const response = {
    error: err.name || 'Internal Server Error',
    message: isProduction ? 'An error occurred' : err.message,
  };

  // Include stack trace only in development
  if (!isProduction && err.stack) {
    response.stack = err.stack;
  }

  res.status(statusCode).json(response);
}

module.exports = {
  apiLimiter,
  statsLimiter,
  authLimiter,
  validateContainerId,
  validateLogin,
  validateRefreshToken,
  handleValidationErrors,
  sanitizeError,
};
