
ai generate

usage

```python
from ai_bridge import AIBridge

async def main():
    bridge = AIBridge(config_file="config.json")

    openai_response = await bridge.ask("openai", "What is the weather like today?")
    google_response = await bridge.ask("google", "How many continents are there?")

    print("OpenAI Response:", openai_response)
    print("Google Response:", google_response)

import asyncio
asyncio.run(main())
```
