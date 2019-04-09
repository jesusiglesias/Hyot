# Hyot

> A blockchain (BC) solution for activity registration in the Internet of Things. Specifically, a permissioned blockchain is used to record anomalous occurrences associated with sensors located on a Raspberry Pi 3. Likewise, a web system is provided to consume the information collected in real time.
 
@version: 1.0.0 
@last-modified: 2019-04-09

## Description

**Hyot** is an open source Proof of Concept (PoC) for the traceability of a controlled IoT environment using Hyperledger Fabric technology.  This solution, which is highly configurable by the user, transparently manages a series of events -temperature, humidity and distance- of the environment that are constantly monitored in real time from input data sources such as the sensors, connected to a Raspberry Pi. The information collected is analysed to determine if the read values are considered anomalous or not at a specific time and therefore determine if an unauthorised event is occurring in the environment.

At all times, the actions performed and the measurements made are notified to the user both through the terminal and through the output devices that the hardware prototype has. If the current reading of values presents data that exceed one or more of the pre-established thresholds, then it is considered as a possible indication of an incidence on the environment. In this situation, the procedure to be followed is more exhaustive in order to certify the originality and authenticity of recorded data. An incident is an uncontrolled event or action that takes place in the environment that is being monitored and originates the execution of an alert protocol (see Figure below):

![](docs/figures/hyot_flow.png?raw=true)

### Components

In short, the protocol for the management of metadata and evidence recording is organised around three main components:

- Component for monitoring events in the IoT environment through sensors located in a Raspberry Pi device.
- Incident registration protocol in the BC of Hyperledger Fabric and storage of protected evidence in the cloud.
- Web app that acts as a client and consumes in real time the information registered by the Raspberry Pi.

Other than that the main components, two additional elements have been developed in order to complete the project and facilitate the tasks of:

- Initial configuration of the Raspberry Pi device for the subsequent execution of the component for event monitoring in the IoT environment.

- Decryption of the evidence previously encrypted and signed. In this component, in addition to the decryption process, the signature is shown and the integrity of the content of the evidence obtained is verified. At this point of verification, the confidence that is deposited in this technology is crucial since in case of hash mismatch, we can conclude that the evidence stored in the cloud was improperly modified.

### Prototype

The diagram of the prototype used in Hyot by the event monitoring component of the IoT environment is displayed in Figure below.

![](docs/figures/prototype.png?raw=true)

The list of electronic components is given by:

- A Raspberry Pi 3 to implement the control system.
- A V2 camera module as video recording and main piece of digital evidence  in our scheme.
- A DHT-11 sensor to monitor the temperature and humidity.
- An HC-SR04 sensor to monitor the distance of any potential intruder with respect to the location of the control system (i.e., the Raspberry Pi).
-  Two 16×2 LCD displays and a red LED as visual alert system.
    
## Getting started

TBA

### Prerequisites

### Installing


## Usage

TBA


## FAQ

TBA


## License

TBA


## Authors

* **Jesús Iglesias García** [(Linkedin)](https://www.linkedin.com/in/jesusgiglesias/)
* **David Arroyo Guardeño**

