from argparse import Namespace
import threading
import time
import unrealsdk #type: ignore
from mods_base import get_pc, build_mod, SETTINGS_DIR, command, NestedOption, ButtonOption, GroupedOption, ENGINE, SliderOption #type: ignore
from ui_utils import show_hud_message #type: ignore
from typing import TypedDict
import os, json

class Loadout(TypedDict):
    character: str
    pointsused: int
    actionskills: list[list[str, str]]
    actionskillaugments: list[list[str, str, str]]
    skills: list[list[str, int]]


savedZaneLoadouts: list = []
savedFlakLoadouts: list = []
savedMozeLoadouts: list = []
savedAmaraLoadouts: list = []
ZaneLoadouts: NestedOption = NestedOption("Zane Loadouts", [])
FlakLoadouts: NestedOption = NestedOption("Flak Loadouts", [])
MozeLoadouts: NestedOption = NestedOption("Moze Loadouts", [])
AmaraLoadouts: NestedOption = NestedOption("Amara Loadouts", [])

dsavedZaneLoadouts: list = []
dsavedFlakLoadouts: list = []
dsavedMozeLoadouts: list = []
dsavedAmaraLoadouts: list = []
dZaneLoadouts: NestedOption = NestedOption("Zane Loadouts", [])
dFlakLoadouts: NestedOption = NestedOption("Flak Loadouts", [])
dMozeLoadouts: NestedOption = NestedOption("Moze Loadouts", [])
dAmaraLoadouts: NestedOption = NestedOption("Amara Loadouts", [])

if not os.path.exists(f"{SETTINGS_DIR}\\SkillTreeSaver"):
    os.makedirs(f"{SETTINGS_DIR}\\SkillTreeSaver")
    print("Created save folder")

def getSavedTrees() -> None:
    global savedZaneLoadouts, savedFlakLoadouts, savedMozeLoadouts, savedAmaraLoadouts, dsavedZaneLoadouts, dsavedFlakLoadouts, dsavedMozeLoadouts, dsavedAmaraLoadouts

    # for loading
    savedZaneLoadouts = []
    savedFlakLoadouts = []
    savedMozeLoadouts = []
    savedAmaraLoadouts = []

    # for deleting
    dsavedZaneLoadouts = []
    dsavedFlakLoadouts = []
    dsavedMozeLoadouts = []
    dsavedAmaraLoadouts = []

    for filename in os.listdir(f"{SETTINGS_DIR}/SkillTreeSaver"):
        file = open(f"{SETTINGS_DIR}/SkillTreeSaver/{filename}", "r")
        temploadout: Loadout = json.load(file)
        file.close()

        if temploadout["character"] == "Zane":
            savedZaneLoadouts.append(ButtonOption(f"{filename.removesuffix(".json")}", on_press = lambda _: load(_.identifier)))
        if temploadout["character"] == "FL4K":
            savedFlakLoadouts.append(ButtonOption(f"{filename.removesuffix(".json")}", on_press = lambda _: load(_.identifier)))
        if temploadout["character"] == "Moze":
            savedMozeLoadouts.append(ButtonOption(f"{filename.removesuffix(".json")}", on_press = lambda _: load(_.identifier)))
        if temploadout["character"] == "Amara":
            savedAmaraLoadouts.append(ButtonOption(f"{filename.removesuffix(".json")}", on_press = lambda _: load(_.identifier)))

        if temploadout["character"] == "Zane":
            dsavedZaneLoadouts.append(ButtonOption(f"[red]Delete[/red] {filename.removesuffix(".json")}", on_press = lambda _: delete(_.identifier)))
        if temploadout["character"] == "FL4K":
            dsavedFlakLoadouts.append(ButtonOption(f"[red]Delete[/red] {filename.removesuffix(".json")}", on_press = lambda _: delete(_.identifier)))
        if temploadout["character"] == "Moze":
            dsavedMozeLoadouts.append(ButtonOption(f"[red]Delete[/red] {filename.removesuffix(".json")}", on_press = lambda _: delete(_.identifier)))
        if temploadout["character"] == "Amara":
            dsavedAmaraLoadouts.append(ButtonOption(f"[red]Delete[/red] {filename.removesuffix(".json")}", on_press = lambda _: delete(_.identifier)))

    ZaneLoadouts.children = savedZaneLoadouts
    FlakLoadouts.children = savedFlakLoadouts
    MozeLoadouts.children = savedMozeLoadouts
    AmaraLoadouts.children = savedAmaraLoadouts

    dZaneLoadouts.children = dsavedZaneLoadouts
    dFlakLoadouts.children = dsavedFlakLoadouts
    dMozeLoadouts.children = dsavedMozeLoadouts
    dAmaraLoadouts.children = dsavedAmaraLoadouts

    return None


getSavedTrees()


maxNameLength: SliderOption = SliderOption("Max Name Length", 20, 20, 64, 1, True, description="Max number of characters your characters name can be, since this mod uses it as the saved skill tree name. This only has to be set once per character.\n\nThis is 20 by default.")

def setnamelength() -> None:
    get_pc().CurrentSavegame.NameCharacterLimit = maxNameLength.value
    return None

setMaxNameLength: ButtonOption = ButtonOption("Set Max Name Length", on_press = lambda _: setnamelength())
nameGroup: GroupedOption = GroupedOption("Name Options", [maxNameLength, setMaxNameLength])

SaveCurrentLoadout: ButtonOption = ButtonOption("Save Your Current Skill Tree", on_press = lambda _: save(), description="Will use your characters current name as the save name")

SaveGroup: GroupedOption = GroupedOption("Save Skill Tree", [SaveCurrentLoadout])
LoadGroup: GroupedOption = GroupedOption("Load Skill Tree", [ZaneLoadouts, FlakLoadouts, MozeLoadouts, AmaraLoadouts])
DeleteGroup: GroupedOption = GroupedOption("Delete Saved Trees", [dZaneLoadouts, dFlakLoadouts, dMozeLoadouts, dAmaraLoadouts])

currentloadout: Loadout = {
    "character": "None",
    "pointsused": 0,
    "actionskills": [["None", "None"]],
    "actionskillaugments": [["None", "None", "None"]],
    "skills": [["None", 0]]
}
def saveTheGame() -> bool: # this feels super scuffed but it gets the skills into the savegame so im usin it
    desiredstation = ENGINE.GameViewport.World.GameState.TravelStationTracker.GetLastActiveTravelToStation(get_pc())
    for station in unrealsdk.find_all("TravelStationObject", exact=False):
        if "Default" in str(station):
            pass
        elif station == desiredstation:
            pass
        else:
            station.OnTravelStationActivated(desiredstation)
            desiredstation.OnTravelStationActivated(station)
            print("Skill Tree Saver: trying to save the game")
            return True
    return False

def saveTrees() -> None:
    time.sleep(0.5)
    ac: list = []
    aca: list = []
    skill: list = []
    points: int = 0
    for actionskill in get_pc().OakCharacter.OakPlayerAbilityManager.AbilitySlotList.Items:
        ac.append([str(actionskill.SlotData), str(actionskill.AbilityClass)])
    for augment in get_pc().OakCharacter.OakPlayerAbilityManager.AugmentSlotList.Items:
        aca.append([str(augment.ActionAbilityClass), str(augment.SlotData), str(augment.AugmentData)])
    for ability in get_pc().CurrentSavegame.AbilityData.TreeItemList:
        skill.append([str(ability.ItemAssetPath), ability.Points])
        points += ability.Points
    
    currentloadout["character"] = get_pc().CurrentSavegame.PlayerClassData.PlayerClassPath.CharacterName
    currentloadout["pointsused"] = points
    currentloadout["actionskills"] = ac
    currentloadout["actionskillaugments"] = aca
    currentloadout["skills"] = skill
    
    
    file = open(f"{SETTINGS_DIR}/SkillTreeSaver/{get_pc().CurrentSaveGame.PreferredCharacterName}.json", "a")
    json.dump(currentloadout, file)
    file.close()
    print(f"Saved {get_pc().CurrentSaveGame.PreferredCharacterName} Skill Trees")
    show_hud_message("[skillScreenGreen]Saved Successfully[/skillScreenGreen]", f"[skillbold]{get_pc().CurrentSaveGame.PreferredCharacterName}[/skillbold] Skill Trees Saved.")
    getSavedTrees()
    return None

def save() -> None:
    if saveTheGame() == False:
        print(f"[ERROR] Unable to forcefully save the game, try going to a different map and resave")
        show_hud_message("[red]Error[/red]", "Unable to forcefully save the game, go to a new map")
        return None
    if os.path.exists(f"{SETTINGS_DIR}/SkillTreeSaver/{get_pc().CurrentSaveGame.PreferredCharacterName}.json"):
        print(f"[ERROR] {SETTINGS_DIR}/SkillTreeSaver/{get_pc().CurrentSaveGame.PreferredCharacterName}.json already exists! Will not save over it.")
        show_hud_message("[red]Error[/red]", "Tried to overwrite existing save, not doin it.")
        return None
    
    threading.Thread(target=saveTrees).start()
    
    return None

@command("saveloadout")
def savecommand(args: Namespace) -> None:
    save()
    return None

def load(loadoutname: str) -> None:
    global currentloadout
    file = open(f"{SETTINGS_DIR}/SkillTreeSaver/{str(loadoutname)}.json", "r")
    currentloadout = json.load(file)
    file.close()
    if get_pc().CurrentSavegame.PlayerClassData.PlayerClassPath.CharacterName != currentloadout["character"]:
        print(f"[Warning] Loading a {currentloadout["character"]} save on {get_pc().CurrentSavegame.PlayerClassData.PlayerClassPath.CharacterName} wont do anything, skipping.")
        show_hud_message("[actionskill]Warning[/actionskill]", "Incorrect character save, skipping.")
        return None
    
    get_pc().OakCharacter.OakPlayerAbilityManager.PurchaseAbilityRespec()

    if get_pc().OakHUD.CachedExperienceBar.PlayerAbilityTree.AbilityPoints < currentloadout["pointsused"]:
        print(f"[Warning] This character doesnt have enough skill points for the selected build. gonna spec what we can anyways.")
        show_hud_message("[actionskill]Warning[/actionskill]", "Not Enough Points, trying to spec anyways.")

    for skill in currentloadout["skills"]:
        if skill[1] > 0:
            i: int = 0
            splitskillname = skill[0].split("'")
            while i < skill[1]:
                get_pc().OakCharacter.OakPlayerAbilityManager.PlayerAbilityTree.AddPointToAbilityTreeItem(unrealsdk.find_object(splitskillname[0], splitskillname[1]))
                i += 1
    for actionskill in currentloadout["actionskills"]:
        if actionskill[1] != "None":
            slot = actionskill[0].split("'")
            ability = actionskill[1].split("'")
            get_pc().OakCharacter.OakPlayerAbilityManager.SetSlotAbilityClass(unrealsdk.find_object("OakPlayerAbilitySlotData", slot[1]), unrealsdk.find_object("BlueprintGeneratedClass", ability[1]))
    for augment in currentloadout["actionskillaugments"]:
        if augment[2] != "None":
            abilityclass = augment[0].split("'")
            augmentslot = augment[1].split("'")
            augmentchoice = augment[2].split("'")
            get_pc().OakCharacter.OakPlayerAbilityManager.SetSlotAugment(unrealsdk.find_object("BlueprintGeneratedClass", abilityclass[1]), unrealsdk.find_object("OakActionAbilityAugmentSlotData", augmentslot[1]), unrealsdk.find_object(augmentchoice[0], augmentchoice[1]))

    if get_pc().OakHUD.CachedExperienceBar.PlayerAbilityTree.AbilityPoints >= currentloadout["pointsused"]:
        print(f"Loaded {loadoutname} Skill Trees")
        show_hud_message("[skillScreenGreen]Loaded Successfully[/skillScreenGreen]", f"[skillbold]{loadoutname}[/skillbold] Skill Trees Loaded.")

    return None

@command("loadloadout")
def loadcommand(args: Namespace) -> None:
    load(args.loadout)
    return None

loadcommand.add_argument("loadout", help="The name of the loadout file you want to load")


def delete(loadoutname: str) -> None:
    loadoutname = loadoutname.removeprefix("[red]Delete[/red] ")
    if os.path.exists(f"{SETTINGS_DIR}/SkillTreeSaver/{loadoutname}.json"):
        os.remove(f"{SETTINGS_DIR}/SkillTreeSaver/{loadoutname}.json")
        print(f"deleted {loadoutname}.json")
        show_hud_message("[actionskill]Deleted Successfully[/actionskill]", f"[skillbold]{loadoutname}[/skillbold] Skill Tree Deleted.")
        getSavedTrees()
    else:
        print(f"{loadoutname}.json does not exist, cant delete it.")
        show_hud_message("[red]Error[/red]", f"[skillbold]{loadoutname}[/skillbold] doesn't exist.")
    return None

@command("deleteloadout")
def deletecommand(args: Namespace) -> None:
    delete(args.loadout)
    return None

deletecommand.add_argument("loadout", help="The name of the loadout file you want to delete")

build_mod(options=[nameGroup, SaveGroup, LoadGroup, DeleteGroup])