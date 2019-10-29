# CRQ1
import pandas as pd
import numpy as np
import seaborn as sns
import json
import matplotlib.pyplot as plt

# OPENING THE FILES (IF YOU PASTE ON JUPYTER NOTEBOOK UPLOAD THE FILES AND JUST PUT 'matches-England.json" AS PATH)
with open('matches_England.json') as json_file:
    jmatches = json.load(json_file)

with open('teams.json') as json_file:
    jteams = json.load(json_file)
    
with open('events_England.json') as json_file:
    jevents = json.load(json_file)
    
with open('players.json') as json_file:
    play = json.load(json_file)
    
    
# CREATING DATA FRAME FROM FILES
match = pd.DataFrame(jmatches)
teams = pd.DataFrame(jteams)
events = pd.DataFrame(jevents)
plyer =  pd.DataFrame(play) 


# make the time intervals

def eventtime(matchPeriod, eventSec):

    import math
    if math.ceil(eventSec/60)>45:
        if matchPeriod == '1H':
            return '45+'
        else:
            return '90+'
    elif matchPeriod == '2H':
        return math.floor(math.ceil(eventSec/60)/10+4.5)
    else:
        return math.floor(math.ceil(eventSec/60)/10)
        
  events['timeintervals'] = events.apply(lambda x: eventtime(x['matchPeriod'], x['eventSec']), axis=1)
  
  
  ## find the goals
def goals(x):
    
    for i in x:
        if i['id']==101:
            return 1
        
events['golas'] = events['tags'].apply(goals)
goaltime = events[['timeintervals','golas']]
goaltime.dropna(axis=0, how='any', inplace= True)

# Plot the goals in time intervalse by seaborn
ss = pd.DataFrame(goaltime['timeintervals'].value_counts(), index=[0, 1, 2, 3, 4, '45+', 5, 6, 7, 8, 9, '90+'] )
import seaborn as sns

sns.barplot(ss.index , y = ss['timeintervals'] , data = ss, palette = 'Dark2' )

# same plot with pandas
ss.plot.bar()

# find the top 10 teamId by number of goals
events[['teamId', 'timeintervals','golas']].groupby('timeintervals').get_group(8).groupby('teamId').sum().sort_values(by=['golas'], ascending = False).head(10)

# make a data frame
plyergoal = events[['playerId', 'timeintervals','golas']].dropna(axis=0, how='any')
# Find the players ID with at leat one goal at 8 intervals
plyid = plyergoal.groupby('playerId').agg(lambda x: len(x['timeintervals'].value_counts())>=8).groupby('timeintervals').get_group(True).index

# show the number of goals in each timeintervals and player shortname
pd.merge(pd.pivot_table(plyergoal, columns= 'timeintervals', index='playerId', values='golas', aggfunc = sum).dropna(axis=0,thresh=8 ), plyer[plyer['wyId'].apply(lambda x: x in plyid)==True][['wyId', 'shortName']].set_index('wyId'),left_index=True,right_index=True).head()

# plot number of the unique time intervals each player have goals by player name
plt.figure(figsize=(20,6))
pd.merge(pd.pivot_table(plyergoal, columns= 'timeintervals', index='playerId', values='golas', aggfunc = sum).dropna(axis=0,thresh=8 ), plyer[plyer['wyId'].apply(lambda x: x in plyid)==True][['wyId', 'shortName']].set_index('wyId'),left_index=True,right_index=True).set_index('shortName').count(axis=1).plot.bar()
plt.ylabel('timeintervals')
plt.title('Number of unique timeintervals each player have a goal')
plt.show()

# same chart with seaborn
ee =pd.merge(pd.pivot_table(plyergoal, columns= 'timeintervals', index='playerId', values='golas', aggfunc = sum).dropna(axis=0,thresh=8 ), plyer[plyer['wyId'].apply(lambda x: x in plyid)==True][['wyId', 'shortName']].set_index('wyId'),left_index=True,right_index=True).set_index('shortName').count(axis=1)
fig = plt.figure(figsize=(20,6))
ax = plt.subplot(111)
ax = sns.barplot(ee.keys() , ee.values, ax = ax )
ax.set_xticklabels(ax.get_xticklabels(),rotation=30,  ha='right')
plt.title('Number of unique timeintervals each player have a goal')
plt.show()


plyer[plyer['wyId'].apply(lambda x: x in plyid)==True][['wyId', 'shortName']].set_index('wyId').head(7)

# players name with at leat one goal at 8 intervals
plyer[plyer['wyId'].apply(lambda x: x in plyid)==True][['firstName','lastName','shortName']].head()

# CRQ2

with open('matches_Spain.json') as json_file:
    spmatches = json.load(json_file)
    
with open('events_Spain.json') as json_file:
    spevent = json.load(json_file)

    
spmatch = pd.DataFrame(spmatches)
spevents = pd.DataFrame(spevent) 

with open('matches_Italy.json') as json_file:
    itmatches = json.load(json_file)
    
with open('events_Italy.json') as json_file:
    itevent = json.load(json_file)

    
itmatch = pd.DataFrame(itmatches)
itevents = pd.DataFrame(itevent)  


##  Barcelona - Real Madrid played on the 6 May 2018
spmatch[spmatch['label']=='Barcelona - Real Madrid, 2 - 2']

# find each players info

for i in range(len(play)):
    if play[i]['shortName']== 'Cristiano Ronaldo':
        print(play[i])
 for i in range(len(play)):
    if play[i]['shortName']== 'L. Messi':
        print(play[i])   
        
        
ronaldo = spevents[(spevents['playerId']==3322)& (spevents['matchId']==2565907)& ((spevents['eventId']==1)|(spevents['eventId']==3)|(spevents['eventId']==8)|(spevents['eventId']==10))]
messi = spevents[(spevents['playerId']==3359)& (spevents['matchId']==2565907)& ((spevents['eventId']==1)|(spevents['eventId']==3)|(spevents['eventId']==8)|(spevents['eventId']==10))]
  
 # built a dataframe of the positions

def position(positionlistdict):
    xstart = []
    ystart = []

    xstop = []
    ystop = []

    for i in positionlistdict.index:
            xstart.append(positionlistdict[i][0]['x'])
            ystart.append(positionlistdict[i][0]['y'])
            xstop.append(positionlistdict[i][1]['x'])
            ystop.append(positionlistdict[i][1]['y'])
    
    return  pd.DataFrame(zip(xstart,ystart,xstop,ystop ), columns=['xstart','ystart','xstop','ystop'] )       
     
ronaldopos = position(ronaldo['positions'])
messipos = position(messi['positions'])


# Make football pitch , I copied this from internet

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, ConnectionPatch, Arc

def draw_pitch(ax):
    # focus on only half of the pitch
    #Pitch Outline & Centre Line
    Pitch = Rectangle([0,0], width = 120, height = 80, fill = False)
    #Left, Right Penalty Area and midline
    LeftPenalty = Rectangle([0,22.3], width = 14.6, height = 35.3, fill = False)
    RightPenalty = Rectangle([105.4,22.3], width = 14.6, height = 35.3, fill = False)
    midline = ConnectionPatch([60,0], [60,80], "data", "data")

    #Left, Right 6-yard Box
    LeftSixYard = Rectangle([0,32], width = 4.9, height = 16, fill = False)
    RightSixYard = Rectangle([115.1,32], width = 4.9, height = 16, fill = False)


    #Prepare Circles
    centreCircle = plt.Circle((60,40),8.1,color="black", fill = False)
    centreSpot = plt.Circle((60,40),0.71,color="black")
    #Penalty spots and Arcs around penalty boxes
    leftPenSpot = plt.Circle((9.7,40),0.71,color="black")
    rightPenSpot = plt.Circle((110.3,40),0.71,color="black")
    leftArc = Arc((9.7,40),height=16.2,width=16.2,angle=0,theta1=310,theta2=50,color="black")
    rightArc = Arc((110.3,40),height=16.2,width=16.2,angle=0,theta1=130,theta2=230,color="black")
    
    element = [Pitch, LeftPenalty, RightPenalty, midline, LeftSixYard, RightSixYard, centreCircle, 
               centreSpot, rightPenSpot, leftPenSpot, leftArc, rightArc]
    for i in element:
        ax.add_patch(i)


fig=plt.figure(figsize=(12,8)) #set up the figures
#fig.set_size_inches(7, 5)
ax=fig.add_subplot(1,1,1)
draw_pitch(ax) #overlay our different objects on the pitch
plt.ylim(-2, 82)
plt.xlim(-2, 122)
plt.axis('off')
plt.show()

# kdeplot of players movements to compare them
import seaborn as sns

ax = sns.kdeplot(list(ronaldopos['xstart'])+list(ronaldopos['xstop']), list(ronaldopos['ystart'])+ list(ronaldopos['ystop']), shade= True, n_levels=15 ,kernel='cos' , cmap="Reds", shade_lowest=False)
ax1 = ax.twinx()
sns.kdeplot(list(messipos['xstart'])+list(messipos['xstop']), list(messipos['ystart'])+ list(messipos['ystop']), shade= False, n_levels=15 ,kernel='cos' , cmap="Blues", shade_lowest= False, ax = ax)
createPitch(ax1)
plt.title('Ronaldo & Messi position campare')
# plt.xticks([])
# plt.yticks([])
plt.ylim(-2, 92)
plt.xlim(-2, 132)
ax.axis('off')
plt.axis('off')
plt.show()


# Ronaldo
import matplotlib.pyplot as plt
import seaborn as sns
fig = plt.figure(figsize=(12,8))
ax=fig.add_subplot(1,1,1)

ax1 = ax.twinx()

createPitch(ax1)
ax = sns.kdeplot(list(ronaldopos['xstart'])+list(ronaldopos['xstop']), list(ronaldopos['ystart'])+ list(ronaldopos['ystop']), shade="True", n_levels=15 ,kernel='cos' , cmap="Greens", ax =ax)

plt.axis('off')
ax.axis('off')

plt.ylim(-2, 92)
plt.xlim(-2, 132)
plt.show()


# Messi
fig = plt.figure(figsize=(7,5))
ax=fig.add_subplot(1,1,1)

ax1 = ax.twinx()
sns.kdeplot(list(messipos['xstart'])+list(messipos['xstop']), list(messipos['ystart'])+ list(messipos['ystop']), shade="True", n_levels=15 ,kernel='cos' , cmap="Greens" , ax=ax)


#ax=fig.add_subplot(1,1,1)
draw_pitch(ax1) #overlay our different objects on the pitch

plt.ylim(-2, 82)
plt.xlim(-2, 122)
plt.axis('off')
ax.axis('off')

plt.show()

# Messi passes

fig=plt.figure() #set up the figures
fig.set_size_inches(10, 6)
ax=fig.add_subplot(1,1,1)


ax = sns.kdeplot(list(messipos['xstart'])+list(messipos['xstop']), list(messipos['ystart'])+ list(messipos['ystop']), shade="True", n_levels=15 ,kernel='cos' , cmap="Greens", ax =ax)
for i in messipos.index:
    # annotate draw an arrow from a current position to pass_end_location
    ax.annotate("", xy = (messipos['xstop'][i] , messipos['ystop'][i]), xycoords = 'data',
                   xytext = (messipos['xstart'][i] , messipos['ystart'][i]), textcoords = 'data',
                   arrowprops=dict(arrowstyle="->",connectionstyle="arc3", color = "blue"))

ax1 = ax.twinx()
draw_pitch(ax1)
plt.axis('off')
ax.axis('off')

plt.ylim(-1, 82)
plt.xlim(-1, 121)

plt.show()

plyer[plyer['firstName']=='Cristiano Ronaldo']['role']

##   Juventus - Napoli played on the 22 April 2018
itmatch[itmatch['label']== "Juventus - Napoli, 0 - 1"]
# looking for the requested data
itmatches[41]
plyer[plyer['wyId']==21315]
plyer[plyer['wyId']==20443]

Jorginho = itevents[(itevents['playerId']==21315)& (itevents['matchId']==2576295)& (itevents['eventId']==8)]
Pjanic = itevents[(itevents['playerId']==20443)& (itevents['matchId']==2576295)& (itevents['eventId']==8)] 

import numpy as np
Jorginhoaccurate  = position(Jorginho[Jorginho['tags'].apply(lambda x: len([k for k in x if k['id']==1801]))==0]['positions'])
Pjanicaccurate = position(Pjanic[Pjanic['tags'].apply(lambda x: len([k for k in x if k['id']==1801]))==0]['positions'])

jorginhopos = position(Jorginho['positions'])
pjanicpos = position(Pjanic['positions'])

# jorginho

import seaborn as sns

fig=plt.figure(figsize= (10, 6)) #set up the figures
#fig.set_size_inches(7, 5)
ax=fig.add_subplot(1,1,1)

ax = sns.kdeplot(list(jorginhopos['xstart'])+list(jorginhopos['xstop']), list(jorginhopos['ystart'])+ list(jorginhopos['ystop']), shade="True", n_levels=15 ,kernel='cos' , cmap="Greens", ax= ax)
for i in jorginhopos.index:
    # annotate draw an arrow from a current position to pass_end_location
    ax.annotate("", xy = (jorginhopos['xstop'][i] , jorginhopos['ystop'][i]), xycoords = 'data',
                   xytext = (jorginhopos['xstart'][i] , jorginhopos['ystart'][i]), textcoords = 'data',
                   arrowprops=dict(arrowstyle="->",connectionstyle="arc3", color = "blue"))


ax1 = ax.twinx()
#draw_pitch(ax1)
createPitch(ax1)
plt.tight_layout()
plt.ylim(-1, 90)
plt.xlim(-1, 131)
plt.axis('off')
ax.axis('off')
plt.show()

# compare the pass between two players

fig=plt.figure() #set up the figures
fig.set_size_inches(12, 8)
ax=fig.add_subplot(1,1,1)

sns.kdeplot(list(jorginhopos['xstart'])+list(jorginhopos['xstop']), list(jorginhopos['ystart'])+ list(jorginhopos['ystop']), shade=True, n_levels=15 ,kernel='cos' , cmap="Greens")
sns.kdeplot(list(pjanicpos['xstart'])+list(pjanicpos['xstop']), list(pjanicpos['ystart'])+ list(pjanicpos['ystop']), shade=False , n_levels=15 ,kernel='cos' , cmap="Reds")

for i in jorginhopos.index:
    try:
        # annotate draw an arrow from a current position to pass_end_location
        ax.annotate("", xy = (jorginhopos['xstop'][i] , jorginhopos['ystop'][i]), xycoords = 'data',
                       xytext = (jorginhopos['xstart'][i] , jorginhopos['ystart'][i]), textcoords = 'data',
                       arrowprops=dict(arrowstyle="->",connectionstyle="arc3", color = "y"))


        ax.annotate("", xy = (pjanicpos['xstop'][i] , pjanicpos['ystop'][i]), xycoords = 'data',
                       xytext = (pjanicpos['xstart'][i] , pjanicpos['ystart'][i]), textcoords = 'data',
                       arrowprops=dict(arrowstyle="->",connectionstyle="arc3", color = "blue"))    
    
    except:
        pass
    
#draw_pitch(ax)
#plt.axis('off')
plt.show()

# compare the pass between two players

fig=plt.figure() #set up the figures
fig.set_size_inches(12, 8)
ax=fig.add_subplot(1,1,1)

sns.kdeplot(list(jorginhopos['xstart'])+list(jorginhopos['xstop']), list(jorginhopos['ystart'])+ list(jorginhopos['ystop']), shade=True, n_levels=15 ,kernel='cos' , cmap="Greens")

for i in jorginhopos.index:
    
    # annotate draw an arrow from a current position to pass_end_location
    ax.annotate("", xy = (jorginhopos['xstop'][i] , jorginhopos['ystop'][i]), xycoords = 'data',
                   xytext = (jorginhopos['xstart'][i] , jorginhopos['ystart'][i]), textcoords = 'data',
                   arrowprops=dict(arrowstyle="->",connectionstyle="arc3", color = "blue"))

for j in Jorginhoaccurate.index:
        ax.annotate("", xy = (Jorginhoaccurate['xstop'][j] , Jorginhoaccurate['ystop'][j]), xycoords = 'data',
                       xytext = (Jorginhoaccurate['xstart'][j] , Jorginhoaccurate['ystart'][j]), textcoords = 'data',
                       arrowprops=dict(arrowstyle="->",connectionstyle="arc3", color = "red"))    
    
    

plt.axis('off')
plt.show()


fig=plt.figure() #set up the figures
fig.set_size_inches(12, 8)
ax=fig.add_subplot(1,1,1)

sns.kdeplot(list(pjanicpos['xstart'])+list(pjanicpos['xstop']), list(pjanicpos['ystart'])+ list(pjanicpos['ystop']), shade=True, n_levels=15 ,kernel='cos' , cmap="Greens")

    
for i in pjanicpos.index:
    # annotate draw an arrow from a current position to pass_end_location
    ax.annotate("", xy = (pjanicpos['xstop'][i] , pjanicpos['ystop'][i]), xycoords = 'data',
                   xytext = (pjanicpos['xstart'][i] , pjanicpos['ystart'][i]), textcoords = 'data',
                   arrowprops=dict(arrowstyle="->",connectionstyle="arc3", color = "blue"))

for j in Pjanicaccurate.index:
    ax.annotate("", xy = (Pjanicaccurate['xstop'][j] , Pjanicaccurate['ystop'][j]), xycoords = 'data',
                   xytext = (Pjanicaccurate['xstart'][j] , Pjanicaccurate['ystart'][j]), textcoords = 'data',
                   arrowprops=dict(arrowstyle="->",connectionstyle="arc3", color = "red"))    

plt.axis('off')
#plt.autoscale(enable=True) 
plt.show()
  
# compare the pass between two players

fig=plt.figure() #set up the figures
fig.set_size_inches(12, 8)
ax=fig.add_subplot(1,1,1)

ax1 = ax.twinx()
sns.kdeplot(list(jorginhopos['xstart'])+list(jorginhopos['xstop']), list(jorginhopos['ystart'])+ list(jorginhopos['ystop']), shade=True, n_levels=15 ,kernel='cos' , cmap="Greens" , ax =ax)

for i in jorginhopos.index:
    
    # annotate draw an arrow from a current position to pass_end_location
    ax.annotate("", xy = (jorginhopos['xstop'][i] , jorginhopos['ystop'][i]), xycoords = 'data',
                   xytext = (jorginhopos['xstart'][i] , jorginhopos['ystart'][i]), textcoords = 'data',
                   arrowprops=dict(arrowstyle="->",connectionstyle="arc3", color = "blue"))

for j in Jorginhoaccurate.index:
        ax.annotate("", xy = (Jorginhoaccurate['xstop'][j] , Jorginhoaccurate['ystop'][j]), xycoords = 'data',
                       xytext = (Jorginhoaccurate['xstart'][j] , Jorginhoaccurate['ystart'][j]), textcoords = 'data',
                       arrowprops=dict(arrowstyle="->",connectionstyle="arc3", color = "red"))    
    
    
draw_pitch(ax1)
plt.axis('off')
plt.ylim(-1,82)
plt.xlim(-1, 130)
ax.axis('off')
plt.show()

fig=plt.figure() #set up the figures
fig.set_size_inches(12, 8)
ax=fig.add_subplot(1,1,1)
ax1 = ax.twinx()
sns.kdeplot(list(pjanicpos['xstart'])+list(pjanicpos['xstop']), list(pjanicpos['ystart'])+ list(pjanicpos['ystop']), shade=True, n_levels=15 ,kernel='cos' , cmap="Greens", ax =ax)

    
for i in pjanicpos.index:
    # annotate draw an arrow from a current position to pass_end_location
    ax.annotate("", xy = (pjanicpos['xstop'][i] , pjanicpos['ystop'][i]), xycoords = 'data',
                   xytext = (pjanicpos['xstart'][i] , pjanicpos['ystart'][i]), textcoords = 'data',
                   arrowprops=dict(arrowstyle="->",connectionstyle="arc3", color = "blue"))

for j in Pjanicaccurate.index:
    ax.annotate("", xy = (Pjanicaccurate['xstop'][j] , Pjanicaccurate['ystop'][j]), xycoords = 'data',
                   xytext = (Pjanicaccurate['xstart'][j] , Pjanicaccurate['ystart'][j]), textcoords = 'data',
                   arrowprops=dict(arrowstyle="->",connectionstyle="arc3", color = "red"))    

draw_pitch(ax1)
plt.axis('off')
plt.ylim(-1,82)
plt.xlim(-1, 130)
ax.axis('off')
plt.show()
