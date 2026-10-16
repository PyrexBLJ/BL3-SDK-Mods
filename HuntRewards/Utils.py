import unrealsdk #type: ignore
from unrealsdk.unreal import UObject, IGNORE_STRUCT #type: ignore
from mods_base import get_pc, ENGINE, HiddenOption, BoolOption, SliderOption #type: ignore

FastSpeed: SliderOption = SliderOption("Fast Game Speed:", 2, 2, 16, 1, True)
SlowSpeed: SliderOption = SliderOption("Slow Game Speed:", 0.5, 0.001, 0.99, 0.01, False)
SellItemsOnDelete: BoolOption = BoolOption("Sell deleted dropped items", False, "Yes", "No")
BarrelQueue: HiddenOption = HiddenOption("Barrel Queue", 0)
NoHud: HiddenOption = HiddenOption("No Hud", False)
TalkToLilithOpt: HiddenOption = HiddenOption("Talk To Lilith", False)

def InFrontOfPlayer(player: UObject) -> UObject:
    x = player.Pawn.K2_GetActorLocation().X + (player.GetActorForwardVector().X * 200)
    y = player.Pawn.K2_GetActorLocation().Y + (player.GetActorForwardVector().Y * 200)
    loc = unrealsdk.make_struct("Vector", X=x, Y=y, Z=player.Pawn.K2_GetActorLocation().Z)
    return loc

def AmIHost() -> bool:
    if get_pc().PlayerState == ENGINE.GameViewport.World.GameState.HostPlayerState:
        return True
    else:
        return False
    
def PlayerIsHost(pc: UObject) -> bool:
    if pc.PlayerState == ENGINE.GameViewport.World.GameState.HostPlayerState:
        return True
    else:
        return False
    
def GetPlayerCharacter(player: UObject) -> UObject:
    if player.OakCharacter == None:
        return player.PrimaryCharacter
    if "IronBear" in str(player.OakCharacter):
        return player.OakCharacter.Gunner
    else:
        return player.OakCharacter
    
def Notify(player: UObject, title: str, msg: str, duration: float) -> None:
    player.DisplayRolloutNotification(title, msg, duration * ENGINE.GameViewport.World.CurrentLevel.WorldSettings.TimeDilation)
    return None

def get_spawn_point() -> UObject | None:
    OakSpawnPoint = unrealsdk.construct_object("OakSpawnPoint", outer=ENGINE.GameViewport.World.CurrentLevel.OwningWorld.PersistentLevel)
    OakSpawnPoint.RootComponent.AttachChildren.append(OakSpawnPoint.SpawnPointComponent)
    return OakSpawnPoint.SpawnPointComponent

    
def get_spawner() -> UObject | None:
    for spawner in unrealsdk.find_all("OakSpawnerComponent"):
        if spawner.bEnabled and "GEN_VARIABLE" not in str(spawner) and "Default" not in str(spawner):
                return spawner
    return None

def SpawnInteractiveObject(obj: str, package: str, Location: None, Rotation: None) -> None:
    factory = unrealsdk.find_class("SpawnFactory_OakInteractiveObject").ClassDefaultObject
    unrealsdk.load_package(package)
    factory.InteractiveObjectClass = unrealsdk.find_object("BlueprintGeneratedClass", obj)
    spawnpoint = get_spawn_point()
    spawnpoint.K2_SetWorldLocation(Location, True, IGNORE_STRUCT, True)
    spawnpoint.K2_SetWorldRotation(Rotation, True, IGNORE_STRUCT, True)
    actor = unrealsdk.find_object("Object", "/Script/GbxSpawn.Default__SpawnerBlueprintLibrary").SpawnActorWithSpawner(get_pc(), factory, spawnpoint, get_spawner(), None)
    return actor