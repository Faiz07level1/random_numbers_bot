from operator import itemgetter
from app.database.models import Game_len
async def gamers_statistic(gamers, ranks) -> str:

    
    gamers_stat = ""
    gamer_list = []
    rank = str()
    for gamer in gamers:
        for r in ranks:
            if r.wins <= gamer.wins:
                rank = r.rank
                break

            
        gamer_list.append({"username": gamer.username, "wins": gamer.wins, "rank": rank, "sticker": gamer.sticker if gamer.sticker else ""})
    gamer_list = sorted(gamer_list, key=itemgetter("wins"), reverse=True)

    for gamer in gamer_list:
        gamers_stat += F"\nИгрок: {gamer["username"]}{gamer["sticker"]}   Количество побед: {gamer["wins"]},  ранг: {gamer["rank"]}\n"
    return gamers_stat


async def get_rank(wins, ranks) -> str:


    gamer_level_big_then_wins = []

    for r in ranks:
        if r.wins <= wins:
            gamer_level_big_then_wins.append({"wins": r.wins, "rank": r.rank})    
    rank = sorted(gamer_level_big_then_wins, key=lambda x: x['wins'])[-1]["rank"]

    return rank

async def rank_clasification(ranks) -> str:
    text = ""
    for r in ranks:
        text += F"От {r.wins} побед - ранг: {r.rank}\n\n"
    return text




    