import unrealsdk #type: ignore
from unrealsdk.unreal import UObject #type: ignore
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