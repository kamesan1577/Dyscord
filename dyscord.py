import discord
import re

#使うときはDiscord Developer PortalでServer Member Intentをオンにしてください
intents = discord.Intents.default()
intents.members = True

bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    print("On_ready")

@bot.event
async def on_message(message):
    print(message)
    if message.author.bot:
        return
    #"/save {メッセージID}"と入れるとそのメッセージを保存してくれる
    if re.fullmatch(r"/save\s\d{18}",message.content):
        saved_message = await message.channel.fetch_message(re.search(r"\d{18}",message.content).group())
        print(saved_message)
        await saved_message.reply(("保存主："+str(message.author)+"\n書き込み主："+str(saved_message.author)+"\n内容："+str(saved_message.content)+""))

    #"/delete {メッセージID}"と入れると保存されたメッセージを削除してくれる
    if re.fullmatch(r"/delete\s\d{18}",message.content):
        deleted_message = await message.channel.fetch_message(re.search(r"\d{18}",message.content).group())
        print(deleted_message)

        #人間のメッセージは削除できないようにする
        if deleted_message.author.bot:
            try:
                #もし保存主とコマンド実行者が同じなら削除
                if str(re.search(r"保存主：[^\n]*\n",deleted_message.content).group()) == "保存主："+ str(message.author)+"\n":
                    await deleted_message.delete()
                    await message.channel.send("メッセージを削除しました")
                else:
                    await message.channel.send("メッセージの保存主しか削除できません")
                    print(str(re.search(r"保存主：[^\n]*\n",deleted_message.content).group()))
                    print("保存主："+ str(message.author))
            except Exception:
                await message.channel.send("このメッセージは削除できません")
        else:
            await message.channel.send("このメッセージは削除できません")

bot.run('ここにbotのTOKENを入れる')

