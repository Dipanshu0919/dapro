import io
import sys
import traceback
import os

__all__ = ["daeval", "daopen"]

async def daeval(event, client, owners):
    """
    Evaluates arbitrary Python code in Telegram using `.eval` command.
    
    Parameters:
        event: The Telegram event (usually a Message).
        client: The Telethon client instance.
        owners: A list of authorized user IDs.
    """
    if event.sender_id not in owners:
        return

    reply = await event.reply("**×•× Processing.... ×•×**")
    cmd = event.raw_text.split(" ", maxsplit=1)[1] if " " in event.raw_text else None

    if not cmd:
        await reply.edit("Provide some code to evaluate.")
        return

    old_stdout, old_stderr = sys.stdout, sys.stderr
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()

    exc, stdout, stderr = None, None, None

    try:
        await _aexec(cmd, client=client, event=event, owners=owners)
    except Exception:
        exc = traceback.format_exc()

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    result = ""
    if exc:
        result = f"`{exc.strip()}`"
    elif stderr:
        result = f"`{stderr.strip()}`"
    elif stdout:
        result = f"`{stdout.strip()}`"
    else:
        result = "**Success:**"

    await reply.edit(f"**•• Eval ••**\n`{cmd}`\n\n**•• Output ••**\n{result}")


async def _aexec(code: str, **kwargs):
    """
    Helper function to `exec` async code in an isolated local scope.

    Parameters:
        code: Python code as a string.
        kwargs: Variables to pass to the execution scope.
    """
    """Execute code dynamically with provided variables."""
    local_vars = {}
    global_vars = {
        "client": kwargs.get("client"),
        "event": kwargs.get("event"),
        "OWNERS": kwargs.get("owners"),
        "__name__": "__main__"
    }

    exec(
        f"async def __aexec(client, event):\n"
        + "\n".join(f"    {line}" for line in code.strip().split("\n")),
        global_vars,
        local_vars
    )

    return await local_vars["__aexec"](global_vars["client"], global_vars["event"])


async def daopen(event, client):
    """
    Opens a file sent in a replied-to message, sends its contents in chunks.

    Parameters:
        event: The Telegram event (usually a Message).
        client: The Telethon client instance.
    """
    if not event.is_reply:
        await event.reply("Please reply to a file!")
        return

    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await event.reply("No document found in the replied message.")
        return

    try:
        file_path = await client.download_media(reply_message.media)
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        chunks = [content[i:i + 4096] for i in range(0, len(content), 4096)]
        for chunk in chunks:
            await event.reply(chunk)

        os.remove(file_path)
    except Exception as e:
        await event.reply(f"An error occurred: {e}")
