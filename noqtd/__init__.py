import unrealsdk
from typing import Any
from mods_base import build_mod, hook, ENGINE, BoolOption, Game
from unrealsdk.hooks import Type, Block
from unrealsdk.unreal import BoundFunction, UObject, WrappedStruct


blockQTD: BoolOption = BoolOption("Disable Quit to Desktop Btn", True, "Yes", "No")

if Game.get_current() is Game.BL3:
    blockRTM: BoolOption = BoolOption("Disable Quit To Title Screen Btn", True, "Yes", "No")

    @hook("/Script/OakGame.GFxPauseMenu:OnQuitChoiceMade", Type.PRE)
    def checkSQ(obj: UObject, args: WrappedStruct, _3: Any, _4: BoundFunction) -> type[Block] | None:
        if blockQTD.value == True and args.ChoiceNameId == "QuitToDesktop":
            return Block
        else: return None

    @hook("/Script/OakGame.GFxOakMainMenu:OnQuitChoiceMade", Type.PRE)
    def checkRTM(obj: UObject, args: WrappedStruct, _3: Any, _4: BoundFunction) -> type[Block] | None:
        if blockRTM.value == True and args.ChoiceNameId == "GbxMenu_Secondary2":
            return Block
        else: return None

if Game.get_current() is Game.WL:
    @hook("/Script/OakGame.OakUIDataCollector_CommonMenu:OnLeaveGameChoiceMade", Type.PRE)
    def checkQTDWL(obj: UObject, args: WrappedStruct, _3: Any, _4: BoundFunction) -> type[Block] | None:
        if blockQTD.value == True and args.ChoiceNameId == "QuitToDesktop":
            return Block
        else: return None


build_mod()