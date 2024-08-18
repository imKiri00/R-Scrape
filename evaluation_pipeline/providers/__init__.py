from .llama import LlamaProvider
from .ollama import OllamaProvider
from .groq import GroqProvider

def get_provider(provider_name, config):
    providers = {
        "llama": LlamaProvider,
        "ollama": OllamaProvider,
        "groq": GroqProvider
    }
    return providers[provider_name](config)