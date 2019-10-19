from guizero import App, Text, PushButton, Combo, Picture, TextBox, info, Window, CheckBox, Slider
import RPi.GPIO as GPIO
import time
from w1thermsensor import W1ThermSensor
from threading import Thread

class TempRead(Thread):
    global htl_temp
    global t_sensor
    def __init__(self):
        Thread.__init__(self)
        self.running = True
    def run(self):
        global htl_temp
        global t_sensor
        while self.running:
            htl_temp = float(t_sensor.get_temperature())
            HTL_temp_status.value = str(htl_temp) + " Celcius"
            time.sleep(0.1)
    def stop(self):
        self.running=False

#initialise all values
def init():
    global pump1_pos
    global pump2_pos
    global valve1_pos
    global valve2_pos
    global valve3_pos
    global valve4_pos
    global valve5_pos
    global valve6_pos
    global kettle_full_lvl_sns
    global kettle_empty_lvl_sns
    global htl_temp
    global mashtun_temp
    global kettle_temp
    global kettle_ele_lvl_sns
    global kettle_covered
    global underback_lvl_sns
    global htl_empty_lvl_sns
    global mashtun_full_lvl_sns
    global htl_covered
    global strike_started
    global sparge_started
    global vorlauf_started
    global drain_started
    global htl_empty
    global boil_started
    global mashtun_full
    global pwmPin
    global pump1_pin
    global pump2_pin
    global valve1_pin
    global valve2_pin
    global valve3_pin
    global valve4_pin
    global valve5_pin
    global valve6_pin
    global htl_pin
    global htl_temp_pin
    global mashtun_temp_pin
    global kettle_temp_pin
    global stop
    global pwm
    global init_run
    global t_sensor

    init_run = True

    t_sensor = W1ThermSensor()
    
    pump1_pos = "Disabled"
    pump2_pos = "Disabled"
    valve1_pos = "Closed"
    valve2_pos = "Closed"
    valve3_pos = "Closed"
    valve4_pos = "Closed"
    valve5_pos = "Closed"
    valve6_pos = "Closed"

    pwmPin = 18
    pump1_pin = 10
    pump2_pin = 23
    valve1_pin = 24
    valve2_pin = 25
    valve3_pin = 8
    valve4_pin = 7
    valve5_pin = 9
    valve6_pin = 11
    htl_pin = 2
    htl_temp_pin = 3
    mashtun_temp_pin = 4
    kettle_temp_pin = 17

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pwmPin, GPIO.OUT)
    pwm = GPIO.PWM(pwmPin, 50)
    pwm.start(0.0)
    GPIO.setup(pump1_pin, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(pump2_pin, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(valve1_pin, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(valve2_pin, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(valve3_pin, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(valve4_pin, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(valve5_pin, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(valve6_pin, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(htl_temp_pin, GPIO.IN)
    GPIO.setup(mashtun_temp_pin, GPIO.IN)
    GPIO.setup(kettle_temp_pin, GPIO.IN)
    
    pump_status_update()
    valve_status_update()
    
    kettle_full_lvl_sns = False
    Kettle_full_lvl_sns_status.value = str(kettle_full_lvl_sns)
    kettle_empty_lvl_sns = False
    Kettle_emp_lvl_sns_status.value = str(kettle_empty_lvl_sns)
    htl_temp = 0
    HTL_temp_status.value = str(htl_temp) + " Celcius"
    mashtun_temp = 0
    Mashtun_temp_probe_status.value = str(mashtun_temp) + " Celcius"
    kettle_temp = 0
    Kettle_temp_probe_status.value = str(kettle_temp) + " Celcius"
    kettle_ele_lvl_sns = 0
    Kettle_ele_lvl_sns_status.value = str(kettle_ele_lvl_sns)
    kettle_covered = False
    Kettle_covered_status.value = str(kettle_covered)
    underback_lvl_sns = 0
    Underback_lvl_sns_status.value = str(underback_lvl_sns)
    htl_empty_lvl_sns = False
    HTL_emp_lvl_sns_status.value = str(htl_empty_lvl_sns)
    mashtun_full_lvl_sns = False
    Mashtun_full_lvl_sns_status.value = str(mashtun_full_lvl_sns)
    htl_covered = False    
    HTL_covered_status.value = str(kettle_covered)
    strike_started = False
    sparge_started = False
    vorlauf_started = False
    drain_started = False
    boil_started = False
    htl_empty = False
    mashtun_full = False
    stop = False

    update_temp_kettle()
    kettle_full_lvl_sns_update()
    kettle_empty_lvl_sns_update()
    kettle_ele_lvl_sns_update()
    kettle_covered_update()

    underback_lvl_sns_update()

    update_temp_htl()
    htl_empty_lvl_sns_update()
    htl_covered_update()

    update_temp_mashtun()
    mashtun_full_lvl_sns_update()

    a = TempRead()
    a.start()

    init_run = False

#routines to update pump and valve status
def pump_status_update():
    global pump1_pos
    global pump2_pos
    global pump1_pin
    global pump2_pin

    if(pump1_pos == "Enabled"):
        GPIO.output(pump1_pin, GPIO.HIGH)
        pump1_status.text_color = "green"
    if(pump2_pos == "Enabled"):
        GPIO.output(pump2_pin, GPIO.HIGH)
        pump2_status.text_color = "green"
        
    if(pump1_pos == "Disabled"):
        GPIO.output(pump1_pin, GPIO.LOW)
        pump1_status.text_color = "red"
    if(pump2_pos == "Disabled"):
        GPIO.output(pump2_pin, GPIO.LOW)
        pump2_status.text_color = "red"
        
    pump1_status.value = pump1_pos
    pump2_status.value = pump2_pos

def valve_status_update():
    global valve1_pos
    global valve2_pos
    global valve3_pos
    global valve4_pos
    global valve5_pos
    global valve6_pos
    global valve1_pin
    global valve2_pin
    global valve3_pin
    global valve4_pin
    global valve5_pin
    global valve6_pin
    
    if(valve1_pos == "Open"):
        GPIO.output(valve1_pin, GPIO.HIGH)
        valve1_status.text_color = "green"
    if(valve2_pos == "Open"):
        GPIO.output(valve2_pin, GPIO.HIGH)
        valve2_status.text_color = "green"
    if(valve3_pos == "Open"):
        GPIO.output(valve3_pin, GPIO.HIGH)
        valve3_status.text_color = "green"
    if(valve4_pos == "Open"):
        GPIO.output(valve4_pin, GPIO.HIGH)
        valve4_status.text_color = "green"
    if(valve5_pos == "Open"):
        GPIO.output(valve5_pin, GPIO.HIGH)
        valve5_status.text_color = "green"
    if(valve6_pos == "Open"):
        GPIO.output(valve6_pin, GPIO.HIGH)
        valve6_status.text_color = "green"
        
    if(valve1_pos == "Closed"):
        GPIO.output(valve1_pin, GPIO.LOW)
        valve1_status.text_color = "red"
    if(valve2_pos == "Closed"):
        GPIO.output(valve2_pin, GPIO.LOW)
        valve2_status.text_color = "red"
    if(valve3_pos == "Closed"):
        GPIO.output(valve3_pin, GPIO.LOW)
        valve3_status.text_color = "red"
    if(valve4_pos == "Closed"):
        GPIO.output(valve4_pin, GPIO.LOW)
        valve4_status.text_color = "red"
    if(valve5_pos == "Closed"):
        GPIO.output(valve5_pin, GPIO.LOW)
        valve5_status.text_color = "red"
    if(valve6_pos == "Closed"):
        GPIO.output(valve6_pin, GPIO.LOW)
        valve6_status.text_color = "red"
        
    valve1_status.value = valve1_pos
    valve2_status.value = valve2_pos
    valve3_status.value = valve3_pos
    valve4_status.value = valve4_pos
    valve5_status.value = valve5_pos
    valve6_status.value = valve6_pos

#routines to update debug temperatures and sensors
def update_temp_htl():
    global htl_temp
    global init_run
    #htl_temp = int(HTL_temp_input.value)
    HTL_temp_status.value = str(htl_temp) + " Celcius"
    HTL_temp_status.text_color = (int(htl_temp), 0, 255-int(htl_temp))
    if init_run == True:
        return
    start_htl()

def update_temp_htl_txt():
    global htl_temp
    global init_run
    while GPIO.input(3):
        print("checking")
        devices = find_devices()
        for device in devices:
            valid, raw = read_temp(device)
            if valid:
                c = raw / 1000.0
                htl_temp = c
        HTL_temp_status.value = str(htl_temp) + " Celcius"
        HTL_temp_status.text_color = (int(htl_temp), 0, 255-int(htl_temp))
        time.sleep(0.5)

def update_temp_mashtun():
    global mashtun_temp
    mashtun_temp = Mashtun_temp_input.value
    Mashtun_temp_probe_status.value = str(mashtun_temp) + " Celcius"
    Mashtun_temp_probe_status.text_color = (int(mashtun_temp), 0, 255-int(mashtun_temp))

def update_temp_kettle():
    global kettle_temp
    global init_run
    kettle_temp = int(Kettle_temp_input.value)
    Kettle_temp_probe_status.value = str(kettle_temp) + " Celcius"
    Kettle_temp_probe_status.text_color = (int(kettle_temp), 0, 255-int(kettle_temp))
    if init_run == True:
        return
    start_boil()

def kettle_full_lvl_sns_update():
    global kettle_full_lvl_sns
    if Kettle_full_lvl_sns_check.value == 1:
        kettle_full_lvl_sns = True
        Kettle_full_lvl_sns_status.text_color = "red"
    if Kettle_full_lvl_sns_check.value == 0:
        kettle_full_lvl_sns = False
        Kettle_full_lvl_sns_status.text_color = "green"
    Kettle_full_lvl_sns_status.value = str(kettle_full_lvl_sns)

def kettle_empty_lvl_sns_update():
    global kettle_empty_lvl_sns
    if Kettle_empty_lvl_sns_check.value == 1:
        kettle_empty_lvl_sns = True
        Kettle_emp_lvl_sns_status.text_color = "red"
    if Kettle_empty_lvl_sns_check.value == 0:
        kettle_empty_lvl_sns = False
        Kettle_emp_lvl_sns_status.text_color = "green"
    Kettle_emp_lvl_sns_status.value = str(kettle_empty_lvl_sns)

def kettle_ele_lvl_sns_update():
    global kettle_ele_lvl_sns
    kettle_ele_lvl_sns = float(Kettle_ele_lvl_sns_input.value)
    Kettle_ele_lvl_sns_status.value = str(kettle_ele_lvl_sns)

def kettle_covered_update():
    global kettle_covered
    if Kettle_covered_check.value == 1:
        kettle_covered = True
        Kettle_covered_status.text_color = "green"
    if Kettle_covered_check.value == 0:
        kettle_covered = False
        Kettle_covered_status.text_color = "red"
    Kettle_covered_status.value = str(kettle_covered)

def underback_lvl_sns_update():
    global underback_lvl_sns
    underback_lvl_sns = float(Underback_lvl_sns_input.value)
    Underback_lvl_sns_status.value = str(underback_lvl_sns)

def htl_empty_lvl_sns_update():
    global htl_empty_lvl_sns
    if HTL_empty_lvl_sns_check.value == 1:
        htl_empty_lvl_sns = True
        HTL_emp_lvl_sns_status.text_color = "red"
    if HTL_empty_lvl_sns_check.value == 0:
        htl_empty_lvl_sns = False
        HTL_emp_lvl_sns_status.text_color = "green"
    HTL_emp_lvl_sns_status.value = str(htl_empty_lvl_sns)

def mashtun_full_lvl_sns_update():
    global mashtun_full_lvl_sns
    if Mashtun_full_lvl_sns_check.value == 1:
        mashtun_full_lvl_sns = True
        Mashtun_full_lvl_sns_status.text_color = "red"
    if Mashtun_full_lvl_sns_check.value == 0:
        mashtun_full_lvl_sns = False
        Mashtun_full_lvl_sns_status.text_color = "green"
    Mashtun_full_lvl_sns_status.value = str(mashtun_full_lvl_sns)

def htl_covered_update():
    global htl_covered
    if HTL_covered_check.value == 1:
        htl_covered = True
        HTL_covered_status.text_color = "green"
    if HTL_covered_check.value == 0:
        htl_covered = False
        HTL_covered_status.text_color = "red"
    HTL_covered_status.value = str(htl_covered)

#routines to start and stop each stage
def start_htl():
    global htl_started
    global htl_temp
    global htl_temp_sp
    global htl_covered
    global boil_started
    global stop

    if boil_started == True:
        stop_boil()

    if stop == True:
        info("Warning!", "Stop button enabled")
        return
    
    htl_started = True
    try:
        #HTL temp control
        if htl_started == True and int(htl_temp_sp) == int(htl_temp) and htl_covered == True: #and HTL_temp_probe = True
            HTL_temp_status.value = str(htl_temp) + " Celcius"
            HTL_ele_sns_status.value = "Heated"
            HTL_ele_sns_status.text_color = "green"
            HTL_start_button.bg = "green"
            HTL_stop_button.bg = "gray"
        elif htl_started == True and int(htl_temp) < int(htl_temp_sp) and htl_covered == True:
            HTL_temp_status.value = str(htl_temp) + " Celcius"
            HTL_ele_sns_status.value = "Heating"
            HTL_ele_sns_status.text_color = "red"
            HTL_start_button.bg = "green"
            HTL_stop_button.bg = "gray"
        else:
            stop_htl()
            info("Warning!", "Is the HTL element covered?")
    except NameError:
        info("Warning!", "You haven't defined a set point for the HTL!")
        stop_htl()
        htl_started = False
        

def stop_htl():
    HTL_start_button.bg = "gray"
    HTL_stop_button.bg = "red"
    htl_started = False

def start_boil():
    global boil_started
    global boil_ele_started
    global kettle_temp
    global kettle_covered
    global drain_started
    global htl_started

    if htl_started == True:
        stop_htl()
    if drain_started == True:
        stop_drain()

    boil_started = True
    if boil_started == True and kettle_temp <= 99 and kettle_covered == True: #and kettle_temp_probe = True
        Kettle_temp_probe_status.value = str(Kettle_temp_input.value) + " Celcius"
        Kettle_ele_status.value = "Enabled"
        Kettle_ele_status.text_color = "green"
        boil_ele_started = True
        Boil_start_button.bg = "green"
        Boil_stop_button.bg = "gray"
    elif boil_started == True and kettle_temp > 99:
        stop_boil()
        stop()
        #reduce power 
    else:
        stop_boil()
        info("Warning!", "Ensure kettle temperature is under 99C and kettle is covered!")

def stop_boil():
    Boil_start_button.bg = "gray"
    Boil_stop_button.bg = "red"
    boil_started = False
    Kettle_ele_status.text_color = "red"
    Kettle_ele_status.value = "Disabled"

def start_strike():
    global sparge_started
    global strike_started
    global vorlauf_started
    global htl_temp
    global htl_temp_sp
    global valve1_pos
    global valve2_pos
    global valve3_pos
    global valve4_pos
    global valve5_pos
    global valve6_pos
    global pump1_pos
    global mashtun_full
    global htl_empty
    global drain_started
    global stop

    if stop == True:
        info("Warning!", "Stop button enabled")
        return
    
    strike_started = True
    if sparge_started == True:
        stop_sparge()
    if vorlauf_started == True:
        stop_vorlauf()
    if drain_started == True:
        stop_drain()
    try:
        if strike_started == True and htl_temp == htl_temp_sp and htl_empty == False and mashtun_full == False:
            valve1_pos = "Open"
            valve2_pos = "Closed"
            valve3_pos = "Closed"
            valve4_pos = "Closed"
            valve5_pos = "Closed"
            valve6_pos = "Closed"
            pump1_pos = "Enabled"
            pump_status_update()
            valve_status_update()
            Strike_start_button.bg = "green"
            Strike_stop_button.bg = "gray"
        else:
            stop_strike()
            info("Warning!", "Ensure HTL temperature matches set point, HTL is not empty and mashtun is not full!")
    except NameError:
        stop_strike()
        info("Warning!", "You haven't defined a set point for the HTL!")

def stop_strike():
    global valve1_pos
    global valve2_pos
    global valve3_pos
    global valve4_pos
    global valve5_pos
    global valve6_pos
    global pump1_pos
    global strike_started
    
    valve1_pos = "Closed"
    valve2_pos = "Closed"
    valve3_pos = "Closed"
    valve4_pos = "Closed"
    valve5_pos = "Closed"
    valve6_pos = "Closed"
    pump1_pos = "Disabled"
    pump_status_update()
    valve_status_update()
    Strike_start_button.bg = "gray"
    Strike_stop_button.bg = "red"
    strike_started = False

def start_vorlauf():
    global valve1_pos
    global valve2_pos
    global valve3_pos
    global valve4_pos
    global valve5_pos
    global valve6_pos
    global pump1_pos
    global underback_lvl_sns
    global vorlauf_started
    global strike_started
    global sparge_started
    global drain_started
    global stop

    if stop == True:
        info("Warning!", "Stop button enabled")
        return
    
    vorlauf_started = True
    if sparge_started == True:
        stop_sparge()
    if strike_started == True:
        stop_strike()
    if drain_started == True:
        stop_drain()
    if vorlauf_started == True and underback_lvl_sns > 0:
        valve1_pos = "Closed"
        valve2_pos = "Open"
        valve3_pos = "Closed"
        valve4_pos = "Closed"
        valve5_pos = "Closed"
        valve6_pos = "Closed"
        pump1_pos = "Enabled"
        pump_status_update()
        valve_status_update()
        Vorlauf_start_button.bg = "green"
        Vorlauf_stop_button.bg = "gray"
    else:
        info("Warning!", "Ensure there is something in the underback")
        stop_vorlauf()

def stop_vorlauf():
    global valve1_pos
    global valve2_pos
    global valve3_pos
    global valve4_pos
    global valve5_pos
    global valve6_pos
    global pump1_pos
    global vorlauf_started
    valve1_pos = "Closed"
    valve2_pos = "Closed"
    valve3_pos = "Closed"
    valve4_pos = "Closed"
    valve5_pos = "Closed"
    valve6_pos = "Closed"
    pump1_pos = "Disabled"
    pump_status_update()
    valve_status_update()
    Vorlauf_start_button.bg = "gray"
    Vorlauf_stop_button.bg = "red"
    vorlauf_started = False

def start_sparge():
    global valve1_pos
    global valve2_pos
    global valve3_pos
    global valve4_pos
    global valve5_pos
    global valve6_pos
    global pump1_pos
    global pump2_pos
    global htl_temp
    global htl_temp_sp
    global kettle_full_lvl_sns
    global underback_lvl_sns
    global sparge_started
    global vorlauf_started
    global strike_started
    global drain_started
    global stop

    if stop == True:
        info("Warning!", "Stop button enabled")
        return
    
    sparge_started = True
    if vorlauf_started == True:
        stop_vorlauf()
    if strike_started == True:
        stop_strike()
    if drain_started == True:
        stop_drain()
    try:
        if sparge_started == True and htl_temp == htl_temp_sp and kettle_full_lvl_sns == False and underback_lvl_sns > 0 and htl_empty_lvl_sns == False:
            valve1_pos = "Open"
            valve2_pos = "Closed"
            valve3_pos = "Open"
            valve4_pos = "Open"
            valve5_pos = "Closed"
            valve6_pos = "Closed"
            pump1_pos = "Enabled"
            pump_status_update()
            valve_status_update()
            Sparge_start_button.bg = "green"
            Sparge_stop_button.bg = "gray"
            #while underback_lvl_sns > 0
            pump2_pos = "Enabled"
            pump_status_update()
        else:
            info("Warning!", "Ensure HTL temperature matches set point, HTL is not empty, kettle is not full and there is something in the underback!")
            stop_sparge()
    except NameError:
        info("Warning!", "You haven't defined a set point for the HTL!")
        stop_sparge()

def stop_sparge():
    global valve1_pos
    global valve2_pos
    global valve3_pos
    global valve4_pos
    global valve5_pos
    global valve6_pos
    global pump1_pos
    global pump2_pos
    global sparge_started

    valve1_pos = "Closed"
    valve2_pos = "Closed"
    valve3_pos = "Closed"
    valve4_pos = "Closed"
    valve5_pos = "Closed"
    valve6_pos = "Closed"
    pump1_pos = "Disabled"
    pump2_pos = "Disabled"
    pump_status_update()
    valve_status_update()
    Sparge_start_button.bg = "gray"
    Sparge_stop_button.bg = "red"
    sparge_started = False

def start_drain():
    global valve1_pos
    global valve2_pos
    global valve3_pos
    global valve4_pos
    global valve5_pos
    global valve6_pos
    global pump2_pos
    global kettle_empty_lvl_sns
    global sparge_started
    global vorlauf_started
    global strike_started
    global drain_started
    global boil_started
    global stop

    if stop == True:
        info("Warning!", "Stop button enabled")
        return
    if sparge_started == True:
        stop_sparge()
    if vorlauf_started == True:
        stop_vorlauf()
    if strike_started == True:
        stop_strike()
    if boil_started == True:
        stop_boil()
    drain_started = True
    if drain_started == True and kettle_empty_lvl_sns == False:
        valve1_pos = "Closed"
        valve2_pos = "Closed"
        valve3_pos = "Closed"
        valve4_pos = "Closed"
        valve5_pos = "Open"
        valve6_pos = "Open"
        pump2_pos = "Enabled"
        Drain_start_button.bg = "green"
        Drain_stop_button.bg = "gray"
        pump_status_update()
        valve_status_update()
    else:
        info("Warning!", "Ensure kettle is not empty!")
        stop_drain()

def stop_drain():
    global valve1_pos
    global valve2_pos
    global valve3_pos
    global valve4_pos
    global valve5_pos
    global valve6_pos
    global pump2_pos
    valve1_pos = "Closed"
    valve2_pos = "Closed"
    valve3_pos = "Closed"
    valve4_pos = "Closed"
    valve5_pos = "Closed"
    valve6_pos = "Closed"
    pump2_pos = "Disabled"
    pump_status_update()
    valve_status_update()
    Drain_start_button.bg = "gray"
    Drain_stop_button.bg = "red"
    drain_started = False

def update_temp_htl_sp():
    global htl_temp_sp
    htl_temp_sp = HTL_SetPoint_input.value

def Stop():
    global stop
    stop = True
    valve1_pos = "Closed"
    valve2_pos = "Closed"
    valve3_pos = "Closed"
    valve4_pos = "Closed"
    valve5_pos = "Closed"
    valve6_pos = "Closed"
    pump1_pos = "Closed"
    pump1_pos = "Closed"
    pump_status_update()
    valve_status_update()
    stop_strike()
    stop_sparge()
    stop_vorlauf()
    stop_boil()
    stop_htl()
    stop_drain()
    stop_label.value = "Stopped"
    stop_label.text_color = "Red"
    stop_button.bg = "Red"

def reset():
    global stop
    stop = False
    stop_label.value = "Running"
    stop_label.text_color = "Green"
    stop_button.bg = "Gray"


def open_debug_window():
    debug.show()

def change_pwm(slider_value):
    global pwm
    pwm.ChangeDutyCycle(float(slider_value))

app = App(title="BreweryGUI", layout="grid", width=1000, height=800)
debug = Window(app, title="Debug Window", layout="grid", width=600)
debug.hide()

########################################################################################################################
#defining all labels and text
stop_label = Text(app, grid=[0,0], text="Running", size=15, color="Green")
stop_button = PushButton(app, grid=[2,0], text="Stop", command=Stop, align="left")
reset_button = PushButton(app, grid=[1,0], text="Reset", command=reset, align="left")
error_text = Text(app, grid=[0,3], text="", size=15, color="Red")
debug_window = PushButton(app, grid=[4,0], text="Open Debug Commands", command=open_debug_window)

#pumps
pump1_label = Text(app, grid=[0,1], text="Pump 1", size=15, color="Blue")
pump1_status = Text(app, grid=[1,1], text="Deactivated", size=15, color="Red")
pump2_label = Text(app, grid=[0,2], text="Pump 2", size=15, color="Blue")
pump2_status = Text(app, grid=[1,2], text="Deactivated", size=15, color="Red")

#valves
valve1_label = Text(app, grid=[0,3], text="Valve 1", size=15, color="Purple")
valve1_status = Text(app, grid=[1,3], text="Deactivated", size=15, color="Red")
valve2_label = Text(app, grid=[0,4], text="Valve 2", size=15, color="Purple")
valve2_status = Text(app, grid=[1,4], text="Deactivated", size=15, color="Red")
valve3_label = Text(app, grid=[0,5], text="Valve 3", size=15, color="Purple")
valve3_status = Text(app, grid=[1,5], text="Deactivated", size=15, color="Red")
valve4_label = Text(app, grid=[0,6], text="Valve 4", size=15, color="Purple")
valve4_status = Text(app, grid=[1,6], text="Deactivated", size=15, color="Red")
valve5_label = Text(app, grid=[0,7], text="Valve 5", size=15, color="Purple")
valve5_status = Text(app, grid=[1,7], text="Deactivated", size=15, color="Red")
valve6_label = Text(app, grid=[0,8], text="Valve 6", size=15, color="Purple")
valve6_status = Text(app, grid=[1,8], text="Deactivated", size=15, color="Red")

#HTL
HTL_ele_sns_label = Text(app, grid=[2,1], text="HTL element sensor", size=15, color="Yellow", align="left")
HTL_ele_sns_status = Text(app, grid=[3,1], text="Deactivated", size=15, color="Red")

HTL_emp_lvl_sns_label = Text(app, grid=[2,2], text="HTL empty Level sensor", size=15, color="Yellow", align="left")
HTL_emp_lvl_sns_status = Text(app, grid=[3,2], text="Deactivated", size=15, color="Red")
HTL_empty_lvl_sns_check = CheckBox(debug, command=htl_empty_lvl_sns_update, grid=[2,23], text="HTL empty", align="left")

HTL_covered_label = Text(app, grid=[2,3], text="HTL covered", size=15, color="Yellow", align="left")
HTL_covered_status = Text(app, grid=[3,3], text="Deactivated", size=15, color="Red")
HTL_covered_check = CheckBox(debug, grid=[2,25], text="HTL element covered", command=htl_covered_update)

HTL_temp_label = Text(app, grid=[2,4], text="HTL temperature", size=15, color="Yellow", align="left")
HTL_temp_status = Text(app, grid=[3,4], text="Deactivated", size=15, color="Red")

#Underback
Underback_lvl_sns_label = Text(app, grid=[2,5], text="Underback level sensor", size=15, color="Indian red", align="left")
Underback_lvl_sns_status = Text(app, grid=[3,5], text="Deactivated", size=15, color="Red")
Underback_lvl_sns_input_button = PushButton(debug, command=underback_lvl_sns_update, grid=[1,22], text="Underback level sensor", align="left")
Underback_lvl_sns_input = TextBox(debug, grid=[2,22], text = "0")

#Mashtun
Mashtun_full_lvl_sns_label = Text(app, grid=[2,6], text="Mashtun full level sensor", size=15, color="Orange2", align="left")
Mashtun_full_lvl_sns_status = Text(app, grid=[3,6], text="Deactivated", size=15, color="Red")
Mashtun_full_lvl_sns_check = CheckBox(debug, command=mashtun_full_lvl_sns_update, grid=[2,24], text="Mashtun full", align="left")

Mashtun_temp_probe_label = Text(app, grid=[2,7], text="Mashtun temperature sensor", size=15, color="Orange2", align="left")
Mashtun_temp_probe_status = Text(app, grid=[3,7], text="Deactivated", size=15, color="Red")

#Kettle
Kettle_full_lvl_sns_label = Text(app, grid=[2,8], text="Kettle full level sensor", size=15, color="Dark slate gray", align="left")
Kettle_full_lvl_sns_status = Text(app, grid=[3,8], text="Deactivated", size=15, color="Red")
Kettle_full_lvl_sns_check = CheckBox(debug, command=kettle_full_lvl_sns_update, grid=[2,18], text="Kettle full", align="left")

Kettle_emp_lvl_sns_label = Text(app, grid=[2,9], text="Kettle empty level sensor", size=15, color="Dark slate gray", align="left")
Kettle_emp_lvl_sns_status = Text(app, grid=[3,9], text="Deactivated", size=15, color="Red")
Kettle_empty_lvl_sns_check = CheckBox(debug, command=kettle_empty_lvl_sns_update, grid=[2,19], text="Kettle empty", align="left")

Kettle_ele_lvl_sns_label = Text(app, grid=[2,10], text="Kettle element level sensor", size=15, color="Dark slate gray", align="left")
Kettle_ele_lvl_sns_status = Text(app, grid=[3,10], text="Deactivated", size=15, color="Red")
Kettle_ele_lvl_sns_input_button = PushButton(debug, command=kettle_ele_lvl_sns_update, grid=[1,20], text="Kettle element level sensor", align="left")
Kettle_ele_lvl_sns_input = TextBox(debug, grid=[2,20], text = "0")

Kettle_ele_label = Text(app, grid=[2,11], text="Kettle element", size=15, color="Dark slate gray", align="left")
Kettle_ele_status = Text(app, grid=[3,11], text="Deactivated", size=15, color="Red")

Kettle_temp_probe_label = Text(app, grid=[2,12], text="Kettle temperature sensor", size=15, color="Dark slate gray", align="left")
Kettle_temp_probe_status = Text(app, grid=[3,12], text="Deactivated", size=15, color="Red")

Kettle_covered_label = Text(app, grid=[2,13], text="Kettle covered", size=15, color="Dark slate gray", align="left")
Kettle_covered_status = Text(app, grid=[3,13], text="Deactivated", size=15, color="Red")
Kettle_covered_check = CheckBox(debug, grid=[2,21], text="Kettle element covered", command=kettle_covered_update)

#PWM
PWM_label = Text(app, grid=[3,15], text="PWM speed", size=15)
PWM_slider = Slider(app, grid=[3,16], start=0, end=100, command=change_pwm, horizontal=True)

########################################################################################################################

#declaring debug inputs
setpoint_mode_label = Text(app, grid=[0,14], text="Setpoint mode", size=15, align="left")
setpoint_mode = Combo(app, grid=[1,14], options=["Strike", "Sparge", "Manual Input"], align="left")

HTL_temp_input_label = Text(debug, grid=[0,15], text="Debug HTL temp", size=15, align="left")
HTL_temp_input = TextBox(debug, grid=[1,15], text = "0")
HTL_update_temp = PushButton(debug, command=update_temp_htl, grid=[2,15], text="Update temp", align="left")

Mashtun_temp_input_label = Text(debug, grid=[0,16], text="Debug Mashtun temp", size=15, align="left")
Mashtun_temp_input = TextBox(debug, grid=[1,16], text = "0")
Mashtun_update_temp = PushButton(debug, command=update_temp_mashtun, grid=[2,16], text="Update temp", align="left")

Kettle_temp_input_label = Text(debug, grid=[0,17], text="Debug Kettle temp", size=15, align="left")
Kettle_temp_input = TextBox(debug, grid=[1,17], text = "0")
Kettle_update_temp = PushButton(debug, command=update_temp_kettle, grid=[2,17], text="Update temp", align="left")

HTL_start_button = PushButton(app, command=start_htl, grid=[0,18], text="Start HTL", align="left")
HTL_stop_button = PushButton(app, command=stop_htl, grid=[1,18], text="Stop HTL", align="left")

Boil_start_button = PushButton(app, command=start_boil, grid=[0,19], text="Start boil", align="left")
Boil_stop_button = PushButton(app, command=stop_boil, grid=[1,19], text="Stop boil", align="left")

Strike_start_button = PushButton(app, command=start_strike, grid=[0,20], text="Start strike", align="left")
Strike_stop_button = PushButton(app, command=stop_strike, grid=[1,20], text="Stop strike", align="left")

Vorlauf_start_button = PushButton(app, command=start_vorlauf, grid=[0,21], text="Start vorlauf", align="left")
Vorlauf_stop_button = PushButton(app, command=stop_vorlauf, grid=[1,21], text="Stop vorlauf", align="left")

Sparge_start_button = PushButton(app, command=start_sparge, grid=[0,22], text="Start sparge", align="left")
Sparge_stop_button = PushButton(app, command=stop_sparge, grid=[1,22], text="Stop sparge", align="left")

Drain_start_button = PushButton(app, command=start_drain, grid=[0,23], text="Start drain", align="left")
Drain_stop_button = PushButton(app, command=stop_drain, grid=[1,23], text="Stop drain", align="left")

HTL_SetPoint_input_label = Text(app, grid=[3,14], text="HTL temp set point", size=15, align="left")
HTL_SetPoint_input = TextBox(app, grid=[4,14], text = "0")
HTL_update_SetPoint = PushButton(app, command=update_temp_htl_sp, grid=[5,14], text="Update temp", align="left")

########################################################################################################################

init()

app.display()



GPIO.cleanup()
