export type Language = 'auto' | 'en' | 'hi' | 'mr';
export type AnswerLanguage = Exclude<Language, 'auto'>;

export interface Source {
  id: string;
  document: string;
  section: string;
  text: string;
}

export interface ChatResponse {
  answer: string;
  status: 'answered' | 'not_found' | 'refused';
  language: AnswerLanguage;
  confidence: number;
  sources: Source[];
  reason?: string | null;
}

export type ApiErrorKind = 'config' | 'network' | 'timeout' | 'rate_limit' | 'invalid' | 'server';

export class ApiError extends Error {
  readonly kind: ApiErrorKind;

  constructor(kind: ApiErrorKind, message: string) {
    super(message);
    this.name = 'ApiError';
    this.kind = kind;
  }
}

/** The backend URL, from VITE_API_URL, without a trailing slash. */
export function apiBase(): string {
  const url = (import.meta.env.VITE_API_URL as string | undefined)?.trim();
  if (!url) {
    throw new ApiError('config', 'The backend address is not configured (VITE_API_URL).');
  }
  return url.replace(/\/+$/, '');
}

async function request<T>(path: string, init: RequestInit = {}, timeoutMs = 20000): Promise<T> {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  const outer = init.signal;
  outer?.addEventListener('abort', () => controller.abort());
  try {
    const response = await fetch(`${apiBase()}${path}`, { ...init, signal: controller.signal });
    if (response.status === 429) {
      throw new ApiError('rate_limit', 'Too many requests.');
    }
    if (response.status === 422) {
      const body = (await response.json().catch(() => ({}))) as { detail?: unknown };
      throw new ApiError('invalid', typeof body.detail === 'string' ? body.detail : 'Invalid request.');
    }
    if (!response.ok) {
      throw new ApiError('server', `The server answered with status ${response.status}.`);
    }
    return (await response.json()) as T;
  } catch (error) {
    if (error instanceof ApiError) throw error;
    if (outer?.aborted) throw error;
    if (controller.signal.aborted) throw new ApiError('timeout', 'The server took too long to answer.');
    throw new ApiError('network', 'Could not reach the server.');
  } finally {
    clearTimeout(timer);
  }
}

export function health(signal?: AbortSignal, timeoutMs = 8000): Promise<{ status: string }> {
  return request('/health', { signal }, timeoutMs);
}

export function suggestions(language: Language, signal?: AbortSignal): Promise<string[]> {
  return request(`/suggestions?lang=${language}`, { signal });
}

export function chat(message: string, language: Language, signal?: AbortSignal): Promise<ChatResponse> {
  return request(
    '/chat',
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, language }),
      signal,
    },
    60000,
  );
}
