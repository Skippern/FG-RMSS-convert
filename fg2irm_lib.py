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
    __professions = __reference.find("professions")
    __professions_data = {}
    for prof in __professions:
        __professions_data[prof.tag] = {}
        __professions_data[prof.tag]['name'] = prof.find("name").text
        __professions_data[prof.tag]['description'] = prof.find("text")
        __professions_data[prof.tag]['prime_stats'] = []
        __professions_data[prof.tag]['dev cost'] = {}
        __professions_data[prof.tag]['realm'] = prof.find("realm")
    __skilllist = __reference.find("skilllist")
    __skillcat = __skilllist.find("categoryskills")
    __categorylist = __skillcat.find("list")
    __skillcat_data = {}
    __skillcat_data['categories'] = []
    catIndex = 0
    for skillCat in __categorylist:
        __skillcat_data['categories'].append({})
        __skillcat_data['categories'][catIndex]['name'] = skillCat.find("fullname").text
        __skillcat_data['categories'][catIndex]['group'] = skillCat.find("group").text
        __skillcat_data['categories'][catIndex]['description'] = skillCat.find("description").text
        try:
            __skillcat_data['categories'][catIndex]['stats'] = skillCat.find("stats").text.split("/")
        except:
            __skillcat_data['categories'][catIndex]['stats'] = [ "realm" ]
        __typeInt = int(skillCat.find("type").text)
        __typeString = "SM"
        if (__typeInt == 1): __typeString = "MM"
        elif (__typeInt == 3): __typeString = "OB"
        elif (__typeInt == 4): __typeString = "SP"
        elif (__typeInt == 5): __typeString = "SC"
        __skillcat_data['categories'][catIndex]['type'] = __typeString
        __typeInt = int(skillCat.find("calc").text)
        if (__typeInt == 1): __skillcat_data['categories'][catIndex]['skillprog'] = 2
        elif (__typeInt == 2): __skillcat_data['categories'][catIndex]['skillprog'] = 3
        elif (__typeInt == 3): __skillcat_data['categories'][catIndex]['skillprog'] = 1
        elif (__typeInt == 4): __skillcat_data['categories'][catIndex]['skillprog'] = -1
        elif (__typeInt == 5): __skillcat_data['categories'][catIndex]['skillprog'] = -1
        for cost in skillCat.find("costs"):
            __professions_data[cost.tag]['dev cost'][skillCat.find("fullname").text] = cost.text.split("/")
        catIndex += 1
    __racedata = __reference.find("racedata")
    __race_data = {}
    for race in __racedata.find("list"):
        raceIndex = race.find("name").text.lower().replace(" ", "").replace("-", "")
        __race_data[raceIndex] = {}
        __race_data[raceIndex]["name"] = race.find("name").text
        __race_data[raceIndex]["plural_name"] = race.find("title").text
        __race_data[raceIndex]["race_bonus"] = {}
        __race_data[raceIndex]["race_bonus"]["st"] = int(race.find("statbonuses").find("strength").text)
        __race_data[raceIndex]["race_bonus"]["qu"] = int(race.find("statbonuses").find("quickness").text)
        __race_data[raceIndex]["race_bonus"]["pr"] = int(race.find("statbonuses").find("presence").text)
        __race_data[raceIndex]["race_bonus"]["in"] = int(race.find("statbonuses").find("intuition").text)
        __race_data[raceIndex]["race_bonus"]["em"] = int(race.find("statbonuses").find("empathy").text)
        __race_data[raceIndex]["race_bonus"]["co"] = int(race.find("statbonuses").find("constitution").text)
        __race_data[raceIndex]["race_bonus"]["ag"] = int(race.find("statbonuses").find("agility").text)
        __race_data[raceIndex]["race_bonus"]["re"] = int(race.find("statbonuses").find("reasoning").text)
        __race_data[raceIndex]["race_bonus"]["me"] = int(race.find("statbonuses").find("memory").text)
        __race_data[raceIndex]["race_bonus"]["sd"] = int(race.find("statbonuses").find("selfdiscipline").text)
        __race_data[raceIndex]["resistances"] = {}
        __race_data[raceIndex]["resistances"]["essence"] = int(race.find("resistances").find("essence").text)
        __race_data[raceIndex]["resistances"]["channeling"] = int(race.find("resistances").find("channeling").text)
        __race_data[raceIndex]["resistances"]["mentalism"] = int(race.find("resistances").find("mentalism").text)
        try:
            __race_data[raceIndex]["resistances"]["arcane"] = int(race.find("resistances").find("arcane").text)
        except:
            __race_data[raceIndex]["resistances"]["arcane"] = 0
        __race_data[raceIndex]["resistances"]["poison"] = int(race.find("resistances").find("poison").text)
        __race_data[raceIndex]["resistances"]["disease"] = int(race.find("resistances").find("disease").text)
        __race_data[raceIndex]["resistances"]["terror"] = int(race.find("resistances").find("terror").text)
        __race_data[raceIndex]["soul_departure"] = int(race.find("souldep").text)
        __race_data[raceIndex]["stat_decline"] = int(race.find("statdec").text)
        __race_data[raceIndex]["recovery_multiplier"] = race.find("recx").text
        __race_data[raceIndex]["starting_languages"] = int(race.find("languages").text)
        __race_data[raceIndex]["base_move"] = int(race.find("bmr").text)
        __race_data[raceIndex]["max_hits"] = int(race.find("maxhits").text)
        __race_data[raceIndex]['adolescence'] = {}
    __adolescence = __reference.find("adolescence")
    for ad in __adolescence.find("list"):
        for r in ad.find("rank"):
            __race_data[r.tag]['adolescence'][ad.find("name").text] = int(r.text)
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
        __npc_data["name"] = npc.find("name").text
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
        try:
            __npc_data["defences"] = npc.find("defences").text
        except:
            pass
        __npc_data["attacks"] = []
        try:
            for attack in npc.find("weapons"):
                __my_value = {}
                __my_value['OB'] = attack.find("ob").text
                __my_value['name'] = attack.find("name").text
                __my_value['type'] = int(attack.find("type").text)
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
            __my_value['bonus'] = skill.find("bonus").text
            try:
                __my_value['ranks'] = skill.find("ranks").text
            except:
                __my_value['ranks'] = None
            __npc_data["skills"].append(__my_value)
        f = open(__filename, 'wb')
        f.write(json.dumps( __npc_data , indent=3, sort_keys=True))
        f.close()
except:
    raise
    pass
