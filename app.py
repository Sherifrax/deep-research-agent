import os
import gradio as gr
from dotenv import load_dotenv
from research_manager import ResearchManager, STAGE_COUNT
from styles import CSS, JS, EXAMPLES, HEADER_HTML

load_dotenv(override=True)

STEP_LABELS = ["Plan", "Search", "Write", "Deliver"]


def render_status(stage: int, message: str) -> str:
    steps = []
    for i, label in enumerate(STEP_LABELS):
        state = "done" if stage > i else ("active" if stage == i else "")
        steps.append(
            f'<div class="dr-step {state}"><span class="dr-step-dot"></span>'
            f'<span class="dr-step-label">{label}</span></div>'
        )
    return (
        '<div class="dr-status">'
        f'<div class="dr-steps">{"".join(steps)}</div>'
        f'<div class="dr-status-msg">{message}</div>'
        '</div>'
    )


async def run(query: str):
    busy_button = gr.update(interactive=False, value="Researching…")
    idle_button = gr.update(interactive=True, value="Investigate")

    if not query or not query.strip():
        yield render_status(0, "Enter a research question to get started."), "", idle_button
        return

    yield render_status(0, "Warming up..."), "", busy_button
    try:
        async for update in ResearchManager().run(query):
            if update.kind == "report":
                yield render_status(STAGE_COUNT, "Done"), update.message, idle_button
            else:
                yield render_status(update.stage, update.message), gr.update(), busy_button
    except Exception as exc:
        yield f'<div class="dr-status dr-status-error">Something went wrong: {exc}</div>', gr.update(), idle_button


with gr.Blocks(title="Deep Research") as ui:
    gr.HTML(HEADER_HTML)

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

    status = gr.HTML(elem_id="dr-status")
    report = gr.Markdown(elem_id="dr-report")

    run_button.click(run, inputs=query_textbox, outputs=[status, report, run_button])
    query_textbox.submit(run, inputs=query_textbox, outputs=[status, report, run_button])


if __name__ == "__main__":
    ui.launch(
        css=CSS,
        js=JS,
        theme=gr.themes.Base(),
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 7860))
    )
