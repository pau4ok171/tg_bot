

class TelebotCommandsManager:
    def __init__(self, bot):
        self.bot = bot

    async def send_message(self, message, text, reply_markup):
        await self.bot.send_message(
            message.chat.id,
            text,
            reply_markup=reply_markup)

    async def edit_message(self, call, text, reply_markup):
        await self.bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.id,
            reply_markup=reply_markup
        )