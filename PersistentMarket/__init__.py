import unrealsdk #type: ignore
from mods_base import build_mod, SliderOption, hook #type: ignore
from unrealsdk.hooks import Type #type: ignore
from unrealsdk.unreal import BoundFunction, UObject, WrappedStruct #type: ignore
from typing import Any

quantity: SliderOption = SliderOption("Number of Items in Vendor", 25, 9, 50, 1, True)

setthethings: bool = False

@hook("/Script/OakGame.VendingMachine:RegisterWithPersistenceManagerPostSpawn", Type.POST)
def setvendorpools(obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction) -> None:
    if "BlackMarket" in str(obj):
        obj.PostUseRespawnDelaySeconds = 0.0
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