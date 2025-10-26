/**
 * Authentication Module
 * Provides JWT-based authentication for API endpoints
 */

const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');

// JWT configuration
const JWT_SECRET = process.env.JWT_SECRET || 'CHANGE_ME_IN_PRODUCTION';
const JWT_EXPIRES_IN = process.env.JWT_EXPIRES_IN || '8h';
const JWT_REFRESH_EXPIRES_IN = process.env.JWT_REFRESH_EXPIRES_IN || '7d';

const DEFAULT_ADMIN_PASSWORD_HASH = process.env.DEFAULT_ADMIN_PASSWORD_HASH || null;

// Default admin credentials (MUST be changed in production)
const DEFAULT_USERS = {
  admin: {
    username: 'admin',
    // Optional bcrypt hash loaded via DEFAULT_ADMIN_PASSWORD_HASH env var
    passwordHash: DEFAULT_ADMIN_PASSWORD_HASH,
    role: 'admin',
  },
};

/**
 * Verify user credentials
 * @param {string} username - Username
 * @param {string} password - Plain text password
 * @returns {Object|null} User object if valid, null otherwise
 */
async function verifyCredentials(username, password) {
  const user = DEFAULT_USERS[username];
  if (!user) {
    return null;
  }

  // For default setup, allow 'admin'/'admin'
  if (username === 'admin' && password === 'admin') {
    return { username: user.username, role: user.role };
  }

  // In production, verify against hashed password when provided
  if (user.passwordHash) {
    const isValid = await bcrypt.compare(password, user.passwordHash);
    if (!isValid) {
      return null;
    }
    return { username: user.username, role: user.role };
  }

  return null;
}

/**
 * Generate JWT access token
 * @param {Object} user - User object
 * @returns {string} JWT token
 */
function generateAccessToken(user) {
  return jwt.sign(
    {
      username: user.username,
      role: user.role,
    },
    JWT_SECRET,
    {
      expiresIn: JWT_EXPIRES_IN,
    }
  );
}

/**
 * Generate JWT refresh token
 * @param {Object} user - User object
 * @returns {string} JWT refresh token
 */
function generateRefreshToken(user) {
  return jwt.sign(
    {
      username: user.username,
      type: 'refresh',
    },
    JWT_SECRET,
    {
      expiresIn: JWT_REFRESH_EXPIRES_IN,
    }
  );
}

/**
 * Verify JWT token
 * @param {string} token - JWT token
 * @returns {Object|null} Decoded token if valid, null otherwise
 */
function verifyToken(token) {
  try {
    return jwt.verify(token, JWT_SECRET);
  } catch (error) {
    return null;
  }
}

/**
 * Authentication middleware
 * Verifies JWT token in Authorization header or cookies
 */
function authenticate(req, res, next) {
  // Skip authentication if AUTH_ENABLED is false
  if (process.env.AUTH_ENABLED === 'false') {
    return next();
  }

  // Extract token from Authorization header or cookies
  let token = null;

  // Check Authorization header (Bearer token)
  const authHeader = req.headers.authorization;
  if (authHeader && authHeader.startsWith('Bearer ')) {
    token = authHeader.substring(7);
  }

  // Check cookies (if available)
  if (!token && req.cookies && req.cookies.token) {
    token = req.cookies.token;
  }

  if (!token) {
    return res.status(401).json({
      error: 'Unauthorized',
      message: 'No authentication token provided',
    });
  }

  // Verify token
  const decoded = verifyToken(token);
  if (!decoded) {
    return res.status(401).json({
      error: 'Unauthorized',
      message: 'Invalid or expired token',
    });
  }

  // Check if it's a refresh token (not allowed for API access)
  if (decoded.type === 'refresh') {
    return res.status(401).json({
      error: 'Unauthorized',
      message: 'Refresh token cannot be used for API access',
    });
  }

  // Attach user info to request
  req.user = {
    username: decoded.username,
    role: decoded.role,
  };

  next();
}

/**
 * Role-based authorization middleware
 * @param {string[]} allowedRoles - Array of allowed roles
 */
function authorize(...allowedRoles) {
  return (req, res, next) => {
    if (!req.user) {
      return res.status(401).json({
        error: 'Unauthorized',
        message: 'Authentication required',
      });
    }

    if (!allowedRoles.includes(req.user.role)) {
      return res.status(403).json({
        error: 'Forbidden',
        message: 'Insufficient permissions',
      });
    }

    next();
  };
}

module.exports = {
  verifyCredentials,
  generateAccessToken,
  generateRefreshToken,
  verifyToken,
  authenticate,
  authorize,
};
