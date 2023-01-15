import jsondiff as jd
import json

g = {
	"messages": [
		{
			"body": "halo",
			"cid": "0ad005ea-a150-4db7-8e1a-6209bedf473a@ares-parties.eu2.pvp.net",
			"game_name": "WatchFlankBro",
			"game_tag": "yoma",
			"id": "1669574397698:1",
			"mid": "0ad005ea-a150-4db7-8e1a-6209bedf473a@ares-parties.eu2.pvp.net:53f0e053-da42-5fe4-be34-326b738949a4@ru1.pvp.net:1669574397698:1",
			"name": "",
			"pid": "53f0e053-da42-5fe4-be34-326b738949a4@ru1.pvp.net",
			"puuid": "53f0e053-da42-5fe4-be34-326b738949a4",
			"read": "true",
			"region": "ru1",
			"time": "1669574398945",
			"type": "groupchat"
		},
		{
			"body": "help",
			"cid": "0ad005ea-a150-4db7-8e1a-6209bedf473a@ares-parties.eu2.pvp.net",
			"game_name": "WatchFlankBro",
			"game_tag": "yoma",
			"id": "1669574404945:2",
			"mid": "0ad005ea-a150-4db7-8e1a-6209bedf473a@ares-parties.eu2.pvp.net:53f0e053-da42-5fe4-be34-326b738949a4@ru1.pvp.net:1669574404945:2",
			"name": "",
			"pid": "53f0e053-da42-5fe4-be34-326b738949a4@ru1.pvp.net",
			"puuid": "53f0e053-da42-5fe4-be34-326b738949a4",
			"read": "true",
			"region": "ru1",
			"time": "1669574406301",
			"type": "groupchat"
		},
		{
			"body": "maybe now?",
			"cid": "0ad005ea-a150-4db7-8e1a-6209bedf473a@ares-parties.eu2.pvp.net",
			"game_name": "WatchFlankBro",
			"game_tag": "yoma",
			"id": "1669574489807:3",
			"mid": "0ad005ea-a150-4db7-8e1a-6209bedf473a@ares-parties.eu2.pvp.net:53f0e053-da42-5fe4-be34-326b738949a4@ru1.pvp.net:1669574489807:3",
			"name": "",
			"pid": "53f0e053-da42-5fe4-be34-326b738949a4@ru1.pvp.net",
			"puuid": "53f0e053-da42-5fe4-be34-326b738949a4",
			"read": "true",
			"region": "ru1",
			"time": "1669574491102",
			"type": "groupchat"
		},
		{
			"body": "why",
			"cid": "0ad005ea-a150-4db7-8e1a-6209bedf473a@ares-parties.eu2.pvp.net",
			"game_name": "WatchFlankBro",
			"game_tag": "yoma",
			"id": "1669574564813:4",
			"mid": "0ad005ea-a150-4db7-8e1a-6209bedf473a@ares-parties.eu2.pvp.net:53f0e053-da42-5fe4-be34-326b738949a4@ru1.pvp.net:1669574564813:4",
			"name": "",
			"pid": "53f0e053-da42-5fe4-be34-326b738949a4@ru1.pvp.net",
			"puuid": "53f0e053-da42-5fe4-be34-326b738949a4",
			"read": "true",
			"region": "ru1",
			"time": "1669574566196",
			"type": "groupchat"
		}
	]
}

h = {
	"messages": [
		{
			"body": "halo",
			"cid": "0ad005ea-a150-4db7-8e1a-6209bedf473a@ares-parties.eu2.pvp.net",
			"game_name": "WatchFlankBro",
			"game_tag": "yoma",
			"id": "1669574397698:1",
			"mid": "0ad005ea-a150-4db7-8e1a-6209bedf473a@ares-parties.eu2.pvp.net:53f0e053-da42-5fe4-be34-326b738949a4@ru1.pvp.net:1669574397698:1",
			"name": "",
			"pid": "53f0e053-da42-5fe4-be34-326b738949a4@ru1.pvp.net",
			"puuid": "53f0e053-da42-5fe4-be34-326b738949a4",
			"read": "true",
			"region": "ru1",
			"time": "1669574398945",
			"type": "groupchat"
		},
		{
			"body": "help",
			"cid": "0ad005ea-a150-4db7-8e1a-6209bedf473a@ares-parties.eu2.pvp.net",
			"game_name": "WatchFlankBro",
			"game_tag": "yoma",
			"id": "1669574404945:2",
			"mid": "0ad005ea-a150-4db7-8e1a-6209bedf473a@ares-parties.eu2.pvp.net:53f0e053-da42-5fe4-be34-326b738949a4@ru1.pvp.net:1669574404945:2",
			"name": "",
			"pid": "53f0e053-da42-5fe4-be34-326b738949a4@ru1.pvp.net",
			"puuid": "53f0e053-da42-5fe4-be34-326b738949a4",
			"read": "true",
			"region": "ru1",
			"time": "1669574406301",
			"type": "groupchat"
		},
		{
			"body": "maybe now?",
			"cid": "0ad005ea-a150-4db7-8e1a-6209bedf473a@ares-parties.eu2.pvp.net",
			"game_name": "WatchFlankBro",
			"game_tag": "yoma",
			"id": "1669574489807:3",
			"mid": "0ad005ea-a150-4db7-8e1a-6209bedf473a@ares-parties.eu2.pvp.net:53f0e053-da42-5fe4-be34-326b738949a4@ru1.pvp.net:1669574489807:3",
			"name": "",
			"pid": "53f0e053-da42-5fe4-be34-326b738949a4@ru1.pvp.net",
			"puuid": "53f0e053-da42-5fe4-be34-326b738949a4",
			"read": "true",
			"region": "ru1",
			"time": "1669574491102",
			"type": "groupchat"
		},
		{
			"body": "why",
			"cid": "0ad005ea-a150-4db7-8e1a-6209bedf473a@ares-parties.eu2.pvp.net",
			"game_name": "WatchFlankBro",
			"game_tag": "yoma",
			"id": "1669574564813:4",
			"mid": "0ad005ea-a150-4db7-8e1a-6209bedf473a@ares-parties.eu2.pvp.net:53f0e053-da42-5fe4-be34-326b738949a4@ru1.pvp.net:1669574564813:4",
			"name": "",
			"pid": "53f0e053-da42-5fe4-be34-326b738949a4@ru1.pvp.net",
			"puuid": "53f0e053-da42-5fe4-be34-326b738949a4",
			"read": "true",
			"region": "ru1",
			"time": "1669574566196",
			"type": "groupchat"
		},
		{
			"body": "s",
			"cid": "0ad005ea-a150-4db7-8e1a-6209bedf473a@ares-parties.eu2.pvp.net",
			"game_name": "WatchFlankBro",
			"game_tag": "yoma",
			"id": "1669574638684:5",
			"mid": "0ad005ea-a150-4db7-8e1a-6209bedf473a@ares-parties.eu2.pvp.net:53f0e053-da42-5fe4-be34-326b738949a4@ru1.pvp.net:1669574638684:5",
			"name": "",
			"pid": "53f0e053-da42-5fe4-be34-326b738949a4@ru1.pvp.net",
			"puuid": "53f0e053-da42-5fe4-be34-326b738949a4",
			"read": "true",
			"region": "ru1",
			"time": "1669574640070",
			"type": "groupchat"
		}
	]
}

f = jd.diff(g, h)


print(f)

if(f == {}):
    print("mtsm")

