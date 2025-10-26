#!/usr/bin/env node
/**
 * MCP Server Health Check
 * Lightweight script to ping MCP servers and verify they're responding
 */

const { spawn } = require('child_process');
const fs = require('fs').promises;
const path = require('path');

class MCPHealthCheck {
  constructor(mcpConfigPath) {
    this.mcpConfigPath = mcpConfigPath;
    this.servers = {};
    this.results = {};
  }

  async loadConfig() {
    try {
      const configData = await fs.readFile(this.mcpConfigPath, 'utf-8');
      const config = JSON.parse(configData);
      this.servers = config.servers || {};
      return true;
    } catch (error) {
      console.error(`✗ Failed to load MCP config: ${error.message}`);
      return false;
    }
  }

  async checkServer(serverName, serverConfig, timeout = 5000) {
    return new Promise((resolve) => {
      const startTime = Date.now();
      const command = serverConfig.command;
      const args = serverConfig.args || [];

      // Resolve environment variables
      const resolvedArgs = args.map(arg => {
        if (typeof arg === 'string') {
          return arg.replace('${workspaceFolder}', process.cwd());
        }
        return arg;
      });

      const env = { ...process.env };
      if (serverConfig.env) {
        Object.entries(serverConfig.env).forEach(([key, value]) => {
          if (value.startsWith('${env:') && value.endsWith('}')) {
            const envVar = value.slice(6, -1);
            env[key] = process.env[envVar] || '';
          } else {
            env[key] = value;
          }
        });
      }

      const initRequest = {
        jsonrpc: '2.0',
        id: 1,
        method: 'initialize',
        params: {
          protocolVersion: '2024-11-05',
          capabilities: {},
          clientInfo: { name: 'mcp-health-check', version: '1.0.0' }
        }
      };

      const process_spawn = spawn(command, resolvedArgs, {
        env,
        stdio: ['pipe', 'pipe', 'pipe'],
        shell: true
      });

      let responded = false;
      let stdout = '';

      process_spawn.stdout.on('data', (data) => {
        stdout += data.toString();
        const lines = stdout.split('\n');

        lines.forEach(line => {
          if (!line.trim()) return;
          try {
            const response = JSON.parse(line);
            if (response.id === 1 && (response.result || response.error)) {
              responded = true;
              const duration = Date.now() - startTime;
              const status = response.result ? 'healthy' : 'error';
              resolve({
                server: serverName,
                status,
                duration,
                error: response.error?.message
              });
              process_spawn.kill();
            }
          } catch (e) {
            // Not valid JSON
          }
        });
      });

      process_spawn.on('error', (error) => {
        resolve({
          server: serverName,
          status: 'failed',
          duration: Date.now() - startTime,
          error: error.message
        });
      });

      process_spawn.on('close', (code) => {
        if (!responded) {
          resolve({
            server: serverName,
            status: code === 0 ? 'timeout' : 'failed',
            duration: Date.now() - startTime,
            error: `Process exited with code ${code}`
          });
        }
      });

      setTimeout(() => {
        process_spawn.stdin.write(JSON.stringify(initRequest) + '\n');
      }, 100);

      setTimeout(() => {
        if (!responded) {
          process_spawn.kill();
          resolve({
            server: serverName,
            status: 'timeout',
            duration: Date.now() - startTime,
            error: `No response after ${timeout}ms`
          });
        }
      }, timeout);
    });
  }

  async checkAll() {
    console.log('\n' + '='.repeat(70));
    console.log('MCP SERVER HEALTH CHECK');
    console.log('='.repeat(70) + '\n');

    const checks = Object.entries(this.servers).map(([name, config]) =>
      this.checkServer(name, config)
    );

    const results = await Promise.all(checks);

    results.forEach(result => {
      this.results[result.server] = result;
      const icon = result.status === 'healthy' ? '✓' : '✗';
      const color = result.status === 'healthy' ? '\x1b[32m' : '\x1b[31m';
      const reset = '\x1b[0m';

      console.log(`${color}${icon}${reset} ${result.server.padEnd(20)} ${result.status.padEnd(10)} (${result.duration}ms)`);
      if (result.error) {
        console.log(`  └─ ${result.error}`);
      }
    });

    const healthy = results.filter(r => r.status === 'healthy').length;
    const total = results.length;

    console.log('\n' + '='.repeat(70));
    console.log(`Health: ${healthy}/${total} servers responding`);
    console.log('='.repeat(70) + '\n');

    return { healthy, total, results: this.results };
  }

  async printJSON() {
    return JSON.stringify(this.results, null, 2);
  }
}

async function main() {
  const args = process.argv.slice(2);
  const jsonOutput = args.includes('--json');

  const workspaceRoot = path.join(__dirname, '..', '..', '..');
  const mcpConfig = path.join(workspaceRoot, '.vscode', 'mcp.json');

  const healthCheck = new MCPHealthCheck(mcpConfig);

  if (!await healthCheck.loadConfig()) {
    process.exit(1);
  }

  const result = await healthCheck.checkAll();

  if (jsonOutput) {
    console.log(await healthCheck.printJSON());
  }

  process.exit(result.healthy === result.total ? 0 : 1);
}

if (require.main === module) {
  main().catch(error => {
    console.error('Fatal error:', error);
    process.exit(1);
  });
}

module.exports = { MCPHealthCheck };
