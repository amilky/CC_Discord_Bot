from enum import Enum


# Class of enums to access boss index kc on hiscores
class Bosses(Enum):
    ABYSSAL_SIRE, ALCHEMICAL_HDYRA, AMOXLIATL, ARAXXOR, ARTIO, BARROWS, BRYOPHYTA, CALLISTO, \
        CALVARION, CERBERUS, COX, COX_CM, CHAOS_ELEMENTAL, CHAOS_FANATIC, \
        COMMANDER_ZILYANA, CORPORAL_BEAST, CRAZY_ARCHAEOLOGIST, DAG_PRIME, \
        DAG_REX, DAG_SUPREME, DERANGED_ARCHAEOLOGIST, \
        DUKE_SUCELLUS, GENERAL_GRAARDOR, GIANT_MOLE, GROTESQUE_GUARDIANS, \
        HESPORI, KALPHITE_QUEEN, KING_BLACK_DRAGON, KRAKEN, KREEARRA, \
        KRIL_TSUTSAROTH, LUNAR_CHESTS, MIMIC, NEX, NIGHTMARE, \
        PHOSANIS_NIGHTMARE, OBOR, \
        PHANTOM_MUSPAH, SARACHNIS, SCORPIA, SCURRIUS, SKOTIZO, SOL_HEREDIT, \
        SPINDEL, TEMPOROSS, \
        GAUNTLET, CORRUPTED_GAUNTLET, THE_HUEYCOATL, LEVIATHAN, THE_ROYAL_TITANS, WHISPERER, TOB, \
        TOB_HM, THERMONUCLEAR_SMOKE_DEVIL, TOA, TOA_HM, ZUK, JAD, \
        VARDORVIS, \
        VENENATIS, VETION, VORKATH, WINTERTODT, ZALCANO, ZULRAH = range(43, 108)

# Note: range is 1 more than the number of items in the list

# PROBABLY NEED TO FIX RANGE BECAUSE OF COLLECTIONS LOGGED