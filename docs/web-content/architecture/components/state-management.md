---
date_created: "2025-10-26T18:32:25.962425+00:00"
last_updated: "2025-10-26T18:32:25.962425+00:00"
tags: ['documentation', 'web-content', 'architecture']
description: "Documentation for state management"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:
- web-content
- architecture
- javascript
description: State management strategy using React hooks
---\n# State Management

## Custom Hooks

**`useClusterHealth.ts`**
- Fetches and manages cluster health data
- Provides health score and status
- Auto-refresh every 30 seconds

**`useClusterMetrics.ts`**
- Aggregates cluster-wide metrics
- Provides CPU, memory, network stats
- Real-time updates

**`useDockerStats.ts`**
- Fetches container statistics
- Manages polling interval
- Handles loading and error states

## Hook Pattern

```typescript
export const useClusterHealth = () => {
  const [health, setHealth] = useState<ClusterHealth | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    // Fetch data
    // Set state
    // Handle errors
  }, []);

  return { health, loading, error };
};
```

## State Management Principles

1. **Local State** - Component-specific state with useState
2. **Derived State** - Computed from props or other state
3. **Shared State** - Via custom hooks, not global store
4. **Async State** - Loading, error, data pattern

**No Redux** - React hooks sufficient for current complexity.
