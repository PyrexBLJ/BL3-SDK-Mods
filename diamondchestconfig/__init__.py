import unrealsdk
from mods_base import build_mod, DropdownOption, SliderOption, ButtonOption, GroupedOption

chest: DropdownOption = DropdownOption("Chest To Change", "Diamond Chest", ["Diamond Chest", "Golden Chest"])
currencytype: DropdownOption = DropdownOption("Diamond Chest Currency", "Diamond Key", ["Diamond Key", "Golden Key", "Eridium", "Money"])
diamondkeyprice: SliderOption = SliderOption("Diamond Key Price", 1, 0, 5, 1, True)
goldenkeyprice: SliderOption = SliderOption("Golden Key Price", 10, 0, 50, 1, True)
eridiumprice: SliderOption = SliderOption("Eridium Price", 1000, 0, 10000, 100, True)
moneyprice: SliderOption = SliderOption("Money Price", 2500000, 0, 10000000, 100000, True)
setprices: ButtonOption = ButtonOption("Set Prices", on_press = lambda _: setinfo())

chestgroup: GroupedOption = GroupedOption("Chest", [chest])
currencygroup: GroupedOption = GroupedOption("Used Currency", [currencytype])
pricesgroup: GroupedOption = GroupedOption("Prices", [diamondkeyprice, goldenkeyprice, eridiumprice, moneyprice])
setpricesgroup: GroupedOption = GroupedOption("Apply Changes", [setprices])

def setinfo() -> None:
    chestobject = None
    if chest.value == "Diamond Chest":
        chestobject = unrealsdk.find_object("UsableTypeDefinition", "/Game/PatchDLC/DiamondLootChest/InteractiveObjects/chestobject/Data/UIData_DiamondKeyUsePrompt.UIData_DiamondKeyUsePrompt")
    elif chest.value == "Golden Chest":
        chestobject = unrealsdk.find_object("UsableTypeDefinition", "/Game/UI/InteractionPrompt/UIData_GoldenKey.UIData_GoldenKey")
    else:
        chestobject = unrealsdk.find_object("UsableTypeDefinition", "/Game/PatchDLC/DiamondLootChest/InteractiveObjects/chestobject/Data/UIData_DiamondKeyUsePrompt.UIData_DiamondKeyUsePrompt")
        print("Invalid chest selection, defaulting to diamond chest")


    if currencytype.value == "Diamond Key":
        chestobject.ActionText = 'Spend [diamondkeyicon]%i'
        chestobject.CurrencyType = unrealsdk.find_object("InventoryCategoryData", "/Game/Gear/_Shared/_Design/InventoryCategories/InventoryCategory_DiamondKey.InventoryCategory_DiamondKey")
        chestobject.Cost.BaseValueConstant = diamondkeyprice.value
    elif currencytype.value == "Golden Key":
        chestobject.ActionText = 'Spend [goldenkeyicon]%i'
        chestobject.CurrencyType = unrealsdk.find_object("InventoryCategoryData", "/Game/Gear/_Shared/_Design/InventoryCategories/InventoryCategory_GoldenKey.InventoryCategory_GoldenKey")
        chestobject.Cost.BaseValueConstant = goldenkeyprice.value
    elif currencytype.value == "Eridium":
        chestobject.ActionText = 'Spend [eridiumicon]%i'
        chestobject.CurrencyType = unrealsdk.find_object("InventoryCategoryData", "/Game/Gear/_Shared/_Design/InventoryCategories/InventoryCategory_Eridium.InventoryCategory_Eridium")
        chestobject.Cost.BaseValueConstant = eridiumprice.value
    elif currencytype.value == "Money":
        chestobject.ActionText = 'Spend [cashicon]%i'
        chestobject.CurrencyType = unrealsdk.find_object("InventoryCategoryData", "/Game/Gear/_Shared/_Design/InventoryCategories/InventoryCategory_Money.InventoryCategory_Money")
        chestobject.Cost.BaseValueConstant = moneyprice.value
    return None


build_mod(options=[chestgroup, currencygroup, pricesgroup, setpricesgroup])