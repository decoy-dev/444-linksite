# 444 Link Site — Handoff

A one-screen artist link hub for **FOUR FOUR FOUR**. Everything lives in a single
self-contained **`index.html`** (no build step, no framework). It opens with an
"initializing / boot-up" sequence, then reveals a vertical HUD panel with a music
player + social links over a WebGL chrome backdrop.

---

## Run & deploy

```bash
./serve.sh           # → http://localhost:8779/  (python3 -m http.server)
```
Must be served over **HTTP**, not opened as a `file://` — WebGL (ES module imports)
and audio need a real origin.

**Deploy = GitHub Pages from `main`.** Repo: `decoy-dev/444-linksite`. There's a
`.nojekyll` file so Pages serves it as-is. Push to `main` and it goes live:
```bash
git push origin main
```
(Pushing requires write access to `decoy-dev/444-linksite`; the design work was
done under a different account, so make sure `gh`/git is authed as `decoy-dev`.)

**Client handoff:** for shipping this to the client's own host/domain (it's a fully
static site — host anywhere, no build), see **[`DEPLOY.md`](DEPLOY.md)**, written for
the client and their AI assistant.

---

## Files

| Path | What |
|------|------|
| `index.html` | The entire site — HTML, CSS, and 3 inline `<script>` blocks |
| `wispies.glb` | The 3D "relic" (deformed torus knot, ~3 MB) shown in the background |
| `wordmark.png` / `symbol.png` / `single-four.png` | Brand marks (white-on-transparent masks) |
| `wordmark-outline.svg` | Stroke-only **hollow outline** of the wordmark — used as the intro `#boot-logo`. Traced from `wordmark.png` with `potrace`; `fill:none` + `stroke` baked into an internal `<style>` (`vector-effect:non-scaling-stroke`). Regen: `sips -s format bmp wordmark.png --out /tmp/wm.bmp && potrace -i -s -O 1 -t 12 /tmp/wm.bmp -o out.svg`, then re-add the `<style>`. |
| `audio/444-*-demo.m4a` | The three transmissions (ENIGMA / FADEAWAY / NRG) |
| `fonts/`, `icons/` | Audiowide / Inter / JetBrains Mono; SVG icons are inline in the HTML |
| `vendor/three.module.js`, `vendor/jsm/**` | Pinned Three.js + addon passes/loaders (importmap maps `"three"`) |

---

## How `index.html` is organized

1. **`<style>`** — `:root` brand palette + the `--hud-shape` panel silhouette, the
   `#boot` overlay + FX styles, the `#stage` hub, and responsive media queries.
2. **Inline script** — sets the `--wm` CSS var to the wordmark URL.
3. **WebGL module** (`<script type="module">`) — Three.js backdrop: the relic,
   floating motes, lighting, and the post-processing composer. Exposes
   `window.__relicMode(...)` for the boot to drive.
4. **Boot + UI + audio** (`<script>` IIFE) — the intro sequence (`runBoot`), the
   hub reveal/typewriter, clock, population counter, and the audio player.

### Layering (z-index)
`#webgl` (0) → `#vignette`/`#grain` (2) → `#stage` (10, the live hub) →
`#boot` (50, the intro overlay; `#boot-fx` panels at 6 inside it) →
`#boot-flash` (60, the white reveal flash).
`#stage` starts at `opacity:0` and is shown (`.live`) under the white flash so the
intro never reveals the hub early.

---

## The intro / boot sequence

Driven by `runBoot()` in the boot script — a timeline of `at(ms, fn)` (setTimeout)
calls, ~8.4s of build + a ~1.4s white fade. Phases:

1. **Black** → console wakes; `INITIALIZING` flashes vertically on the left edge.
2. **"Installs"** — installer **dialogs** (`MOUNT`/`AUDIO`/`RELAY`/`NODES`), a
   **flooding console** (`PROC`), and **telemetry histograms** (`SYS`/`MEM`) scan
   in. Steady **flicker-blocks** step down the sides on a cadence.
3. **Logo builds out** (~1.4s) — `#boot-logo` (the `wordmark-outline.svg` **hollow
   outline**, see below) opens from the centre via a `clip-path` reveal with a
   brief leading-edge glow, settling dim (`opacity ~0.56`). It is **not** the
   persistent mark — the live *filled* hub wordmark takes over at the white flash.
4. **The menu UI is "created"** — `#skel-module` (a skeleton whose sections mirror
   the real panel: header → label → player → tracks → 2×3 links) fades in and
   **draws downward** behind a scanline.
5. **Relic constructs** — last, subtle: the real `wispies.glb` builds **from the
   centre outward** as a grey wireframe (see below).
6. **`RENDER COMPLETE`** → white flash → relic resolves to chrome, `#stage` goes
   `.live`, overlays clear, white fades over ~1.4s. (There is intentionally **no**
   pre-flash `flick()` before this — the final white flash is the only one.)

**FX helpers** (boot script): `spawnDialog`, `spawnRect` (scrolling histogram),
`spawnConsole` (flooding log), `flashBlock`/`blkBeat` (flicker-blocks), `bigText`
(rotated edge text), `flick` (full-screen flash), `appear`/`dismiss`, `fxClearAll`.
~Half the panels use the `boot` variant (flash in squished → full → then render
contents); the rest use `in` (scan reveal). All intervals are tracked and cleared
in `fxClearAll`. **Reduced-motion** (`prefers-reduced-motion`) skips the whole
sequence and just fades the hub in.

---

## The WebGL relic

`wispies.glb` is loaded once and driven by **`window.__relicMode(mode)`**:
- `off` — nothing renders (default, until the late build).
- `wire` — a **heavily decimated** (`DECIMATE = 9`, ~1/9 of triangles) wireframe,
  rendered with a custom `ShaderMaterial` that **discards edges beyond a growing
  radius** (`uReveal`) with a glowing leading edge → "constructs from the centre
  out." `updateRelic(dt)` (in the render `tick`) animates the build.
- `solid` — the real chrome `MeshPhysicalMaterial` (the final backdrop).

The boot does `wire` late, then `solid` under the white flash.
**During the intro the heavy composer is bypassed** — the tick calls
`renderer.render()` (cheap, crisp, no bloom) and only switches to
`composer.render()` (bloom + DoF + 8× MSAA + radial blur) once `relicMode === 'solid'`.
Background is pure black during the intro and swaps to the slate gradient on reveal.

---

## The HUD panel (`.module`)

Vertical "voltra"-style HUD:
- **Silhouette** = `--hud-shape` (a `clip-path` polygon: chamfered corners, a
  notched top-right, an angled bottom-left). The same shape is on `#skel-module`
  so the build skeleton matches.
- **Border** = two layers: `.module` background is the edge colour, `::before`
  (inset 1.5px, same clip-path) is the fill → a crisp rim that follows the chamfers.
- `::after` = top-edge glint. (The old `.hud-deco` overlay — corner hatch + `BC·444`
  id + `+` ticks — was **removed** as fluff; don't reintroduce it.)
- Content stacks vertically: wordmark → `// Transmissions` → player → track pills →
  **2×3** social links. Narrow/portrait; mobile-first media queries keep it tidy.

---

## Common tunables (all in `index.html`)

| Want to change | Where |
|----------------|-------|
| Intro pacing / what appears when | the `at(...)` schedule in `runBoot()` |
| Intro logo opacity / glow | the two `bootLogo.style.opacity` values on the `at(1400,…)` / `at(1900,…)` beats (currently `0.62` build → `0.56` settled), and the matching `reduce` path |
| Intro logo outline weight | `stroke-width` in the `<style>` inside `wordmark-outline.svg` (currently `1.3`) |
| When the white flash fires | `at(8400, startWhiteFlash)` + the 1.4s fade in `startWhiteFlash` |
| Flicker-block cadence / count | `setInterval(blkBeat, 370)` and `at(5000, clearInterval)` |
| Relic subtlety | `WIRE_BASE` (0.46) and `fadeVeil(0.34)` at the build beat |
| Relic build speed | the lerp `dt * 0.95` in `updateRelic` |
| Wireframe density | `DECIMATE` (9 = ~1/9 of triangles) |
| Panel shape | `--hud-shape` in `:root` |
| Brand colours / fonts | `:root` palette + `fonts/fonts.css` |
| Tracks / links | `TX` array (audio) + the `.links` `<a>` list in the HTML |
| Default volume / fade-in | `volume = 0.5` (persisted to `localStorage['444-vol']`) + the gain `setTargetAtTime` fade in `play()` — output runs through a `GainNode` (`sn → analyser → gain → destination`) so playback never starts at full blast |
| Volume slider / mute look | `.p-vol*` CSS rules + `syncVol()` (the `--fill` track gradient + `VOL_ON`/`VOL_OFF` speaker glyphs) |
| Idle waveform look | the `else` (standby) branch in the `draw()` loop — travelling sines + breathing envelope; honours `prefers-reduced-motion` |

---

## Gotchas / perf landmines

- **Headless Chrome has no GPU** → the WebGL relic won't render under `--disable-gpu`,
  and that run aborts the WebGL script before the model loads (so it can't catch
  relic bugs). Verify with software WebGL (`--enable-unsafe-swiftshader`) or a tiny
  standalone test page; use a probe `<style>` (`animation:none;opacity:1`) to inspect
  the DOM intro overlays, since headless freezes CSS transitions/animations.
- **Never** build `THREE.WireframeGeometry` / `THREE.Points` per mesh at load — it
  hangs the main thread on this model and tanks FPS. Use `material.wireframe` / a
  decimated index instead.
- **Never** add a Mesh child *inside* `gltf.scene.traverse(...)` — `traverse` will
  re-visit it forever (stack overflow). Collect meshes first, then add children.
- The composer (bloom/DoF/MSAA/radial-blur) is the real fill-rate cost — that's why
  it's bypassed during the wireframe intro.

## Known issues / next

- On narrow mobile the top **rail** (`SIGNAL ACTIVE // time`) and footer text can run
  slightly past the right edge — could use a shrink/wrap pass.
- The HUD panel is a solid first take on the "voltra" direction; further detailing
  (more frame variants, animated ticks) is possible.
