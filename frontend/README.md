---
date_created: '2025-10-27T02:37:39Z'
last_updated: '2025-10-27T02:37:39Z'
tags: [web, frontend, vite, typescript, tailwind]
description: 'Frontend build and development configuration'
---

# Web Configuration

Frontend application build and development configuration.

## 📁 Files

### `vite.config.ts`
**Vite build tool configuration**.

Features:
- Hot module replacement (HMR)
- TypeScript support
- Build optimization
- Development server

---

### `tsconfig.json`
**TypeScript compiler configuration**.

Settings:
- Target: ES2020
- Module: ESNext
- Strict type checking
- Path aliases

---

### `tailwind.config.js`
**Tailwind CSS configuration**.

Features:
- Custom theme
- JIT mode
- Purge unused styles
- Custom plugins

---

### `postcss.config.js`
**PostCSS configuration**.

Plugins:
- Tailwind CSS
- Autoprefixer
- CSS nesting

---

### `.eslintrc.cjs`
**ESLint configuration**.

Rules:
- TypeScript linting
- React rules
- Code style enforcement

---

### `nginx.conf`
**Production NGINX configuration**.

Features:
- Static file serving
- Gzip compression
- Cache headers
- SPA routing (fallback to index.html)

---

## 🚀 Quick Start

### Development

```powershell
# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Production Build

```powershell
# Build and serve with NGINX
docker-compose build cluster-web1
docker-compose up -d cluster-web1
```

---

## 🎯 Best Practices

✅ **Code splitting** - Use dynamic imports  
✅ **Asset optimization** - Compress images, lazy load  
✅ **Type safety** - Enable strict TypeScript checks  
✅ **Linting** - Run ESLint before commits  
✅ **Testing** - Add unit and integration tests  

---

## 📚 References

- [Vite Documentation](https://vitejs.dev/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
