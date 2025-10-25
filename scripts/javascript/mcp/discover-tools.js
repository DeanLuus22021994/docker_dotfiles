#!/usr/bin/env node
/**
 * MCP Tool Discovery Script
 * Queries all configured MCP servers to extract complete tool lists and detect overlaps.
 */

const { spawn } = require('child_process');
const fs = require('fs').promises;
const path = require('path');

class MCPToolDiscovery {
  constructor(mcpConfigPath) {
    this.mcpConfigPath = mcpConfigPath;
    this.servers = {};
    this.toolsByServer = {};
    this.allTools = [];
    this.toolOverlaps = {};
  }

  async loadConfig() {
    try {
      const configData = await fs.readFile(this.mcpConfigPath, 'utf-8');
      const config = JSON.parse(configData);
      this.servers = config.servers || {};
      console.log(`\n✓ Loaded ${Object.keys(this.servers).length} servers from config\n`);
      return true;
    } catch (error) {
      console.error(`✗ Failed to load MCP config: ${error.message}`);
      return false;
    }
  }

  async queryServerTools(serverName, serverConfig) {
    console.log(`\n📡 Querying server: ${serverName}`);
    console.log(`   Command: ${serverConfig.command} ${serverConfig.args?.join(' ') || ''}`);

    return new Promise((resolve) => {
      const tools = [];
      const command = serverConfig.command;
      const args = serverConfig.args || [];
      
      // Resolve environment variables in args
      const resolvedArgs = args.map(arg => {
        if (typeof arg === 'string') {
          // Replace ${workspaceFolder} with actual path
          return arg.replace('${workspaceFolder}', process.cwd());
        }
        return arg;
      });

      // Prepare environment
      const env = { ...process.env };
      if (serverConfig.env) {
        Object.entries(serverConfig.env).forEach(([key, value]) => {
          // Resolve ${env:VAR_NAME} references
          if (value.startsWith('${env:') && value.endsWith('}')) {
            const envVar = value.slice(6, -1);
            env[key] = process.env[envVar] || '';
          } else {
            env[key] = value;
          }
        });
      }

      // Build MCP initialize request
      const initRequest = {
        jsonrpc: '2.0',
        id: 1,
        method: 'initialize',
        params: {
          protocolVersion: '2024-11-05',
          capabilities: {
            roots: { listChanged: true },
            sampling: {}
          },
          clientInfo: {
            name: 'mcp-tool-discovery',
            version: '1.0.0'
          }
        }
      };

      // Build MCP tools/list request
      const toolsRequest = {
        jsonrpc: '2.0',
        id: 2,
        method: 'tools/list',
        params: {}
      };

      const process_spawn = spawn(command, resolvedArgs, {
        env,
        stdio: ['pipe', 'pipe', 'pipe'],
        shell: true  // Use shell to resolve npx properly on Windows
      });

      let stdout = '';
      let stderr = '';
      let responseCount = 0;

      process_spawn.stdout.on('data', (data) => {
        stdout += data.toString();
        
        // Try to parse each line as JSON-RPC response
        const lines = stdout.split('\n');
        stdout = lines.pop(); // Keep incomplete line in buffer

        lines.forEach(line => {
          if (!line.trim()) return;
          
          try {
            const response = JSON.parse(line);
            
            // Handle initialize response
            if (response.id === 1 && response.result) {
              responseCount++;
              console.log(`   ✓ Server initialized`);
              // Server initialized, now request tools
              process_spawn.stdin.write(JSON.stringify(toolsRequest) + '\n');
            }
            
            // Handle tools/list response
            if (response.id === 2 && response.result) {
              responseCount++;
              const serverTools = response.result.tools || [];
              tools.push(...serverTools);
              console.log(`   ✓ Found ${serverTools.length} tools`);
              process_spawn.kill();
            }

            // Handle errors
            if (response.error) {
              console.error(`   ✗ Error: ${response.error.message}`);
              process_spawn.kill();
            }
          } catch (e) {
            // Not valid JSON, continue
          }
        });
      });

      process_spawn.stderr.on('data', (data) => {
        stderr += data.toString();
      });

      process_spawn.on('error', (error) => {
        console.error(`   ✗ Failed to start: ${error.message}`);
        resolve(tools);
      });

      process_spawn.on('close', (code) => {
        if (stderr && !stderr.includes('WARNING')) {
          console.error(`   ⚠ Stderr: ${stderr.slice(0, 200)}`);
        }
        if (tools.length === 0 && responseCount === 0) {
          console.log(`   ⚠ No tools retrieved (exit code: ${code})`);
        }
        resolve(tools);
      });

      // Send initialize request
      setTimeout(() => {
        process_spawn.stdin.write(JSON.stringify(initRequest) + '\n');
      }, 100);

      // Timeout after 15 seconds
      setTimeout(() => {
        if (responseCount < 2) {
          console.log(`   ⚠ Timeout after 15s (got ${responseCount}/2 responses)`);
          process_spawn.kill();
          resolve(tools);
        }
      }, 15000);
    });
  }

  async discoverAllTools() {
    console.log('\n' + '='.repeat(80));
    console.log('MCP TOOL DISCOVERY');
    console.log('='.repeat(80));

    for (const [serverName, serverConfig] of Object.entries(this.servers)) {
      const tools = await this.queryServerTools(serverName, serverConfig);
      this.toolsByServer[serverName] = tools;
      
      tools.forEach(tool => {
        this.allTools.push({
          ...tool,
          server: serverName
        });
      });
    }
  }

  analyzeOverlaps() {
    const toolNames = {};

    Object.entries(this.toolsByServer).forEach(([serverName, tools]) => {
      tools.forEach(tool => {
        const toolName = tool.name;
        if (!toolNames[toolName]) {
          toolNames[toolName] = [];
        }
        toolNames[toolName].push(serverName);
      });
    });

    // Identify overlaps
    Object.entries(toolNames).forEach(([toolName, servers]) => {
      if (servers.length > 1) {
        this.toolOverlaps[toolName] = servers;
      }
    });
  }

  async generateReport(outputPath) {
    const report = {
      metadata: {
        timestamp: new Date().toISOString(),
        total_servers: Object.keys(this.servers).length,
        total_tools: this.allTools.length,
        total_overlaps: Object.keys(this.toolOverlaps).length
      },
      servers: {},
      overlaps: this.toolOverlaps,
      all_tools: []
    };

    // Group tools by server with detailed info
    Object.entries(this.toolsByServer).forEach(([serverName, tools]) => {
      const serverInfo = this.servers[serverName];
      report.servers[serverName] = {
        command: serverInfo.command,
        args: serverInfo.args,
        runtime: serverInfo.command,
        tool_count: tools.length,
        tools: tools.map(tool => ({
          name: tool.name,
          description: tool.description,
          inputSchema: tool.inputSchema || {}
        }))
      };
    });

    // Flat list of all tools with server attribution
    report.all_tools = this.allTools.map(tool => ({
      name: tool.name,
      server: tool.server,
      description: tool.description
    }));

    await fs.writeFile(outputPath, JSON.stringify(report, null, 2));
    console.log(`\n✓ Report saved to: ${outputPath}`);
  }

  printSummary() {
    console.log('\n' + '='.repeat(80));
    console.log('MCP TOOL DISCOVERY SUMMARY');
    console.log('='.repeat(80) + '\n');

    console.log(`Total Servers: ${Object.keys(this.servers).length}`);
    console.log(`Total Tools: ${this.allTools.length}\n`);

    console.log('Tools by Server:');
    const sortedServers = Object.entries(this.toolsByServer)
      .sort((a, b) => b[1].length - a[1].length);

    sortedServers.forEach(([serverName, tools]) => {
      console.log(`  ${serverName.padEnd(30, '.')} ${tools.length.toString().padStart(4)} tools`);
    });

    if (Object.keys(this.toolOverlaps).length > 0) {
      console.log(`\n⚠ Tool Name Overlaps:`);
      console.log(`  ${Object.keys(this.toolOverlaps).length} tools exist in multiple servers:\n`);
      Object.entries(this.toolOverlaps).forEach(([toolName, servers]) => {
        console.log(`  '${toolName}'`);
        console.log(`    → Servers: ${servers.join(', ')}`);
      });
    } else {
      console.log('\n✓ No tool name overlaps detected');
    }

    console.log('\n' + '='.repeat(80) + '\n');
  }
}

async function main() {
  const workspaceRoot = path.join(__dirname, '..', '..', '..');
  const mcpConfig = path.join(workspaceRoot, '.vscode', 'mcp.json');
  const outputFile = path.join(workspaceRoot, '.vscode', 'configs', 'mcp', 'documentation', 'tools_report.json');

  const discovery = new MCPToolDiscovery(mcpConfig);

  if (!await discovery.loadConfig()) {
    process.exit(1);
  }

  await discovery.discoverAllTools();
  discovery.analyzeOverlaps();
  await discovery.generateReport(outputFile);
  discovery.printSummary();

  console.log('✓ Tool discovery complete!');
}

main().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});
