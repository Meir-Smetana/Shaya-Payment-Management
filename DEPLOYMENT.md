# ShuttleOps — Deployment Guide
## Montreal ↔ NYC Digital Dispatcher & Ledger PWA

---

## Architecture Overview

This is a **pure HTML/JS PWA** (no backend server required). All data is stored in the browser's `localStorage` with a Service Worker for offline support. The only external call is to the **Anthropic API** for AI payment screenshot analysis.

```
shuttleops/
├── index.html          ← Entire app (auth + all tabs + modals)
├── manifest.json       ← PWA installation config
├── sw.js               ← Service Worker (offline cache)
├── generate_icons.py   ← Run once to generate all icons
└── icons/
    ├── icon-72.png
    ├── icon-96.png
    ├── icon-128.png
    ├── icon-144.png
    ├── icon-152.png
    ├── icon-180.png
    ├── icon-192.png     ← Required for Android install
    ├── icon-384.png
    ├── icon-512.png     ← Required for Android install
    └── splash.png       ← Apple launch screen
```

---

## Step 1: Generate Icons

```bash
pip install Pillow
python generate_icons.py
```

This creates all required icon sizes in `/icons/`.

> **Tip**: Replace with your own branded icons later. The script generates geometric shuttle icons as placeholders.

---

## Step 2: Set Up Anthropic API Key

The AI payment matching feature uses Claude's Vision API. You need to add your API key.

**Option A — Netlify/Vercel Environment Variable (Recommended)**

Deploy to Netlify or Vercel and set:
```
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

Then create a simple serverless function to proxy the API call (prevents key exposure):

**`netlify/functions/analyze-payment.js`**:
```javascript
const { Anthropic } = require('@anthropic-ai/sdk');

exports.handler = async (event) => {
  const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });
  const body = JSON.parse(event.body);
  
  const message = await client.messages.create({
    model: 'claude-sonnet-4-20250514',
    max_tokens: 500,
    messages: body.messages,
  });
  
  return {
    statusCode: 200,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(message),
  };
};
```

Then update the fetch URL in `index.html`:
```javascript
// Change this line in analyzePaymentScreenshot():
const response = await fetch('/.netlify/functions/analyze-payment', {
```

**Option B — Direct (for personal/private use only)**

If the app is strictly for your own use (not shared), you can set the key directly in `index.html`. Search for the `analyzePaymentScreenshot` function and add:
```javascript
headers: {
  'Content-Type': 'application/json',
  'x-api-key': 'sk-ant-YOUR-KEY-HERE',
  'anthropic-version': '2023-06-01',
},
```

⚠️ **Never commit an API key to a public GitHub repo.**

---

## Step 3: Deploy to GitHub Pages (Free, Fast)

### 3a. Create GitHub Repository

```bash
git init
git add .
git commit -m "Initial ShuttleOps PWA"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/shuttleops.git
git push -u origin main
```

### 3b. Enable GitHub Pages

1. Go to your repo → **Settings** → **Pages**
2. Source: **Deploy from branch**
3. Branch: `main` / `/ (root)`
4. Click **Save**
5. Your app will be live at: `https://YOUR_USERNAME.github.io/shuttleops/`

> ⚠️ GitHub Pages serves over HTTPS — required for PWA features (Service Worker, Camera, Share API).

---

## Step 4: Deploy to Netlify (Recommended — Supports Serverless Functions)

### 4a. Via Netlify CLI

```bash
npm install -g netlify-cli
netlify login
netlify init
netlify deploy --prod
```

### 4b. Via Drag & Drop

1. Go to [app.netlify.com](https://app.netlify.com)
2. Drag your `dispatcher/` folder onto the deploy zone
3. Your site is live instantly with a `*.netlify.app` URL

### 4c. Add Custom Domain

1. Netlify → Site Settings → Domain Management
2. Add custom domain: `dispatch.yourcompany.com`
3. Netlify auto-provisions SSL

---

## Step 5: Install as PWA on Phone

### iPhone / iPad (Safari)
1. Open your deployed URL in **Safari**
2. Tap the **Share button** (box with arrow)
3. Scroll down → tap **"Add to Home Screen"**
4. Name it "ShuttleOps" → tap **Add**
5. App opens full-screen with no browser UI ✅

### Android (Chrome)
1. Open your URL in **Chrome**
2. Tap the **⋮ menu** → **"Add to Home screen"**
   OR Chrome will show an install banner automatically
3. Tap **Install**
4. App appears in your app drawer ✅

---

## Step 6: Update Deployed App

```bash
git add .
git commit -m "Update: improved dispatch manifest"
git push
```

GitHub Pages / Netlify auto-deploys. The Service Worker will update within 24 hours, or users can manually refresh.

To force immediate update:
```javascript
// In sw.js, bump the cache version:
const CACHE_NAME = 'shuttleops-v2'; // was v1
```

---

## Data Persistence Architecture

All data lives in `localStorage` under these keys:

| Key | Contents | Cleared When |
|-----|----------|--------------|
| `shuttleops_auth` | Auth session + expiry | Logout / 30-day expiry |
| `shuttleops_users` | Hashed user accounts | Never (manual only) |
| `shuttleops_active_trip` | Current live trip | On "Finalize" or "Cancel" |
| `shuttleops_dispatch` | Pickup route stops | On "Clear Route" |
| `shuttleops_history` | Archived trips | Never (manual only) |

### Zero Data Loss Guarantee

- Every state mutation calls `saveTrip()` or `saveDispatch()` immediately
- App reads from localStorage on every boot via `loadState()`
- Switching apps, backgrounding, or refreshing does NOT reset state
- Only "Finalize" or "Cancel" explicitly clears the active trip

---

## Security Notes

- Passwords are stored as `btoa()` (Base64) — sufficient for personal single-device use
- For a production multi-user deployment, add a proper backend with bcrypt hashing
- The auth system uses `localStorage` sessions with optional 30-day expiry
- API keys should ALWAYS be proxied via serverless functions in production

---

## Customization Checklist

- [ ] Replace `icons/` with your branded logo
- [ ] Update `manifest.json` `"name"` and `"short_name"`
- [ ] Set your default exchange rate in `state.exchangeRate`
- [ ] Customize route options in the "New Trip" modal dropdown
- [ ] Set up Anthropic API key via serverless function proxy
- [ ] Add custom domain in Netlify/GitHub Pages
- [ ] (Optional) Add push notification support via Web Push API

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | Vanilla JS (no bundler required) |
| Styling | Custom CSS with CSS Variables |
| Storage | `localStorage` + Service Worker Cache |
| AI Vision | Anthropic Claude Sonnet (Vision) |
| PWA | Service Worker + Web App Manifest |
| Share | Web Share API (native OS share sheet) |
| Hosting | GitHub Pages / Netlify (free tier) |
| Fonts | Space Grotesk + JetBrains Mono |

---

*ShuttleOps — Built for the road. Designed for the operator.*
