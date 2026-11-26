import { useCallback, useEffect, useState } from 'react';
import { ApiError, health } from './api';

export type ServerStatus = 'checking' | 'waking' | 'ready' | 'unavailable';

interface Options {
  /** How long a first check may take before the "waking up" message appears. */
  wakingAfterMs?: number;
  /** Delay between checks while the server is not answering. */
  retryEveryMs?: number;
  /** Give up and show "unavailable" after this long. */
  giveUpAfterMs?: number;
}

/**
 * Polls /health. A free-tier backend sleeps when idle and needs up to a minute
 * to start, so slow or failing checks move the status to "waking" instead of
 * showing an error.
 */
export function useServerStatus({
  wakingAfterMs = 2500,
  retryEveryMs = 3000,
  giveUpAfterMs = 120000,
}: Options = {}) {
  const [status, setStatus] = useState<ServerStatus>('checking');
  const [attempt, setAttempt] = useState(0);

  useEffect(() => {
    let cancelled = false;
    const controller = new AbortController();
    const started = Date.now();
    let retryTimer: ReturnType<typeof setTimeout> | undefined;

    const wakingTimer = setTimeout(() => {
      if (!cancelled) setStatus((current) => (current === 'checking' ? 'waking' : current));
    }, wakingAfterMs);

    const check = async () => {
      try {
        await health(controller.signal);
        if (!cancelled) {
          clearTimeout(wakingTimer);
          setStatus('ready');
        }
      } catch (error) {
        if (cancelled) return;
        if (error instanceof ApiError && error.kind === 'config') {
          clearTimeout(wakingTimer);
          setStatus('unavailable');
          return;
        }
        if (Date.now() - started >= giveUpAfterMs) {
          clearTimeout(wakingTimer);
          setStatus('unavailable');
          return;
        }
        setStatus('waking');
        retryTimer = setTimeout(check, retryEveryMs);
      }
    };
    void check();

    return () => {
      cancelled = true;
      controller.abort();
      clearTimeout(wakingTimer);
      clearTimeout(retryTimer);
    };
  }, [attempt, wakingAfterMs, retryEveryMs, giveUpAfterMs]);

  const retry = useCallback(() => {
    setStatus('checking');
    setAttempt((n) => n + 1);
  }, []);
  return { status, retry };
}
