#!/usr/bin/env python
import click
from mychatai import ChatService, OpenAIClient, OllamaClient, GeminiClient,AnthropicClient, DeepSeekClient
from mychatai.utils.display import stream_to_stdout

@click.command()
@click.argument("question")
@click.option(
    "--provider", "-p",
    #type=click.Choice(["openai", "ollama", "gemini"]),
    type=click.Choice(["openai", "ollama", "anthropic", "gemini", "deepseek"]),
    default="openai",
    show_default=True,
)
@click.option("--stream/--no-stream", default=True, show_default=True)
def main(question: str, provider: str, stream: bool) -> None:
    """Ask an LLM a question from the shell."""
    if provider not in ["openai", "ollama", "gemini", "anthropic", "deepseek"]:
        raise click.BadParameter(f"Invalid provider: {provider}")   
    # Initialize the appropriate client based on the provider
    if provider == "openai":
        client = OpenAIClient()
    elif provider == "ollama":
        client = OllamaClient()
    elif provider == "gemini":
        client = GeminiClient()
    elif provider == "anthropic":
        client = AnthropicClient()
    elif provider == "deepseek":
        client = DeepSeekClient()
    else:
        raise click.BadParameter(f"Unsupported provider: {provider}")
    
    # Create the ChatService with the selected client
    chat   = ChatService(client)

    answer = chat.answer(question, stream=stream)

    if stream:
        stream_to_stdout(answer)       # type: ignore[arg-type]
    else:
        click.echo(answer)

if __name__ == "__main__":
    main()
