import unrealsdk #type: ignore
from mods_base import ENGINE, get_pc, hook, keybind, build_mod #type: ignore
from unrealsdk.hooks import Type #type: ignore
from unrealsdk.unreal import BoundFunction, UObject, WrappedStruct, IGNORE_STRUCT #type: ignore
from .Utils import BarrelQueue, FastSpeed, SlowSpeed, SellItemsOnDelete, TalkToLilithOpt, NoHud, Notify
from .Effects import *
from typing import Any



@keybind("Barrel Troll")
def barrel_Troll() -> None:
    spawnABarrel(False, get_pc())
    return None

@keybind("1 Health")
def one_Health() -> None:
    OneHealth(get_pc())
    return None

@keybind("Toggle Gravity")
def zero_Gravity_Toggle() -> None:
    ZeroGravity(get_pc())
    return None

@keybind("No Ammo")
def no_Ammo() -> None:
    NoAmmo(get_pc())
    return None

@keybind("Drop Shield")
def drop_Shield() -> None:
    DropShield(get_pc())
    return None

@keybind("Close BL3")
def close_Game() -> None:
    CloseGame()
    return None

@keybind("Instant Death")
def instant_Death() -> None:
    InstantDeath(get_pc())
    return None

@keybind("Reset Game Speed")
def reset_Game_Speed() -> None:
    ResetGameSpeed()
    return None

@keybind("Fast Game Speed")
def fast_Game_Speed() -> None:
    FastGameSpeed()
    return None

@keybind("Slow Game Speed")
def slow_Game_Speed() -> None:
    SlowGameSpeed()
    return None

@keybind("Reset Skill Trees")
def reset_Skill_Trees() -> None:
    ResetSkillTrees(get_pc())
    return None

@keybind("Drop Held Weapon")
def drop_Held_Weapon() -> None:
    DropHeldWeapon(get_pc())
    return None

@keybind("Drop Random Item")
def drop_Random_Item() -> None:
    DropRandomItem(get_pc())
    return None

@keybind("Drop Your Entire Inventory")
def drop_Inventory() -> None:
    DropEntireInventory(get_pc())
    return None

@keybind("Toggle HUD")
def toggle_HUD() -> None:
    ToggleHUD(get_pc())
    return None

@keybind("Delete Dropped Items")
def delete_Pickups() -> None:
    DeleteDroppedItems(get_pc())
    return None

@keybind("Talk To Lilith")
def talk_To_Long_Neck() -> None:
    TalkToLilith()
    return None

@hook("/Script/OakGame.GFxExperienceBar:extFinishedDim", Type.POST)
def loadMap(obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction) -> None:
    global TalkToLilithOpt, NoHud, BarrelQueue
    if TalkToLilithOpt.value == True:
        print("Talking to lilith")
        TalkToLilithOpt.value = False
        TalkToLilithOpt.save()
        Notify(get_pc(), "Hunt 'Rewards'", "Talk to Lilith.", 3.5)
        if "Sanctuary3_P" in str(ENGINE.GameViewport.World.CurrentLevel):
            loc = unrealsdk.make_struct("Vector", X=14704.2880859375, Y=-7532.5576171875, Z=-4.765133380889893)
            rot = unrealsdk.make_struct("Rotator", Pitch=0.0, Yaw=-89.46526336669922, Roll=0.0)
            get_pc().Pawn.K2_SetActorLocationAndRotation(loc, rot, False, IGNORE_STRUCT, True)
    
    if NoHud.value == True and "Default" in str(get_pc().OakHUD.GetCurrentHUDState(get_pc())):
        get_pc().OakHUD.PushHUDState(get_pc(), unrealsdk.find_object("GbxHUDStateData", "/Game/UI/HUD/HUDStates/UIData_HUDState_Menu.UIData_HUDState_Menu"), True)

    return None

count: int = 0
@hook("/Script/Engine.Actor:ReceiveTick", Type.POST)
def forbiddenTickHook(obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction) -> None:
    global count
    if "BPCont_Player_C_0" in str(obj):
        count += 1

        if count >= 15000:
            count = 0
            if BarrelQueue.value < 0:
                BarrelQueue.value = 0
                BarrelQueue.save()
            if AmIHost():
                therearebarrelshere: bool = False
                barrels: list = []
                try:
                    for explodyboi in unrealsdk.find_all("BP_ExplodingObject_Barrel_C", exact=False):
                        if "default" not in str(explodyboi).lower():
                            if explodyboi.OakDamage.GetCurrentHealth() > 0.0 and explodyboi.ExplodingObjectState == 0:
                                barrels.append(explodyboi)
                                therearebarrelshere = True
                    barrels.clear()
                except:
                    therearebarrelshere = False
                    return None
                
                if therearebarrelshere and BarrelQueue.value > 0:
                    spawnABarrel(True, get_pc())
            else:
                if BarrelQueue.value > 0:
                    spawnABarrel(False, get_pc())
    return None


@hook("/Script/Engine.PlayerController:ServerChangeName", Type.PRE)
def ServerChangeNameHook(obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction) -> None:
    
    
    if "-HR_" in args.S:
        request: list = args.S.split("-", 1)

        if str(get_pc().PlayerState.PlayerID) == request[0]:
            #print("Got a client request from ourself, this really shouldnt ever happen.")
            return None

        if request[1] == "HR_Instant_Death":
            InstantDeath(obj)

        elif request[1] == "HR_Drop_Entire_Inventory":
            DropEntireInventory(obj)
        
        elif request[1] == "HR_1_Health":
            OneHealth(obj)

        elif request[1] == "HR_No_Ammo":
            NoAmmo(obj)

        elif request[1] == "HR_Drop_Shield":
            DropShield(obj)

        elif request[1] == "HR_Reset_Skill_Trees":
            ResetSkillTrees(obj)

        elif request[1] == "HR_Drop_Held_Weapon":
            DropHeldWeapon(obj)

        elif request[1] == "HR_Drop_Random_Item":
            DropRandomItem(obj)

        elif request[1] == "HR_Delete_Dropped_Items":
            DeleteDroppedItems(obj)

        elif request[1] == "HR_No_Gravity":
            ZeroGravity(obj)
            
        elif request[1] == "HR_Barrel_Troll":
           spawnABarrel(True, obj)

    return None

@hook("/Script/Engine.PlayerController:ClientMessage", Type.PRE)
def ClientMessageHook(obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction) -> None:
    global BarrelQueue
    if args.Type == "HR":
        if args.MsgLifeTime != float(get_pc().PlayerState.PlayerID) or AmIHost():
            return None
        if args.S == "Failed To Spawn Barrel":
            BarrelQueue.value += 1
            BarrelQueue.save()
        if args.S == "Successfully Spawned a Barrel":
            BarrelQueue.value -= 1
            BarrelQueue.save()
    return None


build_mod(options=[FastSpeed, SlowSpeed, SellItemsOnDelete, BarrelQueue, NoHud, TalkToLilithOpt])