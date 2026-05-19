
# Switches

## Wiring
There are 3 places you can connect wires on the switch, labeled NC (normally closed), NO (normally open), and C (ground). C will always connect to ground, while NC or NO will connect to the GP pins

## Soldering
* C must always be connected to ground, while you can choose between using NC or NO to save space as they both tell you when the switch is pressed. Which one you choose to solder will change how your code works.
* If you set value_when_pressed=False for switches, it makes more sense to solder it so that NO is connected 

## Programming
If a switch is wired so it connects to NC and value_when_pressed=False in the code for a switch, the switch being pressed will be detected by the code as event.release and the switch being released will be detected as event.pressed. 

## Resources
