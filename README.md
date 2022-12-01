**Note:** This application uses Docker to facilitate simpler program modifications between various lab/office devices while collecting, transferring, and storing chemical data. Using additional packages and dependencies makes Docker more effective, but the fundamentals remain the same. I easily may adapt to more advanced and enterprise applications of data management tools.

# Receive Data from STM32MP15 Microcontroller and store them into MongoDB

### Build & Execution
`sudo docker -t serial_receiver .`   
`sudo docker run -t -i --device=/dev/ttyACM0 IMAGE_ID`
- by using the --device flag we give access to the dev directory through which we receive our data


### Desciption
Our goal is to receive sensor data from the STM32 Microcontroller via computer and store those data in our MongoDB Local Server. Because we use different computers and Microcontrollers between Lab and Office.
- `FROM python3` environment as the basic docker layer (n)
- `COPY receive_from_serial_port.py`  additional layer  (n+1) for the executable program
- `RUN pip3 install pyserial pymongo` additional layer  (n+2) for the packages needed from the executable program
- `CMD []` additional layer  (n+3) for the execution


![img](/img.jpg "img")

1. STM32MP15 Microcontroller executes in a continues loop a program which reads from sensors and dispatch these sensor data via Serial Port
2. A Linux Computer reads via the Serial Port sensor data from the STM32MP15 Microcontroller
3. These data are stored in a MongoDB and they have a json shape


### Data Shape:

**All .json file data will have the following info:**

1. Experiment type (SR-CAMMS, UW-CAMMS, or VS-CMS) <= **type: String**
2. Experiment notes: (a text box in the client for the user to put some notes on the experiments being performed) <= **type: String**
3. Mode (raw_data, or processed spectra) <= **type: List of Float Values**
4. client start timestamp (Justin - is the current format easily convertible to a date/time?) <= **type: Float**
5. experiment start <= **type: Float**
6. current acquisition number <= **type: Float**
7. current acquisition timestamp <= **type: Float**
8. gain <= **type: Int**
9. frame cound <= **type: Int**
10. discard frames <= **type: Int**
11. frame delay <= **type: Int**
12. temperature <= **type: Float**
13. data directory <= **type: String**
14. data file (raw or processed spectra) - the data could be included as part of the .json file <= **type: String**
15. gain file <= **type: String**
