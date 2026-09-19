from __future__ import annotations

import os
import traceback
import gradio as gr
from dotenv import load_dotenv
from research_manager import ResearchManager, ResearchUpdate
from styles import CSS, JS, EXAMPLES, HEADER_HTML

load_dotenv(override=True)

STAGES = [
    ("plan", "Plan"),
    ("search", "Search"),
    ("write", "Write"),
    ("deliver", "Deliver"),
]


def render_stepper(active_stage: str | None, done: bool = False, error: bool = False) -> str:
    """Render the Plan/Search/Write/Deliver progress stepper as HTML."""
    stage_order = [key for key, _ in STAGES]
    active_index = stage_order.index(active_stage) if active_stage in stage_order else -1

    steps = []
    for index, (key, label) in enumerate(STAGES):
        if error and index == active_index:
            status = "error"
        elif done or index < active_index:
            status = "done"
        elif index == active_index:
            status = "active"
        else:
            status = "pending"
        steps.append(
            f'<div class="dr-step dr-step-{status}">'
            f'<span class="dr-step-dot"></span>'
            f'<span class="dr-step-label">{label}</span>'
            f"</div>"
        )
    return f'<div class="dr-stepper">{"".join(steps)}</div>'


IDLE_BUTTON = gr.update(value="Investigate", interactive=True)
BUSY_BUTTON = gr.update(value="Researching…", interactive=False)


async def run(query: str):
    query = (query or "").strip()
    if not query:
        yield render_stepper(None), "", IDLE_BUTTON
        return

    yield render_stepper("plan"), "", BUSY_BUTTON

    try:
        async for update in ResearchManager().run(query):
            if update.kind == "status":
                yield render_stepper(update.stage), gr.update(), BUSY_BUTTON
            elif update.kind == "report":
                yield render_stepper("deliver", done=True), update.message, IDLE_BUTTON
    except Exception:
        traceback.print_exc()
        yield (
            render_stepper("deliver", error=True),
            "**Something went wrong while researching this query. Please try again.**",
            IDLE_BUTTON,
        )


with gr.Blocks(title="Deep Research") as ui:
    with gr.Row(elem_classes="dr-header-row"):
        gr.HTML(HEADER_HTML)
        gr.HTML(
            '<button class="dr-theme-toggle" onclick="window.drToggleTheme && window.drToggleTheme()" '
            'aria-label="Toggle dark mode" title="Toggle dark mode">'
            '<span class="dr-theme-icon"></span>'
            "</button>"
        )

    with gr.Row(elem_classes="dr-query-row"):
        query_textbox = gr.Textbox(
            placeholder="Type a research question...",
            show_label=False,
            container=False,
            autofocus=True,
            elem_id="dr-query",
            scale=5,
        )
        run_button = gr.Button("Investigate", variant="primary", elem_id="dr-run", scale=1)

    gr.HTML('<div class="dr-examples-label">Try one</div>')
    gr.Examples(examples=EXAMPLES, inputs=query_textbox, elem_id="dr-examples")

    stepper = gr.HTML(render_stepper(None), elem_id="dr-stepper-wrap")
    report = gr.Markdown(elem_id="dr-report")

    run_button.click(run, inputs=query_textbox, outputs=[stepper, report, run_button])
    query_textbox.submit(run, inputs=query_textbox, outputs=[stepper, report, run_button])


if __name__ == "__main__":
    ui.launch(
        css=CSS,
        js=JS,
        theme=gr.themes.Base(),
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 7860))
    )
