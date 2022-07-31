#Change Detection
#Hsiang-Yun Wu
#SID: 3035347238

from psychopy import visual, core, event, gui, monitors, tools
import numpy as np
import pandas as pd
import random

#To start the program, use the command line below:
# python3 main.py 
############################################# Functions for ##############################################
def randomposition(): #Randomly choose a position in each quadrant
    #Define the index numbers of four quadrants
    area_one = [32,33,34,39,40,41,46,47,48]
    area_two = [28,29,30,35,36,37,42,43,44]
    area_three = [0,1,2,7,8,9,14,15,16]
    area_four = [4,5,6,11,12,13,18,19,20]
    #Randomly choose one index number in each quadrant
    ran_area_one = random.choice(area_one)
    ran_area_two = random.choice(area_two)
    ran_area_three = random.choice(area_three)
    ran_area_four = random.choice(area_four) 
    return ran_area_one, ran_area_two, ran_area_three, ran_area_four

def check_ans(inputkey,ans): #Check whether the participant's answer is correct
    if (inputkey == 'm'): #participant answered that two stimuli are identical 
        if (ans == 1): #the correct ans: identical
            return 1 #Correctnes of the reponse == True
        else: #the correct ans: different
            return 0 #Correctness of the response == False
    elif (inputkey == "c"): #participant answered that two stimuli are different
        if (ans == 1): #the correct ans: identical
            return 0 #Correctnes of the reponse == False
        else:  #the correct ans: different
            return 1 #Correctnes of the reponse == True
    else: #if the participant presses any key other than "m" or "c"
        return "NA"


############################################################# Data Entry ###############################
#Enter the participant's ID and the condition 
gui = gui.Dlg()
gui.addField("Subject ID:")
gui.addField("Condition 1 or 2 :")
gui.show()
subj_id = gui.data[0]
exp_con = gui.data[1]

############################################################# Environment Setup ###############################

#Initial the environment
mon = monitors.Monitor(name='mymac', width=37, distance=60)
mon.setSizePix((800,600))
win = visual.Window(size = [800,600], units = 'pix',fullscr = False, color=[0,0,0])

#Convert size in degrees to size in pixels and save it 
checkwidth = tools.monitorunittools.deg2pix (0.65, monitor=mon)
intercheck= tools.monitorunittools.deg2pix (2.0, monitor=mon)

#Form 7*7 squares 
num_check = 7 
checksize = [checkwidth,checkwidth]

#Determine the central point of the grid 
low, high = num_check // -2, num_check // 2
if abs(low) != high:
    low += 1
    high += 1
    loc = np.array([0,checkwidth // 2 - checksize[0] // 4])
else:
    loc = np.array([checkwidth // 2 + intercheck // 2, checkwidth // 2, checksize[0]//4])
#Creat a list that store the position of each check
xys = []
for y in range (low, high):
    i = 0
    for x in range (low, high):
        i += 1
        if i % 2 == 0:
            y_delta = -checksize[0]/2
        else:
            y_delta = 0
        xys.append(((checksize[0] + intercheck) * x, checksize[1] * y+y_delta))

#Stimulus Specification
checks = visual.ElementArrayStim(win, fieldPos=loc, nElements=num_check**2,sizes=(checksize[0],checksize[1]),xys=xys,elementTex= None,elementMask=None)

#Initial the response lists.
response_key = []
response_time = []
response_correct = []

############################################## Define a Trial ##############################################
def trial(stim,encode_c1,encode_c2,encode_c3,encode_c4, probe_c1, probe_c2, probe_c3, probe_c4):
    
    ##Function variables
    #Index number of chosen positions
    ran_one, ran_two, ran_three, ran_four = randomposition()
    #Define the cross
    cross = visual.TextStim(win=win, text="+", pos=[0,0], color=[-1,-1,-1])

    #Create clock instance
    clock_trial = core.Clock()

    #Define the colors (the rgb of each color)
    #These colors are called using the integers in the csv.file
    all_colors = [
        [0,0,0], #This item isn't used. We create it because the csv.file is 1-indexing while python is 0-indexing and we don't want to use -1 repetitively.
        [1,0,0], # 1
        [0,0,1], # 2
        [0.93, 0.009, 0.93], # 3
        [0,1,0], # 4
        [1,1,0], # 5
        [-1,-1,-1], # 6
        [1,1,1], # 7
        [0,0,0] # 8
        ]
   
    ##Fixation
    cross.draw()
    win.flip()
    core.wait(0.2)

    ##Encode
    #Create array of rgbs that filled with 0 for each check 
    colors=np.zeros((num_check**2,3))
    #Fill the color into four chosen checks
    colors[ran_one,:] = all_colors[encode_c1]
    colors[ran_two,:] = all_colors[encode_c2]
    colors[ran_three,:] = all_colors[encode_c3]
    colors[ran_four,:] = all_colors[encode_c4]
    #Specify the colors of stimulus
    stim.colors = colors
    stim.draw()
    cross.draw()
    win.flip()
    core.wait(0.5)
   
    ##Fixation
    cross.draw()
    win.flip()
    core.wait(0.9)
    
    #Reset the clock so that we can measure the response time accurately
    clock_trial.reset()

    ##Probe
    #Create array of rgbs that filled with 0 for each check 
    colors=np.zeros((num_check**2,3))
    #Fill the color into four chosen checks
    colors[ran_one,:] = all_colors[probe_c1]
    colors[ran_two,:] = all_colors[probe_c2]
    colors[ran_three,:] = all_colors[probe_c3]
    colors[ran_four,:] = all_colors[probe_c4]
    stim.colors = colors
    stim.draw()
    cross.draw()
    win.flip()
    key_info = event.waitKeys(maxWait = 2, timeStamped=clock_trial)

    #Collect the reponse 
    try:
        response_key.append(key_info[0][0])
        response_time.append(key_info[0][1])
        response_correct.append(check_ans(key_info[0][0],ans[0]))

    #If the participant misses the response, key_info[0][0] and key_info[0][1] will be 'Nonetype' object.
    #Because 'Nonetype' object is not subscriptable, we create this exception to keep the project running even when the error occurs.
    except: 
        pass

    ##Jittered
    jittered = random.uniform(.65, .95)
    win.flip()
    core.wait(jittered)
    win.flip()

    #Clear all events
    event.clearEvents()

############################################## Text instances ##############################################
session_start = visual.TextStim(win=win, text="Your task is to determine as accurately and quickly as possible whether the color of any square has changed.\nPress any key to proceed.", pos=[0,0], color=[-1,-1,-1],alignHoriz='center',alignVert='center')
txt = """Please press M if they are the same.\nPlease press C if any of them has changed.\nPress any key to start."""
session_ins1 = visual.TextStim(win=win, text="Session1\n"+txt, pos=[0,0], color=[-1,-1,-1])
session_ins2 = visual.TextStim(win=win, text="Session2\n"+txt, pos=[0,0], color=[-1,-1,-1])
Goodbye = visual.TextStim(win=win, text="The experiment is over.\nPress any key to end.",pos=[0,0], color=[-1,-1,-1])

############################################## Functions for the experiment procedure ##############################################
def welcome(): #Present the welcoming words
    session_start.draw()
    win.flip()
    event.waitKeys()

def session_intro(words): #Instruction for the session
    words.draw()
    win.flip()
    event.waitKeys() 

def read_file(filename):
    #Read the data file
    data = pd.read_csv(filename)
    #Randomize the order
    dataran = data.sample(frac = 1).reset_index(drop = True)
    #create variables
    encoding_first = dataran['encoding_first'].values
    encoding_second = dataran['encoding_second'].values
    encoding_third = dataran['encoding_third'].values
    encoding_fourth = dataran['encoding_fourth'].values
    probe_first = dataran['probe_first'].values
    probe_second = dataran['probe_second'].values
    probe_third = dataran['probe_third'].values
    probe_fourth = dataran['probe_fourth'].values
    ans = dataran['ans'].values
    return dataran,encoding_first, encoding_second, encoding_third, encoding_fourth,probe_first,probe_second,probe_third,probe_fourth,ans

def trial_repeat(times): #repeat trials by iterating through the columns of color integers in each repetition
    for i in range(times):
        trial(checks, encoding_first[i], encoding_second[i], encoding_third[i], encoding_fourth[i], probe_first[i], probe_second[i],probe_third[i],probe_fourth[i])



############################################## Experiment Procedure ##############################################
#Counterbalance 
if int(exp_con) == 1:
    welcome()  
    session_intro(session_ins1)
    dataran,encoding_first, encoding_second, encoding_third, encoding_fourth,probe_first,probe_second,probe_third,probe_fourth,ans = read_file('set4.csv')
    trial_repeat(40)
    session_intro(session_ins2)
    dataran,encoding_first, encoding_second, encoding_third, encoding_fourth,probe_first,probe_second,probe_third,probe_fourth,ans = read_file('set2.csv')
    trial_repeat(40)
    Goodbye.draw()
    win.flip()
    event.waitKeys()

elif int(exp_con) == 2: 
    welcome()  
    session_intro(session_ins1)
    dataran,encoding_first, encoding_second, encoding_third, encoding_fourth,probe_first,probe_second,probe_third,probe_fourth,ans = read_file('set2.csv')
    trial_repeat(40)
    session_intro(session_ins2)
    dataran,encoding_first, encoding_second, encoding_third, encoding_fourth,probe_first,probe_second,probe_third,probe_fourth,ans = read_file('set4.csv')
    trial_repeat(40)
    Goodbye.draw()
    win.flip()
    event.waitKeys()

#If the participant type the wrong condition number
else: 
    wrongcod = visual.TextStim(win=win, text="Wrong condition number.\nThe condition number should be 1 or 2.\nPlease press any key to end.",pos=[0,0], color=[-1,-1,-1])
    wrongcod.draw()
    win.flip()
    event.waitKeys()
    win.close()
    core.quit()



############################################## Save the data and end the program ##############################################
#Save the behavioral data
def save_behavioral_data(response_key, response_time, response_correct):
    trial_info = dataran
    output = {
        'trial_key': response_key,
        'trial_time': response_time,
        'trial_correct': response_correct
        }
    response_info = pd.DataFrame(output)
    #Merge two dataframes
    df = pd.concat([trial_info, response_info],axis=1, sort=False)
    df.to_csv('./' + subj_id +'.csv', index=False, header=True)

save_behavioral_data(response_key, response_time, response_correct)
win.close()
core.quit()