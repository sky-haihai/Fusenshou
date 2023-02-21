import pyautogui as gui
import time as t

#set interval between each pyautogui call
gui.PAUSE = 1
duration=1 # mouse travel duration

print(gui.size())
print(gui.position())

currentState='Entry'

def getCoord(imagePath,confidence=0.9,maxTrial=0):
    trial=0
    coord=gui.locateCenterOnScreen(imagePath,confidence=confidence)
    while(coord==None):
        if(maxTrial!=0 and trial >= maxTrial):break

        coord=gui.locateCenterOnScreen(imagePath,confidence=confidence)
        trial+=1
        
    return coord

def changeState(targetState):
     global currentState
     print(f'Switching State to {targetState}')
     currentState=targetState


# enter match making
def onStartDuel():
    x,y=getCoord('res/start_duel_btn.png')
    gui.moveTo(x,y,duration)
    gui.click()
    # wait for coin flip
    t.sleep(20)
    changeState('TurnOffCounter')

# turn off counter prompt
def onTurnOffCounter():
    x,y=getCoord('res/counter_auto_btn.png')
    t.sleep(2)
    gui.moveTo(x,y,duration)
    gui.click()
    gui.moveTo(x+100,y-100,duration)
    t.sleep(5)

    coord=getCoord('res/oppo_turn_main1_btn.png',maxTrial=10)    
    if(coord!=None):
        changeState('OpponentTurn')
    else:
        changeState('PlayerTurn')


# if sees a drawing deck(second move)
# click the drawing deck

# if sees a blue turn button(first move)
# click turn button 
# click turn over    
def onPlayerTurn():
    #draw card
    gui.click()
    gui.click()
    t.sleep(1)

    #click turn btn
    x,y=getCoord('res/turn_main1_btn.png',0.9)
    gui.moveTo(x,y,duration)
    print('Click Turn Btn')
    gui.click()

    #click end btn
    x,y=getCoord('res/turn_end_btn.png')
    gui.moveTo(x,y,duration)
    print('Click End Btn')
    gui.click()
    
    t.sleep(2)
    coord=getCoord('res/discard_prompt.png',maxTrial=10)
    print(coord)
    if(coord!=None):
        changeState('DiscardCard')
    else:
        changeState('OpponentTurn')

def onOpponentTurn():
    while(True):
        coord=getCoord('res/continue_turn_prompt.png',maxTrial=1)
        if(coord!=None):
            x,y=getCoord('res/continue_turn_confirm_btn.png')
            gui.moveTo(x,y,duration)
            print('Click No to not continue players turn')
            gui.click()
            t.sleep(1)
        if(getCoord('res/drawing_deck_btn.png',maxTrial=1)!=None):
            changeState('PlayerTurn')
            return
        if(getCoord('res/defeat_prompt.png',maxTrial=1)!=None):
            changeState('EndDuel')
            return
        if(getCoord('res/victory_prompt.png',maxTrial=1)!=None):
            changeState('EndDuel')
            return

#click confirm three times and back to start duel
def onEndDuel():
    for i in range(3):
        x,y=getCoord('res/confirm_btn.png')
        gui.moveTo(x,y,duration)
        gui.click()

    x,y=getCoord('res/return_to_menu_btn.png')
    gui.moveTo(x,y,duration)
    gui.click()
    t.sleep(1)

    #in case obtained something
    coord=getCoord('res/confirm_btn.png',max_trail=5)
    if(coord!=None):
        x,y=coord
        gui.moveTo(x,y,duration)
        gui.click()

    if(getCoord('res/start_duel_btn.png',1)!=None):
        changeState('StartDuel')

#find a random card and discard
def onDiscardCard():
    x,y=getCoord('res/discard_confirm_btn.png')
    #select card
    gui.moveTo(x,y-100,duration)
    gui.click()
    #confirm
    gui.moveTo(x,y,duration)
    gui.click()

    changeState('OpponentTurn')

try:
    while(True):
        match currentState:
            case 'Entry':
                changeState('StartDuel')
            case 'StartDuel':
                onStartDuel()
            case 'TurnOffCounter':
                onTurnOffCounter()
            case 'PlayerTurn':
                onPlayerTurn()
            case 'OpponentTurn':
                onOpponentTurn()
            case 'DiscardCard':
                onDiscardCard()
            case 'EndDuel':
                onEndDuel()    
except KeyboardInterrupt:
    print('Stop Grinding')
    pass