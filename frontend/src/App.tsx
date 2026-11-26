import { useCallback, useEffect, useRef, useState } from 'react';
import { ApiError, chat, suggestions, type AnswerLanguage, type Language } from './api';
import { Composer } from './components/Composer';
import { MessageView, type ChatMessage } from './components/MessageView';
import { ServerBanner } from './components/ServerBanner';
import { Suggestions } from './components/Suggestions';
import { LANGUAGE_OPTIONS, STRINGS } from './i18n';
import { useServerStatus } from './useServerStatus';

export default function App() {
  const [language, setLanguage] = useState<Language>('auto');
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [busy, setBusy] = useState(false);
  const [input, setInput] = useState('');
  const [suggested, setSuggested] = useState<string[]>([]);
  const { status, retry } = useServerStatus();
  const nextId = useRef(1);
  const endRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // The interface follows the chosen language, or the language of the last answer.
  const lastAnswer = [...messages].reverse().find((m) => m.response)?.response;
  const uiLanguage: AnswerLanguage = language === 'auto' ? (lastAnswer?.language ?? 'en') : language;
  const strings = STRINGS[uiLanguage];

  useEffect(() => {
    if (status !== 'ready') return;
    const controller = new AbortController();
    suggestions(language, controller.signal)
      .then(setSuggested)
      .catch(() => setSuggested([]));
    return () => controller.abort();
  }, [status, language]);

  useEffect(() => {
    endRef.current?.scrollIntoView?.({ block: 'end', behavior: 'smooth' });
  }, [messages, busy]);

  const send = useCallback(
    async (text: string, { showQuestion = true }: { showQuestion?: boolean } = {}) => {
      setInput('');
      if (showQuestion) {
        setMessages((current) => [...current, { id: nextId.current++, role: 'user', text }]);
      }
      setBusy(true);
      try {
        const response = await chat(text, language);
        setMessages((current) => [
          ...current,
          { id: nextId.current++, role: 'assistant', text: response.answer, response },
        ]);
      } catch (error) {
        const kind = error instanceof ApiError ? error.kind : 'network';
        setMessages((current) => [
          ...current,
          {
            id: nextId.current++,
            role: 'error',
            text: STRINGS[uiLanguage].errors[kind],
            retryText: kind === 'config' || kind === 'invalid' ? undefined : text,
          },
        ]);
      } finally {
        setBusy(false);
      }
    },
    [language, uiLanguage],
  );

  const retryMessage = useCallback(
    (text: string) => {
      setMessages((current) => current.filter((m) => m.role !== 'error'));
      void send(text, { showQuestion: false });
    },
    [send],
  );

  const clear = () => {
    setMessages([]);
    setInput('');
  };

  return (
    <div className="app">
      <header className="header">
        <div className="brand">
          <img src="/favicon.svg" alt="" width="36" height="36" />
          <div>
            <h1>CampusAI</h1>
            <p>{strings.tagline}</p>
          </div>
        </div>
        <div className="header-controls">
          <label htmlFor="language">{strings.language}</label>
          <select
            id="language"
            value={language}
            onChange={(event) => setLanguage(event.target.value as Language)}
          >
            {LANGUAGE_OPTIONS.map((option) => (
              <option key={option.value} value={option.value}>
                {option.value === 'auto' ? strings.autoDetect : option.label}
              </option>
            ))}
          </select>
          <button type="button" className="button" onClick={clear} disabled={messages.length === 0}>
            {strings.clear}
          </button>
        </div>
      </header>

      <p className="notice">{strings.sampleNotice}</p>
      <ServerBanner status={status} strings={strings} onRetry={retry} />

      <main className="chat">
        {messages.length === 0 && !busy ? (
          <section className="empty">
            <h2>{strings.emptyTitle}</h2>
            <p>{strings.emptyBody}</p>
          </section>
        ) : (
          <ol className="messages" role="log" aria-live="polite" aria-label="Conversation">
            {messages.map((message) => (
              <MessageView key={message.id} message={message} strings={strings} onRetry={retryMessage} />
            ))}
            {busy && (
              <li className="message message-assistant message-pending" role="status">
                <span className="dots" aria-hidden="true">
                  <i />
                  <i />
                  <i />
                </span>
                <span>{strings.thinking}</span>
              </li>
            )}
          </ol>
        )}
        <div ref={endRef} />
      </main>

      <footer className="footer">
        {messages.length === 0 && (
          <Suggestions items={suggested} strings={strings} disabled={busy} onPick={(question) => {
              setInput(question);
              inputRef.current?.focus();
            }} />
        )}
        <Composer
          strings={strings}
          busy={busy || status === 'unavailable'}
          inputRef={inputRef}
          value={input}
          onChange={setInput}
          onSend={(text) => void send(text)}
        />
        {status === 'waking' && <p className="footer-hint">{strings.waitingForServer}…</p>}
      </footer>
    </div>
  );
}
