import unrealsdk
from mods_base import hook, build_mod, SliderOption
from unrealsdk.hooks import Type
from unrealsdk.unreal import BoundFunction, UObject, WrappedStruct
from typing import Any

MaximumDamage: SliderOption = SliderOption("Max Amount of Damage", 50, 25, 100, 1, True, description="The percentage of your total health and shield a max velocity fall will deal as damage, default is 50 so 50% of your max health + max shield.")
MinimumFallVelocity: SliderOption = SliderOption("Minimum Fall Speed", 1000, 800, 3000, 1, True, description="How fast you have to be falling for it to deal any damage, default is 1000.")

@hook("/Game/PlayerCharacters/_Shared/_Design/Character/BPChar_Player.BPChar_Player_C:OnLanded", Type.PRE)
def OnLandedHook(obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction) -> None:
    fallvelocity = min(obj.OakCharacterMovement.Velocity.Z * -1, 4000)
    if fallvelocity > MinimumFallVelocity.value:
        fallvelocity -= 1000

        totalhp = obj.OakDamageComponent.GetTotalMaxHealth()
        shield = obj.OakDamageComponent.GetCurrentShield()
        health = obj.OakDamageComponent.GetCurrentHealth()

        fallpercentage = (fallvelocity / 3000) * 100
        maxfalldamage = totalhp * (MaximumDamage.value / 100) 
        totaldamage = maxfalldamage * fallpercentage / 100

        if shield - totaldamage < 0:
            totaldamage -= shield
            obj.OakDamageComponent.SetCurrentShield(0)
            obj.OakDamageComponent.SetCurrentHealth(health - totaldamage)
        else:
            obj.OakDamageComponent.SetCurrentShield(shield - totaldamage)

    return None

build_mod()