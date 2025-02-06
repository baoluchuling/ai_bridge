
ai generate

usage

```python
from ai_bridge import AIBridge

async def main():
    # 通过加载配置文件动态注册提供商
    bridge = AIBridge(config_file="config.json")

    # 使用已注册的提供商
    openai_response = await bridge.ask("openai", "What is the weather like today?")
    google_response = await bridge.ask("google", "How many continents are there?")

    print("OpenAI Response:", openai_response)
    print("Google Response:", google_response)

import asyncio
asyncio.run(main())
```
