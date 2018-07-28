#===============================================================================================================
#
# -- PROgram - A ZenGM Football Draft Class Creator by immatx --
# -- Last Updated: 2018.07.28 --
# -- Initial Release -- 2018.07.26 --
#
#===============================================================================================================
#
# - Version History -
#
#---------------------------------------------------------------------------------------------------------------
#
# 2018.07.26 - New Feature: Added option to import custom college list.
# 2018.07.28 - Bug Fixed: Players will no longer not show up on the roster screen after being drafted. Also
#              added a catch for potential negative ratings.
#
#===============================================================================================================
#
# - Introduction -
#
#---------------------------------------------------------------------------------------------------------------
#
# This program allows you to export draft classes from ZenGM College Football into ZenGM Pro Football without
# going through the hassel of manually importing them all. Since this isn't built directly into the ZenGM
# code there is still some work that must be done by the user, but this program is designed specifically
# to decrease that process from several hours down to about 30 minutes of work.
#
#===============================================================================================================
#
# - Instructions -
#
#---------------------------------------------------------------------------------------------------------------
#
# 1) Copy paste all needed players into a text file
#
# 	a) Before adding another player, put a | behind the end of the last player
#
# 		ex) "name": "Aaron McLaughlin",|
#
# 2) Navigate to the program location in command prompt / terminal
#
# 3) Run the program
# 
# 		ex) python program.py (this runs the script)
# 
# 4) (Optional) Enter a custom colleges file.
#
# 	a) You can find the list of your colleges by searching 'teamregionscache' in the export
#
# 	b) Simply copy and paste the entire list into a text file and run it
# 
# 5) Enter the file with the list of players
#
# 		ex) Enter the file name for the draft class => 2024 draft class
#
# 6) Upload the resulting json file newdraftclass.json into your ZenGM NFL draft class slot
#
# 	a) If you wish to keep each instance of the output, change the name prior to running the program again
#
#===============================================================================================================
#
# - Potential Errors -
#
#---------------------------------------------------------------------------------------------------------------
#
# 1) If the ending of the skills section inside of ratings doesn't have the ending ] on a seperate line it can
# result in a mis-write of the json file. Simply moving the ] onto the next line and re-running the program
# will fix the issue. Also manually fixing it in the json is rather simple so that's another option.
#
# 		ERROR MESSAGE: None
#
# 2) If you accidentally deleted a comma while pasting players into the text file then the draft class won't
# upload. Usually the deleted comma is after a player's name, so you can just control f "name" in the new
# json or the text file to see where the missing comma goes. If it's not after a name then you'll just have
# to manually go through each line. :(
#
# 		ERROR MESSAGE: None
#
# 3) If a player was cut or was a transfer in the export then they may not belong to any team, resulting in this 
# error. This is simply due to slightly different player info and in a slightly different order. It can be 
# avoided by using an export in which all drafted players are already on a team, or manually fixing the data in 
# the text file prior to running the program.
#
# 	a) This error can also occur when transfer players have stats for two different teams. Just delete the
# 	secondary tid under tid stats and the error will go away.
#
# 		ERROR MESSAGE: tid = int(file[i][-11][-3:-1])
# 				ValueError: invalid literal for int() with base 10: ' ]'
#
#===============================================================================================================
#
# - Stat Caps Setup -
#
#---------------------------------------------------------------------------------------------------------------
#
# The values below are the max values for an incoming rookie to have. So any stat that is a 100 will be lowered
# to equal the value placed below. Additionally, any stat below 100 will be lowered in proportion to the new
# cap. If you wish to change positional stat caps or how good rookies are when entering the league, all you
# need to do is raise or lower the caps until you have the results you're looking for. More caps can be added
# or some removed at the user's leasure, just make sure the last stat in each list doesnt have a comma after it.
#
# hgt = speed, stre = strength, spd = endurance, jmp = athleticism, endu = height, hnd = hands, ins = game iq,
# dnk = tougness, ft = awareness, fg = aggressiveness, tp = motor, blk = passing, stl = receiving, drb = blocking,
# pss = defrush, reb = tackling, cvr = coverage, kck = kicking
#
#===============================================================================================================

stat_caps = {

	#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
	#
	# - Quarterback Caps -
	#
	#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

	"QB": {
		"hgt": 0.75,
		"stre": 0.80,
		"spd": 0.70,
		"jmp": 0.70,
		"ins": 0.75,
		"dnk": 0.65,
		"ft": 0.55,
		"blk": 0.65
	},

	#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
	#
	# - Runningback Caps -
	#
	#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

	"RB": {
		"hgt": 0.80,
		"stre": 0.75,
		"spd": 0.55,
		"jmp": 0.70,
		"hnd": 0.60,
		"dnk": 0.75,
		"ft": 0.65,
		"stl": 0.70,
		"drb": 0.65
	},

	#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
	#
	# - Wide Receiver Caps -
	#
	#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

	"WR": {
		"hgt": 0.80,
		"stre": 0.70,
		"jmp": 0.70,
		"dnk": 0.75,
		"ft": 0.55,
		"stl": 0.60,
		"drb": 0.63
	},

	#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
	#
	# - Tight End Caps -
	#
	#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

	"TE": {
		"hgt": 0.70,
		"stre": 0.75,
		"dnk": 0.80,
		"ft": 0.55,
		"stl": 0.65,
		"drb": 0.70
	},

	#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
	#
	# - Offensive Lineman Caps -
	#
	#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

	"OL": {
		"hgt": 0.85,
		"stre": 0.85,
		"jmp": 0.80,
		"hnd": 0.80,
		"dnk": 0.70,
		"ft": 0.70,
		"drb": 0.80
	},

	#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
	#
	# - Defensive Lineman Caps -
	#
	#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

	"DL": {
		"hgt": 0.70,
		"stre": 0.70,
		"jmp": 0.67,
		"hnd": 0.60,
		"fg": 0.80,
		"tp": 0.65,
		"pss": 0.75,
		"reb": 0.70
	},

	#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
	#
	# - Linebacker Caps -
	#
	#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

	"LB": {
		"hgt": 0.72,
		"stre": 0.70,
		"jmp": 0.72,
		"fg": 0.65,
		"tp": 0.67,
		"pss": 0.70,
		"reb": 0.80,
		"cvr": 0.58
	},

	#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
	#
	# - Safety Caps -
	#
	#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

	"S": {
		"hgt": 0.70,
		"stre": 0.70,
		"jmp": 0.65,
		"hnd": 0.63,
		"tp": 0.65,
		"reb": 0.70,
		"cvr": 0.75
	},

	#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
	#
	# - Cornerback Caps -
	#
	#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

	"CB": {
		"hgt": 0.75,
		"hnd": 0.70,
		"fg": 0.67,
		"tp": 0.65,
		"reb": 0.70,
		"cvr": 0.70
	},

	#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
	#
	# - Kicker Caps -
	#
	#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

	"K": {
		"stre": 0.90,
		"jmp": 0.80,
		"ins": 0.77,
		"ft": 0.70
	}

}

#===============================================================================================================
#
# - Potential Setup -
#
#---------------------------------------------------------------------------------------------------------------
#
# Potential is partially randomized and partially calculated based on age, overall, and estimated draft 
# position. Either one of these three can be given a greater or lower weight in order to customize the amount
# of randomness potential can have.
#
#===============================================================================================================

# The average decrease in potential for each year older a prospect is
p_age = 7.5

# The average decrease in potential per increase in overall.
p_ovr = 0.45

# The average decrease in potential for each estimated pick prior to the player being picked
p_draft = 0.08

# The average degree of randomness to which potential might vary outside of the result
p_random = 5

#===============================================================================================================
#
# - MAIN CODE -
#
#---------------------------------------------------------------------------------------------------------------
#
# Editting beyond here may result in possible file loss or damage, or potentially rendering this program
# entirely useless. Edit at your own risk
#
#===============================================================================================================
import random

# Estimates overall based on positional growths
def check_ovr (overalls, grade, sum, i, position):
	if overalls[position][i] != 0:
		sum += float(grade) / overalls[position][i]
	return(sum)

# Calculates potential based on the pre-defined multipliers
def calc_potential (est_ovr, coll_ovr, potential, age, position, page, povr, pdraft, prandom):
	npot = 100
	npot -= (age - 20) * page

	if (position == "RB") or (position == "WR") or (position == "CB"):
		npot -= (est_ovr - 30) * povr * 3 / 2
		if ((coll_ovr + potential) > 190) and (coll_ovr > 90):
			dpos = 0
		elif ((coll_ovr + potential) > 190) or (coll_ovr > 90):
			dpos = 10
		elif coll_ovr > 88:
			dpos = 30
		elif ((coll_ovr + potential) > 175) and (coll_ovr > 85):
			dpos = 60
		elif coll_ovr > 83:
			dpos = 120
		else:
			dpos = 200
		npot -= dpos * pdraft * 1 / 2

	elif position == "QB":
		npot -= (est_ovr - 30) * povr * 3 / 4
		if ((coll_ovr + potential) > 185) and (coll_ovr > 90):
			dpos = 0
		elif coll_ovr > 90:
			dpos = 10
		elif coll_ovr > 87:
			dpos = 30
		elif ((coll_ovr + potential) > 170):
			dpos = 60
		elif coll_ovr > 83:
			dpos = 120
		else:
			dpos = 200
		npot -= dpos * pdraft * 2

	else:
		npot -= (est_ovr - 30) * povr
		if ((coll_ovr + potential) > 190) and (coll_ovr > 92):
			dpos = 0
		elif ((coll_ovr + potential) > 180) and (coll_ovr > 89):
			dpos = 10
		elif ((coll_ovr + potential) > 180) or (coll_ovr >87):
			dpos = 30
		elif coll_ovr > 85:
			dpos = 60
		elif coll_ovr > 82:
			dpos = 120
		else:
			dpos = 200
		npot -= dpos * pdraft

	npot += random.randint((prandom * -1), prandom)
	npot = "{:.0f}".format(npot)
	return(npot)

# Reduces all ratings in proportion to a player's position's stat caps
def pro_ratings (ratings, grades, overalls, ovr, potential, position, caps):
	total = 0
	for i in range(len(grades)):
		a = grades[i].split(" ")[-1]

		# Changes ratings and calculates total pro overall
		if ratings[i] in caps[position]:
			x = (int(a[0:-1]) - ((1 - caps[position][ratings[i]]) * 100))
			if x < 0:
				x = 0
			total = check_ovr(overalls, x, total, i, position)
			grades[i] = "          \"" + ratings[i] + "\": " + "{:.0f}".format(x) + grades[i][-1]
		else:
			total = check_ovr(overalls, int(a[0:-1]), total, i, position)
	return(grades, total)

# Compares team id to the school name so that each players school shows up as their location
def find_college (schools, team_id):
	return(schools[team_id])

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# List of colleges in the NZCFL
colleges = [ "Boston College", "Virginia Tech", "Louisville", "Pittsburgh", "Navy", "Wake Forest", "Syracuse", "Virginia", "Clemson", "Florida State", "Georgia Tech", "North Carolina", "Miami", "Army", "Central Florida", "Duke", "Ohio State", "Penn State", "Michigan", "Notre Dame", "Rutgers", "Maryland", "Cincinnati", "Purdue", "Wisconsin", "Michigan State", "Iowa", "Nebraska", "Northwestern", "Minnesota", "Illinois", "Indiana", "Florida", "Georgia", "Ole Miss", "Mississippi State", "Tennessee", "South Carolina", "Kentucky", "Marshall", "Alabama", "LSU", "Auburn", "Texas A&M", "Missouri", "Arkansas", "Vanderbilt", "Memphis", "Oregon", "Utah", "Washington", "Boise State", "California", "Washington State", "Oregon State", "Colorado", "Stanford", "USC", "Arizona", "UCLA", "Arizona State", "San Diego State", "New Mexico", "Hawaii", "Oklahoma", "West Virginia", "Kansas State", "BYU", "Colorado State", "Kansas", "Iowa State", "Wyoming", "Oklahoma State", "Texas Christian", "Texas", "Texas Tech", "Houston", "Baylor", "Tulsa", "Southern Methodist" ]

# List of ratings used in ZenGM Football
ratings = [ "hgt", "stre", "spd", "jmp", "endu", "hnd", "ins", "dnk", "ft", "fg", "tp", "blk", "stl", "drb", "pss", "reb", "cvr", "kck" ]

# Dictionary of how ratings impact overall by position
overalls = {
	"QB": [ 14.286, 7.69, 0, 14.286, 0, 0, 3.704, 14.286, 7.69, 0, 0, 3.704, 0, 0, 0, 0, 0, 0 ],
	"RB": [ 5.56, 5.56, 11.11, 11.11, 0, 11.11, 0, 5.56, 5.56, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
	"WR": [ 3.226, 12.5, 0, 12.5, 0, 0, 0, 12.5, 12.5, 0, 0, 0, 3.226, 12.5, 0, 0, 0, 0 ],
	"TE": [ 9.09, 9.09, 0, 0, 0, 0, 0, 5.88, 5.88, 0, 0, 0, 4.545, 4.545, 0, 0, 0, 0 ],
	"OL": [ 11.11, 5.56, 0, 11.11, 0, 5.56, 0, 11.11, 5.56, 0, 0, 0, 0, 5.56, 0, 0, 0, 0 ],
	"DL": [ 10, 10, 0, 10, 0, 10, 0, 0, 0, 5.26, 10, 0, 0, 0, 5.26, 7.14, 0, 0 ],
	"LB": [ 6.67, 6.67, 0, 25, 0, 0, 0, 0, 0, 6.67, 6.67, 0, 0, 0, 6.67, 6.67, 14.286, 0 ],
	"S": [ 5.26, 10, 0, 10, 0, 20, 0, 0, 0, 10, 10, 0, 0, 0, 0, 5.26, 5.26, 0 ],
	"CB": [ 3.226, 0, 0, 0, 0, 12.5, 0, 0, 0, 12.5, 12.5, 0, 0, 0, 0, 6.67, 3.226, 0 ],
	"K": [ 0, 2.778, 0, 11.11, 0, 0, 11.11, 0, 11.11, 0, 0, 0, 0, 0, 0, 0, 0, 2.778 ]
}

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Check if NZCFL / ask for list of colleges
use_colleges = True
while True:
	print("Use custom colleges?")
	import_colleges = input("Put 'Y' or 'N' for your answer => ")
	if import_colleges == "Y":
		filename = input("\nEnter the file name for the custom colleges => ") + ".txt"
		colleges = open(filename, "r").read().strip().split("\n")
		for i in range(len(colleges)):
			colleges[i] = colleges[i].split('"')
			colleges[i] = colleges[i][1]
			print(colleges[i])
		break
	elif import_colleges == "N":
		while True:
			print("\nUse the default 80 team NZCFL format? If your export uses over 80 teams this may cause an error.")
			default_colleges = input("Put 'Y' or 'N' for your answer => ")
			if default_colleges == "N":
				use_colleges = False
				break
			elif default_colleges == "Y":
				break
			else:
				print("\nPlease use a capital Y or a capital N\n")
		break
	else:
		print("\nPlease use a capital Y or a capital N\n")

# Reading in the text file and prepping it for use
filename = input("\nEnter the file name for the draft class => ") + ".txt"
file = open(filename, "r").read().strip().split("|")
output = open("newdraftclass.json", "w+")
for i in range(len(file)):
	file[i] = file[i].strip().split("\n")

output.write("{" + "\n" + "  \"version\": 27," + "\n" + "  \"players\": [" + "\n")

# Main code loop
for i in range(len(file)):

	# Sets important information as variables to be used later
	values = file[i][0:18]
	ovr = int(file[i][19][-3:-1])
	pot = int(file[i][20][-3:-1])
	tid = int(file[i][-11][-3:-1])
	pos = str(file[i][-6][-4:-2])
	my_school = "USA"
	if use_colleges == True:
		my_school = str(find_college(colleges, tid))
	if pos == "\"S":
		pos = "S"
	elif pos == "\"K":
		pos = "K"

	# Calls the pro rating converter
	pr = pro_ratings(ratings, values, overalls, ovr, pot, pos, stat_caps)
	pro_rat = pr[0]
	new_ovr = pr[1]

	# Calculates potential
	player_age = int(file[i][18][-5:-1]) - int(file[i][-18][-5:-1])
	new_pot = calc_potential(new_ovr, ovr, pot, player_age, pos, p_age, p_ovr, p_draft, p_random)

	# Joins all of the ratings data together into a string for the json
	new_ratings = "\n".join(pro_rat) + "\n" + "          \"ovr\": {:.0f}".format(new_ovr) + "," + "\n" + "          \"pot\": " + str(new_pot) + "\n" + file[i][-21] + "\n"
	if pos == "K":
		new_ratings += " " + file[i][-23][-7:-1] + "\n"
	else:
		new_ratings +=file[i][-22][-7:] + "\n"

	# Joins all of the player info together into a string for the json
	player_info = file[i][-1] + "\n" + "      \"tid\": -2," + "\n" + file[i][-6] + "\n" + file[i][-3] + "\n" + file[i][-5] + "\n" + file[i][-4] + "\n" + file[i][-19] + "\n" + file[i][-18] + "\n" + "        \"loc\": \"" + my_school + "\"" + "\n" + file[i][-16] + "\n" + "      \"ratings\": [" + "\n" + "        {" + "\n" + "          "
	
	# Writes all player data into the json
	output.write("    {" + "\n" + player_info + new_ratings)
	if file[i] != file[-1]:
		output.write("    }," + "\n")

output.write("    }" + "\n" + "  ]" + "\n" + "}")
output.close()