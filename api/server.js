/**
 * Docker API Proxy Server
 * 
 * Provides a secure HTTP API for accessing Docker Engine metrics
 * and container health information for the dashboard.
 */

const express = require('express');
const Docker = require('dockerode');
const cors = require('cors');

const app = express();
const docker = new Docker({ socketPath: '/var/run/docker.sock' });

// Middleware
app.use(cors());
app.use(express.json());

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'healthy', timestamp: new Date().toISOString() });
});

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
app.get('/api/containers/:id/stats', async (req, res) => {
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
    console.error('Error fetching aggregate stats:', error);
    res.status(500).json({ error: error.message });
  }
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error('Unhandled error:', err);
  res.status(500).json({ error: 'Internal server error', message: err.message });
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, '0.0.0.0', () => {
  console.log(`Docker API Proxy listening on port ${PORT}`);
  console.log(`Health check: http://localhost:${PORT}/health`);
});
