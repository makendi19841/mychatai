#!/usr/bin/env python
import click
from mychatai import ChatService, OpenAIClient, OllamaClient
from mychatai.utils.display import stream_to_stdout

@click.command()
@click.argument("question")
@click.option(
    "--provider", "-p",
    type=click.Choice(["openai", "ollama"]),
    default="openai",
    show_default=True,
)
@click.option("--stream/--no-stream", default=True, show_default=True)
def main(question: str, provider: str, stream: bool) -> None:
    """Ask an LLM a question from the shell."""
    client = OpenAIClient() if provider == "openai" else OllamaClient()
    chat   = ChatService(client)

    answer = chat.answer(question, stream=stream)

    if stream:
        stream_to_stdout(answer)       # type: ignore[arg-type]
    else:
        click.echo(answer)

if __name__ == "__main__":
    main()
