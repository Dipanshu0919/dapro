import io
import sys
import traceback
import os

async def daeval(event, client, owners):
    """Handle eval commands directly."""
    if not event.sender.id in owners:
        return
    reply = await event.reply("**×•× Processing.... ×•×**")
    cmd = event.text.split(" ", maxsplit=1)[1] if " " in event.text else None
    if not cmd:
        await reply.edit("Provide some code to evaluate.")
        return

    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()

    stdout, stderr, exc = None, None, None

    try:
        await aexec(cmd, client, event)
    except Exception:
        exc = traceback.format_exc()

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()

    sys.stdout = old_stdout
    sys.stderr = old_stderr

    evaluation = ""
    if exc:
        evaluation = f"`{exc.strip()}`"
    elif stderr:
        evaluation = f"`{stderr.strip()}`"
    elif stdout:
        evaluation = f"`{stdout.strip()}`"
    else:
        evaluation = "**Success:**"
    await reply.edit(f"**•• Eval ••**\n`{cmd}`\n\n**•• Output ••**\n{evaluation}")


async def aexec(code, client, event):
    local_vars = {}
    """Helper for eval_code to execute async code."""
    exec(
        "async def __aexec(client, event): "
        + "".join(f"\n {line}" for line in code.split("\n"))
    )
    return await local_vars["__aexec"](client, event)


async def daopen(event, client):
    """Handle file opening directly."""
    if not event.reply_to:
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
