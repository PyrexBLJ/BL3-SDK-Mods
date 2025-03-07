if True:
    assert __import__("mods_base").__version_info__ >= (1, 0), "Please update the SDK"

import unrealsdk

from typing import Any
from mods_base import build_mod, get_pc, keybind, hook, ENGINE, SliderOption, SpinnerOption, BoolOption, DropdownOption, Game, NestedOption
from ui_utils import show_hud_message
from unrealsdk.hooks import Type, Block
from unrealsdk.unreal import BoundFunction, UObject, WrappedStruct
from .commands import *

noclip: bool = False
godmode: bool = False
maxdashes: int = 3
currentdashes: int = 0
inPhotoMode: bool = False
firstpersoncamera = None
thirdpersoncamera = None
fixedcamera = None
currentcameramode: int = 0
HUDVisible: bool = True
damageNumbers: bool = True


blockQTD: BoolOption = BoolOption("Disable Quit to Desktop Btn", True, "Yes", "No")
FlySpeedSlider: SliderOption = SliderOption("Noclip Speed", 600, 600, 25000, 100, True)
SellItemsOnDelete: BoolOption = BoolOption("Sell deleted dropped items", False, "Yes", "No", description="This [red]WILL[/red] cause a lag spike")
SellLegendariesOnDelete: BoolOption = BoolOption("Sell/Delete Legendaries", False, "Yes", "No", description="Yes = legendaries will be sold/deleted\nNo = legendaries will stay on the ground")
SellCurrenciesOnDelete: BoolOption = BoolOption("Sell/Delete Currencies", False, "Yes", "No", description="Yes = Currencies like monel/eridium etc will be sold/deleted\nNo = Currencies will stay on the ground")
GroundItemsGroup: NestedOption = NestedOption("Sell/Delete Ground Items", [SellItemsOnDelete, SellLegendariesOnDelete, SellCurrenciesOnDelete], description="All the options for the Delete Dropped items hotkey")
DisableVendorPreview: SpinnerOption = SpinnerOption("Disable Vendor Preview", "No", ["No", "Always", "Only in Takedowns"], True, description="Disables the item of the day preview when looking at a vendor\n\nNo = Vanilla behaviour\nAlways = remove it completely\nOnly in Takedowns = leave it vanilla but remove it in takedown maps")
DeleteCorpses: BoolOption = BoolOption("Use Override Corpse Removal Time", True, "Yes", "No")
CorpseDespawnTime: SliderOption = SliderOption("Corpse Despawn Time in Seconds", 5.0, 0.1, 30.0, 0.1, False)
ConsoleFontSize: SliderOption = SliderOption("Console Font Size", 10, 1, 64, 1, True, on_change = lambda _, new_value: setConsoleFontSize(_, new_value))
LoadingScreenFadeTime: SliderOption = SliderOption("Loading Screen Fade In/Out Time", 0.5, 0, 1, 0.1, False, description="How much time the loading screen takes to fade in and out, 0.5 is the default", on_change = lambda _, new_value: setLoadingScreenFade(_, new_value))
UsePhotoModeTweaks: BoolOption = BoolOption("Enable Photo Mode Unlock", True, "Yes", "No")
PhotoModeSpeed: SliderOption = SliderOption("Photo Mode Camera Speed", 800, 100, 800, 1, True, description="Default is 100, 800 in Apoc's mod")
PhotoModeCollisionRadius: SliderOption = SliderOption("Photo Mode Camera Collision Radius", 0, 0, 30, 1, True, description="Default is 30, 0 in Apoc's mod")
PhotoModeUnlock: NestedOption = NestedOption("Photo Mode Unlock", [UsePhotoModeTweaks, PhotoModeSpeed, PhotoModeCollisionRadius], description="This is an sdk port of Apocalyptech's Photo Mode Unlock hotfix mod, settings will apply when you enter photo mode")


# Set console font size on game load
unrealsdk.find_object("Font", "/Engine/EngineFonts/Roboto.Roboto").LegacyFontSize = int(ConsoleFontSize.value)

# Set loading screen fade time on game load
ENGINE.GameInstance.LoadingScreenFadeTime = LoadingScreenFadeTime.value

def setLoadingScreenFade(_: SliderOption, new_value: float) -> None:
    ENGINE.GameInstance.LoadingScreenFadeTime = new_value
    return None

def setConsoleFontSize(_: SliderOption, new_value: int) -> None:
    unrealsdk.find_object("Font", "/Engine/EngineFonts/Roboto.Roboto").LegacyFontSize = int(new_value)
    return None

def ShowMessage(title: str, message: str, duration: int = 2) -> None:
    duration = duration * ENGINE.GameViewport.World.PersistentLevel.WorldSettings.TimeDilation
    #if get_pc().CurrentOakProfile.TutorialInfo.bTutorialsDisabled == False:
        #data = unrealsdk.construct_object("TutorialMessageDataAsset", outer=ENGINE.Outer)
        #data.Header = title
        #data.Body = message
        #data.Duration = duration
        #get_pc().ClientAddTutorialMessage(data)
    #else:
    show_hud_message(title, message, duration)
    return None


@keybind("God Mode")
def god() -> None:
    pcon = get_pc()
    pcon.OakCharacter.OakDamageComponent.bGodMode = not pcon.OakCharacter.OakDamageComponent.bGodMode
    ShowMessage("Bonk Utilities", f"God Mode: {str(pcon.OakCharacter.OakDamageComponent.bGodMode)}")

@keybind("Noclip")
def test1() -> None:
    global noclip
    pcon = get_pc()
    if noclip == False:
        pcon.OakCharacter.OakCharacterMovement.MovementMode = 5
        pcon.OakCharacter.bActorEnableCollision = False
        pcon.OakCharacter.OakDamageComponent.MinimumDamageLaunchVelocity = 9999999999
        pcon.OakCharacter.OakCharacterMovement.MaxFlySpeed.Value = FlySpeedSlider.value
    elif noclip == True:
        pcon.OakCharacter.bActorEnableCollision = True
        pcon.OakCharacter.OakCharacterMovement.MovementMode = 1
        pcon.OakCharacter.OakDamageComponent.MinimumDamageLaunchVelocity = 370
        pcon.OakCharacter.OakCharacterMovement.MaxFlySpeed.Value = 600
    noclip = not noclip
    ShowMessage("Bonk Utilities", f"Noclip: {str(noclip)}")


@keybind("Speed Up Time")
def test2() -> None:
    if ENGINE.GameViewport.World.PersistentLevel.WorldSettings.TimeDilation >= 32:
        ENGINE.GameViewport.World.PersistentLevel.WorldSettings.TimeDilation = 1
    else:
        ENGINE.GameViewport.World.PersistentLevel.WorldSettings.TimeDilation = ENGINE.GameViewport.World.PersistentLevel.WorldSettings.TimeDilation * 2
    ShowMessage("Bonk Utilities", f"Game Speed: {str(ENGINE.GameViewport.World.PersistentLevel.WorldSettings.TimeDilation)}")

@keybind("Slow Down Time")
def test3() -> None:
    if ENGINE.GameViewport.World.PersistentLevel.WorldSettings.TimeDilation <= 0.125:
        ENGINE.GameViewport.World.PersistentLevel.WorldSettings.TimeDilation = 1
    else:
        ENGINE.GameViewport.World.PersistentLevel.WorldSettings.TimeDilation = ENGINE.GameViewport.World.PersistentLevel.WorldSettings.TimeDilation / 2
    ShowMessage("Bonk Utilities", f"Game Speed: {str(ENGINE.GameViewport.World.PersistentLevel.WorldSettings.TimeDilation)}")

@keybind("Reset Cooldowns")
def cooldowns() -> None:
    for pool in get_pc().OakCharacter.ResourcePoolComponent.ResourcePools:
        if "Cooldown" in str(pool.ResourcePoolData) or "Spell" in str(pool.ResourcePoolData) or "Respawn" in str(pool.ResourcePoolData):
            pool.CurrentValue = pool.MaxValue.Value
    ShowMessage("Bonk Utilities", "Cooldowns Reset")

@keybind("Delete Dropped Items")
def deletePickups() -> None:
    ognumberofitems: int = len(ENGINE.GameViewport.World.GameState.PickupList)
    numberofitems: int = len(ENGINE.GameViewport.World.GameState.PickupList)
    deleteindex: int = 0
    if SellItemsOnDelete.value == True:
        combinedvalue: int = 0
        while numberofitems > 0:
            if "RarityData_00_Mission" not in str(ENGINE.GameViewport.World.GameState.PickupList[deleteindex].AssociatedInventoryRarityData) and "GunRack" not in str(ENGINE.GameViewport.World.GameState.PickupList[deleteindex]):
                if SellLegendariesOnDelete.value == True or SellLegendariesOnDelete.value == False and "Legendary" not in str(ENGINE.GameViewport.World.GameState.PickupList[deleteindex].AssociatedInventoryRarityData):
                    if SellCurrenciesOnDelete.value == True or SellCurrenciesOnDelete.value == False and str(ENGINE.GameViewport.World.GameState.PickupList[deleteindex].PickupCategory).split("'")[1] not in ("/Game/Gear/_Shared/_Design/InventoryCategories/InventoryCategory_Eridium.InventoryCategory_Eridium", "/Game/Gear/_Shared/_Design/InventoryCategories/InventoryCategory_Money.InventoryCategory_Money", "/Game/PatchDLC/Indigo1/Common/Pickups/IndCurrency/InventoryCategory_IndCurrency.InventoryCategory_IndCurrency"):
                        try:
                            combinedvalue += ENGINE.GameViewport.World.GameState.PickupList[deleteindex].CachedInventoryBalanceComponent.MonetaryValue
                        except:
                            print(f"no monetary value on this item, just deletin it: {str(ENGINE.GameViewport.World.GameState.PickupList[deleteindex])}")
                        ENGINE.GameViewport.World.GameState.PickupList[deleteindex].K2_DestroyActor_DEPRECATED()
                        numberofitems -= 1
                    else:
                        deleteindex += 1
                        numberofitems -= 1
                else:
                    deleteindex += 1
                    numberofitems -= 1
            else:
                deleteindex += 1
                numberofitems -= 1
        get_pc().ServerAddCurrency(combinedvalue, unrealsdk.find_object("InventoryCategoryData", "/Game/Gear/_Shared/_Design/InventoryCategories/InventoryCategory_Money.InventoryCategory_Money"))
    else:
        while numberofitems > 0:
            if "RarityData_00_Mission" not in str(ENGINE.GameViewport.World.GameState.PickupList[deleteindex].AssociatedInventoryRarityData) and "GunRack" not in str(ENGINE.GameViewport.World.GameState.PickupList[deleteindex]):
                if SellLegendariesOnDelete.value == True or SellLegendariesOnDelete.value == False and "Legendary" not in str(ENGINE.GameViewport.World.GameState.PickupList[deleteindex].AssociatedInventoryRarityData):
                    if SellCurrenciesOnDelete.value == True or SellCurrenciesOnDelete.value == False and str(ENGINE.GameViewport.World.GameState.PickupList[deleteindex].PickupCategory).split("'")[1] not in ("/Game/Gear/_Shared/_Design/InventoryCategories/InventoryCategory_Eridium.InventoryCategory_Eridium", "/Game/Gear/_Shared/_Design/InventoryCategories/InventoryCategory_Money.InventoryCategory_Money", "/Game/PatchDLC/Indigo1/Common/Pickups/IndCurrency/InventoryCategory_IndCurrency.InventoryCategory_IndCurrency"):
                        ENGINE.GameViewport.World.GameState.PickupList[deleteindex].K2_DestroyActor_DEPRECATED()
                        numberofitems -= 1
                    else:
                        deleteindex += 1
                        numberofitems -= 1
                else:
                    deleteindex += 1
                    numberofitems -= 1
            else:
                deleteindex += 1
                numberofitems -= 1
    ShowMessage("Bonk Utilities", f"{ognumberofitems - deleteindex} Items Deleted")
    

@keybind("Self Revive")
def reviveSelf() -> None:
    if get_pc().OakCharacter.BPFightForYourLifeComponent.IsInDownState() == True:
        get_pc().OakCharacter.BPFightForYourLifeComponent.ActivateSecondWind()
    return None

@keybind("Drop Held Weapon")
def dropHeldWeapon() -> None:
    for item in get_pc().OakCharacter.GetInventoryComponent().InventoryList.Items:
        if str(item.StoredActor) == str(get_pc().OakCharacter.ActiveWeapons.WeaponSlots[0].AttachedWeapon):
            get_pc().OakCharacter.GetInventoryComponent().ServerDropItem(item.Handle, get_pc().Pawn.K2_GetActorLocation(), get_pc().K2_GetActorRotation())
    return None

@keybind("Cycle Camera Mode")
def cycleCameraMode() -> None:
    global firstpersoncamera, thirdpersoncamera, fixedcamera, currentcameramode

    currentcameramode += 1
    if currentcameramode > 2:
        currentcameramode = 0

    if currentcameramode == 0:
        get_pc().OakPlayerCameraManager.CameraModesManager.CurrentMode = firstpersoncamera
        ShowMessage("Bonk Utilities", f"Set First Person")
    elif currentcameramode == 1:
        get_pc().OakPlayerCameraManager.CameraModesManager.CurrentMode = thirdpersoncamera
        ShowMessage("Bonk Utilities", f"Set Third Person")
    elif currentcameramode == 2:
        get_pc().OakPlayerCameraManager.CameraModesManager.CurrentMode = fixedcamera
        ShowMessage("Bonk Utilities", f"Set Fixed Camera")
    return None

@keybind("Toggle HUD")
def toggleHUD() -> None:
    if "Default" in str(get_pc().OakHUD.GetCurrentHUDState(get_pc())):
        get_pc().OakHUD.PushHUDState(get_pc(), unrealsdk.find_object("GbxHUDStateData", "/Game/UI/HUD/HUDStates/UIData_HUDState_Menu.UIData_HUDState_Menu"), True)
    else:
        get_pc().OakHUD.ClearToDefaultHUDState(get_pc())
    return None

@keybind("Drop Your Entire Inventory", description="Most people dont have a use for this ik")
def dropInventory() -> None:
    numofitems: int = len(get_pc().OakCharacter.GetInventoryComponent().InventoryList.Items)
    dropindex: int = 0
    while numofitems > 0:
        if get_pc().OakCharacter.GetInventoryComponent().InventoryList.Items[dropindex].PlayerDroppability > 0:
            dropindex +=1
        get_pc().OakCharacter.GetInventoryComponent().ServerDropItem(get_pc().OakCharacter.GetInventoryComponent().InventoryList.Items[dropindex].Handle, get_pc().Pawn.K2_GetActorLocation(), get_pc().K2_GetActorRotation())
        numofitems -= 1
    return None

@keybind("Drop One Item From Your Inventory", description="Most people dont have a use for this ik")
def dropOneInventory() -> None:
    dropindex: int = 0
    while get_pc().OakCharacter.GetInventoryComponent().InventoryList.Items[dropindex].PlayerDroppability > 0:
        dropindex += 1
    get_pc().OakCharacter.GetInventoryComponent().ServerDropItem(get_pc().OakCharacter.GetInventoryComponent().InventoryList.Items[dropindex].Handle, get_pc().Pawn.K2_GetActorLocation(), get_pc().K2_GetActorRotation())
    return None

@keybind("Sell Looked at Item", description="Sells & deletes the current item you are looking at on the ground, basically how the autosell feature should have been implemented in the first place")
def sellGroundItem() -> None:
    if get_pc().UseComponent.CurrentlySelectedPickup != None:
        if get_pc().UseComponent.CurrentlySelectedPickup.CachedInventoryBalanceComponent.MonetaryValue > 0 and "RarityData_00_Mission" not in str(get_pc().UseComponent.CurrentlySelectedPickup.AssociatedInventoryRarityData):
            get_pc().ServerAddCurrency(get_pc().UseComponent.CurrentlySelectedPickup.CachedInventoryBalanceComponent.MonetaryValue, unrealsdk.find_object("InventoryCategoryData", "/Game/Gear/_Shared/_Design/InventoryCategories/InventoryCategory_Money.InventoryCategory_Money"))
            unrealsdk.find_object("InventoryModuleSettings", "/Script/GbxInventory.Default__InventoryModuleSettings").PickupShrinkDuration = 0.25
            get_pc().UseComponent.CurrentlySelectedPickup.SetLifeSpan(0.01)
            get_pc().UseComponent.CurrentlySelectedPickup.OnRep_BumpAngularDir()
            get_pc().UseComponent.CurrentlySelectedPickup.bIsActive = False
            # get_pc().UseComponent.CurrentlySelectedPickup.K2_DestroyActor_DEPRECATED()
    return None

@keybind("NoTarget", description="Makes enemies ignore you")
def noTarget() -> None:
    get_pc().TeamComponent.bIsTargetableByNonPlayers = not get_pc().TeamComponent.bIsTargetableByNonPlayers
    get_pc().TeamComponent.bIsTargetableByAIPlayers = not get_pc().TeamComponent.bIsTargetableByAIPlayers
    ShowMessage("Bonk Utilities", f"NoTarget: {str(not get_pc().TeamComponent.bIsTargetableByNonPlayers)}")

@keybind("Show Damage Numbers", description="This has been changed, shouldnt crash anymore and wont persist across game boots.")
def damageNumbers() -> None:
    global damageNumbers
    damageNumbers = not damageNumbers
    for damagecomp in unrealsdk.find_all("OakDamageComponent", exact=False):
        damagecomp.bShowDamageNumbers = damageNumbers
    ShowMessage("Bonk Utilities", f"Show Damage Numbers: {str(damageNumbers)}")

@keybind("Refresh Vendor Inventories", description="Gives all loaded vendors a new inventory")
def refreshVendors() -> None:
    ENGINE.GameViewport.World.GameState.LocalSecondsBeforeShopsReset = 0
    ENGINE.GameViewport.World.GameState.ReplicatedSecondsBeforeShopsReset = 0
    ShowMessage("Bonk Utilities", f"Refreshed Shop Inventories")




if Game.get_current() is Game.BL3:
    @hook("/Script/OakGame.GFxPauseMenu:OnQuitChoiceMade", Type.PRE)
    def checkSQ(obj: UObject, args: WrappedStruct, _3: Any, _4: BoundFunction) -> type[Block] | None:
        global firstpersoncamera, thirdpersoncamera, fixedcamera
        firstpersoncamera = None
        thirdpersoncamera = None
        fixedcamera = None
        if blockQTD.value == True and args.ChoiceNameId == "QuitToDesktop":
            return Block
        else: return None
if Game.get_current() is Game.WL:
    @hook("/Script/OakGame.OakUIDataCollector_CommonMenu:OnLeaveGameChoiceMade", Type.PRE)
    def checkQTDWL(obj: UObject, args: WrappedStruct, _3: Any, _4: BoundFunction) -> type[Block] | None:
        if blockQTD.value == True and args.ChoiceNameId == "QuitToDesktop":
            return Block
        else: return None

@hook("/Script/OakGame.OakCharacter_Player:ClientEnterPhotoMode", Type.PRE)
def resetTimescalePM(obj: UObject, args: WrappedStruct, _3: Any, _4: BoundFunction) -> None:
    global inPhotoMode
    inPhotoMode = True
    if UsePhotoModeTweaks.value == True:
        photomodecamera = unrealsdk.find_all("CameraBehavior_OffsetCameraRelativeFromInputs")[-1]
        photomodecamera.MoveLimit.Min = unrealsdk.make_struct("Vector", X=-30000, Y=-30000, Z=-30000)
        photomodecamera.MoveLimit.Max = unrealsdk.make_struct("Vector", X=30000, Y=30000, Z=30000)
        photomodecamera.MoveSpeed = PhotoModeSpeed.value
        photomodecamera.CollisionRadius = PhotoModeCollisionRadius.value
    else:
        photomodecamera = unrealsdk.find_all("CameraBehavior_OffsetCameraRelativeFromInputs")[-1]
        photomodecamera.MoveLimit.Min = unrealsdk.make_struct("Vector", X=-200, Y=-200, Z=-200)
        photomodecamera.MoveLimit.Max = unrealsdk.make_struct("Vector", X=200, Y=200, Z=200)
        photomodecamera.MoveSpeed = 100.0
        photomodecamera.CollisionRadius = 30.0

    if ENGINE.GameViewport.World.PersistentLevel.WorldSettings.TimeDilation != 1:
        ENGINE.GameViewport.World.PersistentLevel.WorldSettings.TimeDilation = 1
        ShowMessage("Bonk Utilities", f"Game Speed: {str(ENGINE.GameViewport.World.PersistentLevel.WorldSettings.TimeDilation)}")
    return None

@hook("/Script/OakGame.OakCharacter_Player:ClientExitPhotoMode", Type.PRE)
def exitPhotoModeHook(obj: UObject, args: WrappedStruct, _3: Any, _4: BoundFunction) -> None:
    global inPhotoMode
    inPhotoMode = False
    return None
"""
@hook("/Script/OakGame.OakPlayerController:MantleReleased", Type.POST)
def mantleReleasedHook(obj: UObject, args: WrappedStruct, _3: Any, _4: BoundFunction) -> None:
    global inPhotoMode
    if inPhotoMode == True and obj == get_pc():
        Canvas = unrealsdk.find_object("Canvas", "/Engine/Transient.CanvasObject")
        XSize: float = Canvas.SizeX
        YSize: float = Canvas.SizeY
        unrealsdk.find_all("TestLibrary", exact=False)[0].TakeScreenshot("BL3BonkScreenshot", unrealsdk.make_struct("Vector2D", X=XSize, Y=YSize), True, True)
        unrealsdk.find_all("PhotoModeController")[-1].TakeScreenshot()
    return None
"""
@hook("/Script/OakGame.GFxExperienceBar:extFinishedDim", Type.POST)
def loadMap(obj: UObject, args: WrappedStruct, _3: Any, _4: BoundFunction) -> None:
    global firstpersoncamera, thirdpersoncamera, fixedcamera, currentcameramode
    currentcameramode = 0
    firstpersoncamera = None
    thirdpersoncamera = None
    fixedcamera = None
    for camera in unrealsdk.find_all("CameraMode")[1:]:
        if camera.Data.ModeName == "Fixed":
            fixedcamera = camera
        elif camera.Data.ModeName == "ThirdPerson":
            thirdpersoncamera = camera
        elif camera.Data.ModeName == "Default":
            firstpersoncamera = camera
    return None

@hook("/Script/GbxGameSystemCore.DamageComponent:ReceiveHealthDepleted", Type.PRE)
def enemyDied(obj: UObject, args: WrappedStruct, _3: Any, _4: BoundFunction) -> None:
    try:
        if DeleteCorpses.value == True:
            obj.GetOwner().CorpseState.bOverrideVisibleCorpseRemovalTime = True
            obj.GetOwner().CorpseState.OverrideVisibleCorpseRemovalTime = CorpseDespawnTime.value
    except:
        pass
    return None

@hook("/Script/OakGame.GFxVendingMachinePrompt:OnLookedAtByPlayer", Type.PRE)
def disableVendorPreview(obj: UObject, args: WrappedStruct, _3: Any, _4: BoundFunction) -> type[Block] | None:
    if "ItemOfTheDay" in str(obj):
        if DisableVendorPreview.value == "No":
            return None
        elif DisableVendorPreview.value == "Always":
            return Block
        elif DisableVendorPreview.value == "Only in Takedowns" and str(ENGINE.GameViewport.World.CurrentLevel) in ("Level'/Game/PatchDLC/Raid1/Maps/Raid/Raid_P.Raid_P:PersistentLevel'", "Level'/Game/PatchDLC/Takedown2/Maps/GuardianTakedown_P.GuardianTakedown_P:PersistentLevel'"):
            return Block
    return None

"""
@hook("/Game/Gear/Game/Resonator/_Design/Action_Melee_Resonator_Success.Action_Melee_Resonator_Success_C:ExecuteUbergraph_Action_Melee_Resonator_Success", Type.POST)
def bitchinator(obj: UObject, args: WrappedStruct, _3: Any, _4: BoundFunction) -> None:
    
    return None


ProcessEvent	/Script/GbxGameSystemCore.GbxAction_SimpleAnim:OnAnimEnd	/Game/Maps/Zone_0/Prologue/Prologue_P.Prologue_P:PersistentLevel.BPChar_Gunner_C_0.GbxAction.Action_Melee_Gunner_Success_C_1
ProcessEvent	/Script/GbxGameSystemCore.GbxAction:OnServerEnd	/Game/Maps/Zone_0/Prologue/Prologue_P.Prologue_P:PersistentLevel.BPChar_Gunner_C_0.GbxAction.Action_Melee_Gunner_Success_C_1
ProcessEvent	/Game/PlayerCharacters/Gunner/_Shared/_Design/Character/Melee/Action_Melee_Gunner_Success.Action_Melee_Gunner_Success_C:OnEnd	/Game/Maps/Zone_0/Prologue/Prologue_P.Prologue_P:PersistentLevel.BPChar_Gunner_C_0.GbxAction.Action_Melee_Gunner_Success_C_1
CallFunction	/Game/PlayerCharacters/Gunner/_Shared/_Design/Character/Melee/Action_Melee_Gunner_Success.Action_Melee_Gunner_Success_C:ExecuteUbergraph_Action_Melee_Gunner_Success	/Game/Maps/Zone_0/Prologue/Prologue_P.Prologue_P:PersistentLevel.BPChar_Gunner_C_0.GbxAction.Action_Melee_Gunner_Success_C_1
CallFunction	/Game/PlayerCharacters/_Shared/_Design/Melee/Action_Melee_Base.Action_Melee_Base_C:OnEnd	/Game/Maps/Zone_0/Prologue/Prologue_P.Prologue_P:PersistentLevel.BPChar_Gunner_C_0.GbxAction.Action_Melee_Gunner_Success_C_1
CallFunction	/Game/PlayerCharacters/_Shared/_Design/Melee/Action_Melee_Base.Action_Melee_Base_C:ExecuteUbergraph_Action_Melee_Base	/Game/Maps/Zone_0/Prologue/Prologue_P.Prologue_P:PersistentLevel.BPChar_Gunner_C_0.GbxAction.Action_Melee_Gunner_Success_C_1
CallFunction	/Script/OakGame.OakAction_Anim:K2_SetPlayerMeleeWeaponVisible	/Game/Maps/Zone_0/Prologue/Prologue_P.Prologue_P:PersistentLevel.BPChar_Gunner_C_0.GbxAction.Action_Melee_Gunner_Success_C_1


@hook("/Script/OakGame.OakPlayerAbilityTree:AddPointToAbilityTreeItem", Type.PRE)
def spentPoint(obj: UObject, args: WrappedStruct, _3: Any, _4: BoundFunction) -> None:
    print(args)
    return None

@hook("/Script/GbxGameSystemCore.GbxDataTableFunctionLibrary:GetDataTableValueFromHandle", Type.POST)
def GetDataTableValueFromHandleHook(obj: UObject, args: WrappedStruct, _3: Any, _4: BoundFunction) -> None:
    print(f"GetDataTableValueFromHandle: {str(args)} | {str(_3)}")
    return None

@hook("/Script/GbxGameSystemCore.GbxDataTableFunctionLibrary:GetDataTableValue", Type.POST)
def GetDataTableValueHook(obj: UObject, args: WrappedStruct, _3: Any, _4: BoundFunction) -> None:
    print(f"GetDataTableValue: {str(args)} | {str(_3)}")
    return

"""

build_mod(options=[blockQTD, FlySpeedSlider, GroundItemsGroup, DisableVendorPreview, DeleteCorpses, CorpseDespawnTime, ConsoleFontSize, LoadingScreenFadeTime, PhotoModeUnlock])