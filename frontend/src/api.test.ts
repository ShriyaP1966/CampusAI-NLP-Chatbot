import { afterEach, describe, expect, it, vi } from 'vitest';
import { ApiError, apiBase, chat } from './api';

function mockFetch(response: Partial<Response> & { json?: () => Promise<unknown> }) {
  const fetchMock = vi.fn().mockResolvedValue({ ok: true, status: 200, ...response });
  vi.stubGlobal('fetch', fetchMock);
  return fetchMock;
}

describe('api', () => {
  afterEach(() => vi.unstubAllEnvs());

  it('posts the message and language to /chat on the configured backend', async () => {
    const body = { answer: 'a', status: 'answered', language: 'en', confidence: 1, sources: [] };
    const fetchMock = mockFetch({ json: async () => body });

    await expect(chat('fees?', 'hi')).resolves.toEqual(body);

    const [url, init] = fetchMock.mock.calls[0];
    expect(url).toBe('http://api.test/chat');
    expect(JSON.parse(init.body)).toEqual({ message: 'fees?', language: 'hi' });
  });

  it('strips a trailing slash from the backend address', () => {
    vi.stubEnv('VITE_API_URL', 'http://api.test///');
    expect(apiBase()).toBe('http://api.test');
  });

  it('refuses to run without a backend address', () => {
    vi.stubEnv('VITE_API_URL', '');
    expect(() => apiBase()).toThrowError(ApiError);
  });

  it.each([
    [429, 'rate_limit'],
    [422, 'invalid'],
    [500, 'server'],
  ])('maps HTTP %i to %s', async (status, kind) => {
    mockFetch({ ok: false, status, json: async () => ({ detail: 'too long' }) });
    await expect(chat('x', 'en')).rejects.toMatchObject({ kind });
  });

  it('reports a network failure', async () => {
    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new TypeError('Failed to fetch')));
    await expect(chat('x', 'en')).rejects.toMatchObject({ kind: 'network' });
  });
});
