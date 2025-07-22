"""Abstract client interface (Strategy pattern)."""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Iterable, Generator, Dict

message = Dict[str, str]

class AbstractModelClient(ABC):
    """A minimal interface every concrete client must implement."""

    @abstractmethod
    def chat(
        self,
	messages: Iterable[message],
        *,
	stream: bool = False,
	**kwargs,
    ) -> str | Generator[str, None, None]: 
        """Return the model's reply or a generator of tokens."""
