# E-Ink Text (Kindle + Kobo starter)

This is a **simple texting app prototype** designed for e-reader browsers:

- plain HTML/CSS/JS frontend (no build tools)
- Flask backend
- SQLite message store
- high-contrast UI for e-ink screens
- quick-word buttons (`yes`, `no`, `what`, `why`, `who`) for faster typing

## Compatibility notes (as of March 25, 2026)

- **KOReader itself is not a chat app runtime**; this project runs as a web app on-device over Wi-Fi.
- **Kobo:** KOReader wiki says the "full Kobo lineup" is supported from Kobo Touch onward.
- **Kindle 4 (NT):** KOReader wiki says KOReader can be installed on jailbroken Kindles, and specifically calls out Kindle 4 non-touch with some minor feature limitations.
- For older/limited browsers, use **`/basic`** mode (no JavaScript required).

## Can I use Vercel?

Yes, you can deploy this Flask app on Vercel with `vercel.json` included in this repo.

Important caveat:

- Vercel serverless file storage is ephemeral, so **SQLite is not durable** there.
- For real usage, switch from local SQLite to a hosted database (Postgres, Turso/libSQL, Supabase, Neon, etc.).

Quick deploy:

```bash
npm i -g vercel
vercel
```

Optional env var:

- `MESSAGES_DB_PATH` (defaults to `messages.db` beside `app.py`; on serverless this is temporary)

## Why this approach

Kindle and Kobo are easiest to support through a lightweight web app. Native apps are not practical on both devices without deep platform-specific hacks.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Then open:

- `http://localhost:8000` (live mode)
- `http://localhost:8000/basic` (legacy mode)

## Next steps for a real product

1. Add authentication (username/password or invite code).
2. Add end-to-end encryption.
3. Add store-and-forward delivery when devices sleep.
4. Add long-polling or WebSocket mode for faster updates.
5. Move persistence to a managed database and secure with HTTPS.
