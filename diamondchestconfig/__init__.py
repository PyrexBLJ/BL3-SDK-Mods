import unrealsdk
from mods_base import build_mod, DropdownOption, SliderOption, GroupedOption, hook
from unrealsdk.hooks import Type
from unrealsdk.unreal import BoundFunction, UObject, WrappedStruct
from typing import Any


DCcurrencytype: DropdownOption = DropdownOption("Selected Currency", "Diamond Key", ["Diamond Key", "Golden Key", "Eridium", "Money"])
DCdiamondkeyprice: SliderOption = SliderOption("Diamond Key Price", 1, 0, 5, 1, True)
DCgoldenkeyprice: SliderOption = SliderOption("Golden Key Price", 10, 0, 50, 1, True)
DCeridiumprice: SliderOption = SliderOption("Eridium Price", 1000, 0, 10000, 100, True)
DCmoneyprice: SliderOption = SliderOption("Money Price", 2500000, 0, 10000000, 100000, True)

GCcurrencytype: DropdownOption = DropdownOption("Selected Currency", "Gold Key", ["Diamond Key", "Golden Key", "Eridium", "Money"])
GCdiamondkeyprice: SliderOption = SliderOption("Diamond Key Price", 1, 0, 5, 1, True)
GCgoldenkeyprice: SliderOption = SliderOption("Golden Key Price", 1, 0, 50, 1, True)
GCeridiumprice: SliderOption = SliderOption("Eridium Price", 1000, 0, 10000, 100, True)
GCmoneyprice: SliderOption = SliderOption("Money Price", 2500000, 0, 10000000, 100000, True)

DiamondChest: GroupedOption = GroupedOption("Diamond Loot Room", [DCcurrencytype, DCdiamondkeyprice, DCgoldenkeyprice, DCeridiumprice, DCmoneyprice])
GoldChest: GroupedOption = GroupedOption("Gold Chest", [GCcurrencytype, GCdiamondkeyprice, GCgoldenkeyprice, GCeridiumprice, GCmoneyprice])

@hook("/Script/GbxGameSystemCore.UsableComponent:K2_CanBeUsed", Type.PRE)
def K2_CanBeUsedHook(obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction) -> None:
    if "BPIO_DiamondChest_V_3.Usable" in str(obj):
        dcchestobject = obj.PrimaryUseDefSelection.ConditionalUseDefs[0].UseDefinition

        if DCcurrencytype.value == "Diamond Key":
            dcchestobject.ActionText = 'Spend [diamondkeyicon]%i'
            dcchestobject.CurrencyType = unrealsdk.find_object("InventoryCategoryData", "/Game/Gear/_Shared/_Design/InventoryCategories/InventoryCategory_DiamondKey.InventoryCategory_DiamondKey")
            dcchestobject.Cost.BaseValueConstant = DCdiamondkeyprice.value
        elif DCcurrencytype.value == "Golden Key":
            dcchestobject.ActionText = 'Spend [goldenkeyicon]%i'
            dcchestobject.CurrencyType = unrealsdk.find_object("InventoryCategoryData", "/Game/Gear/_Shared/_Design/InventoryCategories/InventoryCategory_GoldenKey.InventoryCategory_GoldenKey")
            dcchestobject.Cost.BaseValueConstant = DCgoldenkeyprice.value
        elif DCcurrencytype.value == "Eridium":
            dcchestobject.ActionText = 'Spend [eridiumicon]%i'
            dcchestobject.CurrencyType = unrealsdk.find_object("InventoryCategoryData", "/Game/Gear/_Shared/_Design/InventoryCategories/InventoryCategory_Eridium.InventoryCategory_Eridium")
            dcchestobject.Cost.BaseValueConstant = DCeridiumprice.value
        elif DCcurrencytype.value == "Money":
            dcchestobject.ActionText = 'Spend [cashicon]%i'
            dcchestobject.CurrencyType = unrealsdk.find_object("InventoryCategoryData", "/Game/Gear/_Shared/_Design/InventoryCategories/InventoryCategory_Money.InventoryCategory_Money")
            dcchestobject.Cost.BaseValueConstant = DCmoneyprice.value

    if "BPIO_Lootable_Global_GoldenKey_" in str(obj):
        gcchestobject = obj.PrimaryUseDefSelection.DefaultUseDefinition

        if GCcurrencytype.value == "Diamond Key":
            gcchestobject.ActionText = 'Spend [diamondkeyicon]%i'
            gcchestobject.CurrencyType = unrealsdk.find_object("InventoryCategoryData", "/Game/Gear/_Shared/_Design/InventoryCategories/InventoryCategory_DiamondKey.InventoryCategory_DiamondKey")
            gcchestobject.Cost.BaseValueConstant = GCdiamondkeyprice.value
        elif GCcurrencytype.value == "Golden Key":
            gcchestobject.ActionText = 'Spend [goldenkeyicon]%i'
            gcchestobject.CurrencyType = unrealsdk.find_object("InventoryCategoryData", "/Game/Gear/_Shared/_Design/InventoryCategories/InventoryCategory_GoldenKey.InventoryCategory_GoldenKey")
            gcchestobject.Cost.BaseValueConstant = GCgoldenkeyprice.value
        elif GCcurrencytype.value == "Eridium":
            gcchestobject.ActionText = 'Spend [eridiumicon]%i'
            gcchestobject.CurrencyType = unrealsdk.find_object("InventoryCategoryData", "/Game/Gear/_Shared/_Design/InventoryCategories/InventoryCategory_Eridium.InventoryCategory_Eridium")
            gcchestobject.Cost.BaseValueConstant = GCeridiumprice.value
        elif GCcurrencytype.value == "Money":
            gcchestobject.ActionText = 'Spend [cashicon]%i'
            gcchestobject.CurrencyType = unrealsdk.find_object("InventoryCategoryData", "/Game/Gear/_Shared/_Design/InventoryCategories/InventoryCategory_Money.InventoryCategory_Money")
            gcchestobject.Cost.BaseValueConstant = GCmoneyprice.value
    return None


build_mod(options=[DiamondChest, GoldChest])