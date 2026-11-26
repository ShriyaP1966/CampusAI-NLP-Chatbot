import type { Strings } from '../i18n';
import type { ServerStatus } from '../useServerStatus';

interface Props {
  status: ServerStatus;
  strings: Strings;
  onRetry: () => void;
}

export function ServerBanner({ status, strings, onRetry }: Props) {
  if (status === 'ready' || status === 'checking') return null;

  if (status === 'waking') {
    return (
      <div className="banner banner-waking" role="status">
        <span className="spinner" aria-hidden="true" />
        <div>
          <strong>{strings.wakingTitle}</strong>
          <p>{strings.wakingBody}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="banner banner-error" role="alert">
      <div>
        <strong>{strings.unavailableTitle}</strong>
        <p>{strings.unavailableBody}</p>
      </div>
      <button type="button" className="button" onClick={onRetry}>
        {strings.retry}
      </button>
    </div>
  );
}
