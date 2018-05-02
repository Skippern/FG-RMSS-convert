#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# fg2irm_lib
# 2018 Aun "Skippern" Johnsen <skippern@gimnechiske.org
#
# Converts from Fantasy Grounds formats to irm_lib data
#
import argparse
import os
import json
import re
from lxml import etree

parser = argparse.ArgumentParser(description='Convert from an FG xml to irm_lib')
parser.add_argument('--xml', metavar='FGXML', type=str,
                    help='FG XML File', required=True)
parser.add_argument('--data', metavar='DATADIR', type=str,
                    help='irm_lib data dir', required=True)
parser.add_argument('-v', '--verbose', action='store_true')
parser.add_argument('-vv', '--debug', action='store_true')
parser.add_argument('-s', '--silent', action='store_true')
args = parser.parse_args()

__OUTPUT = 1
if (args.debug):
    __OUTPUT = 3
elif (args.verbose):
    __OUTPUT = 2
elif (args.silent):
    __OUTPUT = 0

def printf(text, level=1):
    if (__OUTPUT >= level):
        print text

def eqtype(type):
    if (type == 0): return "unknown"
    elif (type == 1): return "weapon_1he"
    elif (type == 2): return "weapon_1hc"
    elif (type == 3): return "weapon_2h"
    elif (type == 4): return "weapon_pa"
    elif (type == 5): return "weapon_mis"
    elif (type == 6): return "weapon_th"
    elif (type == 7): return "shield"
    elif (type == 11): return "accessory"
    elif (type == 12): return "armor"
    elif (type == 13): return "herb"
    elif (type == 17): return "food"
    elif (type == 18): return "lodging"
    elif (type == 19): return "transport"
    elif (type == 20): return "service"

    elif (type == 131): return "herb"
    elif (type == 132): return "bread"
    elif (type == 133): return "intox"
    elif (type == 134): return "poison"

    return "unknown"

printf('__OUTPUT {0}'.format(__OUTPUT), 3)

printf('--data {0}'.format(args.data), 3)
printf('--xml {0}'.format(args.xml), 3)

__DATA = args.data
root = etree.parse(args.xml)

__dirname = __DATA + 'tables'
try:
    os.stat(__dirname)
except:
    os.mkdir(__dirname)
__dirname = __DATA + 'skills'
try:
    os.stat(__dirname)
except:
    os.mkdir(__dirname)
__dirname = __DATA + 'races'
try:
    os.stat(__dirname)
except:
    os.mkdir(__dirname)
__dirname = __DATA + 'professions'
try:
    os.stat(__dirname)
except:
    os.mkdir(__dirname)
__dirname = __DATA + 'trainingpackages'
try:
    os.stat(__dirname)
except:
    os.mkdir(__dirname)
__dirname = __DATA + 'spells'
try:
    os.stat(__dirname)
except:
    os.mkdir(__dirname)
__dirname = __DATA + 'talents'
try:
    os.stat(__dirname)
except:
    os.mkdir(__dirname)
__dirname = __DATA + 'flaws'
try:
    os.stat(__dirname)
except:
    os.mkdir(__dirname)
__dirname = __DATA + 'npc'
try:
    os.stat(__dirname)
except:
    os.mkdir(__dirname)

try:
    __tables = root.find("Tables")

    for table in __tables:
        __filename = __DATA + 'tables/' + table.tag + '.json'

        __table_data = {}
        __table_data['id'] = table.find("Id").text
        __table_data['sources'] = []
        __table_data['refs'] = {}
        __table_data['name'] = table.find("Name").text
        __table_data['type'] = table.find("TableType").text
        __table_data['class'] = table.find("Class").text
        __table_data['sort'] = table.find("SortOrder").text

        __columns = table.find("Columns")
        __table_data['column'] = {}
        for col in __columns:
            __table_data['column'][col.tag] = {}
            __table_data['column'][col.tag]['id'] = col.find("Id").text
            __table_data['column'][col.tag]['title'] = col.find("Title").text

        __chart = table.find("Chart")
        __table_data['table'] = {}
        for tbl in __chart:
            __table_data['table'][tbl.tag] = {}
            __table_data['table'][tbl.tag]["roll"] = tbl.find("Roll").text
            try:
                __entries = tbl.find("Entries")
                __table_data['table'][tbl.tag]["entries"] = {}
                for e in __entries:
                    __table_data['table'][tbl.tag]['entries'][e.tag] = {}
                    __table_data['table'][tbl.tag]['entries'][e.tag]['cid'] = e.find("ColumnId").text
                    __table_data['table'][tbl.tag]['entries'][e.tag]['text'] = e.find("Text").text
                    try:
                        __effect = e.find("Effects")
                        __table_data['table'][tbl.tag]['entries'][e.tag]['effect'] = {}
                        for eff in __effect:
                            __table_data['table'][tbl.tag]['entries'][e.tag]['effect']['hits'] = int(eff.find("Hits").text)
                            __table_data['table'][tbl.tag]['entries'][e.tag]['effect']['no_parry'] = int(eff.find("NoParry").text)
                            __table_data['table'][tbl.tag]['entries'][e.tag]['effect']['bleed'] = int(eff.find("Bleed").text)
                            __table_data['table'][tbl.tag]['entries'][e.tag]['effect']['penalty'] = int(eff.find("Penalty").text)
                            __table_data['table'][tbl.tag]['entries'][e.tag]['effect']['penalty_rounds'] = int(eff.find("Penalty Rounds").text)
                            __table_data['table'][tbl.tag]['entries'][e.tag]['effect']['bonus'] = int(eff.find("Bonus").text)
                            __table_data['table'][tbl.tag]['entries'][e.tag]['effect']['bonus_rounds'] = int(eff.find("Bonus Rounds").text)
                            __table_data['table'][tbl.tag]['entries'][e.tag]['effect']['corruption'] = int(eff.find("Corruption").text)
                            __table_data['table'][tbl.tag]['entries'][e.tag]['effect']['powerpoints'] = int(eff.find("Power Points").text)
                    except:
                        pass
            except:
                pass
    f = open(__filename, 'wb')
    f.write(json.dumps( __table_data , indent=3, sort_keys=True))
    f.close()
except:
    pass

try:
    __reference = root.find("reference")
    for tbl in __reference.find("tables"):
        if (tbl.tag == "purchasepricechart"):
            print "GL 12.4.2 (Purchase)"
        if (tbl.tag == "resalepricechart"):
            print "GL 12.4.2 (Resale)"
        if (tbl.tag == "findingaherbpoisoninthewild"):
            print "Dunno"

#        __filename = __DATA + 'tables/' + table.tag + '.json'
#        f = open(__filename, 'wb')
#        f.write(json.dumps( __table_data , indent=3, sort_keys=True))
#        f.close()

    __professions = __reference.find("professions")
    __skilllist = __reference.find("skilllist")
    __skillcat = __skilllist.find("categoryskills")
    __categorylist = __skillcat.find("list")
    for prof in __professions:
        __professions_data = {}
        __professions_data['sources'] = []
        __professions_data['refs'] = {}
        __professions_data['name'] = prof.find("name").text
        __professions_data['description'] = "\n".join(prof.find("text").text)
        for desc in prof.find("text"):
            __professions_data['description'] = __professions_data['description'] + desc.text
        __professions_data['description'] = __professions_data['description'].replace("\n", "").replace("\t", "").strip()
        __professions_data['prime_stats'] = []
        __professions_data['dev cost'] = {}
        __professions_data['realm'] = prof.find("realm").text
        for skillCat in __categorylist:
            for cost in skillCat.find("costs"):
                if (cost.tag == prof.tag):
                    __professions_data['dev cost'][skillCat.find("fullname").text] = cost.text.split("/")
        __filename = __DATA + "/professions/" + __professions_data['name'] + ".json"
        f = open(__filename, 'wb')
        f.write(json.dumps( __professions_data , indent=3, sort_keys=True))
        f.close()
    for skillCat in __categorylist:
        __skillcat_data = {}
        __skillcat_data['sources'] = []
        __skillcat_data['refs'] = {}
        __skillcat_data['name'] = skillCat.find("fullname").text
        __skillcat_data['group'] = skillCat.find("group").text
        __skillcat_data['description'] = skillCat.find("description").text.replace("\n", "").replace("\t", "").strip()
        try:
            __skillcat_data['stats'] = skillCat.find("stats").text.split("/")
        except:
            __skillcat_data['stats'] = [ "realm" ]
        __typeInt = int(skillCat.find("type").text)
        __typeString = "SM"
        if (__typeInt == 1): __typeString = "MM"
        elif (__typeInt == 3): __typeString = "OB"
        elif (__typeInt == 4): __typeString = "SP"
        elif (__typeInt == 5): __typeString = "SC"
        __skillcat_data['type'] = __typeString
        __typeInt = int(skillCat.find("calc").text)
        if (__typeInt == 1): __skillcat_data['skillprog'] = 2
        elif (__typeInt == 2): __skillcat_data['skillprog'] = 3
        elif (__typeInt == 3): __skillcat_data['skillprog'] = 1
        elif (__typeInt == 4): __skillcat_data['skillprog'] = -1
        elif (__typeInt == 5): __skillcat_data['skillprog'] = -1
        __filename = __DATA + "/skills/" + __skillcat_data['name'].replace("/", "_") + ".json"
        f = open(__filename, 'wb')
        f.write(json.dumps( __skillcat_data , indent=3, sort_keys=True))
        f.close()
    __racedata = __reference.find("racedata")
    for race in __racedata.find("list"):
        __race_data = {}
        raceIndex = race.find("name").text.lower().replace(" ", "").replace("-", "")
        __race_data['sources'] = []
        __race_data['refs'] = {}
        __race_data["name"] = race.find("name").text
        __race_data["plural_name"] = race.find("title").text
        __race_data['description'] = None
        __race_data["race_bonus"] = {}
        __race_data["race_bonus"]["st"] = int(race.find("statbonuses").find("strength").text)
        __race_data["race_bonus"]["qu"] = int(race.find("statbonuses").find("quickness").text)
        __race_data["race_bonus"]["pr"] = int(race.find("statbonuses").find("presence").text)
        __race_data["race_bonus"]["in"] = int(race.find("statbonuses").find("intuition").text)
        __race_data["race_bonus"]["em"] = int(race.find("statbonuses").find("empathy").text)
        __race_data["race_bonus"]["co"] = int(race.find("statbonuses").find("constitution").text)
        __race_data["race_bonus"]["ag"] = int(race.find("statbonuses").find("agility").text)
        __race_data["race_bonus"]["re"] = int(race.find("statbonuses").find("reasoning").text)
        __race_data["race_bonus"]["me"] = int(race.find("statbonuses").find("memory").text)
        __race_data["race_bonus"]["sd"] = int(race.find("statbonuses").find("selfdiscipline").text)
        __race_data["resistances"] = {}
        __race_data["resistances"]["essence"] = int(race.find("resistances").find("essence").text)
        __race_data["resistances"]["channeling"] = int(race.find("resistances").find("channeling").text)
        __race_data["resistances"]["mentalism"] = int(race.find("resistances").find("mentalism").text)
        try:
            __race_data["resistances"]["arcane"] = int(race.find("resistances").find("arcane").text)
        except:
            __race_data["resistances"]["arcane"] = 0
        __race_data["resistances"]["poison"] = int(race.find("resistances").find("poison").text)
        __race_data["resistances"]["disease"] = int(race.find("resistances").find("disease").text)
        __race_data["resistances"]["terror"] = int(race.find("resistances").find("terror").text)
        __race_data["soul_departure"] = int(race.find("souldep").text)
        __race_data["stat_decline"] = int(race.find("statdec").text)
        __race_data["recovery_multiplier"] = race.find("recx").text
        __race_data["starting_languages"] = int(race.find("languages").text)
        __race_data["base_move"] = int(race.find("bmr").text)
        __race_data["max_hits"] = int(race.find("maxhits").text)
        __race_data['adolescence'] = {}
        __adolescence = __reference.find("adolescence")
        for ad in __adolescence.find("list"):
            for r in ad.find("rank"):
                if (r.tag == raceIndex):
                    __race_data['adolescence'][ad.find("name").text] = int(r.text)
        __filename = __DATA + "/races/"+raceIndex+".json"
        f = open(__filename, 'wb')
        f.write(json.dumps( __race_data , indent=3, sort_keys=True))
        f.close()
    for npc in __reference.find("npcs"):
        __npc_data = {}
        __dirname = __DATA + 'npc/' + npc.find("group").text
        try:
            os.stat(__dirname)
        except:
            os.mkdir(__dirname)
        if (len(npc.find("subgroup").text) > 0):
            __dirname = __DATA + 'npc/' + npc.find("group").text +"/"+ npc.find("subgroup").text
            try:
                os.stat(__dirname)
            except:
                os.mkdir(__dirname)
        __filename = __dirname +"/"+ npc.find("name").text +".json"
        __npc_data['sources'] = []
        __npc_data['refs'] = {}
        __npc_data["name"] = npc.find("name").text
        __npc_data["sources"] = []
        __npc_data["group"] = npc.find("group").text
        __npc_data["subgroup"] = npc.find("subgroup").text
        __npc_data["level"] = int(npc.find("level").text)
        __npc_data["basemove"] = int(npc.find("baserate").text)
        __npc_data["mnbonus"] = int(npc.find("mnbonus").text)
        __npc_data["hits"] = int(npc.find("hits").text)
        __npc_data["size"] = int(npc.find("size").text)
        __npc_data["AT"] = int(npc.find("at").text)
        __npc_data["DB"] = int(npc.find("db").text)
        try:
            __npc_data["profession"] = npc.find("profession").text
        except:
            pass
        __npc_data["abilities"] = []
        for a in npc.find("abilities"):
            __npc_data["abilities"].append(a.text)
        __npc_data["defences"] = []
        for d in npc.find("defences"):
            __my_value = {}
            __my_value['name'] = d.find("name").text
            try:
                __my_value['melee_bonus'] = int(d.find("meleebonus").text)
            except:
                pass
            try:
                __my_value['missile_bonus'] = int(d.find("missilebonus").text)
            except:
                pass
            __npc_data["defences"].append(__my_value)
        try:
            __npc_data["maxpace"] = int(npc.find("maxpace").text)
        except:
            __npc_data["maxpace"] = None
        try:
            __npc_data["levelcode"] = npc.find("levelcode").text
        except:
            __npc_data["levelcode"] = None
        try:
            __npc_data["hitscode"] = npc.find("hitscode").text
        except:
            __npc_data["hitscode"] = None
        try:
            __npc_data["ms"] = int(npc.find("ms").text)
        except:
            __npc_data["ms"] = None
        try:
            __npc_data["aq"] = int(npc.find("aq").text)
        except:
            __npc_data["aq"] = None
        try:
            __npc_data["critmod"] = npc.find("critmod").text
            if __npc_data["critmod"] == "1":
                __npc_data["critmod"] = None
        except:
            __npc_data["critmod"] = None
        try:
            __npc_data["imunity"] = npc.find("imunity").text
        except:
            __npc_data["imunity"] = None
        try:
            __npc_data["num"] = npc.find("num").text
        except:
            __npc_data["num"] = None
        try:
            __npc_data["treasure"] = npc.find("treasure").text
        except:
            __npc_data["treasure"] = None
        try:
            __npc_data["bonusep"] = npc.find("bonusep").text
        except:
            __npc_data["bonusep"] = None
        try:
            __npc_data["outlook"] = npc.find("outlook").text
        except:
            __npc_data["outlook"] = None
        try:
            __npc_data["iq"] = int(npc.find("iq").text)
        except:
            __npc_data["iq"] = None
        try:
            __npc_data["climate"] = npc.find("climate").text
        except:
            __npc_data["climate"] = None
        try:
            __npc_data["locale"] = npc.find("locale").text
        except:
            __npc_data["locale"] = None
        try:
            __npc_data["freq"] = int(npc.find("freq").text)
        except:
            __npc_data["freq"] = None
        try:
            __npc_data["description"] = npc.find("description").text
        except:
            __npc_data["description"] = None
        try:
            __npc_data["notes"] = npc.find("notes").text
        except:
            __npc_data["notes"] = None
        __npc_data["attacks"] = []
        try:
            for attack in npc.find("weapons"):
                __my_value = {}
                __my_value['OB'] = int(attack.find("ob").text)
                __my_value['name'] = attack.find("name").text
                __my_value['type'] = int(attack.find("type").text)
                __my_value['usage'] = None
                __my_value['sequence_same_round'] = None
                __my_value['sequence_next_round'] = None
                __my_value['group_attack'] = None
                __my_value['multi_attack'] = None
                __my_value['critical'] = None
                try:
                    __my_value["table"] = [ attack.find("attacktable").find("tableid").text, attack.find("attacktable").find("name").text]
                except:
                    __my_value["table"] = []
                __npc_data["attacks"].append(__my_value)
        except:
            pass
        __npc_data["skills"] = []
        for skill in npc.find("skills"):
            __my_value = {}
            __my_value['name'] = skill.find("name").text
            __my_value['bonus'] = int(skill.find("bonus").text)
            try:
                __my_value['ranks'] = int(skill.find("ranks").text)
            except:
                __my_value['ranks'] = None
            __npc_data["skills"].append(__my_value)
        __npc_data["spells"] = []
        for spell in npc.find("spells"):
            __my_value = {}
            __my_value['name'] = skill.find("name").text
            __npc_data["spells"].append(__my_value)
        f = open(__filename, 'wb')
        f.write(json.dumps( __npc_data , indent=3, sort_keys=True))
        f.close()
    __price_destination = [ "town", "city", "rural"]
    for eqlist in __reference.find("equipment"):
        errNo = 0
#        print eqlist.tag
        for eq in eqlist.find("list"):
            __eq = {}
            __eq['sources'] = []
            __eq['refs'] = {}
            __eq['listing'] = "default"
            try:
                __eq['id'] = int(eq.find("inum").text)
            except:
                __eq['id'] = 0
            try:
                __eq['type'] = int(eq.find("type").text)
                if (__eq['type'] == 13 or __eq['type'] == 17):
                    if (eq.tag.find("herb") > -1):
                        __eq['type'] = 131
                    elif (eq.tag.find("bread") > -1):
                        __eq['type'] = 132
                    elif (eq.tag.find("intox") > -1):
                        __eq['type'] = 133
                    elif (eq.tag.find("poison") > -1):
                        __eq['type'] = 134
            except:
                __eq['type'] = 0
            __group = eqtype(__eq['type'])
            __eq['group'] = __group
            try:
                __eq['id'] = int(eq.find("inum").text)
            except:
                try:
                    __eq['name'] = eq.find("inum").text
                except:
                    pass
                __eq['id'] = 0
            try:
                __eq['name'] = eq.find("name").text
            except:
                __eq['name'] = eq.tag
            try:
                __eq['length'] = float(eq.find("length").text)
            except:
                __eq['length'] = None
            try:
                __eq['length_str'] = eq.find("length_s").text
            except:
                __eq['length_str'] = None
            try:
                __eq['weight'] = float(eq.find("weight").text)
            except:
                __eq['weight'] = None
            try:
                __eq['weight_str'] = eq.find("weight_s").text
            except:
                __eq['weight_str'] = None
            try:
                __eq['description'] = eq.find("description").text.replace("\n", "").replace("\t", "").strip()
            except:
                __eq['description'] = None
                pass
            try:
                __eq['production_time'] = eq.find("prod").text
            except:
                __eq['production_time'] = None
            try:
                __eq['AT'] = int(eq.find("armortype").text)
            except:
                __eq['AT'] = None
            try:
                __eq['strength'] = int(eq.find("strength").text)
            except:
                __eq['strength'] = None
            try:
                __eq['breakfactor'] = eq.find("breakfactor").text
            except:
                __eq['breakfactor'] = None
            try:
                __eq['level'] = eq.find("level").text
            except:
                __eq['level'] = None
            try:
                __eq['charges'] = eq.find("charges").text
            except:
                __eq['charges'] = None
            try:
                __eq['composition'] = eq.find("composition").text
            except:
                __eq['composition'] = None
            try:
                __eq['use'] = eq.find("use").text
            except:
                __eq['use'] = None
            try:
                __eq['size'] = eq.find("size").text
            except:
                __eq['size'] = None
            try:
                __eq['OB'] = eq.find("ob").text
            except:
                __eq['OB'] = None
            try:
                __eq['capacity'] = eq.find("capacity").text
            except:
                __eq['capacity'] = None
            try:
                __eq['ft/rnd'] = eq.find("ftrn").text
            except:
                __eq['ft/rnd'] = None
            try:
                __eq['mi/hr'] = eq.find("mihr").text
            except:
                __eq['mi/hr'] = None
            try:
                __eq['maneuver bonus'] = eq.find("mnb").text
            except:
                __eq['maneuver bonus'] = None
            try:
                __eq['ht/wt'] = eq.find("htwt").text
            except:
                __eq['ht/wt'] = None
            try:
                __eq['fumble'] = eq.find("fumble").text
            except:
                __eq['fumble'] = None
            try:
                __eq['range_mod'] = {}
                __eq['range_mod']["point blank"] = (int(eq.find("rng1").text), int(eq.find("mod1").text) )
                __eq['range_mod']["short"] = (int(eq.find("rng2").text), int(eq.find("mod2").text) )
                __eq['range_mod']["medium"] = (int(eq.find("rng3").text), int(eq.find("mod3").text) )
                __eq['range_mod']["long"] = (int(eq.find("rng4").text), int(eq.find("mod4").text) )
                __eq['range_mod']["extreme"] = (int(eq.find("rng5").text), int(eq.find("mod5").text) )
            except:
                __eq['range_mod'] = None
            try:
                __eq['attack table'] = [ eq.find("attacktable").find("tableid").text, eq.find("attacktable").find("name").text]
            except:
                __eq['attack table'] = None
            try:
                __eq['armor_mod'] = {}
                __eq['armor_mod']['plate'] = int(eq.find("at17_20").text)
                __eq['armor_mod']['chain mail'] = int(eq.find("at13_16").text)
                __eq['armor_mod']['rigid leather'] = int(eq.find("at9_12").text)
                __eq['armor_mod']['soft leather'] = int(eq.find("at5_8").text)
                __eq['armor_mod']['skin'] = int(eq.find("at1_4").text)
                __eq['armor_mod']['flak'] = None
            except:
                __eq['armor_mod'] = None
            try:
                tmp = int(eq.find("rngslots").text)
                if (tmp == 1): __eq['maxrange'] = "point blank"
                elif (tmp == 2): __eq['maxrange'] = "short"
                elif (tmp == 3): __eq['maxrange'] = "medium"
                elif (tmp == 4): __eq['maxrange'] = "long"
                elif (tmp == 5): __eq['maxrange'] = "extreme"
                else: __eq['maxrange'] = tmp
            except:
                __eq['maxrange'] = None
            try:
                __eq['special'] = eq.find("special").text
            except:
                __eq['special'] = None
            try:
                __eq['area of effect'] = eq.find("aoe").text
            except:
                __eq['area of effect'] = None
            try:
                __eq['form'] = eq.find("form").text.lower().split("/")[0]
                __eq['prep'] = eq.find("form").text.lower().split("/")[1]
            except:
                __eq['form'] = None
                __eq['prep'] = None
            try:
                __eq['climate'] = eq.find("codes").text.split("-")[0]
                __eq['locale'] = eq.find("codes").text.split("-")[1]
                __eq['find_diff'] = eq.find("codes").text.split("-")[2]
            except:
                __eq['climate'] = None
                __eq['locale'] = None
                __eq['find_diff'] = None
            try:
                __eq['effect'] = eq.find("effect").text
            except:
                __eq['effect'] = None
            __eq['AF'] = None
            try:
                if (__eq['effect'].find("AF") == 0):
                    __eq['AF'] = int(re.findall("\d+", __eq['effect'])[0])
            except:
                pass
            try:
                if ((__eq['level'] == None) and (__eq['effect'].lower().find("(lvl") > -1)):
                    __eq['level'] = int(re.findall("\d+", __eq['effect'])[0])
            except:
                pass
            __eq['price'] = None
            for savefile in __price_destination:
                __eq['available'] = savefile
                try:
                    __eq['price'] = eq.find(savefile).text
                except:
                    continue
                if (__eq['price'] == "-"):
                    continue
                __dirname = __DATA + "eq/"
                try:
                    os.stat(__dirname)
                except:
                    os.mkdir(__dirname)
                __dirname = __DATA + "eq/default/"
                try:
                    os.stat(__dirname)
                except:
                    os.mkdir(__dirname)
                __dirname = __DATA + "eq/default/" + savefile + "/"
                try:
                    os.stat(__dirname)
                except:
                    os.mkdir(__dirname)
                __dirname = __DATA + "eq/default/" + savefile + "/" + __group + "/"
                try:
                    os.stat(__dirname)
                except:
                    os.mkdir(__dirname)
                try:
                    __file_name = eq.find("name").text.lower().replace("(", "_").replace(")", "_").replace("/", "_").replace("*", "").replace("'", "").replace(" ", "")
                except:
                    __file_name = "error"+errNo
                    errNo = errNo + 1
                __filename = __dirname + __file_name + ".json"
                f = open(__filename, 'wb')
                f.write(json.dumps( __eq , indent=3, sort_keys=True))
                f.close()
#            if (__group == "unknown"):
#                print eq.tag, __eq['id'], __eq['name'], __eq['type'], __group
            
except:
    raise
#    pass
