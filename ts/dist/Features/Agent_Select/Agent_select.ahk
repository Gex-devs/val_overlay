#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

#SingleInstance, force
#IfWinActive, VALORANT

for n, param in A_Args  ; For each parameter:
{
    if (%1% = Agent_Lock){
        Lock_Agent()
    }Else{
        Agent_Function(%1%)
    }
}

Lock_Agent(){
    MouseMove, x,y
    MouseClick, left
}

Agent_Function(Agent)
{
    Switch [Agent]
    {
    Case Jett:
        MouseMove 950,900
        MouseClick, left 
    }
}

