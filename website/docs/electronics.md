# Electronics Primer

## Safety

* Avoid working with live wires! Remove power before working on wiring.

    * High voltage: bad for you! Do not contact live wires of moderate voltage (25V AC or 48V DC)
    * Low voltage: can be bad for devices, particularly shorts to other signals or power rails

* Wash hands after soldering.

## Voltage, Current, and Resistance

To understand electronics, you must understand the flow of electrons, base units, and the essential equation of Ohm's Law.

We often use water as an analogy. Consider water flowing through a hose: 

* __Voltage__ (volts, *V*): water pressure. The higher the pressure, the faster the flow.
* __Current__ (amps, *I*): water volume. The total amount of water flowing through per second.
* __Resistance__ (ohms, *R*): a kink or restriction in the hose. 

Electrons only travel through a closed, conductive circuit.

Voltage, current, and resistance are related by *Ohm's Law*:

$$V = I \times R$$

Consider this circuit which includes a battery, LED, and resistor:

<iframe src="https://www.falstad.com/circuit/circuitjs.html?ctz=DwYwlgTgBAZgvAIgIwKgFwM6IAwDpsEECsqYIiSeATAVQOx0DM2AHFQGwCcndqIARoiLZUAB0EJhqAG4QhqALaYhAUwC0SFAD4AUFCjBpUAB4V22KFQAsFpOagsRsRNdQB3eAicKAhsenyAPS6+sAYJmYWjpZE7A5OniLBegbQpghUsVB2FplxVK7OXqhyyAQIyaFuEcj21rlZ9aiJFSEG1el5ljYx+YUtlQYA5jU53bZ1dFTNOK0pwAAyAKIAIjVd0V05M8VQCgD2iAAmKjA+AK4ANmhqlypHfKUoUCBDsy8S3vzkXvgoycBAuAILogA" width="800" height="400"></iframe> 

You can create and simulate your own circuits with the [Falstad Circuit Simulator](https://www.falstad.com/circuit/circuitjs.html) above.

## Primary Components

* Wire
* Resistor
* Capacitor
* Inductor
* Diode
* LED
* Switch
* Transistor
* Connector
* Breadboard

## Power Rails

Voltage is always measured between two points. **Ground** is our term for *0 volts*.

Ground is also referred to as Common, COM, G, GND, or ⏚ .

Common voltage we use for this immersive include:

* __3.3v__: Logic level

    Grove ports, digital inputs and outputs

* __5v__: Device power

    Motor output terminals, PWM ports (servos, LED strings), mini speaker amplifiers

* __12v__: Device power

    PC power, cabinet fans, audio amplifier

* __48v__: High-power solenoids

    Flippers, slingshots, pop bumpers, ball trough


Generally for wire colors, __*black*__ is used to denote ground and <span style="color:red;">__*red*__</span> is used to denote positive voltage.

!!! note "...Generally..."
    House wiring in the US does not follow this standard: __*black*__ is "hot" or power and <span style="color: white; -webkit-text-stroke: 0.5px black;">__*white*__</span> is neutral.

## Pull-up Resistors

We tend to use switches as inputs. Switches inherently work by closing an open circuit (or vice-versa). An input that is not connected is called *floating*, because it's voltage is unknown and may float. Pull-up and pull-down resistors drive the state of the signal to a known value.

<iframe src="https://www.falstad.com/circuit/circuitjs.html?ctz=DwYwlgTgBAZgvAIgIwKgFwM6IAwDpsEECsqYIiSeATAVQOx0DM2AHFQGwCcndqIARoiItUAB0EIi2VADcIQ1AFtMQgKYBaJCgB8AKChRg0AB6IqVACxQkFq+butU8BNKjzkhaQHo9B4AHMoUwRGIiooenDQqOwLJxwEH31DADUAQwgAJTSwABsgsxYWa1soaJK42Ap2VAB3Z15Yd0ZcRiU04xlEFraofjA0rBDW1Aw0RBSAe1y0NP9VRN9DWoKEKiKIuiiwzap4l0Xk4BXg9eKbO0sK-e8l49X7CNYIjZoRKoOkvwBZB9fn8pvG6HPwYVbqRjhN5QCzFIEfVyiChKRSINAQACuCy+yz+cK2UAhUK2wJx92CRN2hMhT3ezluRxOFDo7FpESu8PpINxwVhbKQLNppL0wC84AgeiAA" width="800" height="400"></iframe> 

