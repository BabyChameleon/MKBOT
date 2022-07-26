import discord


class ImmediateAgg:
    def __init__(self):
        self.race = 0
        self.previous_own_msg_id = 0
        self.prev_total_own_score = 0
        self.total_score_per_race = 82
        self.race_history = {}
        self.embed = None
        self.init_embed()


    def init_embed(self):
        self.embed = {
            "title": "即時",
            "color": 0xff0000,
            "fields": [],
        }


    async def send_msg(self, ctx):
        # 前回のembedを削除して新しいやつを表示する
        embed = discord.Embed.from_dict(self.embed)
        # 前回のボットのメッセージを消す
        msg = await ctx.channel.fetch_message(self.previous_own_msg_id)
        await msg.delete()
        # 送信
        msg = await ctx.channel.send(embed=embed)
        self.previous_own_msg_id = msg.id


    def score_by_ranking(self, ranking):
        if ranking >= 3:
            return 13 - ranking
        elif ranking == 2:
            return 12
        elif ranking == 1:
            return 15

    
    async def aggregate(self, ctx, rankings):
        self.race += 1
        self.race_history[self.race] = rankings
        total_own_score = self.calc_total_own_score()
        total_enemy_score = (self.total_score_per_race * self.race) - total_own_score
        this_own_score = total_own_score - self.prev_total_own_score
        this_enemy_score = self.total_score_per_race - this_own_score
        self.prev_total_own_score = total_own_score
        ranking_str = ", ".join([str(ranking) for ranking in rankings])
        race_data = f"Total : {total_own_score}-{total_enemy_score} ({total_own_score - total_enemy_score}) | "\
                    f"Now : {this_own_score}-{this_enemy_score} ({this_own_score - this_enemy_score}) | "\
                    f"Ranking : {ranking_str}"
        race_name = "race" + str(self.race)
        self.embed["fields"].append({"name": race_name, "value": race_data})
        await self.send_msg(ctx)


    def calc_total_own_score(self):
        total_own_score = 0
        for race in self.race_history.values():
            for ranking in race:
                total_own_score += self.score_by_ranking(int(ranking))
        return total_own_score


    async def reset(self, ctx):
        self.race = 0
        self.race_history = {}
        self.init_embed()
        embed = discord.Embed.from_dict(self.embed)
        msg = await ctx.channel.send(embed=embed)
        self.previous_own_msg_id = msg.id


    # async def correct(self, ctx, race, rankings):
    #     self.race_history[race] = rankings
    #     await self.send_msg(ctx)