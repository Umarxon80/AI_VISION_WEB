"""
Gradio app for Hugging Face Spaces. This is the "Live demo" backend
embedded via <iframe> in the main website (see index.html).

Deploy: copy this file, requirements.txt, solution.py and weights/ into
a new Hugging Face Space (SDK: Gradio) and push. See DEPLOY.md.
"""
from __future__ import annotations

import tempfile
from pathlib import Path

import cv2
import gradio as gr

from solution import CLASSES, detect_events

MAX_DURATION_SEC = 150  # a little over the 2-minute clip size the task suggests accepting

COLORS = {
    "accident": "#E8623A", "near_miss": "#E8B44A", "red_light": "#E8B44A",
    "wrong_way": "#E8623A", "illegal_u_turn": "#E8B44A", "stopped_vehicle": "#9099A6",
    "jaywalking": "#E8B44A", "failure_to_yield": "#E8623A", "illegal_turn": "#E8B44A",
    "solid_line_crossing": "#9099A6", "stop_line": "#E8B44A", "congestion": "#9099A6",
    "road_obstacle": "#9099A6", "fire_smoke": "#E8623A",
}


def fmt_t(sec: float) -> str:
    m, s = divmod(int(sec), 60)
    return f"{m:02d}:{s:02d}"


def render_timeline(events: list[list]) -> str:
    if not events:
        return "<p style='color:#9099A6'>No events detected.</p>"
    chips = []
    for start, end, label in sorted(events, key=lambda e: e[0]):
        color = COLORS.get(label, "#9099A6")
        chips.append(
            f"<span style='display:inline-flex;align-items:center;gap:6px;"
            f"font-size:13px;background:#1B2129;border:1px solid #262C35;"
            f"border-radius:999px;padding:6px 12px;margin:4px'>"
            f"<span style='width:8px;height:8px;border-radius:50%;background:{color};"
            f"display:inline-block'></span>{label} · {fmt_t(start)}–{fmt_t(end)}</span>"
        )
    return "<div>" + "".join(chips) + "</div>"


def analyze(video_path: str):
    if not video_path:
        return "<p style='color:#E8623A'>No video received.</p>", []

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    n_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0
    cap.release()
    duration = n_frames / fps if fps else 0

    if duration > MAX_DURATION_SEC:
        msg = (
            f"<p style='color:#E8623A'>This clip is {duration:.0f}s long. "
            f"Please upload something under {MAX_DURATION_SEC}s for the demo — "
            f"CPU inference on the free tier is slow.</p>"
        )
        return msg, []

    events = detect_events(video_path)
    table = [[label, fmt_t(start), fmt_t(end)] for start, end, label in sorted(events, key=lambda e: e[0])]
    return render_timeline(events), table


with gr.Blocks(title="TrafficWatch AI — live demo") as demo:
    gr.Markdown(
        "## TrafficWatch AI — live demo\n"
        f"Upload a clip from the camera (≤{MAX_DURATION_SEC}s). "
        "Runs on free CPU, so a short clip may still take a minute or two.\n\n"
        f"Detects: {', '.join(CLASSES)}."
    )
    video_in = gr.Video(label="Upload video")
    run_btn = gr.Button("Analyze", variant="primary")
    timeline_out = gr.HTML(label="Event timeline")
    table_out = gr.Dataframe(headers=["label", "start", "end"], label="Events")

    run_btn.click(fn=analyze, inputs=video_in, outputs=[timeline_out, table_out])

if __name__ == "__main__":
    demo.launch()
