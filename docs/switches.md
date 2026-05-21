
# Switches

## Wiring
There are 3 places you can connect wires on the switch, labeled NC (normally closed), NO (normally open), and C (ground). C will always connect to ground, while NC or NO will connect to the GP pins

## Soldering
* C must always be connected to ground, while you can choose between using NC or NO to save space as they both tell you when the switch is pressed. Which one you choose to solder will change how your code works.

## Programming
* When the switch is wired so it connects to NC
  * if value_when_pressed=False then the switch being pressed will be seen in the code as event.released and the switch being released would be seen as event.pressed.
  * if value_when_pressed=True then the switch being pressed will be seen in the code as event.pressed and the switch being released would be seen as event.released.
* When the switch is wired so it connects to NO
  * if value_when_pressed=False then the switch being pressed will be seen in the code as event.pressed and the switch being released would be seen as event.released.
  * if value_when_pressed=True then the switch being pressed will be seen in the code as event.released and the switch being released would be seen as event.pressed.

## Resources
