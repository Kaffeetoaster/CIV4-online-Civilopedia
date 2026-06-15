
from python.helper.measure_duration import measure, start_new_log
import importlib




def initGameInfos():
    from python.gameContext.game import GlobalGameContext


    print("Initializing Game Infos was successful. Now Game Context contains: ")
    sum = 0
    for category, entries in GlobalGameContext.items():
        print(f"  {category}: {len(entries)} entries")
        sum += len(entries)
    print(f"  Total: {sum} entries")



