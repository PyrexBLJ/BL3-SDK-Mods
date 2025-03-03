import unrealsdk #type: ignore
from mods_base import build_mod, BoolOption, ButtonOption, GroupedOption, SliderOption, hook #type: ignore
from unrealsdk.hooks import Type, Block #type: ignore
from unrealsdk.unreal import BoundFunction, UObject, WrappedStruct #type: ignore
from typing import Any
from .pools import *

basegame: BoolOption = BoolOption("Base Game Items", True, "Yes", "No", description="Adds 45 items to the veteran rewards vendor in sanctuary")
jackpotdlc: BoolOption = BoolOption("Handsome Jackpot Items", True, "Yes", "No", description="Adds 13 items to the veteran rewards vendor in sanctuary")
tentacledlc: BoolOption = BoolOption("Guns, Love & Tentacles Items", True, "Yes", "No", description="Adds 7 items to the veteran rewards vendor in sanctuary")
fustercluckdlc: BoolOption = BoolOption("Fantastic Fustercluck Items", True, "Yes", "No", description="Adds 4 items to the veteran rewards vendor in sanctuary")
bountydlc: BoolOption = BoolOption("Bounty of Blood Items", True, "Yes", "No", description="Adds 13 items to the veteran rewards vendor in sanctuary")
miscdlc: BoolOption = BoolOption("Miscellaneous Items", True, "Yes", "No", description="Adds 18 items to the veteran rewards vendor in sanctuary")
unobtanium: BoolOption = BoolOption("Unobtainable Items", True, "Yes", "No", description="Adds 11 items to the veteran rewards vendor in sanctuary")
itemcount: SliderOption = SliderOption("Number of Items Per Vendor", 25, 9, 50, 1, True, description="How many items are in the vendor for you to pick from")

setdrops: ButtonOption = ButtonOption("Add selected dlc items to vendor", on_press = lambda _: setitems(), description="Add all items from the selected dlcs into the vendor")
removedrops: ButtonOption = ButtonOption("Remove all dlc items from vendor", on_press = lambda _: removealldlcitemsfromvendor(), description="Go back to just base game items in the vendor")
onlymissionrewards: BoolOption = BoolOption("Only Show Mission Rewards in Vendor", True, "Yes", "No")

settingsgroup: GroupedOption = GroupedOption("Configure Pools", [basegame, jackpotdlc, tentacledlc, bountydlc, fustercluckdlc, miscdlc, unobtanium, onlymissionrewards, itemcount])
applygroup: GroupedOption = GroupedOption("Apply To Vendor", [setdrops, removedrops])


def addtovendor(listtoadd: list) -> None:
    for item in listtoadd:
        itembalance = unrealsdk.make_struct("BalancedInventoryInfo", ItemPoolData=None, InventoryBalanceData=unrealsdk.find_object("InventoryBalanceData", item), ResolvedInventoryBalanceData=unrealsdk.find_object("InventoryBalanceData", item), Weight=unrealsdk.make_struct("AttributeInitializationData", BaseValueConstant=1.0, DataTableValue=unrealsdk.make_struct("DataTableValueHandle", DataTable=None, RowName="None", ValueName="None"), BaseValueAttribute=None, AttributeInitializer=None, BaseValueScale=1.0))
        unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_CrazyEarl_MissionRewards.DA_ItemPool_VendingMachine_CrazyEarl_MissionRewards").BalancedItems.append(itembalance)
    return None
    

def removealldlcitemsfromvendor() -> None:
    if len(unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_CrazyEarl_MissionRewards.DA_ItemPool_VendingMachine_CrazyEarl_MissionRewards").BalancedItems) != 0:
        while len(unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_CrazyEarl_MissionRewards.DA_ItemPool_VendingMachine_CrazyEarl_MissionRewards").BalancedItems) > 0:
            del unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_CrazyEarl_MissionRewards.DA_ItemPool_VendingMachine_CrazyEarl_MissionRewards").BalancedItems[0]
        print("Earl's DLC Vendor: Deleted dlc items from list")
    else:
        print("Earl's DLC Vendor: No need to delete items from list, skipping")
    return None

def onlymissionrewardsfunc(value: bool) -> None: # lets make a war crime rq why not, ok its getting worse someone got an error i cant reproduce where index 0 in the non item of the day pool was out of range so im just gonna try catch my way out of this like an absolute criminal
    if value == True:
        try: # i know i just said it was the non item of the day pool with the issue but i have trust issues now
            unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_CrazyEarl_OfTheDay.DA_ItemPool_VendingMachine_CrazyEarl_OfTheDay").BalancedItems[0].Weight.BaseValueConstant = 0
            unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_CrazyEarl_OfTheDay.DA_ItemPool_VendingMachine_CrazyEarl_OfTheDay").BalancedItems[0].Weight.BaseValueScale = 0
        except:
            print("Something is very broken in the item of the day pool")
        try:
            unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_CrazyEarl.DA_ItemPool_VendingMachine_CrazyEarl").BalancedItems[0].Weight.BaseValueAttribute = None
            unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_CrazyEarl.DA_ItemPool_VendingMachine_CrazyEarl").BalancedItems[0].Weight.BaseValueConstant = 0
            unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_CrazyEarl.DA_ItemPool_VendingMachine_CrazyEarl").BalancedItems[0].Weight.BaseValueScale = 0
        except:
            print("Base vendor pool index 0 error")
        try:
            unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_CrazyEarl.DA_ItemPool_VendingMachine_CrazyEarl").BalancedItems[1].Weight.BaseValueAttribute = None
            unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_CrazyEarl.DA_ItemPool_VendingMachine_CrazyEarl").BalancedItems[1].Weight.BaseValueConstant = 0
            unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_CrazyEarl.DA_ItemPool_VendingMachine_CrazyEarl").BalancedItems[1].Weight.BaseValueScale = 0
        except:
            print("Base vendor pool index 1 error")
        try:
            unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_CrazyEarl.DA_ItemPool_VendingMachine_CrazyEarl").BalancedItems[2].Weight.BaseValueAttribute = None
            unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_CrazyEarl.DA_ItemPool_VendingMachine_CrazyEarl").BalancedItems[2].Weight.BaseValueConstant = 0
            unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_CrazyEarl.DA_ItemPool_VendingMachine_CrazyEarl").BalancedItems[2].Weight.BaseValueScale = 0
        except:
            print("Base vendor pool index 2 error")
        try:
            unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_CrazyEarl.DA_ItemPool_VendingMachine_CrazyEarl").BalancedItems[3].Weight.BaseValueAttribute = None
            unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_CrazyEarl.DA_ItemPool_VendingMachine_CrazyEarl").BalancedItems[3].Weight.BaseValueConstant = 0
            unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_CrazyEarl.DA_ItemPool_VendingMachine_CrazyEarl").BalancedItems[3].Weight.BaseValueScale = 0
        except:
            print("Base vendor pool index 3 error")
        try:
            unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_CrazyEarl.DA_ItemPool_VendingMachine_CrazyEarl").BalancedItems[4].Weight.BaseValueAttribute = None
            unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_CrazyEarl.DA_ItemPool_VendingMachine_CrazyEarl").BalancedItems[4].Weight.BaseValueConstant = 0
            unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_CrazyEarl.DA_ItemPool_VendingMachine_CrazyEarl").BalancedItems[4].Weight.BaseValueScale = 0
        except:
            print("Base vendor pool index 4 error")
        try:
            unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_CrazyEarl.DA_ItemPool_VendingMachine_CrazyEarl").BalancedItems[5].Weight.BaseValueAttribute = None
            unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_CrazyEarl.DA_ItemPool_VendingMachine_CrazyEarl").BalancedItems[5].Weight.BaseValueConstant = 0
            unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_CrazyEarl.DA_ItemPool_VendingMachine_CrazyEarl").BalancedItems[5].Weight.BaseValueScale = 0
        except:
            print("Base vendor pool index 5 error")
    else:
        try:
            unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_CrazyEarl_OfTheDay.DA_ItemPool_VendingMachine_CrazyEarl_OfTheDay").BalancedItems[0].Weight.BaseValueConstant = 0.009999999776482582
            unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_CrazyEarl_OfTheDay.DA_ItemPool_VendingMachine_CrazyEarl_OfTheDay").BalancedItems[0].Weight.BaseValueScale = 1.0
        except:
            print("Something is very broken in the item of the day pool, f")
        try:
            unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_CrazyEarl.DA_ItemPool_VendingMachine_CrazyEarl").BalancedItems[0].Weight.BaseValueAttribute = unrealsdk.find_object("GbxAttributeData", "/Game/GameData/Loot/RarityWeighting/Att_RarityWeight_02_Uncommon.Att_RarityWeight_02_Uncommon")
            unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_CrazyEarl.DA_ItemPool_VendingMachine_CrazyEarl").BalancedItems[0].Weight.BaseValueConstant = 1.0
            unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_CrazyEarl.DA_ItemPool_VendingMachine_CrazyEarl").BalancedItems[0].Weight.BaseValueScale = 1.0
        except:
            print("Base vendor pool index 0 error, f")
        try:
            unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_CrazyEarl.DA_ItemPool_VendingMachine_CrazyEarl").BalancedItems[1].Weight.BaseValueAttribute = unrealsdk.find_object("GbxAttributeData", "/Game/GameData/Loot/RarityWeighting/Att_RarityWeight_03_Rare.Att_RarityWeight_03_Rare")
            unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_CrazyEarl.DA_ItemPool_VendingMachine_CrazyEarl").BalancedItems[1].Weight.BaseValueConstant = 10.0
            unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_CrazyEarl.DA_ItemPool_VendingMachine_CrazyEarl").BalancedItems[1].Weight.BaseValueScale = 1.0
        except:
            print("Base vendor pool index 1 error, f")
        try:
            unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_CrazyEarl.DA_ItemPool_VendingMachine_CrazyEarl").BalancedItems[2].Weight.BaseValueAttribute = unrealsdk.find_object("GbxAttributeData", "/Game/GameData/Loot/RarityWeighting/Att_RarityWeight_04_VeryRare.Att_RarityWeight_04_VeryRare")
            unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_CrazyEarl.DA_ItemPool_VendingMachine_CrazyEarl").BalancedItems[2].Weight.BaseValueConstant = 3.0
            unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_CrazyEarl.DA_ItemPool_VendingMachine_CrazyEarl").BalancedItems[2].Weight.BaseValueScale = 1.0
        except:
            print("Base vendor pool index 2 error, f")
        try:
            unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_CrazyEarl.DA_ItemPool_VendingMachine_CrazyEarl").BalancedItems[3].Weight.BaseValueAttribute = unrealsdk.find_object("GbxAttributeData", "/Game/GameData/Loot/RarityWeighting/Att_RarityWeight_02_Uncommon.Att_RarityWeight_02_Uncommon")
            unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_CrazyEarl.DA_ItemPool_VendingMachine_CrazyEarl").BalancedItems[3].Weight.BaseValueConstant = 1.0
            unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_CrazyEarl.DA_ItemPool_VendingMachine_CrazyEarl").BalancedItems[3].Weight.BaseValueScale = 0.30000001192092896
        except:
            print("Base vendor pool index 3 error, f")
        try:
            unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_CrazyEarl.DA_ItemPool_VendingMachine_CrazyEarl").BalancedItems[4].Weight.BaseValueAttribute = unrealsdk.find_object("GbxAttributeData", "/Game/GameData/Loot/RarityWeighting/Att_RarityWeight_03_Rare.Att_RarityWeight_03_Rare")
            unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_CrazyEarl.DA_ItemPool_VendingMachine_CrazyEarl").BalancedItems[4].Weight.BaseValueConstant = 3.0
            unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_CrazyEarl.DA_ItemPool_VendingMachine_CrazyEarl").BalancedItems[4].Weight.BaseValueScale = 0.30000001192092896
        except:
            print("Base vendor pool index 4 error, f")
        try:
            unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_CrazyEarl.DA_ItemPool_VendingMachine_CrazyEarl").BalancedItems[5].Weight.BaseValueAttribute = unrealsdk.find_object("GbxAttributeData", "/Game/GameData/Loot/RarityWeighting/Att_RarityWeight_04_VeryRare.Att_RarityWeight_04_VeryRare")
            unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_CrazyEarl.DA_ItemPool_VendingMachine_CrazyEarl").BalancedItems[5].Weight.BaseValueConstant = 1.0
            unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_CrazyEarl.DA_ItemPool_VendingMachine_CrazyEarl").BalancedItems[5].Weight.BaseValueScale = 0.30000001192092896
        except:
            print("Base vendor pool index 5 error, f")
    return None

def setitems() -> None:
    removealldlcitemsfromvendor()
    onlymissionrewardsfunc(onlymissionrewards.value)
    if basegame.value == True:
        addtovendor(basegameitems)
    if jackpotdlc.value == True:
        addtovendor(jackpotitems)
    if tentacledlc.value == True:
        addtovendor(tentacleitems)
    if fustercluckdlc.value == True:
        addtovendor(fustercluckitems)
    if bountydlc.value == True:
        addtovendor(bountyofblooditems)
    if miscdlc.value == True:
        addtovendor(miscitems)
    if unobtanium.value == True:
        addtovendor(unobtaniumitems)
    unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_CrazyEarl.DA_ItemPool_VendingMachine_CrazyEarl").Quantity.BaseValueConstant = itemcount.value
    
    print("Earl's DLC Vendor: Set dlc items in vendor")
    return None

@hook("/Game/InteractiveObjects/GameSystemMachines/VendingMachine/_Shared/Blueprints/BP_VendingMachineProxyBase.BP_VendingMachineProxyBase_C:UserConstructionScript", Type.PRE)
def setvendorpools(obj: UObject, args: WrappedStruct, _3: Any, _4: BoundFunction) -> None:
    if "CrazyEarl" in str(obj):
        setitems()
    return None

build_mod(options=[settingsgroup])