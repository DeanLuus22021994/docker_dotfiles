# Dashboard Installation Guide

**Quick setup guide for the React/TypeScript dashboard application.**

## Prerequisites

- Node.js 22+ and npm
- Docker and Docker Compose (for backend services)
- Modern web browser

## Quick Start

### Windows

```cmd
cd dashboard
install.bat
start.bat
```

### PowerShell/Linux/macOS

```bash
cd dashboard
npm install
npm run dev
```

The dashboard will be available at: http://localhost:5173

## Configuration

The dashboard uses shared frontend configurations:

- **TypeScript**: Extends `../frontend/tsconfig.json`
- **Tailwind CSS**: Imports `../frontend/tailwind.config.js`
- **PostCSS**: Imports `../frontend/postcss.config.js`
- **ESLint**: Requires `../frontend/.eslintrc.cjs`

## Development Scripts

```bash
npm run dev      # Start development server (port 5173)
npm run build    # Build for production
npm run preview  # Preview production build
npm run lint     # Run ESLint
npm run format   # Format code with Prettier
```

## Production Build

```bash
# Build static files
npm run build

# Files are output to dashboard/dist/
# Serve with nginx or any static file server
```

## Docker Integration

The dashboard is containerized and served via:

- **Load Balancer**: http://localhost (nginx)
- **Direct Access**: http://localhost:5173 (development)
- **Container**: cluster-web1, cluster-web2, cluster-web3 (production)

## Architecture

For detailed architecture information, see:

- [Dashboard Overview](overview.md)
- [Component Architecture](architecture/overview.md)
- [Services Integration](architecture/services.md)

## Troubleshooting

**Build Errors**: Check `frontend/` configuration files exist
**Port Conflicts**: Change port in `vite.config.ts`
**Docker Issues**: See [Docker Troubleshooting](../troubleshooting/docker.md)
