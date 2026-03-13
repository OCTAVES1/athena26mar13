# athena26mar13


The objective of this project was to establish a covert communication channel across a Local Area Network (LAN) operating purely at Layer 2 (the Data Link Layer) of the OSI model. By hiding payloads within standard Ethernet frames rather than utilizing standard Layer 3 (IP) or Layer 4 (TCP/UDP) protocols, the communication bypasses traditional network monitoring tools and firewalls that primarily inspect routed traffic.

To demonstrate this, we utilized a simulated software-defined network (SDN) environment and built an Intrusion Detection System (IDS) to monitor and visualize the traffic.


2. Network Architecture

The environment was built using Mininet on a Linux virtual machine. The topology consists of a single switch connecting three distinct hosts:

    Host 1 (h1) - The Attacker: The node responsible for injecting the covert payload into the network and generating masking traffic to hide the transmission.

    Host 2 (h2) - The Target: The node running a script in promiscuous mode to capture, filter, and extract the hidden payloads from the network interface.

    Host 3 (h3) - The Bystander: A standard node used to demonstrate that conventional packet sniffing (such as running Wireshark on a normal host) only sees standard network noise or unreadable raw hex data, proving the channel remains covert to unauthorized observers.



3. Core Components

The project relies on three distinct operational components functioning together:

A. Payload Injection (The Covert Channels) Two distinct methods of data exfiltration were implemented:

    Padding Steganography: This method hides variable-length plaintext strings (e.g., "GHOST_IN_THE_WIRE!") inside the ethernet padding section of standard network frames.

    Encrypted Transmission: This method transmits AES-encrypted payloads. The data is formatted into exact 16-byte blocks to satisfy the cryptographic algorithm's block size requirements, requiring the receiver to possess the correct cryptographic logic to decipher the message.

B. Traffic Masking (The Noise Generator) To prevent the covert frames from standing out on an otherwise quiet network, an automated bash sequence is utilized to generate a flood of Address Resolution Protocol (ARP) requests.

    The sequence uses the arping utility to ping a rapid succession of non-existent IP addresses on the subnet.

    This creates a high volume of standard broadcast traffic immediately before and after the covert payload is sent, effectively burying the anomalous frame in a sea of normal network noise.

    The script utilizes subshells to execute these background tasks silently, keeping the attacker's terminal clean.

C. Intrusion Detection System (The Dashboard) To visualize the attack and demonstrate defensive capabilities, a custom monitoring system was deployed:

    Backend: A Scapy-based sniffer that continuously monitors the virtual network interfaces. It logs traffic distributions and flags frames that contain known covert signatures (such as specific ethertypes used by the payload injector).

    Frontend: A Streamlit web application that reads the backend logs and displays real-time metrics. This includes a traffic distribution pie chart and a live data table of intercepted clandestine payloads, allowing defenders to see the covert channel in action.




4. Execution Workflow

When the system is deployed, the operational flow runs as follows:

    Initialization: The Mininet topology is spun up, and the IDS backend and Streamlit dashboard are launched on the main host to begin monitoring network activity.

    Arming the Target: Host 2 executes the receiver script, entering a listening state to silently monitor the switch for frames containing the designated covert ethertype.

    Execution: Host 1 initiates the attack sequence. The terminal spawns a silent background wave of ARP requests, injects the steganographic or encrypted payload directly into the traffic stream, and follows up with a second wave of ARP requests.

    Result: Host 2 successfully intercepts and decodes the payload, Host 3 remains unaware of the transmission, and the Streamlit dashboard successfully flags the anomaly in real-time.

