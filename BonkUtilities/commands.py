from argparse import Namespace
import unrealsdk
from mods_base import get_pc, command, ENGINE

activePlayer: int = -1

@command("buhelp", description="list of available commands")
def help(args: Namespace) -> None:
    print("Commands:\n[command] --help for more details on specific commands\nsend_mail [datatable] [rowname]\naddcurrency [currencytype] [amount]\nmaxlevel\ngiveitem [location] [itemserial]\ngiveitemfrompool [pool]\nmaxsdus\nenablegr\nsetguardianrank [rank]\nsetguardiantokens [tokens]\ngiveskillpoints [points]\ntogglemayhem [value]\ngetmayhemseed\nsetmayhemseed [seed]\ngivebooster [booster name/type]")

@command("send_mail", description="takes a datatable and rowname to recieve items in your mailbox")
def sendMail(args: Namespace) -> None:
    table = args.datatable
    row = args.rowname
    get_pc().AddNPCMailItemFromTableRowHandle(unrealsdk.make_struct("DataTableRowHandle", DataTable=unrealsdk.find_object("DataTable", table), RowName=row))
    print("Sent item to your mail box")

sendMail.add_argument("datatable", help="path + name of datatable the item you want comes from")
sendMail.add_argument("rowname", help="challenge name from the datatable that gives the item you want")

@command("addcurrency", description="add to these currencies: money, eridium, goldkey, diamondkey, vaultcard1key, vaultcard2key, vaultcard3key. Max Value 2147483647")
def addCurrency(args: Namespace) -> None:
    if str(args.currency).lower() == "money":
        get_pc().ServerAddCurrency(int(args.amount), unrealsdk.find_object("InventoryCategoryData", "/Game/Gear/_Shared/_Design/InventoryCategories/InventoryCategory_Money.InventoryCategory_Money"))
        print(f"Added ${int(args.amount)}")

    elif str(args.currency).lower() == "diamondkey":
        get_pc().ServerUpdatePremiumCurrency(unrealsdk.find_object("InventoryCategoryData", "/Game/Gear/_Shared/_Design/InventoryCategories/InventoryCategory_DiamondKey.InventoryCategory_DiamondKey"), int(args.amount))
        print(f"Added {int(args.amount)} Diamond Key(s)")

    elif str(args.currency).lower() == "eridium" or str(args.currency).lower() == "moonorb":
        get_pc().ServerAddCurrency(int(args.amount), unrealsdk.find_object("InventoryCategoryData", "/Game/Gear/_Shared/_Design/InventoryCategories/InventoryCategory_Eridium.InventoryCategory_Eridium"))
        print(f"Added {int(args.amount)} Eridium / Moon Orbs")
    
    elif str(args.currency).lower() == "soul":
        get_pc().ServerAddCurrency(int(args.amount), unrealsdk.find_object("InventoryCategoryData", "/Game/PatchDLC/Indigo1/Common/Pickups/IndCurrency/InventoryCategory_IndCurrency.InventoryCategory_IndCurrency"))
        print(f"Added {int(args.amount)} Souls")
    
    elif str(args.currency).lower() == "crystal":
        get_pc().ServerAddCurrency(int(args.amount), unrealsdk.find_object("InventoryCategoryData", "/Game/Gear/_Shared/_Design/InventoryCategories/InventoryCategory_Cookie.InventoryCategory_Cookie"))
        print(f"Added {int(args.amount)} Crystals")

    elif str(args.currency).lower() == "goldkey":
        get_pc().ServerUpdatePremiumCurrency(unrealsdk.find_object("InventoryCategoryData", "/Game/Gear/_Shared/_Design/InventoryCategories/InventoryCategory_GoldenKey.InventoryCategory_GoldenKey"), int(args.amount))
        print(f"Added {int(args.amount)} Golden Key(s)")

    elif str(args.currency).lower() == "vaultcard1key":
        get_pc().ServerUpdatePremiumCurrency(unrealsdk.find_object("InventoryCategoryData", "/Game/Gear/_Shared/_Design/InventoryCategories/InventoryCategory_VaultCard1Key.InventoryCategory_VaultCard1Key"), int(args.amount))
        print(f"Added {int(args.amount)} Vault Card 1 Key(s)")

    elif str(args.currency).lower() == "vaultcard2key":
        get_pc().ServerUpdatePremiumCurrency(unrealsdk.find_object("InventoryCategoryData", "/Game/Gear/_Shared/_Design/InventoryCategories/InventoryCategory_VaultCard2Key.InventoryCategory_VaultCard2Key"), int(args.amount))
        print(f"Added {int(args.amount)} Vault Card 2 Key(s)")

    elif str(args.currency).lower() == "vaultcard3key":
        get_pc().ServerUpdatePremiumCurrency(unrealsdk.find_object("InventoryCategoryData", "/Game/Gear/_Shared/_Design/InventoryCategories/InventoryCategory_VaultCard3Key.InventoryCategory_VaultCard3Key"), int(args.amount))
        print(f"Added {int(args.amount)} Vault Card 3 Key(s)")

    else:
        print(f"{str(args.currency)} is not a valid currency. These are: money, eridium, moonorb, soul, crystal, goldkey, diamondkey, vaultcard1key, vaultcard2key, vaultcard3key. Max Value 2147483647")

addCurrency.add_argument("currency", help="name of currency to change")
addCurrency.add_argument("amount", help="i think you can figure this one out")

@command("maxlevel", description="Set your character to level 72")
def maxLevel(args: Namespace) -> None:
    get_pc().OakCharacter.PlayerBalanceComponent.AddExperience(9520932 - get_pc().OakCharacter.PlayerBalanceComponent.GetExperience(), 0, 0)
    print("You are now level 72")

@command("giveitem", description="puts items in your inventory or bank, use gear serial numbers with this. Example: BIMgMALoBXdITX+sFB7CtJdTGMEicb5S6Pkmq9KTKWcHsV1GgQM3Vg==")
def giveItem(args: Namespace) -> None:
    loc: int = 0
    if str(args.location).lower() == "backpack":
        loc = 0
    elif str(args.location).lower() == "bank":
        loc = 1
    else:
        print("Invalid location, adding items to backpack")
    get_pc().ServerAddGearToInventory(args.item, loc)
    print("Item has been created")

giveItem.add_argument("location", help="where you want the item to be placed, either backpack or bank")
giveItem.add_argument("item", help="raw serial number of the gear. Example: BIMgMALoBXdITX+sFB7CtJdTGMEicb5S6Pkmq9KTKWcHsV1GgQM3Vg==")

@command("maxsdus", description="Max level all SDU upgrades")
def maxSDUS(args: Namespace) -> None:
    for i in range(0, 28):
        for sdu in unrealsdk.find_all("OakSDUData")[1:]:
            get_pc().OakCharacter.AddSDU(sdu)
    print(f"Set Max Level for all SDUs")

@command("enablegr", description="Enable Guardian Rank before the end of the story")
def enableGuardianRank(args: Namespace) -> None:
    get_pc().OakHUD.CachedExperienceBar.PlayerGuardianRank.ServerStartGuardianRankTracking()
    print("Guardian Rank Enabled")

@command("setguardianrank", description="Enable Guardian Rank before the end of the story")
def setGuardianRank(args: Namespace) -> None:
    get_pc().OakHUD.CachedExperienceBar.PlayerGuardianRank.SetGuardianRank(int(args.rank))
    print(f"{args.rank} Guardian Rank given")

setGuardianRank.add_argument("rank", help="level to set for guardian rank")

@command("setguardiantokens", description="Enable Guardian Rank before the end of the story")
def setGuardianTokens(args: Namespace) -> None:
    get_pc().OakHUD.CachedExperienceBar.PlayerGuardianRank.ServerSetAvailableTokens(int(args.tokens))
    print(f"{args.tokens} Guardian tokens given")

setGuardianTokens.add_argument("tokens", help="number of guardian tokens to set")

@command("giveskillpoints", description="Give X number of available skill points")
def setSkillPoints(args: Namespace) -> None:
    if int(args.points) > get_pc().OakHUD.CachedExperienceBar.PlayerAbilityTree.AbilityPoints and get_pc().OakHUD.CachedExperienceBar.PlayerAbilityTree.AbilityPoints >= 0:
        get_pc().OakHUD.CachedExperienceBar.PlayerAbilityTree.GiveAbilityPoints(int(args.points))
        print(f"{args.points} Skill points given")
    else:
        get_pc().OakHUD.CachedExperienceBar.PlayerAbilityTree.AbilityPoints = int(args.points)
        print(f"{args.points} Skill points given, due to previous skill point state a save quit is required for points to be usable")

setSkillPoints.add_argument("points", help="number of skill points to set")

@command("giveitemfrompool", description="Give a random item from an ItemPoolData object")
def giveItemFromPool(args: Namespace) -> None:
    get_pc().OakCharacter.AddDefaultItemPoolInventory(unrealsdk.find_object("ItemPoolData", args.pool), False, False)
    print("Item added to backpack")

giveItemFromPool.add_argument("pool", help="the item pool to grab an item from")

@command("togglemayhem", description="Toggle Mayhem mode at any time: True for on, False for off")
def toggleMayhemMode(args: Namespace) -> None:
    get_pc().OakHud.GFxBossBar.OakGameState.MayhemModeState.bIsActive = bool(args.value)
    print("Mayhem Mode Toggled")

toggleMayhemMode.add_argument("value", help="True or False")

@command("getmayhemseed", description="print the numbers that determine what modifiers you have, to be used with setmayhemseed command")
def getMayhemSeed(args: Namespace) -> None:
    print(f"Mayhem {str(get_pc().OakHud.GFxBossBar.OakGameState.MayhemModeState.MayhemLevel)} Seed: {str(get_pc().OakHud.GFxBossBar.OakGameState.MayhemModeState.RandomSeed)}\nWith the modifiers:")
    for mod in ENGINE.GameInstance.ModifierManagers[0].ActiveModifierSets[1:]:
        print(f"{mod.UIStats[0].Text}: {mod.UIStats[0].Description}")

@command("setmayhemseed", description="change your current modifier set")
def setMayhemSeed(args: Namespace) -> None:
    get_pc().ServerRequestMayhemReload(int(args.mayhemlevel), int(args.seed))
    print("Mayhem Modifiers Set, Reloading the map")

setMayhemSeed.add_argument("mayhemlevel", help="what mayhem level this seed is for")
setMayhemSeed.add_argument("seed", help="value for random seed")

@command("givebooster", description="apply a citizen science booster to yourself")
def giveBooster(args: Namespace) -> None:
    if str(args.booster) in ("Brain Nanobots", "xp"):
        get_pc().ServerApplyCitizenScienceBooster(0, 7200)
        print("Brain Nanobots (2h) Applied")
    elif str(args.booster) in ("Lucky Jabber Foot", "cash"):
        get_pc().ServerApplyCitizenScienceBooster(1, 7200)
        print("Lucky Jabber Foot (2h) Applied")
    elif str(args.booster) in ("Caffeine Caplets", "speed"):
        get_pc().ServerApplyCitizenScienceBooster(2, 7200)
        print("Caffeine Caplets (2h) Applied")
    elif str(args.booster) in ("Jabber-Cola", "damage"):
        get_pc().ServerApplyCitizenScienceBooster(3, 3600)
        print("Jabber-Cola (1h) Applied")
    elif str(args.booster) in ("Elemental Powder", "element"):
        get_pc().ServerApplyCitizenScienceBooster(4, 3600)
        print("Elemental Powder (1h) Applied")
    elif str(args.booster) in ("Butt Stallion Milk", "loot"):
        get_pc().ServerApplyCitizenScienceBooster(5, 3600)
        print("Butt Stallion Milk (1h) Applied")
    else:
        print("No valid booster provided, use one from this list\n\n    Brain Nanobots - xp\n    Lucky Jabber Foot - cash\n    Caffeine Caplets - speed\n    Jabber-Cola - damage\n    Elemental Powder - element\n    Butt Stallion Milk - loot")

giveBooster.add_argument("booster", help="what booster to set:\n\n    Brain Nanobots - xp\n    Lucky Jabber Foot - cash\n    Caffeine Caplets - speed\n    Jabber-Cola - damage\n    Elemental Powder - element\n    Butt Stallion Milk - loot")