import type { Strings } from '../i18n';

interface Props {
  items: string[];
  strings: Strings;
  disabled: boolean;
  onPick: (question: string) => void;
}

export function Suggestions({ items, strings, disabled, onPick }: Props) {
  if (items.length === 0) return null;
  return (
    <section className="suggestions" aria-labelledby="suggested-title">
      <h2 id="suggested-title">{strings.suggestedTitle}</h2>
      <ul>
        {items.map((item) => (
          <li key={item}>
            <button type="button" className="chip" disabled={disabled} onClick={() => onPick(item)}>
              {item}
            </button>
          </li>
        ))}
      </ul>
    </section>
  );
}
