"""Prompt-building helpers."""
from pathlib import Path
from .config import settings

_ROOT = Path(__file__).resolve().parent
_SYSTEM_PROMPT = (_ROOT / "system_prompt.txt").read_text(encoding="utf-8")


USER_TEMPLATE = (
    "You have received the following technical question:\n"
    "{question}\n\n"
    "Please  provide:\n"
    "  • Concept explanation\n"
    "  • Implementation diagram (ASCII acceptable)\n"
    "  • Architecture specification\n"
    "  • Business use-cases\n"
    "  • Edge-case resilience strategy\n" )

USER_TEMPLATE_embeded = (
    "You have received the following technical question:\n"
    "{What is Camera Calibration}\n\n"
    "Please  provide:\n"
    "  • Concept explanation\n"
    "  • Implementation diagram (ASCII acceptable)\n"
    "  • Architecture specification\n"
    "  • Business use-cases\n"
    "  • Edge-case resilience strategy\n" )

def build_messages(question: str) -> list[dict[str, str]]:
    """Return OpenAI-compatible chat messages."""
    return [
        {"role": "system", "content": _SYSTEM_PROMPT},
        {"role": "user", "content": USER_TEMPLATE.format(question=question)},
    ]

def build_user_prompt() -> list[dict[str, str]]:
    
    return [
        {"role": "user", "content": USER_TEMPLATE_embeded},  
    ]

