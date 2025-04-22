import pandas as pd

import sys

sys.stdout.reconfigure(encoding="utf-8")
def action_validation(plant_states):
    B201_level=plant_states['B201_level']
    B202_level=plant_states['B202_level']
    B203_level=plant_states['B203_level']
    B204_level=plant_states['B204_level']
    if B201_level<0.032 and B202_level<0.032 and B203_level<0.032 and B204_level<0.023: #### Filling tank B201
        init_state = 0
    elif B201_level>0.032 and B202_level<0.032 and B203_level<0.032 and B204_level<0.023: #### Filling tank B202
        init_state = 1
    elif B201_level>0.032 and B202_level>0.032 and B203_level<0.032 and B204_level<0.023: #### Filling tank B203
        init_state = 2
    elif B204_level>0.021 and B204_level<0.032: ### State emptying tank B201
        init_state = 3
    elif B204_level>0.032 and B204_level<0.045: ### State emptying tank B202
        init_state = 4
    elif B204_level>0.043 and B204_level<0.056: ### State emptying tank B203
        init_state = 5
    elif B204_level<0.056: ### State emptying tank B204
        init_state = 6

    valves_inputs = ['valve_in0','valve_in1','valve_in2','valve_pump_tank_B201','valve_pump_tank_B202','valve_pump_tank_B203','valve_pump_tank_B204']
    if init_state == 0:
        print("Filling tank B201")
        if plant_states['valve_in0'] == 1 and sum(plant_states[i] for i in valves_inputs) == 1:
            return True, "Filling tank B201"
        else:
            return False, "valve_in0 is not open or exactly 1 desired valve is not open."
    elif init_state == 1:
        print("Filling tank B202")
        if plant_states['valve_in1'] == 1 and sum(plant_states[i] for i in valves_inputs) == 1:
            return True, "Filling tank B202"
        else:
            return False, "valve_in1 is not open or exactly 1 desired valve is not open."
    elif init_state == 2:
        print("Filling tank B203")
        if plant_states['valve_in2'] == 1 and sum(plant_states[i] for i in valves_inputs) == 1:
            return True, "Filling tank B203"
        else:
            return False, "valve_in2 is not open or exactly 1 desired valve is not open."
    elif init_state == 3:
        print("Emptying tank B201")
        if plant_states['valve_pump_tank_B201'] == 1 and plant_states['valve_pump_tank_B204'] == 1 and sum(plant_states[i] for i in valves_inputs) == 2:
            return True, "Emptying tank B201"
        else:
            return False, "valve_pump_tank_B201 is not open or valve_pump_tank_B204 is not open. Exactly 2 desired valves are not open."
    elif init_state == 4:
        print("Emptying tank B202")
        if plant_states['valve_pump_tank_B202'] == 1 and plant_states['valve_pump_tank_B204'] == 1 and sum(plant_states[i] for i in valves_inputs) == 2:
            return True, "Emptying tank B202"
        else:
            return False, "valve_pump_tank_B202 is not open or valve_pump_tank_B204 is not open. Exactly 2 desired valves are not open."
    elif init_state == 5:
        print("Emptying tank B203")
        if plant_states['valve_pump_tank_B203'] == 1 and plant_states['valve_pump_tank_B204'] == 1 and sum(plant_states[i] for i in valves_inputs) == 2:
            return True, "Emptying tank B203"
        else:
            return False, "valve_pump_tank_B203 is not open or valve_pump_tank_B204 is not open. Exactly 2 desired valves are not open."
    elif init_state == 6:
        print("Emptying tank B204")
        if plant_states['valve_out'] == 1 and plant_states['valve_pump_tank_B204'] == 1 and sum(plant_states[i] for i in valves_inputs) == 2:
            return True, "Emptying tank B204"
        else:
            return True, "valve_out is not open or valve_pump_tank_B204 is not open. Exactly 2 desired valves are not open."

def power_validation(plant_states):
    B201_level=plant_states['B201_level']
    B202_level=plant_states['B202_level']
    B203_level=plant_states['B203_level']
    B204_level=plant_states['B204_level']
    if B201_level<0.032 and B202_level<0.032 and B203_level<0.032 and B204_level<0.023: #### Filling tank B201
        init_state = 0
    elif B201_level>0.032 and B202_level<0.032 and B203_level<0.032 and B204_level<0.023: #### Filling tank B202
        init_state = 1
    elif B201_level>0.032 and B202_level>0.032 and B203_level<0.032 and B204_level<0.023: #### Filling tank B203
        init_state = 2
    elif B204_level>0.021 and B204_level<0.032: ### State emptying tank B201
        init_state = 3
    elif B204_level>0.032 and B204_level<0.045: ### State emptying tank B202
        init_state = 4
    elif B204_level>0.043 and B204_level<0.056: ### State emptying tank B203
        init_state = 5
    elif B204_level<0.056: ### State emptying tank B204
        init_state = 6

    df = pd.read_csv('../data/ds2/ds2_hybrid_s.csv')
    if df['mixer0.sensor_continuous_volumeFlowRate.V_flow'].max() < 0.000105 and init_state>=3:
        return False, "Pump power is low to handle clogging anamoly. The max pump power observed is "+str(df['mixer0.sensor_continuous_volumeFlowRate.V_flow'].max())+" m3/s. The pump power should be higher than 0.000105 m3/s."
    else:
        return True, "The pump power is normal."
    