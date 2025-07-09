if True:
    assert __import__("mods_base").__version_info__ >= (1, 0), "Please update the SDK"

from argparse import Namespace
import unrealsdk

from typing import Any
from mods_base import build_mod, get_pc, keybind, hook, SliderOption, BoolOption, command, GroupedOption, Game
from unrealsdk.hooks import Type
from unrealsdk.unreal import BoundFunction, UObject, WrappedStruct

__version__: str
__version_info__: tuple[int, ...]

currentdashes: int = 0

JumpNumberSlider: SliderOption = SliderOption("# of allowed jumps", 3, 1, 10, 1, True)
JumpSpeedSlider: SliderOption = SliderOption("Boosted Jump Speed", 1000, 1000, 10000, 100, True)
DashNumberSlider: SliderOption = SliderOption("# of allowed dashes", 3, 1, 10, 1, True)
DashSpeedSlider: SliderOption = SliderOption("Dash Speed", 2500, 1000, 10000, 100, True)
UseController: BoolOption = BoolOption("Use Controller Inputs", False, "Yes", "No")
StickDeadzone: SliderOption = SliderOption("Deadzone", 0.1, 0.0, 1.0, 0.01, False)

mainsettings: GroupedOption = GroupedOption("Main Settings", [JumpNumberSlider, JumpSpeedSlider, DashNumberSlider, DashSpeedSlider])
controllersettings: GroupedOption = GroupedOption("Controller Settings", [UseController, StickDeadzone])

axismap = None

@command("setmaxjumps", description="Override the slider and set a max jumps value")
def setMaxJumps(args: Namespace) -> None:
    JumpNumberSlider.value = int(args.numofjumps)

setMaxJumps.add_argument("numofjumps", help="the max number of jumps you want to have")

@command("setmaxdashes", description="Override the slider and set a max dashes value")
def setMaxDashes(args: Namespace) -> None:
    DashNumberSlider.value = int(args.numofdashes)

setMaxDashes.add_argument("numofdashes", help="the max number of dashes you want to have")

def outsideDeadzone(value: float) -> bool:
    if abs(value) > StickDeadzone.value:
        return True
    else:
        return False

def getAxisMap() -> None:
    global axismap
    for mapping in unrealsdk.find_all("GbxInputRebindContext"):
        if "Transient" in str(mapping) and "/Game/PlayerCharacters/_Shared/_Design/Input/Bindings/InputRebindContext_Player_Default.InputRebindContext_Player_Default" in str(mapping.DefaultContext):
            axismap = mapping.AxisBindings[0]

def findKeyForAction(scale: str) -> int:
    global axismap
    index: int = 0
    for mapping in axismap.Axis.Keys:
        if UseController.value == False:
            if "Gamepad" not in str(mapping.Key.KeyName) and str(mapping.Scale3D) == scale:
                return index
            else:
                index += 1
        if UseController.value == True:
            if "Gamepad" in str(mapping.Key.KeyName) and str(mapping.Scale3D) == scale:
                return index
            else:
                index += 1
    return -1

@keybind("Dash")
def dash() -> None:
    global currentdashes, axismap
    pcon = get_pc()
    if pcon.OakCharacter.OakCharacterMovement.CurrentFloor.bBlockingHit == False and currentdashes < int(DashNumberSlider.value):
        if Game.get_current() is Game.BL3:
            getAxisMap()
            AxisMapping = axismap.Axis.Keys
        if Game.get_current() is Game.WL:
            AxisMappingWL = unrealsdk.find_all("InputSettings")[0].AxisMappings # fuck you wonderlands i hate you so much i spent HOURS looking for where rebound keys are saved and u just fuckin yeeted that entire part of the game you piece of shit im so mad.

        dashSpeed = DashSpeedSlider.value
        
        velocity = None

        forwardVelocity = pcon.GetActorForwardVector()
        rightVelocity = pcon.GetActorRightVector()
        leftVelocity = unrealsdk.make_struct("Vector", X=(-rightVelocity.X), Y=(-rightVelocity.Y), Z=(-rightVelocity.Z))
        backVelocity = unrealsdk.make_struct("Vector", X=(-forwardVelocity.X), Y=(-forwardVelocity.Y), Z=(-forwardVelocity.Z))
        
        IsForwardPressed = False
        IsRightPressed = False
        IsLeftPressed = False
        IsBackPressed = False

        if UseController.value == False:
            if Game.get_current() is Game.BL3:
                IsForwardPressed = get_pc().IsInputKeyDown(AxisMapping[findKeyForAction("{X: 0.0, Y: 1.0, Z: 0.0}")].Key) # W
                IsRightPressed = get_pc().IsInputKeyDown(AxisMapping[findKeyForAction("{X: 1.0, Y: 0.0, Z: 0.0}")].Key) # D
                IsLeftPressed = get_pc().IsInputKeyDown(AxisMapping[findKeyForAction("{X: -1.0, Y: 0.0, Z: 0.0}")].Key) # A
                IsBackPressed = get_pc().IsInputKeyDown(AxisMapping[findKeyForAction("{X: 0.0, Y: -1.0, Z: 0.0}")].Key) # S
            elif Game.get_current() is Game.WL:
                IsForwardPressed = get_pc().IsInputKeyDown(AxisMappingWL[0].Key)
                IsRightPressed = get_pc().IsInputKeyDown(AxisMappingWL[2].Key)
                IsLeftPressed = get_pc().IsInputKeyDown(AxisMappingWL[3].Key)
                IsBackPressed = get_pc().IsInputKeyDown(AxisMappingWL[1].Key)
        else:
            if Game.get_current() is Game.BL3:
                if get_pc().GetInputAnalogKeyState(AxisMapping[findKeyForAction("{X: 0.0, Y: 1.0, Z: 0.0}")].Key) > 0 and outsideDeadzone(get_pc().GetInputAnalogKeyState(AxisMapping[findKeyForAction("{X: 0.0, Y: 1.0, Z: 0.0}")].Key)) == True:
                    IsForwardPressed = True
                    IsBackPressed = False
                elif get_pc().GetInputAnalogKeyState(AxisMapping[findKeyForAction("{X: 0.0, Y: 1.0, Z: 0.0}")].Key) < 0 and outsideDeadzone(get_pc().GetInputAnalogKeyState(AxisMapping[findKeyForAction("{X: 0.0, Y: 1.0, Z: 0.0}")].Key)) == True:
                    IsForwardPressed = False
                    IsBackPressed = True
                if get_pc().GetInputAnalogKeyState(AxisMapping[findKeyForAction("{X: 1.0, Y: 0.0, Z: 0.0}")].Key) > 0 and outsideDeadzone(get_pc().GetInputAnalogKeyState(AxisMapping[findKeyForAction("{X: 1.0, Y: 0.0, Z: 0.0}")].Key)) == True:
                    IsRightPressed = True
                    IsLeftPressed = False
                elif get_pc().GetInputAnalogKeyState(AxisMapping[findKeyForAction("{X: 1.0, Y: 0.0, Z: 0.0}")].Key) < 0 and outsideDeadzone(get_pc().GetInputAnalogKeyState(AxisMapping[findKeyForAction("{X: 1.0, Y: 0.0, Z: 0.0}")].Key)) == True:
                    IsRightPressed = False
                    IsLeftPressed = True
            elif Game.get_current() is Game.WL:
                if get_pc().GetInputAnalogKeyState(AxisMappingWL[29].Key) > 0 and outsideDeadzone(get_pc().GetInputAnalogKeyState(AxisMappingWL[29].Key)) == True:
                    IsForwardPressed = True
                    IsBackPressed = False
                elif get_pc().GetInputAnalogKeyState(AxisMappingWL[29].Key) < 0 and outsideDeadzone(get_pc().GetInputAnalogKeyState(AxisMappingWL[29].Key)) == True:
                    IsForwardPressed = False
                    IsBackPressed = True
                if get_pc().GetInputAnalogKeyState(AxisMappingWL[30].Key) > 0 and outsideDeadzone(get_pc().GetInputAnalogKeyState(AxisMappingWL[30].Key)) == True:
                    IsRightPressed = True
                    IsLeftPressed = False
                elif get_pc().GetInputAnalogKeyState(AxisMappingWL[30].Key) < 0 and outsideDeadzone(get_pc().GetInputAnalogKeyState(AxisMappingWL[30].Key)) == True:
                    IsRightPressed = False
                    IsLeftPressed = True

        if IsForwardPressed:
            velocity = unrealsdk.make_struct("Vector", X=(forwardVelocity.X), Y=(forwardVelocity.Y), Z=(forwardVelocity.Z))
            
            if IsRightPressed:
                velocity = unrealsdk.make_struct("Vector", X=(forwardVelocity.X + rightVelocity.X), Y=(forwardVelocity.Y + rightVelocity.Y), Z=(forwardVelocity.Z + rightVelocity.Z))
            elif IsLeftPressed:
                velocity = unrealsdk.make_struct("Vector", X=(forwardVelocity.X + leftVelocity.X), Y=(forwardVelocity.Y + leftVelocity.Y), Z=(forwardVelocity.Z + leftVelocity.Z))
        elif IsBackPressed:
            velocity = unrealsdk.make_struct("Vector", X=(backVelocity.X), Y=(backVelocity.Y), Z=(backVelocity.Z))
            
            if IsRightPressed:
                velocity = unrealsdk.make_struct("Vector", X=(backVelocity.X + rightVelocity.X), Y=(backVelocity.Y + rightVelocity.Y), Z=(backVelocity.Z + rightVelocity.Z))
            elif IsLeftPressed:
                velocity = unrealsdk.make_struct("Vector", X=(backVelocity.X + leftVelocity.X), Y=(backVelocity.Y + leftVelocity.Y), Z=(backVelocity.Z + leftVelocity.Z))
        elif IsRightPressed and not IsForwardPressed and not IsBackPressed:
            velocity = unrealsdk.make_struct("Vector", X=(rightVelocity.X), Y=(rightVelocity.Y), Z=(rightVelocity.Z))
        elif IsLeftPressed and not IsForwardPressed and not IsBackPressed:
            velocity = unrealsdk.make_struct("Vector", X=(leftVelocity.X), Y=(leftVelocity.Y), Z=(leftVelocity.Z))
        
        if velocity is not None:
            currentdashes = currentdashes + 1
            pcon.OakCharacter.LaunchCharacter(unrealsdk.make_struct("Vector", X=(velocity.X * dashSpeed), Y=(velocity.Y * dashSpeed), Z=250), True, True)

@hook("/Game/PlayerCharacters/_Shared/_Design/Character/BPChar_Player.BPChar_Player_C:OnLanded", Type.PRE)
def IsWalkingHook(obj: UObject, args: WrappedStruct, _3: Any, _4: BoundFunction) -> None:
    global currentdashes
    currentdashes = 0
    get_pc().OakCharacter.JumpMaxCount = 1
    return

@hook("/Script/OakGame.OakPlayerController:JumpPressed", Type.PRE)
def JumpPressedHook(obj: UObject, args: WrappedStruct, _3: Any, _4: BoundFunction) -> None:
    pcon = get_pc()
    pcon.OakCharacter.JumpMaxCount = int(JumpNumberSlider.value)

    if pcon.OakCharacter.JumpCurrentCount > 0 and pcon.OakCharacter.JumpCurrentCount < pcon.OakCharacter.JumpMaxCount:
        pcon.OakCharacter.LaunchCharacter(unrealsdk.make_struct("Vector", X=0, Y=0, Z=int(JumpSpeedSlider.value)), False, True)

build_mod(keybinds=[dash], options=[mainsettings, controllersettings])


