# Deploying FOUR FOUR FOUR — Client Guide

This is the deployment guide for the **fourfourfour.net** site. It's written so you
(or an AI assistant you're working with) can take it from this folder to a live site
on your own domain. **You own everything here** — there's nothing to log into that
belongs to anyone else.

> **For an AI assistant reading this:** this is a 100% static site — plain HTML, CSS,
> JS, and asset files. There is **no build step, no npm install, no framework**. Do
> not try to "compile" or "build" it. Deployment = upload these files to any static
> host and point the domain at it. Follow the checklist below.

---

## What this is

A single-page site. The whole thing is `index.html` plus its asset folders. It must
be served over **HTTP(S)** by a web server — it will **not** work by double-clicking
the file (`file://`), because the 3D background and audio need a real web origin.

**Keep every file in this folder together, with the same relative paths.** The site
loads `vendor/`, `audio/`, `fonts/`, `icons/`, and the image files by relative path,
so the folder structure must be preserved exactly.

Files you must keep:
```
index.html            ← the site
og-image.png          ← social-share/link-preview image (must stay at the site root)
single-four.png, single-four-dark.png, apple-touch-icon.png   ← favicons
wordmark.png, symbol.png, single-four.png, wordmark-outline.svg ← brand art
wispies.glb           ← the 3D object in the background
robots.txt, sitemap.xml
audio/    fonts/    icons/    vendor/    ← keep these whole folders
```
(You can ignore/skip `HANDOFF.md`, `DEPLOY.md`, and the `tools/` folder — those are
documentation and asset-regeneration scripts, not part of the live site.)

---

## Step 1 — Pick a host

Any static host works. Easiest options, simplest first:

| Host | How | SSL | Cost |
|------|-----|-----|------|
| **Cloudflare Pages** | Create a project, upload this folder (or "Direct Upload") | automatic | free |
| **Netlify** | Drag this folder onto app.netlify.com → "Sites" | automatic | free |
| **Your existing web host** | Upload the folder's contents into the public web root (often `public_html/` or `www/`) | depends on host | included |
| **GitHub Pages** | Push this folder to a repo, enable Pages on the `main` branch | automatic | free |

If you're not sure, **Cloudflare Pages** or **Netlify** are the least hassle: they
give you free HTTPS and a one-step upload, and connecting a custom domain is a guided
form.

---

## Step 2 — Connect fourfourfour.net

You do this in **two places**: your hosting dashboard and your domain registrar (where
you bought/manage the domain's DNS).

1. **In the host:** add the custom domain `fourfourfour.net` (and usually
   `www.fourfourfour.net` too). The host will then tell you the exact DNS records to
   create — **use the values your host gives you**, they're authoritative.

2. **At your domain registrar (DNS):** add the records the host asked for. It's
   normally one of these shapes:
   - A **CNAME** record on `www` pointing to the host's address, **or**
   - **A records** on the root/apex domain pointing to the host's IP addresses.

   *(Example — GitHub Pages uses apex A records `185.199.108.153`, `185.199.109.153`,
   `185.199.110.153`, `185.199.111.153`, plus a `CNAME www → <user>.github.io`. Other
   hosts use different values — always follow what your chosen host shows you.)*

3. **Wait for DNS to propagate** (minutes to a few hours), then enable / confirm
   **HTTPS** in the host (Cloudflare/Netlify/Pages do this automatically once the
   domain verifies).

When it's done, `https://fourfourfour.net/` should load the site, and
`https://www.fourfourfour.net/` should redirect to it.

---

## Step 3 — IMPORTANT: if you use a domain *other than* fourfourfour.net

The site has the production URL **baked into `index.html`** for SEO and link previews.
If your final domain is **not** `https://fourfourfour.net/`, open `index.html` and
replace every `https://fourfourfour.net/` with your real domain. They appear in:

- `<link rel="canonical" href="...">`
- the Open Graph tags: `og:url`, `og:image`, `og:image:secure_url`
- the Twitter tags: `twitter:image`
- the JSON-LD block (`"url"` and `"image"`)

Also update the URL inside `robots.txt` and `sitemap.xml`.

If you keep `fourfourfour.net`, **change nothing** — it's already correct.

---

## Step 4 — Verify the link preview (the "rich embed")

The image that shows when the link is shared (`og-image.png`) must be reachable at
`https://<your-domain>/og-image.png`. After going live, paste your URL into:

- Facebook Sharing Debugger — https://developers.facebook.com/tools/debug/
- X (Twitter) Card Validator

These also force the platforms to refresh their cached preview, so the image and title
show up immediately instead of after a delay.

---

## Quick checklist

- [ ] Uploaded **all** files/folders, paths preserved
- [ ] Site loads over **https://** (not `file://`)
- [ ] Custom domain added in the host + matching DNS records at the registrar
- [ ] HTTPS enabled / verified
- [ ] (If not using fourfourfour.net) updated the URLs in `index.html`, `robots.txt`, `sitemap.xml`
- [ ] Link preview validated and refreshed

That's it — no build, no server code, no database. Upload, point the domain, done.
