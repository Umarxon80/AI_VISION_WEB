# Deploying the website (free)

There are two separate things to deploy:

1. **The main site** (`index.html`, `assets/`) — static, no backend needed.
2. **The live demo** (`demo-space/`) — needs a real Python backend to run
   YOLO, so it goes on Hugging Face Spaces (free CPU tier), not on a
   static host.

## 1. Main site → GitHub Pages (easiest, since your code is already on GitHub)

```bash
# from your repo root, with this website/ folder committed
git checkout --orphan gh-pages
git rm -rf .
cp -r website/* .
git add .
git commit -m "Deploy website"
git push origin gh-pages
```

Then in your repo on GitHub: **Settings → Pages → Source: `gh-pages`
branch, `/ (root)`**. Your site goes live at
`https://YOUR-ORG.github.io/YOUR-REPO/` within a minute or two.

**Alternative — Vercel (also free, and redeploys on every push):**

```bash
npm i -g vercel
cd website
vercel --prod
```

Follow the prompts (link/create a project); no build step is needed
since this is plain HTML/CSS.

**Alternative — Netlify:** drag the `website/` folder onto
https://app.netlify.com/drop for an instant free URL, or connect the
GitHub repo for auto-deploys from `website/` as the publish directory.

## 2. Live demo → Hugging Face Spaces (free CPU)

1. Create a free account at https://huggingface.co if you don't have one.
2. **New Space** → choose a name (e.g. `trafficwatch-ai`) → **SDK: Gradio**
   → **Hardware: CPU basic (free)** → **Create Space**.
3. Populate `demo-space/` locally with the two files it's missing (see
   `demo-space/README.md`):
   ```bash
   cp ../solution.py demo-space/solution.py
   mkdir -p demo-space/weights
   cp ../weights/yolo11m.pt demo-space/weights/yolo11m.pt
   ```
4. Push it to the Space (Spaces are git repos):
   ```bash
   cd demo-space
   git init
   git remote add space https://huggingface.co/spaces/YOUR-USERNAME/trafficwatch-ai
   git add .
   git commit -m "Initial demo"
   git push --force space main
   ```
5. Wait for the build to finish (Space page shows build logs). Once it
   says "Running", your demo is live at
   `https://YOUR-USERNAME-trafficwatch-ai.hf.space`.
6. Update `index.html`'s `#demo` section: replace both occurrences of
   `https://YOUR-HF-USERNAME-trafficwatch-ai.hf.space` with your real
   Space URL, then redeploy the main site (step 1).

### Notes

- Free Spaces sleep after inactivity and take ~30s to wake up on the
  first visit after a while — mention this near the demo so judges
  aren't confused by the initial delay.
- CPU inference on a full-resolution multi-minute clip will be slow;
  the app already caps uploads at 150s and shows a message if a longer
  clip is uploaded (see `MAX_DURATION_SEC` in `demo-space/app.py`).
- If your weights push is rejected for size, Hugging Face Spaces support
  files up to a few GB fine via plain git, but if you hit LFS prompts,
  run `git lfs install && git lfs track "*.pt"` before committing.
