

class TelebotCommandsManager:
    def __init__(self, bot):
        self.bot = bot

    async def send_message(self, response, text, reply_markup=None):

        await self.bot.send_message(
            response.from_user.id,
            text,
            reply_markup=reply_markup)

    async def edit_message(self, response, text, reply_markup=None):

        await self.bot.edit_message_text(
            text,
            response.from_user.id,
            response.message.id,
            reply_markup=reply_markup
        )