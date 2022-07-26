import discord


class HandsUp:
    def __init__(self):
        self.previous_own_msg_id = 0
        self.hands_up_fields = self.init_hands_up_fields()
        self.hands_up_em = None
        self.init_embed()
        #self.hands_up_embed = discord.Embed.from_dict(self.hands_up_em)


    """
    private
    """

    def remaining_hands(self, hands_up_num : int):
        return 6 - hands_up_num


    def init_hands_up_fields(self):
        return {i: set() for i in range(7,31)}


    def init_embed(self):
        self.hands_up_fields = self.init_hands_up_fields()
        self.hands_up_em = {
            "title": "WAR LIST",
            "color": 0xff0000,
            "fields": [
                {"name": f"21@{self.remaining_hands(len(self.hands_up_fields[21]))}", "value": "なし"},
                {"name": f"22@{self.remaining_hands(len(self.hands_up_fields[22]))}", "value": "なし"},
                {"name": f"23@{self.remaining_hands(len(self.hands_up_fields[23]))}", "value": "なし"},
                {"name": f"24@{self.remaining_hands(len(self.hands_up_fields[24]))}", "value": "なし"},
            ],
        }


    def list2str(self, ls):
        players = ""
        print(f"ls:{ls}")
        if not ls:
            return "なし"
        for elem in ls:
            if players == "":
                players += elem
            else:
                players = players + ", " + elem
        return players


    async def send_msg(self, ctx):
        # 前回のembedを削除して新しいやつを表示する
        embed = discord.Embed.from_dict(self.hands_up_em)
        # 前回のボットのメッセージを消す
        msg = await ctx.channel.fetch_message(self.previous_own_msg_id)
        await msg.delete()
        # 送信
        msg = await ctx.channel.send(embed=embed)
        self.previous_own_msg_id = msg.id

    
    """
    public
    """

    async def clear_table(self, ctx):
        self.init_embed()
        embed = discord.Embed.from_dict(self.hands_up_em)
        msg = await ctx.channel.send(embed=embed)
        self.previous_own_msg_id = msg.id
        print(f"PREVIOUS_OWN_MSG_ID: {self.previous_own_msg_id}")


    async def raise_hand(self, ctx, hour: str):
        hour = int(hour)
        try:
            user_name = ctx.message.author.name
            print(user_name)
            self.hands_up_fields[hour] = self.hands_up_fields[hour] - {"仮" + user_name}
            self.hands_up_fields[hour] = self.hands_up_fields[hour] | {user_name}
            print(self.hands_up_fields[hour])
            self.hands_up_em["fields"][hour-21]["name"] = f"{hour}@{self.remaining_hands(len(self.hands_up_fields[hour]))}"
            self.hands_up_em["fields"][hour-21]["value"] = self.list2str(self.hands_up_fields[hour])
            
            await self.send_msg(ctx)
        except Exception as e:
            print(e)
            await ctx.channel.send("$clearを先に実行してください")


    async def provisional_raise_hand(self, ctx, hour: str):
        hour = int(hour)
        try:
            user_name = ctx.message.author.name
            print(user_name)
            self.hands_up_fields[hour] = self.hands_up_fields[hour] - {user_name}
            self.hands_up_fields[hour] = self.hands_up_fields[hour] | {"仮" + user_name}
            print(self.hands_up_fields[hour])
            self.hands_up_em["fields"][hour-21]["name"] = f"{hour}@{self.remaining_hands(len(self.hands_up_fields[hour]))}"
            self.hands_up_em["fields"][hour-21]["value"] = self.list2str(self.hands_up_fields[hour])
            
            await self.send_msg(ctx)
        except Exception as e:
            print(e)
            await ctx.channel.send("$clearを先に実行してください")


    async def withdraw_hand(self, ctx, hour: str):
        hour = int(hour)
        try:
            user_name = ctx.message.author.name
            print(user_name)
            self.hands_up_fields[hour] = self.hands_up_fields[hour] - {user_name, "仮" + user_name}
            self.hands_up_em["fields"][hour-21]["name"] = f"{hour}@{self.remaining_hands(len(self.hands_up_fields[hour]))}"
            self.hands_up_em["fields"][hour-21]["value"] = self.list2str(self.hands_up_fields[hour])
            
            await self.send_msg(ctx)
        except Exception as e:
            print(e)
            await ctx.channel.send("$clearを先に実行してください")