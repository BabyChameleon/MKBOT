#from hashlib import sha3_224
from discord.ext import commands
import discord

from hands_up import HandsUp
from immediate_agg import ImmediateAgg
from mmr import MMR
import settings

hands_up = HandsUp()
immediate_agg = ImmediateAgg()
mmr = MMR()




DISCORD_TOKEN = settings.DISCORD_TOKEN

client = discord.Client()
bot = commands.Bot(
    command_prefix="$",
    case_insensitive=True
    )


#------------------------------------------------------------------------------
# サーバーに投入されたときに使い方を表示するon_ready
@client.event
async def on_guilde():
    print('ログインしました')



# $cmd: 全コマンドを表示する
@bot.command()
async def cmd(ctx):
    embed = discord.Embed(
        title="All commands",
        color=0xff00ff,
        )
    embed.add_field(name="$start", value="即時情報を初期化します\n$raceコマンドを実行する前にこのコマンドを実行してください", inline=False)    
    embed.add_field(name="$race 味方順位 味方順位 味方順位 味方順位 味方順位 味方順位", value="例）前6の場合\n$race 1 2 3 4 5 6", inline=False)
    embed.add_field(name="$clear", value="挙手リストをクリアします", inline=False)
    embed.add_field(name="$c 時間", value="例）21時に挙手する場合\n$c 21", inline=False)
    embed.add_field(name="$rc 時間", value="例）21時に仮挙手する場合\n$rc 21", inline=False)
    embed.add_field(name="$d 時間", value="例）21時の挙手を取り下げる場合\n$c 21", inline=False)
    embed.add_field(name="$table", value="集計サイトのURLを表示する", inline=False)
    await ctx.channel.send(embed=embed)


# 集計サイト
@bot.command()
async def table(ctx):
    await ctx.channel.send("https://gb.hlorenzi.com/table")

"""
team mmr average
"""

@bot.command()
async def tmmr(ctx):
    guild_id = check_guild_id(ctx)
    #データベースに登録されているメンバー名を取ってくる
    members = mmr.fetch_team_member(guild_id)
    # loungeのコマンドを実行する
    members_str = ",".join([member for member in members])
    mmr_cmd = "^mmr " + members_str
    await ctx.channel.send(mmr_cmd)


@bot.command()
async def add(ctx, *members):
    guild_id = check_guild_id(ctx)
    #データベースにプレイヤーを登録する
    mmr.insert_member(guild_id, members)

    members_str = ", ".join([member for member in members])
    await ctx.channel.send(f"{members_str}を登録しました")


@bot.command()
async def remove(ctx, *members):
    guild_id = check_guild_id(ctx)
    #データベースからプレイヤーを削除する
    mmr.delete_member(guild_id, members)

    members_str = ", ".join([member for member in members])
    await ctx.channel.send(f"{members_str}を削除しました")


@bot.command()
async def list(ctx):
    guild_id = check_guild_id(ctx)
    #データベースに登録されているメンバー名を取ってくる
    guild_id = mmr.fetch_team_member(guild_id)
    # embedでプレイヤー一覧を取得する
    await ctx.channel.send("embed")

"""
挙手
"""

@bot.command()
async def clear(ctx):
    guild_id = check_guild_id(ctx)
    await hands_up.clear_table(ctx)


@bot.command()
async def c(ctx, hour):
    guild_id = check_guild_id(ctx)
    await hands_up.raise_hand(ctx, hour)


@bot.command()
async def rc(ctx, hour):
    guild_id = check_guild_id(ctx)
    await hands_up.provisional_raise_hand(ctx, hour)


@bot.command()
async def d(ctx, hour):
    guild_id = check_guild_id(ctx)
    await hands_up.withdraw_hand(ctx, hour)
    

"""
即時
"""

@bot.command()
async def race(ctx, r1, r2, r3, r4, r5, r6):
    guild_id = check_guild_id(ctx)
    rankings = [r1, r2, r3, r4, r5, r6]
    await immediate_agg.aggregate(ctx, rankings)


@bot.command()
async def start(ctx):
    guild_id = check_guild_id(ctx)
    await immediate_agg.reset(ctx)


# @bot.command()
# async def corr(ctx, race, r1, r2, r3, r4, r5, r6):
#     check_guild_id(ctx)
#     rankings = [r1, r2, r3, r4, r5, r6]
#     immediate_agg.correct(ctx, race, rankings)
#     await ctx.channel.send("race0 | 0-0 (0)")

"""
ID
"""

def check_guild_id(ctx):
    guild_id = ctx.guild.id
    print(f"guild_name: {ctx.guild}")
    print(f"guild_id: {ctx.guild.id}")
    return guild_id

def select_guild(guild_id):
    """
    メッセージの送信先ギルドを決定する
    と思ったけどコマンド打たれてctx.channelにメッセージを返すからそこは気にする必要はない
    guild_idの使い道はデータベースに値を保存したり取り出したりするときに使う
    
    """
    
        

    
	
    
# EXECUTES THE BOT WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.
bot.run(DISCORD_TOKEN)


"""
実装したい機能：
・挙手率の確認
・挙手
・戦績
・どれだけ積極的にチームにかかわっているか
・試合後集計を得点入力するだけで画像まで出すようにする。その時に得点を保存しておく。相手チームの得点も保存する
    大まかな機能：$startwar, $dc name score, $player これは挙手した人を表示するコマンド, $set プレイヤーと得点一覧, 
・個人の平均得点、最高得点
・データベースで管理
・外交機能
・過去戦績から対戦相手をランクづける
・複数チームでこのボットを使ってくれるようになった時のことを考えると戦績とかチームの評価スコアをデータベースに入れておくことでマリカ界隈全体のランク表作れる
・でも不正なデータを入力されると困るからどうしよ。と思ったけど自分のチームの戦績も一緒に管理するためというかそっちがメインでランク表は裏側だけで扱える存在にしておけば不正されないか
・即時
・

やること：
・複数サーバーでも使えるようにする
・挙手系のコマンドを使ったときに前回のメッセージを消す
・日時、自チーム、敵チーム、自チーム得点、敵チーム得点、点差、を記録する
・
・
・
・
・
複数サーバーで使うにはどうすればいいのか？
#発言したチャンネルのIDを取得
# channel_id = message.channel.id
これを参考にmessage.guild.id
とすればどのサーバーでコマンドが実行されたかがわかる説
channel = client.get_channel(channel_id)
await channel.send("出現しました")
これでコマンドが入力されたサーバーにメッセージを送れる
この記事で解決するかも
https://teratail.com/questions/300857
"""