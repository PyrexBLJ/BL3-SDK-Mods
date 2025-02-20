if True:
    assert __import__("mods_base").__version_info__ >= (1, 0), "Please update the SDK"

import unrealsdk

from typing import Any
from mods_base import build_mod, hook, ENGINE, BoolOption, ButtonOption, DropdownOption, GroupedOption
from unrealsdk.hooks import Type, Block
from unrealsdk.unreal import BoundFunction, UObject, WrappedStruct




# this is so horrifically bad in its current state im sorry ill fix it i just dont have the time rn this gotta be done by monday. (its already monday)
# plans changed, had to  revert all the changes i made




LegendaryDropRate: DropdownOption = DropdownOption("World Drop Rate", "Normal (x1)", ["x16", "x8", "Quad (x4)", "Double (x2)", "Normal (x1)", "Half (x0.5)", "Quarter (x0.25)", "No World Drops"], description="These will usually set on map load, if set pools automatically is on yes. otherwise drops will not be changed.\nIf changing to a new setting mid play session it is highly recommended to set the new value then restart the game, some things only grab their drop rates the first time they are loaded.\nNo World Drops will use the old system to remove the drops rather than the new system to set rates.\n\nIf switching from No World Drops to another option press the [red](Old System) Manually add world drops back[/red] button.")
cansetthepools: BoolOption = BoolOption("Set pools automatically", True, "Yes", "No")
manualremovedrops: ButtonOption = ButtonOption("(Old System) Manually remove world drops", on_press = lambda _: removeTheDrops())
manualadddrops: ButtonOption = ButtonOption("(Old System) Manually add world drops back", on_press = lambda _: readdTheDrops())

modoptions: GroupedOption = GroupedOption("Mod Settings", [LegendaryDropRate, cansetthepools])
applysettings: GroupedOption = GroupedOption("(Old System) Apply Settings", [manualremovedrops, manualadddrops])


basegamepools: list = [
    "/Game/GameData/Loot/ItemPools/Guns/ItemPool_Guns_All.ItemPool_Guns_All",
    "/Game/Gear/ClassMods/_Design/ItemPools/ItemPool_ClassMods.ItemPool_ClassMods",
    "/Game/GameData/Loot/ItemPools/Shields/ItemPool_Shields_All.ItemPool_Shields_All",
    "/Game/Gear/Artifacts/_Design/ItemPools/ItemPool_Artifacts.ItemPool_Artifacts",
    "/Game/GameData/Loot/ItemPools/GrenadeMods/ItemPool_GrenadeMods_All.ItemPool_GrenadeMods_All",
    "/Game/Gear/ClassMods/_Design/ItemPools/ItemPool_ClassMods_Operative.ItemPool_ClassMods_Operative",
    "/Game/Gear/ClassMods/_Design/ItemPools/ItemPool_ClassMods_Siren.ItemPool_ClassMods_Siren",
    "/Game/Gear/ClassMods/_Design/ItemPools/ItemPool_ClassMods_Gunner.ItemPool_ClassMods_Gunner",
    "/Game/Gear/ClassMods/_Design/ItemPools/ItemPool_ClassMods_Beastmaster.ItemPool_ClassMods_Beastmaster",
    "/Game/GameData/Loot/ItemPools/Guns/ItemPool_Pistols_All.ItemPool_Pistols_All",
    "/Game/GameData/Loot/ItemPools/Guns/ItemPool_ARandSMG_All.ItemPool_ARandSMG_All",
    "/Game/GameData/Loot/ItemPools/Guns/ItemPool_SniperAndHeavy_All.ItemPool_SniperAndHeavy_All",
]

hibiscuspools: list = [
    "/Game/PatchDLC/Hibiscus/GameData/Loot/ItemPool_Guns_All_Hibiscus.ItemPool_Guns_All_Hibiscus",
    "/Game/PatchDLC/Hibiscus/GameData/Loot/ItemPool_Shields_All_Hibiscus.ItemPool_Shields_All_Hibiscus",
    "/Game/PatchDLC/Hibiscus/GameData/Loot/ItemPool_GrenadeMods_All_Hibiscus.ItemPool_GrenadeMods_All_Hibiscus",
    "/Game/PatchDLC/Hibiscus/GameData/Loot/ItemPool_Hib_SniperAndHeavy_All.ItemPool_Hib_SniperAndHeavy_All",
]

dandelionpools: list = [
    "/Game/PatchDLC/Dandelion/GameData/Loot/ItemPool_Guns_All_Dandelion.ItemPool_Guns_All_Dandelion",
]

geraniumpools: list = [
    "/Game/PatchDLC/Geranium/GameData/Loot/ItemPool_Guns_All_Geranium.ItemPool_Guns_All_Geranium",
    "/Game/PatchDLC/Geranium/GameData/Loot/ItemPool_Shields_All_Geranium.ItemPool_Shields_All_Geranium",
    "/Game/PatchDLC/Geranium/GameData/Loot/ItemPool_GrenadeMods_All_Geranium.ItemPool_GrenadeMods_All_Geranium",
    "/Game/PatchDLC/Geranium/GameData/Loot/Guns/ItemPool_GER_Pistols_All.ItemPool_GER_Pistols_All",
    "/Game/PatchDLC/Geranium/GameData/Loot/Guns/ItemPool_GER_SniperAndHeavy_All.ItemPool_GER_SniperAndHeavy_All",
    "/Game/PatchDLC/Geranium/GameData/Loot/Guns/ItemPool_GER_ARandSMG_All.ItemPool_GER_ARandSMG_All",
]

alismapools: list = [
    "/Game/PatchDLC/Alisma/GameData/Loot/ItemPool_Guns_All_Alisma.ItemPool_Guns_All_Alisma",
    "/Game/PatchDLC/Alisma/GameData/Loot/ItemPool_ClassMods_All_Alisma.ItemPool_ClassMods_All_Alisma",
    "/Game/PatchDLC/Dandelion/GameData/Loot/ItemPool_Guns_All_Dandelion.ItemPool_Guns_All_Dandelion", # dont ask me why this is used in this dlc i dont know
]

ixora2pools: list = [
    "/Game/PatchDLC/Ixora2/GameData/Loot/ItemPool_Guns_All_Ixora2.ItemPool_Guns_All_Ixora2",
    "/Game/PatchDLC/Ixora2/GameData/Loot/ItemPool_Shields_All_Ixora2.ItemPool_Shields_All_Ixora2",
    "/Game/PatchDLC/Ixora2/GameData/Loot/ItemPool_GrenadeMods_All_Ixora2.ItemPool_GrenadeMods_All_Ixora2",
    "/Game/PatchDLC/Ixora2/GameData/Loot/ItemPool_Artifacts_All_Ixora2.ItemPool_Artifacts_All_Ixora2",
]

weirdpools: list = [
    "/Game/PatchDLC/Hibiscus/GameData/Loot/ItemPool_GrenadeMods_All_Hibiscus.ItemPool_GrenadeMods_All_Hibiscus",
    "/Game/PatchDLC/Dandelion/GameData/Loot/ItemPool_Guns_All_Dandelion.ItemPool_Guns_All_Dandelion",
    "/Game/PatchDLC/Geranium/GameData/Loot/ItemPool_Guns_All_Geranium.ItemPool_Guns_All_Geranium",
    "/Game/PatchDLC/Geranium/GameData/Loot/ItemPool_Shields_All_Geranium.ItemPool_Shields_All_Geranium",
    "/Game/PatchDLC/Alisma/GameData/Loot/ItemPool_Guns_All_Alisma.ItemPool_Guns_All_Alisma",
    "/Game/PatchDLC/Geranium/GameData/Loot/Guns/ItemPool_GER_ARandSMG_All.ItemPool_GER_ARandSMG_All",
    "/Game/PatchDLC/Geranium/GameData/Loot/Guns/ItemPool_GER_SniperAndHeavy_All.ItemPool_GER_SniperAndHeavy_All",
    "/Game/PatchDLC/Ixora2/GameData/Loot/ItemPool_Guns_All_Ixora2.ItemPool_Guns_All_Ixora2",
    "/Game/PatchDLC/Ixora2/GameData/Loot/ItemPool_Shields_All_Ixora2.ItemPool_Shields_All_Ixora2",
    "/Game/PatchDLC/Ixora2/GameData/Loot/ItemPool_GrenadeMods_All_Ixora2.ItemPool_GrenadeMods_All_Ixora2",
    "/Game/PatchDLC/Ixora2/GameData/Loot/ItemPool_Artifacts_All_Ixora2.ItemPool_Artifacts_All_Ixora2",
]


def vendorpool() -> None:
    # Health Vendor
    if unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_Health_OfTheDay.DA_ItemPool_VendingMachine_Health_OfTheDay") != None:
        unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_Health_OfTheDay.DA_ItemPool_VendingMachine_Health_OfTheDay").BalancedItems[2].Weight.BaseValueAttribute = None
        unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_Health_OfTheDay.DA_ItemPool_VendingMachine_Health_OfTheDay").BalancedItems[2].Weight.BaseValueConstant = 0
        unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_Health_OfTheDay.DA_ItemPool_VendingMachine_Health_OfTheDay").BalancedItems[2].Weight.BaseValueScale = 0

        unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_Health_OfTheDay.DA_ItemPool_VendingMachine_Health_OfTheDay").BalancedItems[5].Weight.BaseValueAttribute = None
        unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_Health_OfTheDay.DA_ItemPool_VendingMachine_Health_OfTheDay").BalancedItems[5].Weight.BaseValueConstant = 0
        unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_Health_OfTheDay.DA_ItemPool_VendingMachine_Health_OfTheDay").BalancedItems[5].Weight.BaseValueScale = 0

    if unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_Shields.DA_ItemPool_VendingMachine_Shields") != None:
        unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_Shields.DA_ItemPool_VendingMachine_Shields").BalancedItems[4].Weight.BaseValueAttribute = None
        unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_Shields.DA_ItemPool_VendingMachine_Shields").BalancedItems[4].Weight.BaseValueConstant = 0
        unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_Shields.DA_ItemPool_VendingMachine_Shields").BalancedItems[4].Weight.BaseValueScale = 0

    if unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_ClassMods.DA_ItemPool_VendingMachine_ClassMods") != None:
        unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_ClassMods.DA_ItemPool_VendingMachine_ClassMods").BalancedItems[4].Weight.BaseValueAttribute = None
        unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_ClassMods.DA_ItemPool_VendingMachine_ClassMods").BalancedItems[4].Weight.BaseValueConstant = 0
        unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_ClassMods.DA_ItemPool_VendingMachine_ClassMods").BalancedItems[4].Weight.BaseValueScale = 0

    # Weapon Vendor
    if unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_Weapons_OfTheDay.DA_ItemPool_VendingMachine_Weapons_OfTheDay") != None:
        unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_Weapons_OfTheDay.DA_ItemPool_VendingMachine_Weapons_OfTheDay").BalancedItems[2].Weight.BaseValueAttribute = None
        unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_Weapons_OfTheDay.DA_ItemPool_VendingMachine_Weapons_OfTheDay").BalancedItems[2].Weight.BaseValueConstant = 0
        unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_Weapons_OfTheDay.DA_ItemPool_VendingMachine_Weapons_OfTheDay").BalancedItems[2].Weight.BaseValueScale = 0

    if unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_Weapons.DA_ItemPool_VendingMachine_Weapons") != None:
        unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_Weapons.DA_ItemPool_VendingMachine_Weapons").BalancedItems[4].Weight.BaseValueAttribute = None
        unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_Weapons.DA_ItemPool_VendingMachine_Weapons").BalancedItems[4].Weight.BaseValueConstant = 0
        unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_Weapons.DA_ItemPool_VendingMachine_Weapons").BalancedItems[4].Weight.BaseValueScale = 0

    # Ammo Vendor
    if unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_Ammo_OfTheDay.DA_ItemPool_VendingMachine_Ammo_OfTheDay") != None:
        unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_Ammo_OfTheDay.DA_ItemPool_VendingMachine_Ammo_OfTheDay").BalancedItems[2].Weight.BaseValueAttribute = None
        unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_Ammo_OfTheDay.DA_ItemPool_VendingMachine_Ammo_OfTheDay").BalancedItems[2].Weight.BaseValueConstant = 0
        unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_Ammo_OfTheDay.DA_ItemPool_VendingMachine_Ammo_OfTheDay").BalancedItems[2].Weight.BaseValueScale = 0

    if unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_Grenades.DA_ItemPool_VendingMachine_Grenades") != None:
        unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_Grenades.DA_ItemPool_VendingMachine_Grenades").BalancedItems[4].Weight.BaseValueAttribute = None
        unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_Grenades.DA_ItemPool_VendingMachine_Grenades").BalancedItems[4].Weight.BaseValueConstant = 0
        unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_Grenades.DA_ItemPool_VendingMachine_Grenades").BalancedItems[4].Weight.BaseValueScale = 0
    #print("Set Base Game Vendor Pools")

def vendorpooloff() -> None:
    # Health Vendor
    if unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_Health_OfTheDay.DA_ItemPool_VendingMachine_Health_OfTheDay") != None:
        unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_Health_OfTheDay.DA_ItemPool_VendingMachine_Health_OfTheDay").BalancedItems[2].Weight.BaseValueAttribute = unrealsdk.find_object("GbxAttributeData", "/Game/GameData/Loot/RarityWeighting/Att_RarityWeight_05_Legendary.Att_RarityWeight_05_Legendary")
        unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_Health_OfTheDay.DA_ItemPool_VendingMachine_Health_OfTheDay").BalancedItems[2].Weight.BaseValueConstant = 1
        unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_Health_OfTheDay.DA_ItemPool_VendingMachine_Health_OfTheDay").BalancedItems[2].Weight.BaseValueScale = 1

        unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_Health_OfTheDay.DA_ItemPool_VendingMachine_Health_OfTheDay").BalancedItems[5].Weight.BaseValueAttribute = unrealsdk.find_object("GbxAttributeData", "/Game/GameData/Loot/RarityWeighting/Att_RarityWeight_05_Legendary.Att_RarityWeight_05_Legendary")
        unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_Health_OfTheDay.DA_ItemPool_VendingMachine_Health_OfTheDay").BalancedItems[5].Weight.BaseValueConstant = 1
        unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_Health_OfTheDay.DA_ItemPool_VendingMachine_Health_OfTheDay").BalancedItems[5].Weight.BaseValueScale = 1

    if unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_Shields.DA_ItemPool_VendingMachine_Shields") != None:
        unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_Shields.DA_ItemPool_VendingMachine_Shields").BalancedItems[4].Weight.BaseValueAttribute = unrealsdk.find_object("GbxAttributeData", "/Game/GameData/Loot/RarityWeighting/Att_RarityWeight_05_Legendary.Att_RarityWeight_05_Legendary")
        unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_Shields.DA_ItemPool_VendingMachine_Shields").BalancedItems[4].Weight.BaseValueConstant = 1
        unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_Shields.DA_ItemPool_VendingMachine_Shields").BalancedItems[4].Weight.BaseValueScale = 1

    if unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_ClassMods.DA_ItemPool_VendingMachine_ClassMods") != None:
        unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_ClassMods.DA_ItemPool_VendingMachine_ClassMods").BalancedItems[4].Weight.BaseValueAttribute = unrealsdk.find_object("GbxAttributeData", "/Game/GameData/Loot/RarityWeighting/Att_RarityWeight_05_Legendary.Att_RarityWeight_05_Legendary")
        unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_ClassMods.DA_ItemPool_VendingMachine_ClassMods").BalancedItems[4].Weight.BaseValueConstant = 1
        unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_ClassMods.DA_ItemPool_VendingMachine_ClassMods").BalancedItems[4].Weight.BaseValueScale = 1

    # Weapon Vendor
    if unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_Weapons_OfTheDay.DA_ItemPool_VendingMachine_Weapons_OfTheDay") != None:
        unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_Weapons_OfTheDay.DA_ItemPool_VendingMachine_Weapons_OfTheDay").BalancedItems[2].Weight.BaseValueAttribute = unrealsdk.find_object("GbxAttributeData", "/Game/GameData/Loot/RarityWeighting/Att_RarityWeight_05_Legendary.Att_RarityWeight_05_Legendary")
        unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_Weapons_OfTheDay.DA_ItemPool_VendingMachine_Weapons_OfTheDay").BalancedItems[2].Weight.BaseValueConstant = 1
        unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_Weapons_OfTheDay.DA_ItemPool_VendingMachine_Weapons_OfTheDay").BalancedItems[2].Weight.BaseValueScale = 1

    if unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_Weapons.DA_ItemPool_VendingMachine_Weapons") != None:
        unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_Weapons.DA_ItemPool_VendingMachine_Weapons").BalancedItems[4].Weight.BaseValueAttribute = unrealsdk.find_object("GbxAttributeData", "/Game/GameData/Loot/RarityWeighting/Att_RarityWeight_05_Legendary.Att_RarityWeight_05_Legendary")
        unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_Weapons.DA_ItemPool_VendingMachine_Weapons").BalancedItems[4].Weight.BaseValueConstant = 1
        unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_Weapons.DA_ItemPool_VendingMachine_Weapons").BalancedItems[4].Weight.BaseValueScale = 1

    # Ammo Vendor
    if unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_Ammo_OfTheDay.DA_ItemPool_VendingMachine_Ammo_OfTheDay") != None:
        unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_Ammo_OfTheDay.DA_ItemPool_VendingMachine_Ammo_OfTheDay").BalancedItems[2].Weight.BaseValueAttribute = unrealsdk.find_object("GbxAttributeData", "/Game/GameData/Loot/RarityWeighting/Att_RarityWeight_05_Legendary.Att_RarityWeight_05_Legendary")
        unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_Ammo_OfTheDay.DA_ItemPool_VendingMachine_Ammo_OfTheDay").BalancedItems[2].Weight.BaseValueConstant = 1
        unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_Ammo_OfTheDay.DA_ItemPool_VendingMachine_Ammo_OfTheDay").BalancedItems[2].Weight.BaseValueScale = 1

    if unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_Grenades.DA_ItemPool_VendingMachine_Grenades") != None:
        unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_Grenades.DA_ItemPool_VendingMachine_Grenades").BalancedItems[4].Weight.BaseValueAttribute = unrealsdk.find_object("GbxAttributeData", "/Game/GameData/Loot/RarityWeighting/Att_RarityWeight_05_Legendary.Att_RarityWeight_05_Legendary")
        unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_Grenades.DA_ItemPool_VendingMachine_Grenades").BalancedItems[4].Weight.BaseValueConstant = 1
        unrealsdk.find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/VendingMachines/DA_ItemPool_VendingMachine_Grenades.DA_ItemPool_VendingMachine_Grenades").BalancedItems[4].Weight.BaseValueScale = 1
    print("Set Base Game Vendor Pools back to normal")

def checkandsetpoolquantity(pool: str) -> None:
    if unrealsdk.find_object("ItemPoolData", pool) != None:
        unrealsdk.find_object("ItemPoolData", pool).Quantity.BaseValueConstant = 0

def setnodrops(pool: str) -> None:
    try:
        if pool not in ("/Game/PatchDLC/Alisma/GameData/Loot/EnemyPools/ItemPoolList_Boss_Alisma.ItemPoolList_Boss_Alisma", "/Game/PatchDLC/Ixora2/GameData/Loot/ItemPool_ClassMods_All_Ixora2.ItemPool_ClassMods_All_Ixora2"):
            unrealsdk.find_object("ItemPoolData", pool).BalancedItems[4].Weight.BaseValueAttribute = None
            unrealsdk.find_object("ItemPoolData", pool).BalancedItems[4].Weight.BaseValueConstant = 0
            unrealsdk.find_object("ItemPoolData", pool).BalancedItems[4].Weight.BaseValueScale = 0
        if pool in weirdpools:
            unrealsdk.find_object("ItemPoolData", pool).BalancedItems[5].Weight.BaseValueAttribute = None
            unrealsdk.find_object("ItemPoolData", pool).BalancedItems[5].Weight.BaseValueConstant = 0
            unrealsdk.find_object("ItemPoolData", pool).BalancedItems[5].Weight.BaseValueScale = 0
        if pool in ("/Game/PatchDLC/Geranium/GameData/Loot/Guns/ItemPool_GER_ARandSMG_All.ItemPool_GER_ARandSMG_All"):
            unrealsdk.find_object("ItemPoolData", pool).BalancedItems[6].Weight.BaseValueAttribute = None
            unrealsdk.find_object("ItemPoolData", pool).BalancedItems[6].Weight.BaseValueConstant = 0
            unrealsdk.find_object("ItemPoolData", pool).BalancedItems[6].Weight.BaseValueScale = 0
        if pool in ("/Game/PatchDLC/Alisma/GameData/Loot/EnemyPools/ItemPoolList_Boss_Alisma.ItemPoolList_Boss_Alisma"):
            unrealsdk.find_object("ItemPoolData", pool).BalancedItems[7].PoolProbability.BaseValueConstant = 0 # 0.30000001192092896
            unrealsdk.find_object("ItemPoolData", pool).BalancedItems[7].NumberOfTimesToSelectFromThisPool.BaseValueConstant = 0
            unrealsdk.find_object("ItemPoolData", pool).BalancedItems[8].PoolProbability.BaseValueConstant = 0
            unrealsdk.find_object("ItemPoolData", pool).BalancedItems[8].NumberOfTimesToSelectFromThisPool.BaseValueConstant = 0
        if pool in ("/Game/PatchDLC/Ixora2/GameData/Loot/ItemPool_ClassMods_All_Ixora2.ItemPool_ClassMods_All_Ixora2"):
            unrealsdk.find_object("ItemPoolData", pool).BalancedItems[8].Weight.BaseValueAttribute = None
            unrealsdk.find_object("ItemPoolData", pool).BalancedItems[8].Weight.BaseValueConstant = 0
            unrealsdk.find_object("ItemPoolData", pool).BalancedItems[8].Weight.BaseValueScale = 0
            unrealsdk.find_object("ItemPoolData", pool).BalancedItems[9].Weight.BaseValueAttribute = None
            unrealsdk.find_object("ItemPoolData", pool).BalancedItems[9].Weight.BaseValueConstant = 0
            unrealsdk.find_object("ItemPoolData", pool).BalancedItems[9].Weight.BaseValueScale = 0
    except:
        print(f"Could not find {pool}")

def setyesdrops(pool: str) -> None:
    try:
        if pool not in ("/Game/PatchDLC/Alisma/GameData/Loot/EnemyPools/ItemPoolList_Boss_Alisma.ItemPoolList_Boss_Alisma"):
            unrealsdk.find_object("ItemPoolData", pool).BalancedItems[4].Weight.BaseValueAttribute = unrealsdk.find_object("GbxAttributeData", "/Game/GameData/Loot/RarityWeighting/Att_RarityWeight_05_Legendary.Att_RarityWeight_05_Legendary")
            unrealsdk.find_object("ItemPoolData", pool).BalancedItems[4].Weight.BaseValueConstant = 1
            unrealsdk.find_object("ItemPoolData", pool).BalancedItems[4].Weight.BaseValueScale = 1
        if pool in weirdpools:
            unrealsdk.find_object("ItemPoolData", pool).BalancedItems[5].Weight.BaseValueAttribute = unrealsdk.find_object("GbxAttributeData", "/Game/GameData/Loot/RarityWeighting/Att_RarityWeight_05_Legendary.Att_RarityWeight_05_Legendary")
            unrealsdk.find_object("ItemPoolData", pool).BalancedItems[5].Weight.BaseValueConstant = 1
            unrealsdk.find_object("ItemPoolData", pool).BalancedItems[5].Weight.BaseValueScale = 1
        if pool in ("/Game/PatchDLC/Geranium/GameData/Loot/Guns/ItemPool_GER_ARandSMG_All.ItemPool_GER_ARandSMG_All"):
            unrealsdk.find_object("ItemPoolData", pool).BalancedItems[6].Weight.BaseValueAttribute = unrealsdk.find_object("GbxAttributeData", "/Game/GameData/Loot/RarityWeighting/Att_RarityWeight_05_Legendary.Att_RarityWeight_05_Legendary")
            unrealsdk.find_object("ItemPoolData", pool).BalancedItems[6].Weight.BaseValueConstant = 1
            unrealsdk.find_object("ItemPoolData", pool).BalancedItems[6].Weight.BaseValueScale = 1
        if pool in ("/Game/PatchDLC/Alisma/GameData/Loot/EnemyPools/ItemPoolList_Boss_Alisma.ItemPoolList_Boss_Alisma"):
            unrealsdk.find_object("ItemPoolData", pool).BalancedItems[7].PoolProbability.BaseValueConstant = 0.30000001192092896 # 0.30000001192092896
            unrealsdk.find_object("ItemPoolData", pool).BalancedItems[7].NumberOfTimesToSelectFromThisPool.BaseValueConstant = 1
            unrealsdk.find_object("ItemPoolData", pool).BalancedItems[8].PoolProbability.BaseValueConstant = 0.30000001192092896
            unrealsdk.find_object("ItemPoolData", pool).BalancedItems[8].NumberOfTimesToSelectFromThisPool.BaseValueConstant = 1
        if pool in ("/Game/PatchDLC/Ixora2/GameData/Loot/ItemPool_ClassMods_All_Ixora2.ItemPool_ClassMods_All_Ixora2"):
            unrealsdk.find_object("ItemPoolData", pool).BalancedItems[8].Weight.BaseValueAttribute = unrealsdk.find_object("GbxAttributeData", "/Game/GameData/Loot/RarityWeighting/Att_RarityWeight_05_Legendary.Att_RarityWeight_05_Legendary")
            unrealsdk.find_object("ItemPoolData", pool).BalancedItems[8].Weight.BaseValueConstant = 1
            unrealsdk.find_object("ItemPoolData", pool).BalancedItems[8].Weight.BaseValueScale = 1
            unrealsdk.find_object("ItemPoolData", pool).BalancedItems[9].Weight.BaseValueAttribute = unrealsdk.find_object("GbxAttributeData", "/Game/GameData/Loot/RarityWeighting/Att_RarityWeight_05_Legendary.Att_RarityWeight_05_Legendary")
            unrealsdk.find_object("ItemPoolData", pool).BalancedItems[9].Weight.BaseValueConstant = 1
            unrealsdk.find_object("ItemPoolData", pool).BalancedItems[9].Weight.BaseValueScale = 1
    except:
        print(f"Could not find {pool}")

def removeTheDrops() -> None:
    #vendorpool()
    for pool in basegamepools:
        setnodrops(pool)
    #print("Set Base Game Drop Pools")

    if "Hibiscus" in str(ENGINE.GameViewport.World.CurrentLevel):
        for pool in hibiscuspools:
            setnodrops(pool)
        try:
            unrealsdk.find_object("ItemPoolListData", "/Game/PatchDLC/Hibiscus/GameData/Loot/EnemyPools/ItemPool_EquippablesNotGuns_Hibiscus.ItemPool_EquippablesNotGuns_Hibiscus").ItemPools[3].Weight.BaseValueConstant = 0 # 0.05000000074505806
        except:
            print("Could Not Find /Game/PatchDLC/Hibiscus/GameData/Loot/EnemyPools/ItemPool_EquippablesNotGuns_Hibiscus.ItemPool_EquippablesNotGuns_Hibiscus")
        try:
            unrealsdk.find_object("ItemPoolListData", "/Game/PatchDLC/Hibiscus/GameData/Loot/EnemyPools/ItemPoolList_Boss_Hibiscus.ItemPoolList_Boss_Hibiscus").ItemPools[8].PoolProbability.BaseValueConstant = 0 # 0.5
        except:
            print("Could Not Find /Game/PatchDLC/Hibiscus/GameData/Loot/EnemyPools/ItemPoolList_Boss_Hibiscus.ItemPoolList_Boss_Hibiscus")
        try:
            unrealsdk.find_object("ItemPoolListData", "/Game/PatchDLC/Hibiscus/GameData/Loot/EnemyPools/ItemPoolList_BadassEnemyGunsGear_Hibiscus.ItemPoolList_BadassEnemyGunsGear_Hibiscus").ItemPools[5].PoolProbability.BaseValueConstant = 0 # 0.009999999776482582
        except:
            print("Could Not Find /Game/PatchDLC/Hibiscus/GameData/Loot/EnemyPools/ItemPoolList_BadassEnemyGunsGear_Hibiscus.ItemPoolList_BadassEnemyGunsGear_Hibiscus")
        try:
            unrealsdk.find_object("ItemPoolListData", "/Game/PatchDLC/Hibiscus/GameData/Loot/EnemyPools/ItemPoolList_MiniBoss_Hibiscus.ItemPoolList_MiniBoss_Hibiscus").ItemPools[5].PoolProbability.BaseValueConstant = 0
        except:
            print("Could Not Find /Game/PatchDLC/Hibiscus/GameData/Loot/EnemyPools/ItemPoolList_MiniBoss_Hibiscus.ItemPoolList_MiniBoss_Hibiscus")
        #print("Set Hibiscus Drop Pools")

    if "Dandelion" in str(ENGINE.GameViewport.World.CurrentLevel):
        for pool in dandelionpools:
            setnodrops(pool)
        
        try:
            unrealsdk.find_object("ItemPoolListData", "/Game/PatchDLC/Dandelion/GameData/Loot/EnemyPools/ItemPoolList_StandardEnemyGunsandGear_Dandelion.ItemPoolList_StandardEnemyGunsandGear_Dandelion").ItemPools[5].PoolProbability.BaseValueConstant = 0 # 0.009999999776482582
        except:
            print("Could not find /Game/PatchDLC/Dandelion/GameData/Loot/Legendary/ItemPool_ClassMods_Legendary_Dandelion.ItemPool_ClassMods_Legendary_Dandelion in ItemPoolList_StandardEnemyGunsandGear_Dandelion")
        try:
            unrealsdk.find_object("ItemPoolListData", "/Game/PatchDLC/Dandelion/GameData/Loot/EnemyPools/ItemPoolList_MiniBoss_Dandelion.ItemPoolList_MiniBoss_Dandelion").ItemPools[5].PoolProbability.BaseValueConstant = 0 # 0.009999999776482582
        except:
            print("Could not find /Game/PatchDLC/Dandelion/GameData/Loot/Legendary/ItemPool_ClassMods_Legendary_Dandelion.ItemPool_ClassMods_Legendary_Dandelion in ItemPoolList_MiniBoss_Dandelion")
        try:
            unrealsdk.find_object("ItemPoolListData", "/Game/PatchDLC/Dandelion/GameData/Loot/EnemyPools/ItemPoolList_Boss_Dandelion.ItemPoolList_Boss_Dandelion").ItemPools[5].PoolProbability.BaseValueConstant = 0 # 0.009999999776482582
        except:
            print("Could not find /Game/PatchDLC/Dandelion/GameData/Loot/Legendary/ItemPool_ClassMods_Legendary_Dandelion.ItemPool_ClassMods_Legendary_Dandelion in ItemPoolList_Boss_Dandelion")
        #print("Set Dandelion Drop Pools")

    if "Geranium" in str(ENGINE.GameViewport.World.CurrentLevel):
        for pool in geraniumpools:
            setnodrops(pool)
        #print("Set Geranium Drop Pools")

    if "Alisma" in str(ENGINE.GameViewport.World.CurrentLevel):
        for pool in alismapools:
            setnodrops(pool)
        try:
            unrealsdk.find_object("ItemPoolListData", "/Game/PatchDLC/Alisma/GameData/Loot/EnemyPools/ItemPoolList_StandardEnemyGunsandGear_Alisma.ItemPoolList_StandardEnemyGunsandGear_Alisma").ItemPools[5].PoolProbability.BaseValueConstant = 0 # 0.009999999776482582
        except:
            print("Could not find /Game/PatchDLC/Alisma/GameData/Loot/EnemyPools/ItemPoolList_StandardEnemyGunsandGear_Alisma.ItemPoolList_StandardEnemyGunsandGear_Alisma")
        try:
            unrealsdk.find_object("ItemPoolListData", "/Game/PatchDLC/Alisma/GameData/Loot/EnemyPools/ItemPoolList_Boss_Alisma.ItemPoolList_Boss_Alisma").ItemPools[2].PoolProbability.BaseValueConstant = 0
            unrealsdk.find_object("ItemPoolListData", "/Game/PatchDLC/Alisma/GameData/Loot/EnemyPools/ItemPoolList_Boss_Alisma.ItemPoolList_Boss_Alisma").ItemPools[6].PoolProbability.BaseValueConstant = 0
            unrealsdk.find_object("ItemPoolListData", "/Game/PatchDLC/Alisma/GameData/Loot/EnemyPools/ItemPoolList_Boss_Alisma.ItemPoolList_Boss_Alisma").ItemPools[7].PoolProbability.BaseValueConstant = 0
            unrealsdk.find_object("ItemPoolListData", "/Game/PatchDLC/Alisma/GameData/Loot/EnemyPools/ItemPoolList_Boss_Alisma.ItemPoolList_Boss_Alisma").ItemPools[8].PoolProbability.BaseValueConstant = 0
        except:
            print("Could not find /Game/PatchDLC/Alisma/GameData/Loot/EnemyPools/ItemPoolList_Boss_Alisma.ItemPoolList_Boss_Alisma")
        
        #print("Set Alisma Drop Pools")
    
    if "Ixora2" in str(ENGINE.GameViewport.World.CurrentLevel):
        for pool in ixora2pools:
            setnodrops(pool)
        
        #print("Set Ixora2 Drop Pools")

def readdTheDrops() -> None:
    vendorpooloff()
    for pool in basegamepools:
        setyesdrops(pool)
    print("Set Base Game Drop Pools back to normal")

    if "Hibiscus" in str(ENGINE.GameViewport.World.CurrentLevel):
        for pool in hibiscuspools:
            setyesdrops(pool)
        try:
            unrealsdk.find_object("ItemPoolListData", "/Game/PatchDLC/Hibiscus/GameData/Loot/EnemyPools/ItemPool_EquippablesNotGuns_Hibiscus.ItemPool_EquippablesNotGuns_Hibiscus").ItemPools[3].Weight.BaseValueConstant = 0 # 0.05000000074505806
        except:
            print("Could Not Find /Game/PatchDLC/Hibiscus/GameData/Loot/EnemyPools/ItemPool_EquippablesNotGuns_Hibiscus.ItemPool_EquippablesNotGuns_Hibiscus")
        try:
            unrealsdk.find_object("ItemPoolListData", "/Game/PatchDLC/Hibiscus/GameData/Loot/EnemyPools/ItemPoolList_Boss_Hibiscus.ItemPoolList_Boss_Hibiscus").ItemPools[8].PoolProbability.BaseValueConstant = 0.5 # 0.5
        except:
            print("Could Not Find /Game/PatchDLC/Hibiscus/GameData/Loot/EnemyPools/ItemPoolList_Boss_Hibiscus.ItemPoolList_Boss_Hibiscus")
        try:
            unrealsdk.find_object("ItemPoolListData", "/Game/PatchDLC/Hibiscus/GameData/Loot/EnemyPools/ItemPoolList_BadassEnemyGunsGear_Hibiscus.ItemPoolList_BadassEnemyGunsGear_Hibiscus").ItemPools[5].PoolProbability.BaseValueConstant = 0.009999999776482582 # 0.009999999776482582
        except:
            print("Could Not Find /Game/PatchDLC/Hibiscus/GameData/Loot/EnemyPools/ItemPoolList_BadassEnemyGunsGear_Hibiscus.ItemPoolList_BadassEnemyGunsGear_Hibiscus")
        try:
            unrealsdk.find_object("ItemPoolListData", "/Game/PatchDLC/Hibiscus/GameData/Loot/EnemyPools/ItemPoolList_MiniBoss_Hibiscus.ItemPoolList_MiniBoss_Hibiscus").ItemPools[5].PoolProbability.BaseValueConstant = 1.0
        except:
            print("Could Not Find /Game/PatchDLC/Hibiscus/GameData/Loot/EnemyPools/ItemPoolList_MiniBoss_Hibiscus.ItemPoolList_MiniBoss_Hibiscus")
        print("Set Hibiscus Drop Pools back to normal")

    if "Dandelion" in str(ENGINE.GameViewport.World.CurrentLevel):
        for pool in dandelionpools:
            setyesdrops(pool)
        
        try:
            unrealsdk.find_object("ItemPoolListData", "/Game/PatchDLC/Dandelion/GameData/Loot/EnemyPools/ItemPoolList_StandardEnemyGunsandGear_Dandelion.ItemPoolList_StandardEnemyGunsandGear_Dandelion").ItemPools[5].PoolProbability.BaseValueConstant = 0.009999999776482582 # 0.009999999776482582
        except:
            print("Could not find /Game/PatchDLC/Dandelion/GameData/Loot/Legendary/ItemPool_ClassMods_Legendary_Dandelion.ItemPool_ClassMods_Legendary_Dandelion in ItemPoolList_StandardEnemyGunsandGear_Dandelion")
        try:
            unrealsdk.find_object("ItemPoolListData", "/Game/PatchDLC/Dandelion/GameData/Loot/EnemyPools/ItemPoolList_MiniBoss_Dandelion.ItemPoolList_MiniBoss_Dandelion").ItemPools[5].PoolProbability.BaseValueConstant = 0.30000001192092896
        except:
            print("Could not find /Game/PatchDLC/Dandelion/GameData/Loot/Legendary/ItemPool_ClassMods_Legendary_Dandelion.ItemPool_ClassMods_Legendary_Dandelion in ItemPoolList_MiniBoss_Dandelion")
        try:
            unrealsdk.find_object("ItemPoolListData", "/Game/PatchDLC/Dandelion/GameData/Loot/EnemyPools/ItemPoolList_Boss_Dandelion.ItemPoolList_Boss_Dandelion").ItemPools[5].PoolProbability.BaseValueConstant = 0.3499999940395355
        except:
            print("Could not find /Game/PatchDLC/Dandelion/GameData/Loot/Legendary/ItemPool_ClassMods_Legendary_Dandelion.ItemPool_ClassMods_Legendary_Dandelion in ItemPoolList_Boss_Dandelion")
        print("Set Dandelion Drop Pools back to normal")

    if "Geranium" in str(ENGINE.GameViewport.World.CurrentLevel):
        for pool in geraniumpools:
            setyesdrops(pool)
        print("Set Geranium Drop Pools back to normal")

    if "Alisma" in str(ENGINE.GameViewport.World.CurrentLevel):
        for pool in alismapools:
            setyesdrops(pool)
        try:
            unrealsdk.find_object("ItemPoolListData", "/Game/PatchDLC/Alisma/GameData/Loot/EnemyPools/ItemPoolList_StandardEnemyGunsandGear_Alisma.ItemPoolList_StandardEnemyGunsandGear_Alisma").ItemPools[5].PoolProbability.BaseValueConstant = 0.009999999776482582 # 0.009999999776482582
        except:
            print("Could not find /Game/PatchDLC/Alisma/GameData/Loot/EnemyPools/ItemPoolList_StandardEnemyGunsandGear_Alisma.ItemPoolList_StandardEnemyGunsandGear_Alisma")
        try:
            unrealsdk.find_object("ItemPoolListData", "/Game/PatchDLC/Alisma/GameData/Loot/EnemyPools/ItemPoolList_Boss_Alisma.ItemPoolList_Boss_Alisma").ItemPools[2].PoolProbability.BaseValueConstant = 1.0
            unrealsdk.find_object("ItemPoolListData", "/Game/PatchDLC/Alisma/GameData/Loot/EnemyPools/ItemPoolList_Boss_Alisma.ItemPoolList_Boss_Alisma").ItemPools[6].PoolProbability.BaseValueConstant = 0.3499999940395355
            unrealsdk.find_object("ItemPoolListData", "/Game/PatchDLC/Alisma/GameData/Loot/EnemyPools/ItemPoolList_Boss_Alisma.ItemPoolList_Boss_Alisma").ItemPools[7].PoolProbability.BaseValueConstant = 0.30000001192092896
            unrealsdk.find_object("ItemPoolListData", "/Game/PatchDLC/Alisma/GameData/Loot/EnemyPools/ItemPoolList_Boss_Alisma.ItemPoolList_Boss_Alisma").ItemPools[8].PoolProbability.BaseValueConstant = 0.30000001192092896
        except:
            print("Could not find /Game/PatchDLC/Alisma/GameData/Loot/EnemyPools/ItemPoolList_Boss_Alisma.ItemPoolList_Boss_Alisma")
        print("Set Alisma Drop Pools back to normal")
    
    if "Ixora2" in str(ENGINE.GameViewport.World.CurrentLevel):
        for pool in ixora2pools:
            setyesdrops(pool)
        
        print("Set Ixora2 Drop Pools back to normal")


setthepools: bool = False
setthevendorpools: bool = False

@hook("/Script/Engine.PlayerController:ServerNotifyLoadedWorld", Type.POST)
def newMapLoaded(obj: UObject, args: WrappedStruct, _3: Any, _4: BoundFunction) -> None:
    global setthepools, setthevendorpools
    setthepools = True
    setthevendorpools = True
    return None

@hook("/Script/OakGame.GFxExperienceBar:extFinishedDim", Type.POST)
def loadMap(obj: UObject, args: WrappedStruct, _3: Any, _4: BoundFunction) -> None:
    global setthepools
    if setthepools == True:
        setthepools = False
        if cansetthepools.value == True and str(LegendaryDropRate.value) == "No World Drops":
            if ENGINE.GameViewport.World.CurrentLevel != "/Game/Maps/Sanctuary3/Sanctuary3_P.Sanctuary3_P:PersistentLevel":
                removeTheDrops()
            else:
                readdTheDrops()
    return None

#/Script/OakGame.TravelStationObject:OnTravelStationActivated
@hook("/Script/OakGame.TravelStationObject:OnTravelStationActivated", Type.POST)
def activateTravelStation(obj: UObject, args: WrappedStruct, _3: Any, _4: BoundFunction) -> None:
    if cansetthepools.value == True and str(LegendaryDropRate.value) == "No World Drops":
        removeTheDrops()
    return None

@hook("/Script/Engine.Pawn:ReceivePossessed", Type.PRE)
def somethingSpawned(obj: UObject, args: WrappedStruct, _3: Any, _4: BoundFunction) -> None:
    if cansetthepools.value == True and str(LegendaryDropRate.value) == "No World Drops":
        removeTheDrops()
    return None

#@hook("/Game/Lootables/_Design/Shared/BPIO_Lootable.BPIO_Lootable_C:ExecuteUbergraph_BPIO_Lootable", Type.POST)
#def getChest(obj: UObject, args: WrappedStruct, _3: Any, _4: BoundFunction) -> None:
    #print(str(obj))
    #return None

@hook("/Game/InteractiveObjects/GameSystemMachines/VendingMachine/_Shared/Blueprints/BP_VendingMachineProxyBase.BP_VendingMachineProxyBase_C:UserConstructionScript", Type.PRE)
def setvendorpools(obj: UObject, args: WrappedStruct, _3: Any, _4: BoundFunction) -> None:
    global setthevendorpools
    if cansetthepools.value == True and setthevendorpools == True and str(LegendaryDropRate.value) == "No World Drops":
        setthevendorpools = False
        vendorpool()


@hook("/Script/GbxGameSystemCore.GbxAttributeFunctionLibrary:GetValueOfAttribute", Type.PRE)
def GetValueOfAttributeHook(obj: UObject, args: WrappedStruct, _3: Any, _4: BoundFunction) -> type[Block] | None:
    if "Att_LocalRarityModifier_05_Legendary" in str(args.Attribute) and cansetthepools.value == True:
        print("Setting Drop Rate...")
        if LegendaryDropRate.value == "x16":
            return Block, 32000.0
        elif LegendaryDropRate.value == "x8":
            return Block, 16000.0
        elif LegendaryDropRate.value == "Quad (x4)":
            return Block, 8000.0
        elif LegendaryDropRate.value == "Double (x2)":
            return Block, 4000.0
        elif LegendaryDropRate.value == "Normal (x1)":
            return Block, 2000.0
        elif LegendaryDropRate.value == "Half (x0.5)":
            return Block, 1000.0
        elif LegendaryDropRate.value == "Quarter (x0.25)":
            return Block, 500.0
        else:
            return Block, 2000.0
    else:
        return None

    
"""
/Script/Engine.PlayerController:ServerNotifyLoadedWorld
/Game/InteractiveObjects/GameSystemMachines/ZoneMap/Design/BP_ZoneMap.BP_ZoneMap_C:K2_PostLoadedMapMesh
/Script/Engine.GameModeBase:InitializeHUDForPlayer

/Game/Lootables/_Design/Shared/BPIO_Lootable.BPIO_Lootable_C:ExecuteUbergraph_BPIO_Lootable
/Script/OakGame.GFxExperienceBar:extFinishedDim	/Engine/Transient.BPWidget_GFxExperienceBar_C_1
"""

# GbxAttributeData'/Game/GameData/Loot/RarityWeighting/Att_RarityWeight_05_Legendary.Att_RarityWeight_05_Legendary'
# unrealsdk.find_object("GbxAttributeData", "/Game/GameData/Loot/RarityWeighting/Att_RarityWeight_05_Legendary.Att_RarityWeight_05_Legendary")

"""
pools im not sure about
/Game/PatchDLC/Hibiscus/GameData/Loot/Legendary/ItemPool_ClassMods_Legendary_Hibiscus.ItemPool_ClassMods_Legendary_Hibiscus
"""

build_mod(options=[modoptions, applysettings])