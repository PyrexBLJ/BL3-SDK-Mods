from typing import Any #type: ignore
import unrealsdk #type: ignore
from mods_base import get_pc, hook, BoolOption, build_mod #type: ignore
from unrealsdk.hooks import Type #type: ignore
from unrealsdk.unreal import BoundFunction, UObject, WrappedStruct #type: ignore

onlyCap: BoolOption = BoolOption("Only Log Above Damage Cap", False, "Yes", "No", description="Setting this to yes will only log damage above the visual damage cap.")
onlyMyDamage: BoolOption = BoolOption("Only My Damage", True, "Yes", "No", description="Only log damage dealt by the player")
roundTo2: BoolOption = BoolOption("Round Damage To 2 Decimal Places", True, "Yes", "No", description="Cleans up the log a lil bit")

mydamagedealers: list = ["DigiClone", "IronBear", "Pet", "IronCub"]

def doneByMe(instigator: UObject) -> bool:
    global mydamagedealers
    if instigator == get_pc():
        return True
    for dealer in mydamagedealers:
        if dealer in str(instigator):
            return True
    
    return False

@hook("/Script/GbxGameSystemCore.DamageComponent:ReceiveAnyDamage", Type.POST)
def enemyTookDamage(obj: UObject, args: WrappedStruct, _3: Any, _4: BoundFunction) -> None:
    if onlyCap.value and float(args.Damage) >= 1073741823.0 or not onlyCap.value:
        damagesource = str(args.DamageSource).split("_")
        if onlyMyDamage.value and doneByMe(args.InstigatedBy) or not onlyMyDamage.value:
            if args.Details.bWasCrit:
                print(f"Critical {damagesource[-2]} {args.DamageType.DamageIconFrameName} Damage: {round(args.Damage, 2) if roundTo2.value else args.Damage}")
            else:
                print(f"{damagesource[-2]} {args.DamageType.DamageIconFrameName} Damage: {round(args.Damage, 2) if roundTo2.value else args.Damage}")
    return None

build_mod()