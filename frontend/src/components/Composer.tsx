import { useEffect, type FormEvent, type RefObject } from 'react';
import type { Strings } from '../i18n';

export const MAX_LENGTH = 500;

interface Props {
  strings: Strings;
  busy: boolean;
  value: string;
  onChange: (value: string) => void;
  onSend: (text: string) => void;
  inputRef: RefObject<HTMLInputElement | null>;
}

export function Composer({ strings, busy, value, onChange, onSend, inputRef }: Props) {
  useEffect(() => {
    if (!busy) inputRef.current?.focus();
  }, [busy, inputRef]);

  const submit = (event: FormEvent) => {
    event.preventDefault();
    const text = value.trim();
    if (!text || busy) return;
    onSend(text);
  };

  return (
    <form className="composer" onSubmit={submit}>
      <label htmlFor="question" className="visually-hidden">
        {strings.inputLabel}
      </label>
      <input
        id="question"
        ref={inputRef}
        type="text"
        value={value}
        maxLength={MAX_LENGTH}
        autoComplete="off"
        enterKeyHint="send"
        aria-describedby="question-hint"
        placeholder={strings.inputLabel}
        onChange={(event) => onChange(event.target.value)}
      />
      <span id="question-hint" className="visually-hidden">
        {strings.inputHint}
      </span>
      <button type="submit" className="button button-primary" disabled={busy || !value.trim()}>
        {busy ? strings.sending : strings.send}
      </button>
    </form>
  );
}
