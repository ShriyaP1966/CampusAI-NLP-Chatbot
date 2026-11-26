# Contributing to CampusAI

Thanks for your interest. CampusAI is a small project, so the process is light. Bug reports, new languages, better sample documents and test cases are all welcome.

## Ways to help

- Pick an issue labelled [`good first issue`](https://github.com/ShriyaP1966/CampusAI-NLP-Chatbot/labels/good%20first%20issue) or [`help wanted`](https://github.com/ShriyaP1966/CampusAI-NLP-Chatbot/labels/help%20wanted).
- Improve the Hindi or Marathi sample text. Native-speaker review is especially useful.
- Add evaluation questions, particularly ones the bot gets wrong.
- Report a bug with the question you asked and the answer you expected.

## Set up

You need Python 3.11 or newer and Node.js 22 or newer.

```bash
git clone https://github.com/ShriyaP1966/CampusAI-NLP-Chatbot.git
cd CampusAI-NLP-Chatbot

# Backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
uvicorn campusai.api:app --reload   # http://localhost:8000

# Frontend (in a second terminal)
cd frontend
cp .env.example .env.local
npm ci
npm run dev                          # http://localhost:5173
```

## Run the checks

CI runs the same commands on every pull request.

```bash
# Backend
ruff check .
ruff format --check .
pytest
python -m campusai.evaluate          # prints the evaluation tables

# Frontend (from frontend/)
npm run lint
npm run typecheck
npm test
npm run build
```

## Adding or changing documents

Documents live in `data/documents/` and are described in that folder's README. Keep these rules:

- Use only sample or generic information. Do not add private, scraped or copyrighted college data.
- A section has the same id in every language, and a test checks that English, Hindi and Marathi stay in step.
- If you change a document, check that `python -m campusai.evaluate` has not got worse, and add evaluation questions for what you added (`data/eval/questions.csv`).

## Adding a language

1. Add the stop words, normalization and any spoken-form synonyms in `campusai/text.py`.
2. Teach `campusai/language.py` to detect it.
3. Translate the fixed messages in `campusai/messages.py` and the suggestions in `campusai/suggestions.py`.
4. Add the documents (`<doc_id>.<lang>.md`) and the interface strings in `frontend/src/i18n.ts`.
5. Add evaluation questions and tests.

## Pull requests

- Open or comment on an issue first for anything larger than a small fix.
- Keep each pull request to one change, with a clear description of what changed and why. Link the issue with `Closes #123`.
- Add or update tests. Lint, tests and the build must pass.
- Commit messages are short and in the imperative, for example `feat: add Tamil sample documents` or `fix: handle empty query`.

## Security

Please do not open a public issue for a security problem. Use GitHub's "Report a vulnerability" option under the repository's Security tab.

By contributing you agree that your contribution is licensed under the MIT License.
