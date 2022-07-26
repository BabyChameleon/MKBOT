import discord
import motor.motor_asyncio
import asyncio

class MMR:
    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://satoimono:6ugIVJOzrlIkC97V@cluster0.d9ywe.mongodb.net/mkbot?retryWrites=true&w=majority")
        self.db = self.client["mkbot"]
        self.collection = self.db["hands_up"]


async def fetch_team_member(self, guild_id):
    members = []
    async for document in self.collection.find(filter={'guild_id':guild_id}):
        members.append(document)
        print(document)
    return members


def insert_member(self, guild_id, members):
    insert_obj = []
    for member in members:
        if member_exists(guild_id, member):
            insert_obj.append({"guild_id": guild_id, "name": member})
    self.collection.insert_many(insert_obj)


def delete_member(self, guild_id, members):
    for member in members:
        self.collection.delete_one({"guild_id": guild_id, "name": member})


def member_exists(self, guild_id, member):
    if self.collection.find(filter={'guild_id':guild_id, "name": member}):
        return True
    return False



"""
command:
mmrコマンドに渡すプレイヤー一覧表示
mmrコマンドに渡すプレイヤー追加
mmrコマンドに渡すプレイヤー削除
チームmmr実行     e.g. ^mmr Karana,Quilt,haf,takagisan,albinoEs,sunbeams
引数ありとなしで分けるデフォルト引数をNoneにしておいてNoneかどうかで処理を分ける
$emmr (easy mmr)
登録されているプレイヤー一覧をボタンにして簡単に実行できるようにする 
"""