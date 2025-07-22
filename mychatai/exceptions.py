
"""Library-specific exception hierarchy."""

class MyChatAIError(Exception):
    """ Base class for all custon errors. """

class ProviderError(MyChatAIError):
    """ Unrecoverable error returned by upstream LLM Provider."""

class RetryableProviderError(ProviderError):
    """ Temporary failure - consider retry/backoff."""