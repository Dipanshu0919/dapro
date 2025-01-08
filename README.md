# DATOE
DATOE simplifies handling `.eval` and `.open` commands in Python Telegram bots.

## Installation
```bash
pip install DATOE
```
## USAGE
```bot.py
from DATOE import eval_code_handler, open_file_handler

OWNERS = "OWNER_ID"

@client.on(events.NewMessage(pattern=".eval"))
async def eval(event):
    await eval_code_handler(event, client, OWNERS)

@client.on(events.NewMessage(pattern=".open"))
async def open_file(event):
    await open_file_handler(event, client)
```
