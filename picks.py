import webbrowser
from bs4 import BeautifulSoup
import requests 
import re
import numpy
import matplotlib.pyplot as plt


#declaring abbrieviation -> team name 
codes = {
	"ATL" : "Atlanta-Hawks",
	"BKN" : "Brooklyn-Nets",
	"BOS" : "Boston-Celtics",
	"CHA" : "Charlotte-Hornets",
	"CHI" : "Chicago-Bulls",
	"CLE" : "Cleveland-Cavaliers",
	"DAL" : "Dallas-Mavericks",
	"DEN" : "Denver-Nuggets",
	"DET" : "Detroit-Pistons",
	"GSW" : "Golden-State-Warriors",
	"HOU" : "Houston-Rockets",
	"IND" : "Indiana-Pacers",
	"LAC" : "Los-Angeles-Clippers",
	"LAL" : "Los-Angeles-Lakers",
	"MEM" : "Memphis-Grizzlies",
	"MIA" : "Miami-Heat",
	"MIL" : "Milwaukee-Bucks",
	"MIN" : "Minnesota-Timberwolves",
	"NOP" : "New-Orleans-Pelicans",
	"NYK" : "New-York-Knicks",
	"OKC" : "Oklahoma-City-Thunder",
	"ORL" : "Orlando-Magic",
	"PHI" : "Philadelphia-76ers",
	"PHX" : "Phoenix-Suns",
	"POR" : "Portland-Trail-Blazers",
	"SAC" : "Sacramento-Kings",
	"SAS" : "San-Antonio-Spurs",
	"TOR" : "Toronto-Raptors",
	"UTA" : "Utah-Jazz",
	"WAS" : "Washington-Wizards"
}
url = 'https://www.nba.com/players/todays-lineups' 
result = requests.get(url)
doc = BeautifulSoup(result.content, "html.parser")

doc = str(doc).replace("lastName\":\"", "SPLITHERERIGHTNOW")
doc = str(doc).replace("firstName\":\"", "SPLITHERERIGHTNOW")
doc = str(doc).replace("team\":\"", "SPLITHERERIGHTNOW")
lister = str(doc).split("SPLITHERERIGHTNOW")
newl = []
for liste in lister:
	newl.append(liste[0:20])

clean = []
for item in newl:
	clean.append(item.split("\"")[0])
clean.pop(0)
players_wrong_team = []
for xy in range(len(clean)):
	if xy % 3 == 0:
		players_wrong_team.append([clean[xy], clean[xy+1], clean[xy+2]])

players = []
for player in players_wrong_team:
	building_player = ["", "", "", "", ""]
	building_player[3] = player[0]
	building_player[4] = player[1]
	building_player[0] = re.sub(r"[^a-zA-Z0-9]","",player[0])
	building_player[1] = re.sub(r"[^a-zA-Z0-9]","",player[1])
	building_player[2] = codes[player[2]]

	players.append(building_player)

#declaring all players to be checked
#declaring "good" props- hit rate > 95 or <5
good_props = []

for player in players:
	player_first = player[0]
	player_alternatefirst = player[3]
	player_alternatelast = player[4]
	player_last = player[1]
	team = player[2]
	name = player_first + "-" + player_last

#player_first = "miles"
#player_last = "bridges"
#name = player_first + "-" + player_last
#team = "chicago-bulls"

	#function to get and store player lines

	url = "https://www.oddsshopper.com/odds/shop/nba/teams/" + team + "/players/" + player_alternatefirst + "%20" + player_alternatelast
	result = requests.get(url)
	doc = BeautifulSoup(result.content, "html.parser")
	x = str(doc)
	x = x.replace('<!-- -->', '::::::')
	x = x.replace('MuiTypography-root line MuiTypography-body1', '::::::')
	x = x.replace('odds/shop/NBA/offers/PlayerProps/', '::::::')
	x = x.split('::::::')
	arr = []
	list_of_props = ["Assists", "Blocks", "Points", "Pts+Reb+Ast", "Rebounds", "Steals", "3-Pointers"]
	for z in x:
		
		for prop in list_of_props:
			if(z[0:len(prop)] == prop):
				arr.append(prop)
				


		if(z[0:2] == "\">"):
			output = z[0:10]
			output = re.sub("[^\d\.]", "", output)
			arr.append(output)
	
	cut_dups = []
	for z in range(len(arr)):
		if z%2 == 0 and arr[z] in list_of_props:
			cut_dups.append([arr[z],arr[z+1]])


	res = []

	for i in cut_dups:
	    if i not in res:
	        res.append(i)





	#function to get and store player stats
	url = 'https://www.foxsports.com/nba/' + name.lower() + '-player-game-log?season=2021&seasonType=reg' 
	result = requests.get(url)
	doc = BeautifulSoup(result.content, "html.parser")
	scores = []
	pts = []
	ast = []
	blk = []
	ptsrebast = []
	reb = []
	stl = []
	three = []
	count = 0
	print(player_first)
	
	try: 
		for x in doc.find(class_="row-data lh-1pt43 fs-14"):
			pass
	except: 
		continue
		

	for x in doc.find(class_="row-data lh-1pt43 fs-14"):
		count = count + 1
		y = str(x).split('\n')
		array_of_scores = []
		
		for z in y:
			
			if len(str(z).strip()) <=5:
				array_of_scores.append(str(z).strip())

		if (array_of_scores[1] != "PAY" and array_of_scores[1] != "@PAY" and array_of_scores[1] != "IAH" and array_of_scores[1] != "@IAH" and array_of_scores[1] != "BAR" and array_of_scores[1] != "@BAR" and array_of_scores[1] != "WOR" and array_of_scores[1] != "@WOR"):
			if count > len(y):
				pts.append(int(array_of_scores[3]))
				ast.append(int(array_of_scores[10]))
				blk.append(int(array_of_scores[12]))
				ptsrebast.append(int(array_of_scores[10])+int(array_of_scores[3])+int(array_of_scores[9]))
				reb.append(int(array_of_scores[9]))
				stl.append(int(array_of_scores[11]))
		
				three.append(int(array_of_scores[5].split("/")[0]))
			scores.append(array_of_scores)

	#function to calculate percentage
	def calcPer(arr, num, over, checkstat):
		hit = 0
		total = 0
		statcodes = []
		#list_of_props = ["Assists", "Blocks", "Points", "Pts+Reb+Ast", "Rebounds", "Steals", "3-Pointers"]
		if checkstat == "Points":
			statcodes.append(3)
		if checkstat == "Assists":
			statcodes.append(10)
		if checkstat == "Blocks":
			statcodes.append(12)
		if checkstat == "Pts+Reb+Ast":
			statcodes.append(3)
			statcodes.append(10)
			statcodes.append(9)
		if checkstat == "Rebounds":
			statcodes.append(9)
		if checkstat == "Steals":
			statcodes.append(11)
		if checkstat == "3-Pointers":
			statcodes.append(5)

		for record in arr[:num]:
			statrecord = 0
			for stat in statcodes:
				if checkstat == "3-Pointers":
					number = record[stat].split('/')[0]
					statrecord += int(number)
				else:
					statrecord += int(record[stat])

			total += 1
			if (float(statrecord) > float(over)):

				hit += 1
		
		return hit/float(total)

	"""
	COMBINING TOPICS
	this will give you the percentage that the player hits over 1.5 three pointers in the last 5 games
	print(calcPer(scores, 5, 1.5, "3-Pointers"))
	"""
	#just testing assists
	"""
	for x in res:
		line = x[0]
	"""

	
	#change this to change weights
	array_of_weights = [0.1, 0.12, 0.18, 0.12, 0.1, 0.08, 0.1, 0.125, 0.075]

	for stat in res:
		checking = stat[0]
		over = float(stat[1])
		weight = 0
		totalhr = 0.0
		for last in range(3,10):
			totalhr += array_of_weights[weight] * (calcPer(scores, last, over, checking))
			weight += 1

		#adding full season
		totalhr += array_of_weights[7] * (calcPer(scores, len(arr), over, checking))



		x = []
		for y in range(len(pts)):
			x.append(y+1)


		if len(pts) != 0:
		#checking to see which stat to regress for
			if checking == "Points":
				mymodeler = numpy.poly1d(numpy.polyfit(x, pts, 3))
			elif checking == "Assists":
				mymodeler = numpy.poly1d(numpy.polyfit(x, ast, 3))
			elif checking == "Blocks":
				mymodeler = numpy.poly1d(numpy.polyfit(x, blk, 3))
			elif checking == "Pts+Reb+Ast":
				mymodeler = numpy.poly1d(numpy.polyfit(x, ptsrebast, 3))
			elif checking == "Rebounds":
				mymodeler = numpy.poly1d(numpy.polyfit(x, reb, 3))
			elif checking == "Steals":
				mymodeler = numpy.poly1d(numpy.polyfit(x, stl, 3))
			elif checking == "3-Pointers":
				mymodeler = numpy.poly1d(numpy.polyfit(x, three, 3))


			pred = mymodeler(len(x)+1)
			totalhr += array_of_weights[8] * (int(pred)/float(over))
		
			if totalhr > 0.80:
				
				good_props.append([player_first + " " + player_last + " " + checking + " o" + str(over), totalhr*100])

			if totalhr < 0.2:
				good_props.append([player_first + " " + player_last + " " + checking + " u" + str(over), (1.0-totalhr)*100])

		



	"""
	GRAPHING
	myline = numpy.linspace(1, len(pts), 100)
	plt.scatter(x, pts)
	plt.plot(myline, mymodel(myline))
	plt.show()
		#MIN	PTS	FG	3FG	FT	OFF REB	DEF REB	REB	AST	STL	BLK PF	TO	+/- 
	"""


locks = []
for good in good_props:
	if str.__contains__('Blocks', good[0]) or str.__contains__('Steals', good[0]):
		if good[1] > 100:
			locks.append(good)
	else:
		locks.append(good)

print(locks)
