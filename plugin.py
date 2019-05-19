"""
<plugin key="PioneerAVR" name="Pioneer AVR" author="febalci" version="0.9.0">
    <params>
        <param field="Address" label="IP Address" width="250px" required="true" default="192.168.1.60"/>
        <param field="Port" label="Port" width="50px" required="true" default="8102"/>
        <param field="Mode6" label="Debug" width="75px">
            <options>
                <option label="True" value="Debug"/>
                <option label="False" value="Normal"  default="true" />
            </options>
        </param>
    </params>
</plugin>
"""
import Domoticz
import pioneerapi

class BasePlugin:

    nextConnect = 3
    oustandingPings = 0
    VOLUMESTEP = 2

    UNITS = {
        'power': 1,
        'input': 2,
        'display': 3,
        'listening_mode': 4,
        'playing_mode': 5,
        'main_volume': 6
        }
    PioneerConn = None

    power_on = False
    volume_level = None
    mute = None
    input_rgb_name = None
    input_mode = "0"
    listening_mode = None
    playing_mode = None
    display_text = None
    InputIdx = ("01","02","03","04","05","10","14","15","17","25","26")

    def __init__(self):
        #self.var = 123
        return

    def onStart(self):
        Domoticz.Debug("onStart called")

        if Parameters["Mode6"] == "Debug":
            Domoticz.Debugging(1)

        InputSelections = 'Off'
        for a in self.InputIdx:
            InputSelections = InputSelections+'|'+pioneerapi.INPUT_MODES[a]
        Domoticz.Debug('LIST:'+InputSelections)
            
        SourceOptions = {'LevelActions': '|'*InputSelections.count('|'),
                              'LevelNames': InputSelections,
                              'LevelOffHidden': 'false',
                              'SelectorStyle': '1'}

        if self.UNITS['power'] not in Devices:
            Domoticz.Device(Name="Power", Unit=self.UNITS['power'], TypeName="Switch", Image=5, Used=1).Create()
        if self.UNITS['input'] not in Devices:
            Domoticz.Device(Name="Input", Unit=self.UNITS['input'], TypeName="Selector Switch", Switchtype=18, Image=5, Options=SourceOptions, Used=1).Create()
        if self.UNITS['display'] not in Devices:
            Domoticz.Device(Name="Display", Unit=self.UNITS['display'], TypeName="Text", Image=5, Used=1).Create()
        if self.UNITS['listening_mode'] not in Devices:
            Domoticz.Device(Name="Listening Mode", Unit=self.UNITS['listening_mode'], TypeName="Text", Used=1).Create()
        if self.UNITS['playing_mode'] not in Devices:
            Domoticz.Device(Name="Playing Mode", Unit=self.UNITS['playing_mode'], TypeName="Text", Used=1).Create()
        if self.UNITS['main_volume'] not in Devices:
            Domoticz.Device(Name="Volume Main Zone", Unit=self.UNITS['main_volume'], Type=244, Subtype=73, Switchtype=7, Image=8, Used=1).Create()

        DumpConfigToLog()
        self.SyncDevices(1)
        self.PioneerConn = Domoticz.Connection(Name="Telnet", Transport="TCP/IP", Protocol="Line", Address=Parameters["Address"], Port=Parameters["Port"])
        self.PioneerConn.Connect()
        Domoticz.Heartbeat(30)

    def onStop(self):
        Domoticz.Log("onStop called")

    def onConnect(self, Connection, Status, Description):
        global api

        Domoticz.Debug("onConnect called")
        if Status == 0:
            self.isConnected = True
            Domoticz.Debug("Connected successfully to: "+Parameters["Address"]+":"+Parameters["Port"])
            api = pioneerapi.pioneerapi()
            self.PioneerConn.Send('\r') #Send <CR> to wake unit from stanby
            self.PioneerConn.Send(api.qry_PowerStatus, Delay=1)
            self.PioneerConn.Send(api.qry_InputStatus, Delay=2)
            self.PioneerConn.Send(api.qry_VolumeStatus, Delay=3)
            self.PioneerConn.Send(api.qry_ListeningModeStatus, Delay=4)
            wait=5
            for key in self.InputIdx:
                wait += 1
                self.PioneerConn.Send("?RGB"+str(key)+"\r", Delay=wait)
        else:
            self.isConnected = False
            self.power_on = False
            self.SyncDevices(1)
            Domoticz.Debug("Failed to connect ("+str(Status)+") to: "+Parameters["Address"]+":"+Parameters["Port"]+" with error: "+Description)
        return

    def onMessage(self, Connection, Data):
        Domoticz.Debug("onMessage called")
        self.oustandingPings = self.oustandingPings - 1
        strData = Data.decode("utf-8", "ignore")
        Domoticz.Debug("onMessage called with Data: '"+str(strData)+"'")

        strData = strData.strip()
        shaction = strData[0:2]
        shdetail = strData[2:]
        loaction = strData[0:3]
        lodetail = strData[3:]

        if loaction == 'PWR': #POWER
            if lodetail == '0': #PWR0
                self.power_on = True
                self.PioneerConn.Send(api.qry_VolumeStatus, Delay=0)
            else: #PWR1
                self.power_on = False
        elif loaction == 'VOL': #VOLUME
            if self.mute == 'On': # In mute, discard volume processing
                self.volume_level = str(0)
                Domoticz.Debug('VOL command discarded in mute')
            else:
                self.volume_level = str(round((int(str(lodetail))*100)/185))
        elif loaction == 'MUT': #MUTE
            if lodetail == '0': #MUT0
                self.mute = 'On'
            else: #MUT1
                self.mute = 'Off'
        elif loaction == 'RGB': #INPUT NAME
            self.input_rgb_name = api.RGB_decode(str(lodetail))
            if self.input_rgb_name != None:
                Domoticz.Debug('RGB:'+self.input_rgb_name)
                InputSelections = 'Off'
                for a in self.InputIdx:
                    InputSelections = InputSelections+'|'+pioneerapi.INPUT_MODES[a]
                Domoticz.Debug('LIST:'+InputSelections)

                SourceOptions = {'LevelActions': '|'*InputSelections.count('|'),
                                'LevelNames': InputSelections,
                                'LevelOffHidden': 'false',
                                'SelectorStyle': '1'}
                Devices[self.UNITS['input']].Update(nValue = 0, sValue = "Off", Options = SourceOptions)

        elif shaction == 'FN': #INPUT            
            self.input_mode = self.selector_find(str(shdetail), 0)
            Domoticz.Debug('FN:'+str(self.input_mode))
        elif shaction == 'SR': #LISTENING MODE
            self.listening_mode = api.SR_decode(str(shdetail))
            Domoticz.Debug('SR:'+self.listening_mode)
        elif shaction == 'LM': #PLAYING LISTENING MODE
            self.playing_mode = api.LM_decode(str(shdetail))
            Domoticz.Debug('LM:'+self.playing_mode)
        elif shaction == 'FL': #DISPLAY TEXT
            self.display_text = api.FL_decode(str(shdetail))
            Domoticz.Debug('FL:'+self.display_text)
        self.SyncDevices(0)
        return

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Debug("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))
        action, sep, params = Command.partition(' ')
        action = action.capitalize()
        params = params.capitalize()
        if Unit == self.UNITS['power']:
            if Command=='Off':
                Domoticz.Debug("Unit Power Off")
                self.PioneerConn.Send(Message=api.cmd_PowerOff, Delay=0)
                self.power_on = False
            elif Command=='On':
                Domoticz.Debug("Unit Power On")
                self.PioneerConn.Send(Message=api.cmd_PowerOn, Delay=0)
                self.power_on = True
        elif Unit == self.UNITS['main_volume']:
            if (action == "On"):
                self.PioneerConn.Send(Message='MF\r', Delay=0)
            elif (action == "Set"):
                level = int(str(Level))
                delta = level - int(self.volume_level)
                Domoticz.Debug("delta: "+str(delta))
                for i in range(0, abs(delta), self.VOLUMESTEP):
                    if delta < 0:
                        self.volume_level = str(int(self.volume_level)-self.VOLUMESTEP)
                        self.PioneerConn.Send(Message='VD\r', Delay=0)
                        Domoticz.Debug("VD")
                    elif delta > 0:
                        self.volume_level = str(int(self.volume_level)+self.VOLUMESTEP)
                        self.PioneerConn.Send(Message='VU\r', Delay=0)
                        Domoticz.Debug("VU")
            elif (action == "Off"):
                self.PioneerConn.Send(Message='MO\r', Delay=0)
            Domoticz.Debug('Level:'+str(Level))
        elif Unit == self.UNITS['input']:
            if (action == "Set"):
                if Level != "0":
                    self.input_mode = self.selector_find(Level,1)
                    self.PioneerConn.Send(Message=self.input_mode+'FN\r', Delay=0)
                else:
                    self.power_on = False
                    self.PioneerConn.Send(Message=api.cmd_PowerOff, Delay=0)


    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Log("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)

    def onDisconnect(self, Connection):
        Domoticz.Log("onDisconnect called")
        self.isConnected = False

    def onHeartbeat(self):
        if (self.PioneerConn.Connected() == True):
            if (self.oustandingPings > 3):
                Domoticz.Debug("Ping Timeout, Disconnect")
                self.PioneerConn.Disconnect()
                self.nextConnect = 0
            else:
                self.PioneerConn.Send(Message=api.qry_PowerStatus,Delay=0)
                Domoticz.Debug("POWER STATUS Message Sent")
                self.oustandingPings = self.oustandingPings + 1
        else:
            # if not connected try and reconnected every 2 heartbeats
            self.oustandingPings = 0
            self.nextConnect = self.nextConnect - 1
            if (self.nextConnect <= 0):
                self.nextConnect = 3
                self.PioneerConn.Connect()
        return

    def SyncDevices(self, TimedOut):
        if (self.power_on == False):
            UpdateDevice(self.UNITS['power'], 0, "Off", TimedOut)
            UpdateDevice(self.UNITS['input'], 0, "0", TimedOut)
            UpdateDevice(self.UNITS['display'], 0, "", TimedOut)
            UpdateDevice(self.UNITS['listening_mode'], 0, "", TimedOut)
            UpdateDevice(self.UNITS['playing_mode'], 0, "", TimedOut)
            UpdateDevice(self.UNITS['main_volume'], 0, self.volume_level, TimedOut)
        else:
            UpdateDevice(self.UNITS['power'], 1 , "On", TimedOut)
            UpdateDevice(self.UNITS['input'], int(self.input_mode), str(self.input_mode), TimedOut)
            UpdateDevice(self.UNITS['display'], 0, self.display_text, TimedOut)
            UpdateDevice(self.UNITS['listening_mode'], 0, self.listening_mode, TimedOut)
            UpdateDevice(self.UNITS['playing_mode'], 0, self.playing_mode, TimedOut)
            UpdateDevice(self.UNITS['main_volume'],2,self.volume_level, TimedOut)
        return

    def selector_find(self, query, ctype):
            if ctype == 0:
                sel = (self.InputIdx.index(str(query))+1)*10 #Off olduğu için +1 var
                Domoticz.Debug('INDEX:'+str(sel))
            else:
                sel = self.InputIdx[int((query/10)-1)] #Off olduğu için -1 var
            return sel

global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)

def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

# Generic helper functions

def UpdateDevice(Unit, nValue, sValue, TimedOut):
    # Make sure that the Domoticz device still exists (they can be deleted) before updating it 
    if (Unit in Devices):
        if (Devices[Unit].nValue != nValue) or (Devices[Unit].sValue != sValue) or (Devices[Unit].TimedOut != TimedOut):
            Devices[Unit].Update(nValue=nValue, sValue=str(sValue), TimedOut=TimedOut)
            Domoticz.Log("Update "+str(nValue)+":'"+str(sValue)+"' ("+Devices[Unit].Name+")")
    return

def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return
