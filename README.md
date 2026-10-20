# DSMHub

Dark starfield hub: games, movies, community chat, AI assistant and an embedded browser. Assets and games served by **jsDelivr**, site on **GitHub Pages** or as a single SVG on jsDelivr, accounts/chat/sync/AI on **Supabase**.

## Adding games
Put each game in its own folder under `games/`:
```
games/my-game/index.html   (the whole game, self-contained)
games/my-game/logo.png     (the icon)
```
Push. The **Build** workflow (`.github/workflows/build-svg.yml`) wraps each game into `play.svg` (jsDelivr runs scripts in SVG files but serves `.html` as plain text) and updates `games/games.json`, which the site reads. The folder name becomes the title. Games must be one self-contained HTML file; relative asset files are not resolved. Only add games you own or may share.
Enable the workflow's push access once: repo Settings > Actions > General > Workflow permissions > Read and write.

## Movies
Put your Movies page in `movies/index.html` (a full HTML page, or just an embed snippet like an `<iframe>`). The Build workflow wraps it into `movies/play.svg` and the Movies tab shows it. Only use content you are licensed to show. For pushes to `movies/` to rebuild automatically, add `"movies/**"` to the `paths:` list in your workflow (or run it manually from the Actions tab).

## Setup
1. **Config:** edit `config.js`: `GITHUB_USER`, `GITHUB_REPO`, `GITHUB_REF` (use a release tag or commit hash; jsDelivr caches branch URLs for hours), plus Supabase URL and anon key.
2. **Supabase:** create a project, run `supabase/schema.sql` (chat messages + synced user data). Auth settings: set Site URL to wherever you host the site.
3. **AI (optional):** with the Supabase CLI: `supabase link --project-ref <ref>`, `supabase secrets set --env-file .env` (copy `.env.example`), `supabase functions deploy ai`.
4. **Host** (pick one):
   - **GitHub Pages (recommended):** Settings > Pages > branch `main`, root. Logins persist between visits.
   - **jsDelivr only:** open `https://cdn.jsdelivr.net/gh/<user>/<repo>@<ref>/index.svg`. The whole site is wrapped in an SVG by the workflow (or `python3 tools/build_svg.py`). By default it runs in an isolated sandbox, so nothing persists between visits (you sign in each time). `--same-origin` restores persistence but puts session tokens on the shared `cdn.jsdelivr.net` origin where other SVG-hosted pages can read them; do not use it with real accounts.

## Accounts and sync
Signing in (button top right) syncs favorites and recently played games to your account (`user_data` table, protected by Row Level Security). Data is loaded on sign-in and page load, not live between open tabs. Chat and the assistant need an account. Without signing in, favorites and recents stay in the browser only.

## What works
- **Home, Browser:** no setup. The Browser is an embedded frame, not a proxy; many sites block framing.
- **Games:** from the `games/` folder, search, favorites, recently played, sandboxed player.
- **Movies:** your own page in `movies/index.html` (full page or an embed snippet), shown sandboxed.
- **Chat:** three channels, live updates, delete own messages, 500-char limit, 1/sec DB throttle.
- **AI:** text only, signed-in users, via the Supabase Edge Function.

## Known limitations
- Not built: server-side proxy, DMs, replies, reactions, moderation/admin tools, image uploads, saved AI history, per-user AI usage limits.
- Chat display names come from the client and can be spoofed.
- Sync is on load, not realtime. Games.json and assets can lag behind pushes because of jsDelivr caching.
- Tested locally in Chromium (games flow, favorites, player, SVG wrapper); not tested against live Supabase, GitHub Pages or jsDelivr.
