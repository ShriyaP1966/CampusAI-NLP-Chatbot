import { act, render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it, vi } from 'vitest';
import App from './App';

type Handler = (url: string, init?: RequestInit) => Promise<Partial<Response>> | Partial<Response>;

function json(body: unknown, status = 200): Partial<Response> {
  return { ok: status < 400, status, json: async () => body };
}

function backend(routes: Record<string, Handler>) {
  const fetchMock = vi.fn(async (url: string, init?: RequestInit) => {
    const path = url.replace('http://api.test', '').split('?')[0];
    const handler = routes[path];
    if (!handler) throw new Error(`Unexpected request to ${path}`);
    return handler(url, init);
  });
  vi.stubGlobal('fetch', fetchMock);
  return fetchMock;
}

const answer = {
  answer: 'The annual tuition fee is 70,000 rupees for BCA.',
  status: 'answered',
  language: 'en',
  confidence: 1,
  sources: [
    {
      id: 'fees#tuition',
      document: 'Fees and payments',
      section: 'Tuition fees',
      text: 'The annual tuition fee is 85,000 rupees for B.Sc AI, 70,000 rupees for BCA.',
    },
  ],
};

const healthy: Record<string, Handler> = {
  '/health': () => json({ status: 'ok' }),
  '/suggestions': () => json(['How much is the BCA tuition fee?', 'When are the semester exams?']),
};

describe('App', () => {
  it('answers a question and shows its sources', async () => {
    backend({ ...healthy, '/chat': () => json(answer) });
    const user = userEvent.setup();
    render(<App />);

    await user.type(screen.getByLabelText('Your question'), 'BCA fee?');
    await user.click(screen.getByRole('button', { name: 'Send' }));

    expect(await screen.findByText(answer.answer)).toBeInTheDocument();
    expect(screen.getByText('1 source')).toBeInTheDocument();
    expect(screen.getByText(/Fees and payments/)).toBeInTheDocument();
  });

  it('sends the selected language to the backend', async () => {
    const chatRoute = vi.fn<Handler>(() => json({ ...answer, language: 'hi' }));
    backend({ ...healthy, '/chat': chatRoute });
    const user = userEvent.setup();
    render(<App />);

    await user.selectOptions(screen.getByLabelText('Language'), 'hi');
    await user.type(await screen.findByLabelText('आपका प्रश्न'), 'फीस');
    await user.click(screen.getByRole('button', { name: 'भेजें' }));

    await waitFor(() => expect(chatRoute).toHaveBeenCalled());
    expect(JSON.parse(String(chatRoute.mock.calls[0][1]?.body))).toEqual({
      message: 'फीस',
      language: 'hi',
    });
  });

  it('puts a suggested question in the input box', async () => {
    backend({ ...healthy, '/chat': () => json(answer) });
    const user = userEvent.setup();
    render(<App />);

    await user.click(await screen.findByRole('button', { name: 'When are the semester exams?' }));
    expect(screen.getByLabelText('Your question')).toHaveValue('When are the semester exams?');
    // Focus moves to the box so Enter sends the question.
    expect(screen.getByLabelText('Your question')).toHaveFocus();
  });

  it('labels refusals and not-found answers differently from answers', async () => {
    backend({
      ...healthy,
      '/chat': () =>
        json({ answer: 'I could not find that.', status: 'not_found', language: 'en', confidence: 0, sources: [] }),
    });
    const user = userEvent.setup();
    render(<App />);

    await user.type(screen.getByLabelText('Your question'), 'capital of France');
    await user.click(screen.getByRole('button', { name: 'Send' }));

    expect(await screen.findByText('Not in the documents')).toBeInTheDocument();
    expect(screen.queryByText(/source/)).not.toBeInTheDocument();
  });

  it('shows an error with a retry button when the request fails, then recovers', async () => {
    let calls = 0;
    backend({
      ...healthy,
      '/chat': () => {
        calls += 1;
        if (calls === 1) throw new TypeError('Failed to fetch');
        return json(answer);
      },
    });
    const user = userEvent.setup();
    render(<App />);

    await user.type(screen.getByLabelText('Your question'), 'BCA fee?');
    await user.click(screen.getByRole('button', { name: 'Send' }));

    expect(await screen.findByText(/Could not reach the server/)).toBeInTheDocument();
    await user.click(screen.getByRole('button', { name: 'Try again' }));

    expect(await screen.findByText(answer.answer)).toBeInTheDocument();
    expect(screen.queryByText(/Could not reach the server/)).not.toBeInTheDocument();
    expect(screen.getAllByText('BCA fee?')).toHaveLength(1);
  });

  it('shows the waking-up message while the free server starts, then hides it', async () => {
    vi.useFakeTimers();
    let up = false;
    backend({
      '/health': () => {
        if (!up) throw new TypeError('Failed to fetch');
        return json({ status: 'ok' });
      },
      '/suggestions': () => json([]),
    });
    render(<App />);

    await act(async () => {
      await vi.advanceTimersByTimeAsync(100);
    });
    expect(screen.getByText('Waking up the server')).toBeInTheDocument();

    up = true;
    await act(async () => {
      await vi.advanceTimersByTimeAsync(3500);
    });
    expect(screen.queryByText('Waking up the server')).not.toBeInTheDocument();
  });

  it('offers a retry when the server never wakes up', async () => {
    vi.useFakeTimers();
    backend({ '/health': () => { throw new TypeError('Failed to fetch'); } });
    render(<App />);

    await act(async () => {
      await vi.advanceTimersByTimeAsync(130000);
    });
    expect(screen.getByText('The server is not responding')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Try again' })).toBeInTheDocument();
  });

  it('clears the conversation', async () => {
    backend({ ...healthy, '/chat': () => json(answer) });
    const user = userEvent.setup();
    render(<App />);

    await user.type(screen.getByLabelText('Your question'), 'BCA fee?');
    await user.click(screen.getByRole('button', { name: 'Send' }));
    await screen.findByText(answer.answer);
    await user.click(screen.getByRole('button', { name: 'Clear chat' }));

    expect(screen.queryByText(answer.answer)).not.toBeInTheDocument();
    expect(screen.getByText('What would you like to know?')).toBeInTheDocument();
  });
});
