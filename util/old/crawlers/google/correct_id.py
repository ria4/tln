#!/usr/bin/python
#encoding: utf-8

from pymongo import MongoClient

cli = MongoClient()
journal = cli.critique.journal

ids = {"Dedans AlloCiné": "",
       "La Défense sans pareil de la forteresse Deutschkreutz": "tt061394",
       "Les Médecins volants d'Afrique de l'Est": "tt0064334",
       "Les nains aussi ont commencé petits": "tt0065436",
       "Le pays du silence et de l'obscurité": "tt0067324",
       "Rêves": "tt0100998",
       "Hirondelles de saucisson": "",
       "Mondes Intérieurs, Mondes Extérieurs": "",
       "Wodaabe, les bergers du soleil": "tt0098669",
       "Gasherbrum, la montagne lumineuse": "tt0087317",
       "Les Contes de la lune vague après la pluie": "tt0046478",
       "Le Meurtrier terriblement lent à l'Arme extrêmement inefficace": "tt1301160",
       "Shokuzai : Celles qui voulaient oublier": "tt2043616",
       "Shokuzai : Celles qui voulaient se souvenir": "tt2043616",
       "Delicatessen": "tt0101700",
       "Les Mille et Une Nuits - Volume 3 : L'Enchanté": "tt4692242",
       "Les Mille et Une Nuits - Volume 1 : L'Inquiet": "tt3284178",
       "Madonna": "tt4636074",
       "Messes noires et Snuff movies en France": "",
       "Les Petits canards de papier": "",
       "La gueule que tu mérites": "tt0442940",
       "L'île de Giovanni": "tt3178174",
       "Sitcom": "tt0157044",
       "Heimat : Chronique d'un rêve / L'Exode": "tt1998204",
       "Le Paradis": "tt3971202",
       "Le Garçon et le Monde": "tt3183630",
       "Tokyo !": "tt0976060",
       "Sixième Sens": "tt0167404",
       "La Mouche": "tt0091064",
       "Sacrés caractères !": "",
       "Tutotal": "",
       "Le Chant d'une île": "tt0228761",
       "Toto et ses soeurs": "tt2234537",
       "Un jour avec, un jour sans": "tt4768776",
       "Eva ne dort pas": "tt2953182",
       "Dream Work": "tt0303331",
       "Belladonna": "tt0071203",
       "Musique brute, handicap et contre-culture": "",
       "Les Wanted Brothers : Le Chat d'la grand mère d'Abdel Krim": "",
       "Mad Love in New York": "tt3687186",
       "Vaiana, la légende du bout du monde": "tt3521164",
       "Trans, c'est mon genre": "tt6214362",
       "Margot": "tt3209868",
       "Les Enquêtes du département V : Miséricorde": "tt2438644",
       "Requiem pour Noriko": "tt0468820",
       "Betito": "",
       "Le hérisson dans le brouillard": "tt0073099",
       "Personne ne veut jouer avec moi": "tt0074907",
       "Bruno S. - Estrangement is death": "tt0474572",
       "Redemption": "tt3123116"
       }

for item, imdb_id in ids.iteritems():
    journal.update_one({'info.title': item}, {"$set": {"info.$.imdb_id": imdb_id}})

