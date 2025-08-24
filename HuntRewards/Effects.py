from .Utils import AmIHost, PlayerIsHost, InFrontOfPlayer, GetPlayerCharacter, Notify, BarrelQueue, FastSpeed, SlowSpeed, SellItemsOnDelete, TalkToLilithOpt, NoHud
import random
import unrealsdk #type: ignore
from mods_base import get_pc, ENGINE #type: ignore
from unrealsdk.unreal import IGNORE_STRUCT, UObject #type: ignore

def spawnABarrel(skipqueue:bool, pc:UObject) -> None:
    global BarrelQueue
    if AmIHost():
        if skipqueue == False and pc == get_pc():
            BarrelQueue.value += 1
            BarrelQueue.save()
        barrels: list = []
        try:
            for explodyboi in unrealsdk.find_all("BP_ExplodingObject_Barrel_C", exact=False):
                if "default" not in str(explodyboi).lower():
                    if explodyboi.OakDamage.GetCurrentHealth() > 0.0 and explodyboi.ExplodingObjectState == 0:
                        barrels.append(explodyboi)
        except:
            Notify(pc, "Hunt 'Rewards'", "Got a barrel waitin for ya", 3.5)
            if pc != get_pc():
                pc.ClientMessage("Failed To Spawn Barrel", "HR", float(pc.PlayerState.PlayerID))
            return None

        if len(barrels) == 0:
            Notify(pc, "Hunt 'Rewards'", "Got a barrel waitin for ya", 3.5)
            if pc != get_pc():
                pc.ClientMessage("Failed To Spawn Barrel", "HR", float(pc.PlayerState.PlayerID))
            return None

        barrels[0].K2_SetActorLocationAndRotation(InFrontOfPlayer(pc), pc.Pawn.K2_GetActorRotation(), False, IGNORE_STRUCT, True)
        Notify(pc, "Hunt 'Rewards'", "Oh hey a barrel", 3.5)
        if pc == get_pc():
            BarrelQueue.value -= 1
            BarrelQueue.save()
            print(f"{BarrelQueue.value} barrels left in queue.")
        else:
            pc.ClientMessage("Successfully Spawned a Barrel", "HR", float(pc.PlayerState.PlayerID))
            
        barrels.clear()

    else:
        get_pc().ServerChangeName(f"{get_pc().PlayerState.PlayerID}-HR_Barrel_Troll")
    return None

def OneHealth(pc: UObject) -> None:
    if AmIHost():
        GetPlayerCharacter(pc).OakDamageComponent.SetCurrentShield(0)
        GetPlayerCharacter(pc).OakDamageComponent.SetCurrentHealth(1)
        Notify(pc, "Hunt 'Rewards'", "Dont die", 3.5)
    else:
        pc.ServerChangeName(f"{pc.PlayerState.PlayerID}-HR_1_Health")
    return None

def ZeroGravity(pc: UObject) -> None:
    if AmIHost():
        if GetPlayerCharacter(pc).OakCharacterMovement.GravityScale > 0.0:
            GetPlayerCharacter(pc).OakCharacterMovement.GravityScale = 0.0
            Notify(pc, "Hunt 'Rewards'", "Weeeeeeeeeeeeeeee!", 3.5)
        else:
            GetPlayerCharacter(pc).OakCharacterMovement.GravityScale = 1.0
    else:
        pc.ServerChangeName(f"{pc.PlayerState.PlayerID}-HR_No_Gravity")
    return None

def NoAmmo(pc: UObject) -> None:
    if AmIHost():
        for item in GetPlayerCharacter(pc).GetInventoryComponent().InventoryList.Items:
            if str(item.StoredActor) == str(GetPlayerCharacter(pc).ActiveWeapons.WeaponSlots[0].AttachedWeapon):
                item.StoredActor.UseModeState[0].AmmoComponent.ResourcePool.PoolManager.ResourcePools[item.StoredActor.UseModeState[0].AmmoComponent.ResourcePool.PoolIndexInManager].CurrentValue = 0
                item.StoredActor.UseModeState[0].AmmoComponent.LoadedAmmo = 0
                Notify(pc, "Hunt 'Rewards'", "*click*", 3.5)
    else:
        pc.ServerChangeName(f"{pc.PlayerState.PlayerID}-HR_No_Ammo")
    return None

def DropShield(pc: UObject) -> None:
    if AmIHost():
        for item in GetPlayerCharacter(pc).GetInventoryComponent().InventoryList.Items:
            if str(item.StoredActor) == str(GetPlayerCharacter(pc).EquippedInventory.InventorySlots[1].EquippedInventory):
                GetPlayerCharacter(pc).GetInventoryComponent().ServerDropItem(item.Handle, pc.Pawn.K2_GetActorLocation(), pc.K2_GetActorRotation())
                Notify(pc, "Hunt 'Rewards'", "this hurts more than i remember", 3.5)
    else:
        pc.ServerChangeName(f"{pc.PlayerState.PlayerID}-HR_Drop_Shield")
    return None

def CloseGame() -> None:
    Notify(get_pc(), "Hunt 'Rewards'", "bye.", 3.5)
    unrealsdk.find_all("KismetSystemLibrary")[0].QuitGame(get_pc(), get_pc(), 0)
    return None

def InstantDeath(pc: UObject) -> None:
    if AmIHost():
        character = pc.OakCharacter
        if character == None:
            pc.AcknowledgedPawn.DamageComponent.SetCurrentHealth(0)
            GetPlayerCharacter(pc).OakDamageComponent.SetCurrentHealth(0)
            GetPlayerCharacter(pc).BPFightForYourLifeComponent.DownStateTimeExpired(get_pc().OakCharacter.BPFightForYourLifeComponent.DownTimeResourcePool)
        elif "IronBear" in str(character):
            pc.OakCharacter.OnExiting(True)
            GetPlayerCharacter(pc).OakDamageComponent.SetCurrentHealth(0)
            GetPlayerCharacter(pc).BPFightForYourLifeComponent.DownStateTimeExpired(get_pc().OakCharacter.BPFightForYourLifeComponent.DownTimeResourcePool)
        else:
            GetPlayerCharacter(pc).OakDamageComponent.SetCurrentHealth(0)
            GetPlayerCharacter(pc).BPFightForYourLifeComponent.DownStateTimeExpired(get_pc().OakCharacter.BPFightForYourLifeComponent.DownTimeResourcePool)
        Notify(pc, "Hunt 'Rewards'", "Ouch", 3.5)
    else:
        pc.ServerChangeName(f"{pc.PlayerState.PlayerID}-HR_Instant_Death")
    return None

def ResetGameSpeed() -> None:
    ENGINE.GameViewport.World.CurrentLevel.WorldSettings.TimeDilation = 1
    return None

def FastGameSpeed() -> None:
    if ENGINE.GameViewport.World.CurrentLevel.WorldSettings.TimeDilation == SlowSpeed.value or ENGINE.GameViewport.World.CurrentLevel.WorldSettings.TimeDilation == 1:
        ENGINE.GameViewport.World.CurrentLevel.WorldSettings.TimeDilation = FastSpeed.value
        Notify(get_pc(), "Hunt 'Rewards'", "speedge", 3.5)
    else:
        ENGINE.GameViewport.World.CurrentLevel.WorldSettings.TimeDilation = 1
    return None

def SlowGameSpeed() -> None:
    if ENGINE.GameViewport.World.CurrentLevel.WorldSettings.TimeDilation == FastSpeed.value or ENGINE.GameViewport.World.CurrentLevel.WorldSettings.TimeDilation == 1:
        ENGINE.GameViewport.World.CurrentLevel.WorldSettings.TimeDilation = SlowSpeed.value
        Notify(get_pc(), "Hunt 'Rewards'", "neo mode", 3.5)
    else:
        ENGINE.GameViewport.World.CurrentLevel.WorldSettings.TimeDilation = 1
    return None

def ResetSkillTrees(pc: UObject) -> None:
    if AmIHost():
        GetPlayerCharacter(pc).OakPlayerAbilityManager.PurchaseAbilityRespec()
        Notify(pc, "Hunt 'Rewards'", "where my skills go?", 3.5)
    else:
        pc.ServerChangeName(f"{pc.PlayerState.PlayerID}-HR_Reset_Skill_Trees")
    return None

def DropHeldWeapon(pc: UObject) -> None:
    if AmIHost():
        for item in GetPlayerCharacter(pc).GetInventoryComponent().InventoryList.Items:
            if str(item.StoredActor) == str(GetPlayerCharacter(pc).ActiveWeapons.WeaponSlots[0].AttachedWeapon):
                GetPlayerCharacter(pc).GetInventoryComponent().ServerDropItem(item.Handle, pc.Pawn.K2_GetActorLocation(), pc.K2_GetActorRotation())
        Notify(pc, "Hunt 'Rewards'", "oop, butterfingers", 3.5)
    else:
        pc.ServerChangeName(f"{pc.PlayerState.PlayerID}-HR_Drop_Held_Weapon")
    return None

def DropRandomItem(pc: UObject) -> None:
    if AmIHost():
        itemcandrop: bool = False
        attempt: int = 0
        while itemcandrop == False:
            rand: int = random.randint(0, GetPlayerCharacter(pc).GetInventoryComponent().GetInventoryItemCount())
            attempt += 1
            if GetPlayerCharacter(pc).GetInventoryComponent().InventoryList.Items[rand].PlayerDroppability == 0 and str(GetPlayerCharacter(pc).GetInventoryComponent().InventoryList.Items[rand].BaseCategoryDefinition) not in ("InventoryCategoryData'/Game/Gear/_Shared/_Design/InventoryCategories/InventoryCategory_Money.InventoryCategory_Money'", "InventoryCategoryData'/Game/Gear/_Shared/_Design/InventoryCategories/InventoryCategory_Eridium.InventoryCategory_Eridium'"):
                itemcandrop = True
                GetPlayerCharacter(pc).GetInventoryComponent().ServerDropItem(GetPlayerCharacter(pc).GetInventoryComponent().InventoryList.Items[rand].Handle, InFrontOfPlayer(pc), pc.K2_GetActorRotation())
            if attempt > GetPlayerCharacter(pc).GetInventoryComponent().GetInventoryItemCount():
                itemcandrop = True
            Notify(pc, "Hunt 'Rewards'", "Hey i need that!", 3.5)
        
        itemcandrop = False
    else:
        pc.ServerChangeName(f"{pc.PlayerState.PlayerID}-HR_Drop_Random_Item")
    return None

def DropEntireInventory(pc: UObject) -> None:
    if AmIHost():
        numofitems: int = len(GetPlayerCharacter(pc).GetInventoryComponent().InventoryList.Items)
        dropindex: int = 0
        while numofitems > 0:
            if GetPlayerCharacter(pc).GetInventoryComponent().InventoryList.Items[dropindex].PlayerDroppability == 0 and str(GetPlayerCharacter(pc).GetInventoryComponent().InventoryList.Items[dropindex].BaseCategoryDefinition) not in ("InventoryCategoryData'/Game/Gear/_Shared/_Design/InventoryCategories/InventoryCategory_Money.InventoryCategory_Money'", "InventoryCategoryData'/Game/Gear/_Shared/_Design/InventoryCategories/InventoryCategory_Eridium.InventoryCategory_Eridium'"):
                GetPlayerCharacter(pc).GetInventoryComponent().ServerDropItem(GetPlayerCharacter(pc).GetInventoryComponent().InventoryList.Items[dropindex].Handle, pc.Pawn.K2_GetActorLocation(), pc.K2_GetActorRotation())
            else:
                dropindex += 1
            numofitems -= 1
        Notify(pc, "Hunt 'Rewards'", "Goodbye inventory", 3.5)
    else:
        pc.ServerChangeName(f"{pc.PlayerState.PlayerID}-HR_Drop_Entire_Inventory")
    return None

def ToggleHUD(pc: UObject) -> None:
    global NoHud
    if "Default" in str(pc.OakHUD.GetCurrentHUDState(pc)):
        pc.OakHUD.PushHUDState(pc, unrealsdk.find_object("GbxHUDStateData", "/Game/UI/HUD/HUDStates/UIData_HUDState_Menu.UIData_HUDState_Menu"), True)
        NoHud.value = True
        NoHud.save()
    else:
        NoHud.value = False
        NoHud.save()
        pc.OakHUD.ClearToDefaultHUDState(pc)
    return None

def DeleteDroppedItems(pc: UObject) -> None:
    if AmIHost():
        ognumberofitems: int = len(ENGINE.GameViewport.World.GameState.PickupList)
        numberofitems: int = len(ENGINE.GameViewport.World.GameState.PickupList)
        deleteindex: int = 0
        combinedvalue: int = 0
        while numberofitems > 0:
            if "RarityData_00_Mission" not in str(ENGINE.GameViewport.World.GameState.PickupList[deleteindex].AssociatedInventoryRarityData) and "GunRack" not in str(ENGINE.GameViewport.World.GameState.PickupList[deleteindex]):
                if SellItemsOnDelete.value == True:
                    try:
                        combinedvalue += ENGINE.GameViewport.World.GameState.PickupList[deleteindex].CachedInventoryBalanceComponent.MonetaryValue
                    except:
                        pass
                ENGINE.GameViewport.World.GameState.PickupList[deleteindex].K2_DestroyActor_DEPRECATED()
                numberofitems -= 1
            else:
                deleteindex += 1
                numberofitems -= 1
        
        for player in ENGINE.GameViewport.World.GameState.PlayerArray:
            if SellItemsOnDelete.value == True:
                player.Owner.ServerAddCurrency(combinedvalue, unrealsdk.find_object("InventoryCategoryData", "/Game/Gear/_Shared/_Design/InventoryCategories/InventoryCategory_Money.InventoryCategory_Money"))
        Notify(pc, "Hunt 'Rewards'", f"{ognumberofitems - deleteindex} Items Deleted", 3.5)
        combinedvalue = 0
    else:
        pc.ServerChangeName(f"{pc.PlayerState.PlayerID}-HR_Delete_Dropped_Items")
    return None

def TalkToLilith() -> None:
    global TalkToLilithOpt
    TalkToLilithOpt.value = True
    TalkToLilithOpt.save()
    gameplay_statics = unrealsdk.find_class("GameplayStatics").ClassDefaultObject
    gameplay_statics.OpenLevel(get_pc(), "Sanctuary3_P", True, "")
    return None