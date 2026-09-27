---
title: TrafficWatch AI Demo
emoji: 🚦
colorFrom: gray
colorTo: orange
sdk: gradio
sdk_version: "4.44.0"
app_file: app.py
pinned: false
---

# TrafficWatch AI — live demo Space

This folder is a **separate deployable unit** from the main repo: it is
what you push to a Hugging Face Space (not to GitHub Pages). See
`DEPLOY.md` at the repo root for exact steps.

Before pushing, copy in from the main repo:
- `solution.py`
- `weights/yolo11m.pt` (run `weights/download.sh` in the main repo first if you have not already)

so this folder looks like:

```
demo-space/
├── README.md          (this file — the Space's config header)
├── app.py
├── requirements.txt
├── solution.py         ⬅ copy from the main repo
└── weights/
    └── yolo11m.pt      ⬅ copy from the main repo
```
