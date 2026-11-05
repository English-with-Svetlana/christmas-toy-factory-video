# Father Frost helps Santa — video embed

A static, dependency-free embed for Genially. The local repository is prepared for its first publication. No commit, push, or deployment has been performed.

## Local review

Run `python3 -m http.server 8000 --bind 127.0.0.1` from this folder if the server is no longer running.

- Main: http://127.0.0.1:8000/
- Iframe simulation: http://127.0.0.1:8000/iframe-preview.html

The simulation has a dark surrounding background to make transparent margins visible. The production page contains only the video, with a transparent background. Both stage and iframe use 16:9; a differently shaped host gets transparent letterboxing, never cropping.

## Media

| Property | Original | Optimized |
| --- | --- | --- |
| Bytes | 7,078,373 | 2,692,957 |
| Decimal MB | 7.08 | 2.69 |
| Resolution | 1920×1080 | 1280×720 |
| Codec | H.264 High | H.264, yuv420p |
| Frame rate / count | 24 fps / 188 | 24 fps / 188 |
| Video duration | 7.833333 s | 7.833333 s |
| Container duration | 7.85 s | 7.833333 s |
| Audio | AAC stereo | None |

Reduction: 61.95%. The shorter container duration comes from removing the slightly longer audio stream. No video frames were trimmed, duplicated, reordered, or composited. CRF 21 encoding resizes and compresses the original composition. Faststart was verified by checking that `moov` precedes `mdat`. The first decoded optimized frame supplies the 257,784-byte JPEG poster.

The browser uses native looping without resetting the source, clearing the video, or showing controls. Seam continuity depends on the original endpoints and browser decoding; absolute absence of loop flashes across all devices cannot be guaranteed without testing those devices. No crossfade or visual content alteration was added. Browser autoplay policies, low-power settings, and host permissions can still block playback; in that case the poster remains visible without UI.

## QA

Automated headless Google Chrome tests passed in an iframe at 1280×720 and 390×844 viewports:

- Autoplay advanced the video without interaction.
- Muted/defaultMuted, autoplay, loop and playsInline were true; controls false.
- One loop rollover occurred in each test; no paused samples.
- Decoded resolution 1280×720; readyState 4.
- Stage aspect ratio 16:9 within subpixel rounding, no scrollbars, transparent background.
- Page, iframe, poster and video returned HTTP 200; no page script errors.
- Desktop screenshot visually reviewed: full frame, no added UI or borders.

Raw results and screenshots are in `qa/` (excluded from Git). `scripts/test.cjs` uses Playwright and an installed Google Chrome for development tests only. No runtime dependencies are needed. Real iOS Safari, live Genially, deployed HTTPS and frame-by-frame loop-flash testing have not been performed. Mobile compatibility attributes and H.264/yuv420p encoding are configured, but phone-size Chrome testing does not establish Safari compatibility.

## Publishing after local approval

Publish `index.html`, `assets/`, and `.nojekyll` at the repository root. The original root MP4 is ignored by Git and remains untouched locally. The iframe preview, browser test script and QA artifacts are excluded from Git. The replacement builder remains in the repository as a maintenance tool.

GitHub repository → Settings → Pages → Build and deployment:

- Source: Deploy from a branch
- Branch: main (or your actual publication branch)
- Folder: /(root)
- Use HTTPS.

Reference: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site

Keep the same repository and root page URL for all future replacements. Repository: https://github.com/English-with-Svetlana/christmas-toy-factory-video

Expected permanent Pages URL after publication: https://english-with-svetlana.github.io/christmas-toy-factory-video/

This URL is not deployed or verified live yet.

Paste this into Genially after replacing `FINAL_GITHUB_PAGES_URL` with the permanent HTTPS page URL (including its repository path and trailing slash):

```html
<iframe
  src="FINAL_GITHUB_PAGES_URL"
  title="Father Frost helps Santa"
  width="1280"
  height="720"
  style="display:block;width:100%;aspect-ratio:16/9;height:auto;border:0;background:transparent;overflow:hidden"
  allow="autoplay; fullscreen"
  allowfullscreen>
</iframe>
```

Use a 16:9 embed box in Genially. Verify the published quest on the intended classroom and mobile devices.

## Future video replacement

With FFmpeg installed, run:

```sh
python3 scripts/build.py '/path/to/replacement.mp4'
```

The builder preserves aspect ratio, fits within 1280×720, strips audio and generates SHA-256-based filenames for video and poster. It regenerates `index.html` with relative references, leaving the publication URL unchanged. Review locally before publishing the updated HTML together with new assets. Retain old hashed assets until the new deployment is verified; the builder deliberately does not delete them. A browser holding old HTML may temporarily use the old asset until the page revalidates, but new HTML cannot accidentally reuse stale media bytes under an unchanged filename. Already open iframes need a reload to receive updates.
