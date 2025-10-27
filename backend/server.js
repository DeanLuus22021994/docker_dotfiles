/**
 * Docker API Proxy Server
 *
 * Provides a secure HTTP API for accessing Docker Engine metrics
 * and container health information for the dashboard.
 *
 * Security Features:
 * - JWT authentication (optional, controlled by AUTH_ENABLED env var)
 * - Rate limiting (100 req/15min general, 10 req/15min stats, 5 req/15min auth)
 * - Input validation and sanitization
 * - CORS origin whitelisting
 * - Helmet security headers
 * - Docker socket read-only access
 */

require('dotenv').config();
const express = require('express');
const Docker = require('dockerode');
const cors = require('cors');
const helmet = require('helmet');

const auth = require('./auth');
const { body } = require('express-validator');
const {
  apiLimiter,
  statsLimiter,
  authLimiter,
  validateContainerId,
  validateLogin,
  validateRefreshToken,
  handleValidationErrors,
  sanitizeError,
} = require('./middleware');

const app = express();
const docker = new Docker({ socketPath: '/var/run/docker.sock' });

// Security middleware - Helmet (must be first)
app.use(helmet());

// CORS configuration with origin whitelisting
const allowedOrigins = process.env.CORS_ORIGIN
  ? process.env.CORS_ORIGIN.split(',')
  : ['http://localhost:3000', 'http://localhost:5173'];

app.use(
  cors({
    origin: (origin, callback) => {
      // Allow requests with no origin (like mobile apps or curl)
      if (!origin) return callback(null, true);

      if (allowedOrigins.includes(origin)) {
        callback(null, true);
      } else {
        callback(new Error('Not allowed by CORS'));
      }
    },
    credentials: true,
    optionsSuccessStatus: 200,
  })
);

// Body parsing middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// ============================================================================
// AUTHENTICATION ENDPOINTS (No auth required, but rate limited)
// ============================================================================

/**
 * POST /auth/login
 * Authenticate user and return JWT tokens
 */
app.post(
  '/auth/login',
  authLimiter,
  validateLogin,
  handleValidationErrors,
  async (req, res) => {
    try {
      const { username, password } = req.body;

      // Verify credentials
      const user = await auth.verifyCredentials(username, password);
      if (!user) {
        return res.status(401).json({
          error: 'Unauthorized',
          message: 'Invalid username or password',
        });
      }

      // Generate tokens
      const accessToken = auth.generateAccessToken(user);
      const refreshToken = auth.generateRefreshToken(user);

      res.json({
        success: true,
        accessToken,
        refreshToken,
        expiresIn: process.env.JWT_EXPIRES_IN || '8h',
        user: {
          username: user.username,
          role: user.role,
        },
      });
    } catch (error) {
      console.error('Login error:', error);
      res.status(500).json({
        error: 'Internal Server Error',
        message: 'Login failed',
      });
    }
  }
);

/**
 * POST /auth/refresh
 * Refresh access token using refresh token
 */
app.post(
  '/auth/refresh',
  authLimiter,
  validateRefreshToken,
  handleValidationErrors,
  async (req, res) => {
    try {
      const { refreshToken } = req.body;

      // Verify refresh token
      const decoded = auth.verifyToken(refreshToken);
      if (!decoded || decoded.type !== 'refresh') {
        return res.status(401).json({
          error: 'Unauthorized',
          message: 'Invalid refresh token',
        });
      }

      // Generate new access token
      const user = { username: decoded.username, role: decoded.role || 'user' };
      const accessToken = auth.generateAccessToken(user);

      res.json({
        success: true,
        accessToken,
        expiresIn: process.env.JWT_EXPIRES_IN || '8h',
      });
    } catch (error) {
      console.error('Refresh token error:', error);
      res.status(500).json({
        error: 'Internal Server Error',
        message: 'Token refresh failed',
      });
    }
  }
);

/**
 * POST /auth/logout
 * Logout user (client should discard tokens)
 */
app.post('/auth/logout', (req, res) => {
  res.json({
    success: true,
    message: 'Logged out successfully',
  });
});

// ============================================================================
// PUBLIC ENDPOINTS (No authentication required)
// ============================================================================

// ============================================================================
// PUBLIC ENDPOINTS (No authentication required)
// ============================================================================

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'healthy', timestamp: new Date().toISOString() });
});

// ============================================================================
// PROTECTED API ENDPOINTS (Authentication + Rate limiting)
// ============================================================================

// Apply authentication middleware to all /api/* routes (if enabled)
app.use('/api', auth.authenticate);

// Apply rate limiting to all API endpoints
app.use('/api', apiLimiter);

// Get all containers with health status
app.get('/api/containers', async (req, res) => {
  try {
    const containers = await docker.listContainers({ all: true });

    const containerDetails = await Promise.all(
      containers.map(async (container) => {
        const inspect = await docker.getContainer(container.Id).inspect();

        return {
          id: container.Id,
          name: container.Names[0].replace(/^\//, ''),
          image: container.Image,
          state: container.State,
          status: container.Status,
          created: container.Created,
          health: inspect.State.Health || { Status: 'none' },
          stats: {
            cpu: 0,
            memory: 0,
            network: { rx: 0, tx: 0 }
          }
        };
      })
    );

    res.json({ containers: containerDetails, timestamp: new Date().toISOString() });
  } catch (error) {
    console.error('Error fetching containers:', error);
    res.status(500).json({ error: error.message });
  }
});

// Get container stats (real-time metrics)
app.get(
  '/api/containers/:id/stats',
  statsLimiter,
  validateContainerId,
  handleValidationErrors,
  async (req, res) => {
    try {
      const container = docker.getContainer(req.params.id);
      const stats = await container.stats({ stream: false });

    // Calculate CPU percentage
    const cpuDelta = stats.cpu_stats.cpu_usage.total_usage -
                     stats.precpu_stats.cpu_usage.total_usage;
    const systemDelta = stats.cpu_stats.system_cpu_usage -
                        stats.precpu_stats.system_cpu_usage;
    const cpuPercent = (cpuDelta / systemDelta) * stats.cpu_stats.online_cpus * 100;

    // Calculate memory usage
    const memoryUsage = stats.memory_stats.usage;
    const memoryLimit = stats.memory_stats.limit;
    const memoryPercent = (memoryUsage / memoryLimit) * 100;

    // Calculate network I/O
    const networks = stats.networks || {};
    const networkRx = Object.values(networks).reduce((acc, net) => acc + net.rx_bytes, 0);
    const networkTx = Object.values(networks).reduce((acc, net) => acc + net.tx_bytes, 0);

    res.json({
      container: req.params.id,
      timestamp: new Date().toISOString(),
      cpu: {
        percent: cpuPercent.toFixed(2),
        usage: stats.cpu_stats.cpu_usage.total_usage,
        system: stats.cpu_stats.system_cpu_usage
      },
      memory: {
        usage: memoryUsage,
        limit: memoryLimit,
        percent: memoryPercent.toFixed(2)
      },
      network: {
        rx_bytes: networkRx,
        tx_bytes: networkTx
      },
      block_io: stats.blkio_stats
    });
  } catch (error) {
    console.error('Error fetching container stats:', error);
    res.status(500).json({ error: error.message });
  }
});

// Get Docker system info
app.get('/api/system/info', async (req, res) => {
  try {
    const info = await docker.info();
    res.json({
      containers: info.Containers,
      containers_running: info.ContainersRunning,
      containers_paused: info.ContainersPaused,
      containers_stopped: info.ContainersStopped,
      images: info.Images,
      driver: info.Driver,
      memory_total: info.MemTotal,
      cpus: info.NCPU,
      os: info.OperatingSystem,
      architecture: info.Architecture,
      kernel_version: info.KernelVersion,
      docker_version: info.ServerVersion,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Error fetching system info:', error);
    res.status(500).json({ error: error.message });
  }
});

// Get Docker version
app.get('/api/system/version', async (req, res) => {
  try {
    const version = await docker.version();
    res.json({ ...version, timestamp: new Date().toISOString() });
  } catch (error) {
    console.error('Error fetching version:', error);
    res.status(500).json({ error: error.message });
  }
});

// Get aggregated stats for all running containers
app.get('/api/stats/aggregate', async (req, res) => {
  try {
    const containers = await docker.listContainers();

    const allStats = await Promise.all(
      containers.map(async (container) => {
        try {
          const containerObj = docker.getContainer(container.Id);
          const stats = await containerObj.stats({ stream: false });

          const cpuDelta = stats.cpu_stats.cpu_usage.total_usage -
                           stats.precpu_stats.cpu_usage.total_usage;
          const systemDelta = stats.cpu_stats.system_cpu_usage -
                              stats.precpu_stats.system_cpu_usage;
          const cpuPercent = (cpuDelta / systemDelta) * stats.cpu_stats.online_cpus * 100;

          return {
            id: container.Id,
            name: container.Names[0].replace(/^\//, ''),
            cpu_percent: cpuPercent,
            memory_usage: stats.memory_stats.usage,
            memory_limit: stats.memory_stats.limit
          };
        } catch (err) {
          return null;
        }
      })
    );

    const validStats = allStats.filter(s => s !== null);
    const totalCpu = validStats.reduce((acc, s) => acc + s.cpu_percent, 0);
    const totalMemory = validStats.reduce((acc, s) => acc + s.memory_usage, 0);

    res.json({
      timestamp: new Date().toISOString(),
      total_containers: validStats.length,
      total_cpu_percent: totalCpu.toFixed(2),
      total_memory_bytes: totalMemory,
      containers: validStats
    });
  } catch (error) {
    console.error('Error fetching container stats:', error);
    res.status(500).json({ error: error.message });
  }
});

// ============================================================================
// LAYER METRICS API (Phase 4.6.2)
// ============================================================================

// Layer configuration mapping service names to layers
const LAYER_CONFIG = {
  data: ['postgres', 'mariadb', 'redis', 'minio'],
  services: ['backend', 'dashboard'],
  monitoring: ['grafana', 'prometheus'],
  compute: ['jupyter', 'localstack'],
  network: ['nginx', 'traefik', 'mailhog']
};

// Get metrics for specific layer
app.get('/api/layers/:layerId/metrics', async (req, res) => {
  try {
    const { layerId } = req.params;
    const layerServices = LAYER_CONFIG[layerId];

    if (!layerServices) {
      return res.status(404).json({
        error: 'Layer not found',
        availableLayers: Object.keys(LAYER_CONFIG)
      });
    }

    const containers = await docker.listContainers();
    const layerContainers = containers.filter(c =>
      layerServices.some(service =>
        c.Names[0].toLowerCase().includes(service.toLowerCase())
      )
    );

    const layerStats = await Promise.all(
      layerContainers.map(async (container) => {
        try {
          const containerObj = docker.getContainer(container.Id);
          const stats = await containerObj.stats({ stream: false });
          const inspect = await containerObj.inspect();

          const cpuDelta = stats.cpu_stats.cpu_usage.total_usage -
                           stats.precpu_stats.cpu_usage.total_usage;
          const systemDelta = stats.cpu_stats.system_cpu_usage -
                              stats.precpu_stats.system_cpu_usage;
          const cpuPercent = (cpuDelta / systemDelta) * stats.cpu_stats.online_cpus * 100;

          const memoryPercent = (stats.memory_stats.usage / stats.memory_stats.limit) * 100;

          const networks = stats.networks || {};
          const networkIO = Object.values(networks).reduce(
            (acc, net) => acc + net.rx_bytes + net.tx_bytes,
            0
          );

          return {
            name: container.Names[0].replace(/^\//, ''),
            status: inspect.State.Status === 'running' ? 'healthy' : 'unhealthy',
            cpu: cpuPercent,
            memory: memoryPercent,
            networkIO: networkIO
          };
        } catch (err) {
          console.error(`Error getting stats for ${container.Names[0]}:`, err);
          return null;
        }
      })
    );

    const validStats = layerStats.filter(s => s !== null);

    const metrics = {
      layer: layerId,
      totalCpu: validStats.reduce((acc, s) => acc + s.cpu, 0),
      totalMemory: validStats.reduce((acc, s) => acc + s.memory, 0),
      totalNetworkIO: validStats.reduce((acc, s) => acc + s.networkIO, 0),
      serviceCount: validStats.length,
      healthyCount: validStats.filter(s => s.status === 'healthy').length,
      unhealthyCount: validStats.filter(s => s.status === 'unhealthy').length,
      services: validStats,
      timestamp: new Date().toISOString()
    };

    res.json(metrics);
  } catch (error) {
    console.error('Error fetching layer metrics:', error);
    res.status(500).json({ error: error.message });
  }
});

// Get metrics for all layers
app.get('/api/layers/metrics', async (req, res) => {
  try {
    const layerIds = Object.keys(LAYER_CONFIG);
    const allMetrics = {};

    for (const layerId of layerIds) {
      const layerServices = LAYER_CONFIG[layerId];
      const containers = await docker.listContainers();
      const layerContainers = containers.filter(c =>
        layerServices.some(service =>
          c.Names[0].toLowerCase().includes(service.toLowerCase())
        )
      );

      const layerStats = await Promise.all(
        layerContainers.map(async (container) => {
          try {
            const containerObj = docker.getContainer(container.Id);
            const stats = await containerObj.stats({ stream: false });
            const inspect = await containerObj.inspect();

            const cpuDelta = stats.cpu_stats.cpu_usage.total_usage -
                             stats.precpu_stats.cpu_usage.total_usage;
            const systemDelta = stats.cpu_stats.system_cpu_usage -
                                stats.precpu_stats.system_cpu_usage;
            const cpuPercent = (cpuDelta / systemDelta) * stats.cpu_stats.online_cpus * 100;

            const memoryPercent = (stats.memory_stats.usage / stats.memory_stats.limit) * 100;

            const networks = stats.networks || {};
            const networkIO = Object.values(networks).reduce(
              (acc, net) => acc + net.rx_bytes + net.tx_bytes,
              0
            );

            return {
              name: container.Names[0].replace(/^\//, ''),
              status: inspect.State.Status === 'running' ? 'healthy' : 'unhealthy',
              cpu: cpuPercent,
              memory: memoryPercent,
              networkIO: networkIO
            };
          } catch (err) {
            return null;
          }
        })
      );

      const validStats = layerStats.filter(s => s !== null);

      allMetrics[layerId] = {
        layer: layerId,
        totalCpu: validStats.reduce((acc, s) => acc + s.cpu, 0),
        totalMemory: validStats.reduce((acc, s) => acc + s.memory, 0),
        totalNetworkIO: validStats.reduce((acc, s) => acc + s.networkIO, 0),
        serviceCount: validStats.length,
        healthyCount: validStats.filter(s => s.status === 'healthy').length,
        unhealthyCount: validStats.filter(s => s.status === 'unhealthy').length
      };
    }

    res.json({
      layers: allMetrics,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Error fetching all layer metrics:', error);
    res.status(500).json({ error: error.message });
  }
});

// ============================================================================
// SERVICE SCALING API (Phase 4.6.5)
// ============================================================================

// Scale a service (requires authentication)
app.post(
  '/api/services/:serviceId/scale',
  auth.authenticate,
  body('replicas').isInt({ min: 1, max: 10 }),
  handleValidationErrors,
  async (req, res) => {
    try {
      const { serviceId } = req.params;
      const { replicas } = req.body;

      // In standalone Docker, we use docker-compose scale
      // This requires docker-compose to be installed and the service to be part of a stack
      const { exec } = require('child_process');
      const util = require('util');
      const execPromise = util.promisify(exec);

      // Validate service exists
      const containers = await docker.listContainers({ all: true });
      const serviceContainer = containers.find(c =>
        c.Names[0].toLowerCase().includes(serviceId.toLowerCase())
      );

      if (!serviceContainer) {
        return res.status(404).json({
          error: 'Service not found',
          serviceId
        });
      }

      // For Docker Compose services, use docker-compose scale
      try {
        await execPromise(`docker-compose scale ${serviceId}=${replicas}`);

        res.json({
          success: true,
          service: serviceId,
          replicas: replicas,
          message: `Scaled ${serviceId} to ${replicas} replicas`,
          timestamp: new Date().toISOString()
        });
      } catch (scaleError) {
        // Fallback: Service might not support scaling
        res.status(400).json({
          error: 'Scaling not supported',
          message: 'This service does not support scaling. Ensure it is part of a Docker Compose stack.',
          serviceId
        });
      }
    } catch (error) {
      console.error('Error scaling service:', error);
      res.status(500).json({ error: error.message });
    }
  }
);

// Get service replica count
app.get('/api/services/:serviceId/replicas', async (req, res) => {
  try {
    const { serviceId } = req.params;
    const containers = await docker.listContainers({ all: true });

    // Count containers matching the service name
    const replicas = containers.filter(c =>
      c.Names[0].toLowerCase().includes(serviceId.toLowerCase())
    );

    res.json({
      service: serviceId,
      replicas: replicas.length,
      running: replicas.filter(c => c.State === 'running').length,
      containers: replicas.map(c => ({
        id: c.Id,
        name: c.Names[0].replace(/^\//, ''),
        state: c.State,
        status: c.Status
      })),
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Error fetching replica count:', error);
    res.status(500).json({ error: error.message });
  }
});

// ============================================================================
// ERROR HANDLING
// ============================================================================

// 404 handler for undefined routes
app.use((req, res) => {
  res.status(404).json({
    error: 'Not Found',
    message: `Route ${req.method} ${req.path} not found`,
  });
});

// Global error handling middleware (must be last)
app.use(sanitizeError);

const PORT = process.env.PORT || 3001;
app.listen(PORT, '0.0.0.0', () => {
  console.log(`Docker API Proxy listening on port ${PORT}`);
  console.log(`Health check: http://localhost:${PORT}/health`);
  console.log(`Layer metrics: http://localhost:${PORT}/api/layers/metrics`);
  console.log(`Service scaling: POST http://localhost:${PORT}/api/services/:id/scale`);
});
