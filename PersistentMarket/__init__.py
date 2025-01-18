import unrealsdk #type: ignore
from mods_base import build_mod, SliderOption, hook, DropdownOption #type: ignore
from unrealsdk.hooks import Type #type: ignore
from unrealsdk.unreal import BoundFunction, UObject, WrappedStruct #type: ignore
from typing import Any

quantity: SliderOption = SliderOption("Number of Items in Vendor", 25, 9, 50, 1, True)

options: list = ["Dont Replace Pool"]

i = 1
while i <= 52:
    pool = unrealsdk.find_object("ItemPoolData", f"/Game/PatchDLC/Ixora2/Loot/VendingMachines/WeeklyPools/ItemPool_BMV_Week{i}.ItemPool_BMV_Week{i}")
    options.append(f"Week {i} - {str(pool.BalancedItems[0].InventoryBalanceData).split("_")[-1][:-1]}, {str(pool.BalancedItems[1].InventoryBalanceData).split("_")[-1][:-1]}, {str(pool.BalancedItems[2].InventoryBalanceData).split("_")[-1][:-1]}")
    pool = None
    i += 1

week: DropdownOption = DropdownOption("Selected Week: ", "Dont Replace Pool", options, description="The items in each weeks pools are listed on mental mars's black market location guide webpage. Somewhat near the bottom of the page in the \"Borderlands 3 Black Market Loot Pools\" drop down section.")

setthethings: bool = False

@hook("/Script/OakGame.VendingMachine:RegisterWithPersistenceManagerPostSpawn", Type.POST)
def setvendorpools(obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction) -> None:
    if "BlackMarket" in str(obj):
        obj.PostUseRespawnDelaySeconds = 0.0
        if str(week.value) != "Dont Replace Pool":
            obj.InventoryShopComponent.RandomlySelectedItemPools.ItemPools[0].ItemPool = unrealsdk.find_object("ItemPoolData", f"/Game/PatchDLC/Ixora2/Loot/VendingMachines/WeeklyPools/ItemPool_BMV_Week{str(week.value).split(" ")[1]}.ItemPool_BMV_Week{str(week.value).split(" ")[1]}")
            print(f"Black Market pool set to {str(week.value)}")
        obj.InventoryShopComponent.RandomlySelectedItemPools.ItemPools[0].NumberOfTimesToSelectFromThisPool.BaseValueConstant = quantity.value
    return None


@hook("/Script/Engine.PlayerController:ServerNotifyLoadedWorld", Type.POST)
def newMapLoaded(obj: UObject, args: WrappedStruct, _3: Any, _4: BoundFunction) -> None:
    global setthethings
    setthethings = True
    return None

@hook("/Script/OakGame.GFxExperienceBar:extFinishedDim", Type.POST)
def loadMap(obj: UObject, args: WrappedStruct, _3: Any, _4: BoundFunction) -> None:
    global setthethings
    if setthethings == True:
        setthethings = False
        for chest in unrealsdk.find_all("OakSingletons")[-1].LevelActorPersistenceManager.AllCurrentMapActors:
            if "Lootable" in str(chest):
                chest.PersistenceData.bStoreInSaveGame = False
    return None

build_mod()