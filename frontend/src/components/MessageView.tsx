import type { ChatResponse } from '../api';
import type { Strings } from '../i18n';

export interface ChatMessage {
  id: number;
  role: 'user' | 'assistant' | 'error';
  text: string;
  response?: ChatResponse;
  /** For error messages: the question to send again. */
  retryText?: string;
}

interface Props {
  message: ChatMessage;
  strings: Strings;
  onRetry: (text: string) => void;
}

function Sources({ response, strings }: { response: ChatResponse; strings: Strings }) {
  if (response.sources.length === 0) return null;
  return (
    <details className="sources">
      <summary>{strings.sources(response.sources.length)}</summary>
      <ul>
        {response.sources.map((source) => (
          <li key={source.id} lang={response.language}>
            <p className="source-title">
              {source.document} <span aria-hidden="true">›</span>
              <span className="visually-hidden">, </span> {source.section}
            </p>
            <p className="source-text">{source.text}</p>
          </li>
        ))}
      </ul>
    </details>
  );
}

export function MessageView({ message, strings, onRetry }: Props) {
  if (message.role === 'user') {
    return (
      <li className="message message-user">
        <span className="visually-hidden">{strings.you}: </span>
        <p>{message.text}</p>
      </li>
    );
  }

  if (message.role === 'error') {
    return (
      <li className="message message-error">
        <p>{message.text}</p>
        {message.retryText && (
          <button type="button" className="button" onClick={() => onRetry(message.retryText ?? '')}>
            {strings.retry}
          </button>
        )}
      </li>
    );
  }

  const response = message.response;
  const status = response?.status ?? 'answered';
  const label =
    status === 'refused' ? strings.refusedLabel : status === 'not_found' ? strings.notFoundLabel : null;

  return (
    <li className={`message message-assistant message-${status}`}>
      <span className="visually-hidden">{strings.assistant}: </span>
      {label && <p className="message-label">{label}</p>}
      <p lang={response?.language}>{message.text}</p>
      {response && <Sources response={response} strings={strings} />}
    </li>
  );
}
