#!/usr/bin/env python
import gradio as gr
from gradio.exceptions import Error as GradioError

from mychatai import (
    ChatService,
    OpenAIClient,
    OllamaClient,
    GeminiClient,
    AnthropicClient,
    DeepSeekClient,
)
from mychatai.config import settings   # ← to check which keys exist


# ── Build a client based on dropdown choice ──────────────────────────────────
def make_client(provider: str):
    if provider == "openai":
        if not settings.openai_api_key:
            raise GradioError("OPENAI_API_KEY not set in this environment.")
        return OpenAIClient()

    if provider == "ollama":
        return OllamaClient()

    if provider == "gemini":
        if not settings.gemini_api_key:
            raise GradioError("GOOGLE_API_KEY (Gemini) not set.")
        return GeminiClient()

    if provider == "anthropic":
        if not settings.anthropic_api_key:
            raise GradioError("ANTHROPIC_API_KEY not set.")
        return AnthropicClient()

    if provider == "deepseek":
        if not settings.deepseek_api_key:
            raise GradioError("DEEPSEEK_API_KEY not set.")
        return DeepSeekClient()

    raise GradioError(f"Unknown provider: {provider}")


# ── Core inference function Gradio calls ─────────────────────────────────────
def chat_with_llm(provider: str, question: str, stream: bool):
    chat = ChatService(make_client(provider))

    answer_iter = chat.answer(question, stream=stream)
    if stream:
        # answer_iter is a generator
        for token in answer_iter:              # type: ignore[arg-type]
            yield token
    else:
        yield answer_iter                      # full string

# ── Gradio UI setup ───────────────────────────────────────────────────────────
with gr.Blocks(title="MyChatAI") as demo:
    gr.Markdown("Chat with LLMs")
    
    with gr.Row():
        provider = gr.Dropdown(
            choices=["openai", "ollama", "gemini", "anthropic", "deepseek"],
            label="LLM Provider",
            value="ollama",
            interactive=True, 
        )
        question = gr.Textbox(label="Ask a question:", placeholder="Type your question here...")
        stream = gr.Checkbox(label="Stream response", value=True)

    answer_box = gr.Textbox(label="Answer")

    ask_btn = gr.Button("Ask")
    
    ask_btn.click(
        chat_with_llm,
        inputs=[provider, question, stream],
        outputs=answer_box,
        api_name="chat_with_llm"
    )

# ── Launch the Gradio app ───────────────────────────────────────────────────
if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=True, debug=True)