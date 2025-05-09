import os
import json
import pandas as pd
import utils as u


def create_sim_setup(mos_path, dict_setup):
    """
    creating the call.mos file that contains the simulation setup.
    """
    sim_setup = dict_setup['sim_setup']
    vanilla_mos_file = u.read_file('vanilla_call.mos')

    new_mos_file = []
    for l in vanilla_mos_file:
        if l.startswith('cd("../data'):
            l = f'cd("../data/{dict_setup['ds_name']}");'
        elif l.startswith('simulate'):
            setup = l.split()
            new_setup = []
            for arg in setup:
                if arg.startswith('startTime'):
                    arg = f'startTime={sim_setup["startTime"]}'
                elif arg.startswith('stopTime'):
                    arg = f'stopTime={sim_setup["stopTime"]}'
                elif arg.startswith('numberOfIntervals'):
                    arg = f'numberOfIntervals={sim_setup["numberOfIntervals"]}'

                new_setup.append(arg)
            l = " ".join(new_setup)
        new_mos_file.append(l)

    with open(mos_path, 'w') as f:
        f.writelines(new_mos_file)
    print(f'simulation setup done and written to {mos_path}.')


def create_plant_sim_model(model_dir, sim_setup):
    """
    adapts the Plant.mo file, accordingly to the simulation setup
    """
    top_block = ['model processPlant', '    replaceable package Medium = Modelica.Media.Water.StandardWater;', '    Modelica.Fluid.System system_plant(energyDynamics = Modelica.Fluid.Types.Dynamics.FixedInitial, massDynamics = Modelica.Fluid.Types.Dynamics.FixedInitial, p_ambient = 1e5, T_ambient = 293.15, m_flow_start = 0.0005, p_start = 1e5, T_start(displayUnit = "K") = 300, dp_small = 100, m_flow_small = 0.01) annotation(Placement(transformation(origin = {-90, 90}, extent = {{-10, -10}, {10, 10}})));']
    dek_block = []
    equ_block = []
    bot_block = ['  annotation(uses(Modelica(version = "4.0.0")), experiment(StartTime = 0, StopTime = 1000, NumberOfIntervals = 500, Tolerance = 1e-6, Interval = 0.1),'                                                                                                                                                                     
                 '  Icon(graphics = {Text(origin = {2, -5}, textColor = {26, 95, 180}, extent = {{44, -51}, {-44, 51}}, textString = "P")}));', 'end processPlant;']

    sim_setup = sim_setup['model']
    mod_setup = sim_setup['modules']
    edg_setup = sim_setup['edges']

    for m in mod_setup:
        if 'source' in m:
            dek_block.append(f'    sourceModule {m}(redeclare package Medium = Medium);')
        elif 'sink' in m:
            dek_block.append(f'    sinkModule {m}(redeclare package Medium = Medium);')
        elif 'mixer' in m:
            dek_block.append(f'    mixerModule {m}(redeclare package Medium = Medium);')
        elif 'filter' in m:
            dek_block.append(f'    filterModule {m}(redeclare package Medium = Medium);')
        elif 'distill' in m:
            dek_block.append(f'    distillModule {m}(redeclare package Medium = Medium);')
        elif 'bottling' in m:
            dek_block.append(f'    bottlingModule {m}(redeclare package Medium = Medium);')
    dek_block.append('equation')

    for e in edg_setup:
        equ_block.append(f'    connect({edg_setup[e][0]},{edg_setup[e][1]});')

    model_block = top_block + dek_block + equ_block + bot_block
    model_block = '\n'.join(model_block)
    with open(os.path.join(model_dir, 'Plant.mo'), 'w') as f:
        f.writelines(model_block)
    print(f'simulation model created and saved {os.path.join(model_dir, "Plant.mo")}.')


def write_anomaly_in_module(module, module_dict, reset=False):
    model_dict = module_dict[module]
    model_code = u.read_file(model_dict['files'])

    new_model_code = []
    if reset:
        for line in model_code:
            if line.startswith('  parameter Boolean'):
                for anomaly in model_dict['faults']:
                    if line.startswith(f'  parameter Boolean {anomaly}'):
                        line = f'  parameter Boolean {anomaly} = false;\n'
            new_model_code.append(line)
    else:
        for line in model_code:
            if line.startswith('  parameter Boolean'):
                for anomaly in model_dict['faults']:
                    if model_dict['faults'][anomaly] == True and line.startswith(f'  parameter Boolean {anomaly}'):
                        line = f'  parameter Boolean {anomaly} = true;\n'
            if line.startswith('  parameter Real'):
                for state in model_dict['init_states']:
                    if line.startswith(f'  parameter Real {state}'):
                        line = f'  parameter Real {state} = {model_dict['init_states'][state]};\n'
            new_model_code.append(line)

    with open(model_dict['files'], 'w') as f:
        f.writelines(new_model_code)

    if not reset: print(f'anomalies have been updated for {module}.')


def induce_anomalies_in_plant(sim_setup, reset=False):
    """
    writes anomalies into modelica simulation models.
    """
    model_setup = sim_setup['model']['modules']

    # iterate through available models in simulation
    for module in model_setup:
        write_anomaly_in_module(module, model_setup, reset)


def data_cleaning(data_dir, sim_setup, modus):
    df = pd.read_csv(os.path.join(data_dir, sim_setup['ds_name'], f'{sim_setup["ds_name"]}.csv'), index_col=False)

    keep_cols = []

    # drop unnecessary info
    drop_cols = [col for col in df.columns if 'der(' in col or 'level_to_boolean' in col]
    df = df.drop(columns=drop_cols)

    # select and add all columns to keep within the dataframe feel free to comment lines out or add lines
    if '_s' in modus:
        keep_cols += [col for col in df.columns if 'state_' in col and not 'monitoring' in col]
    if 'continuous' in modus:
        keep_cols += [col for col in df.columns if '.level' in col]
        keep_cols += [col for col in df.columns if 'sensor_continuous' in col and not 'port' in col]
        keep_cols += [col for col in df.columns if 'volumeFlowRate' in col and 'm_flow' in col]
        keep_cols += [col for col in df.columns if 'N_in' in col]
        keep_cols += [col for col in df.columns if '.port.T' in col]
    if 'discrete' in modus:
        keep_cols += [col for col in df.columns if 'pump_n_in' in col]
        keep_cols += [col for col in df.columns if 'sensor_discrete_' in col]
        keep_cols += [col for col in df.columns if '.opening' in col]
        keep_cols += [col for col in df.columns if '.port.Q_flow' in col]
    if 'hybrid' in modus:
        keep_cols += [col for col in df.columns if '.level' in col]
        keep_cols += [col for col in df.columns if 'sensor_continuous' in col and not 'port' in col]
        keep_cols += [col for col in df.columns if 'volumeFlowRate' in col and 'm_flow' in col]
        keep_cols += [col for col in df.columns if 'N_in' in col]
        keep_cols += [col for col in df.columns if 'pump_n_in' in col]
        keep_cols += [col for col in df.columns if 'sensor_discrete_' in col]
        keep_cols += [col for col in df.columns if '.opening' in col]
        keep_cols += [col for col in df.columns if '.port.T' in col]
        keep_cols += [col for col in df.columns if '.port.Q_flow' in col]

    df = df[keep_cols]
    df.to_csv(os.path.join(data_dir, sim_setup['ds_name'], f'{sim_setup["ds_name"]}_{modus}.csv'))
    os.remove(os.path.join(data_dir, sim_setup['ds_name'], f'{sim_setup["ds_name"]}.csv'))


def run_sim(sim_setup, mos_path='./mixer_call.mos', model_dir='../models', data_dir='../data', modus='hybrid', states=True):
    """
    executes the simulation by calling OpenModelica from the command line and running the call.mos file.
    there are three modes: 'continuous', 'hybrid', and 'discrete'.
    """
    if states: modus = modus + '_s'

    # make data dir
    print(os.path.join(data_dir, sim_setup['ds_name']))

    u.create_dir(os.path.join(data_dir, sim_setup['ds_name']))

    # create simulation model
    create_plant_sim_model(model_dir, sim_setup)

    # induce anomalies to OpenModelica modules
    induce_anomalies_in_plant(sim_setup, reset=False)

    # write simulation file
    create_sim_setup(mos_path, sim_setup)

    # execute simulation
    print('loading simulation files ...')
    os.system("omc mixer_call.mos")

    # delete unnecessarey simulation information and rename it
    filelist = [f for f in os.listdir(os.path.join(data_dir, sim_setup['ds_name'])) if not f.endswith('.csv')]
    for f in filelist:
        os.remove(os.path.join(data_dir, sim_setup['ds_name'], f))
    os.rename(os.path.join(data_dir, sim_setup['ds_name'], 'processPlant_res.csv'), os.path.join(data_dir, sim_setup['ds_name'], f'{sim_setup["ds_name"]}.csv'))

    # save simulation hyperparameters in simulation directory
    with open(os.path.join(data_dir, sim_setup['ds_name'], 'sim_setup.json'), 'w') as f:
        json.dump(sim_setup, f, indent=4)

    # clean dataframe
    data_cleaning(data_dir, sim_setup, modus)

    # resest all anomalies in all files to false again
    induce_anomalies_in_plant(sim_setup, reset=True)

    print(f'simulation finished. data is saved in {os.path.join(data_dir, sim_setup['ds_name'])}')



if __name__ == '__main__':
    df_history=pd.DataFrame()
    a=['true', 'false']
    for i in range(10):
        valve_in0_input=a[i%2]
        valve_in1_input=a[(i+1)%2]
        valve_in2_input=a[i%2]
        valve_out_input=a[(i+1)%2]

        valve_pump_tank_B201_input=a[i%2]
        valve_pump_tank_B202_input=a[i%2]
        valve_pump_tank_B203_input=a[i%2]
        with open('mixer_sim.json') as f:
            setup = json.load(f)
        if i>0:
            setup['ds1']['model']['modules']['mixer0']['init_states']['B201_level']=df_history['mixer0.tank_B201.level'].iloc[-1]
            setup['ds1']['model']['modules']['mixer0']['init_states']['B202_level']=df_history['mixer0.tank_B202.level'].iloc[-1]
            setup['ds1']['model']['modules']['mixer0']['init_states']['B203_level']=df_history['mixer0.tank_B203.level'].iloc[-1]
            setup['ds1']['model']['modules']['mixer0']['init_states']['B204_level']=df_history['mixer0.tank_B204.level'].iloc[-1]

            setup['ds1']['model']['modules']['mixer0']['init_states']['valve_in0_input']=a[i%2]
            setup['ds1']['model']['modules']['mixer0']['init_states']['valve_in1_input']=a[(i+1)%2]
            setup['ds1']['model']['modules']['mixer0']['init_states']['valve_in2_input']=a[i%2]
            setup['ds1']['model']['modules']['mixer0']['init_states']['valve_out_input']=a[(i+1)%2]

            setup['ds1']['model']['modules']['mixer0']['init_states']['valve_pump_tank_B201_input']=a[i%2]
            setup['ds1']['model']['modules']['mixer0']['init_states']['valve_pump_tank_B202_input']=a[(i+1)%2]
            setup['ds1']['model']['modules']['mixer0']['init_states']['valve_pump_tank_B203_input']=True
        print(setup['ds1']['model']['modules']['mixer0']['init_states']['valve_pump_tank_B201_input'])
        for i in setup:
            run_sim(sim_setup=setup[i], modus='hybrid', states=True)

        df = pd.read_csv('../data/ds1/ds1_hybrid_s.csv')
        print(df.head())
        df_history = pd.concat([df_history,df])
    print(df_history.head(1))
    print(df_history.tail(1))
    df_history.to_csv('simulation.csv')
#   parameter Real B201_level_start = 0.01;
#   parameter Real B202_level_start = 0.01;
#   parameter Real B203_level_start = 0.01;
#   parameter Real B204_level_start = 0.01;