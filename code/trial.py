import pandas as pd
from mixer_sim import run_sim
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from pydantic import BaseModel, Field
import json
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

import sys
import os
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
openai_api_key = os.getenv("OPENAI_API_KEY")

class PlantState(BaseModel):
    cot: str = Field(..., title="cot", description="chain of thought of the model, how it arrived to the answer.")
    valve_in0: float = Field(..., title="valve_in01", description="valve_in01 position")
    valve_in1: float = Field(..., title="valve_in02", description="valve_in02 position")
    valve_in2: float = Field(..., title="valve_in03", description="valve_in03 position")
    valve_out: float = Field(..., title="valve_out", description="valve_out position")
    valve_pump_tank_B201: float = Field(..., title="valve_pump_tank_B201", description="valve_pump_tank_B201 position")
    valve_pump_tank_B202: float = Field(..., title="valve_pump_tank_B202", description="valve_pump_tank_B202 position")
    valve_pump_tank_B203: float = Field(..., title="valve_pump_tank_B203", description="valve_pump_tank_B203 position")
    valve_pump_tank_B204: float = Field(..., title="valve_pump_tank_B204", description="valve_pump_tank_B204 position")

    
@CrewBase
class PlantOperatorCrew:
    """Plant Operator Crew"""

    agents_config = "C:/Users/jv624/Desktop/fault_handling_openmodelica/code/crew/config/agents.yaml"
    tasks_config = "C:/Users/jv624/Desktop/fault_handling_openmodelica/code//crew/config/tasks.yaml"

    llm = ChatOpenAI(model="gpt-4o")
    @agent
    def plant_operator(self) -> Agent:
        return Agent(
            config=self.agents_config["plant_operator"],
            llm=self.llm,
            # tools=[code_interpreter],
            verbose=True,
        )

    @task
    def plant_operation(self) -> Task:
        return Task(
            config=self.tasks_config["plant_operation"],
            output_json=PlantState,
        )

    @crew
    def crew(self) -> Crew:
        """Creates the crew to solve the plant model"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

if __name__ == "__main__":
    B201_level = 0.02
    B202_level = 0.02
    B203_level = 0.02
    B204_level = 0.02
    valve_in0 = 0
    valve_in1 = 0
    valve_in2 = 0
    valve_out = 0
    valve_pump_tank_B201 = 0
    valve_pump_tank_B202 = 0
    valve_pump_tank_B203 = 0
    valve_pump_tank_B204 = 0

    message = []
    B201_level_list = []
    B202_level_list = []
    B203_level_list = []
    B204_level_list = []
    valve_in0_list = []
    valve_in1_list = []
    valve_in2_list = []
    valve_out_list = []
    valve_pump_tank_B201_list = []
    valve_pump_tank_B202_list = []
    valve_pump_tank_B203_list = []
    valve_pump_tank_B204_list = []
    total_input_tokens_list = []
    total_output_tokens_list = []
    total_tokens_list = []
    itr_input_tokens_list = []
    itr_output_tokens_list = []
    itr_token_list = []
    total_tokens = 0
    total_input_tokens = 0
    total_output_tokens = 0
    df_history = pd.DataFrame()

    
    for sim_time in range(15):
        print(f"Simulation time: {sim_time}")
        with open('mixer_sim.json') as f:
            setup = json.load(f)
        
        if sim_time==0:
            setup['ds1']['model']['modules']['mixer0']['init_states']['B201_level']=B201_level
            setup['ds1']['model']['modules']['mixer0']['init_states']['B202_level']=B202_level
            setup['ds1']['model']['modules']['mixer0']['init_states']['B203_level']=B203_level
            setup['ds1']['model']['modules']['mixer0']['init_states']['B204_level']=B204_level
            setup['ds1']['model']['modules']['mixer0']['init_states']['valve_in0_input']=valve_in0
            setup['ds1']['model']['modules']['mixer0']['init_states']['valve_in1_input']=valve_in1
            setup['ds1']['model']['modules']['mixer0']['init_states']['valve_in2_input']=valve_in2
            setup['ds1']['model']['modules']['mixer0']['init_states']['valve_out_input']=valve_out
            setup['ds1']['model']['modules']['mixer0']['init_states']['valve_pump_tank_B201_input']=valve_pump_tank_B201
            setup['ds1']['model']['modules']['mixer0']['init_states']['valve_pump_tank_B202_input']=valve_pump_tank_B202
            setup['ds1']['model']['modules']['mixer0']['init_states']['valve_pump_tank_B203_input']=valve_pump_tank_B203
            setup['ds1']['model']['modules']['mixer0']['init_states']['valve_pump_tank_B204_input']=valve_pump_tank_B204
        for i in setup:
            run_sim(sim_setup=setup[i], modus='hybrid', states=True)
        
        df = pd.read_csv('../data/ds1/ds1_hybrid_s.csv')
        B201_level = df['mixer0.tank_B201.level'].iloc[-1]
        B202_level = df['mixer0.tank_B202.level'].iloc[-1]
        B203_level = df['mixer0.tank_B203.level'].iloc[-1]
        B204_level = df['mixer0.tank_B204.level'].iloc[-1]
        B201_level_list.append(df['mixer0.tank_B201.level'].iloc[-1])
        B202_level_list.append(df['mixer0.tank_B202.level'].iloc[-1])
        B203_level_list.append(df['mixer0.tank_B203.level'].iloc[-1])
        B204_level_list.append(df['mixer0.tank_B204.level'].iloc[-1])

        res = PlantOperatorCrew().crew().kickoff(inputs={"B201_level": B201_level, 
                                                    "B202_level": B202_level, 
                                                    "B203_level": B203_level, 
                                                    "B204_level": B204_level, 
                                                    "valve_in0": valve_in0, 
                                                    "valve_in1": valve_in1, 
                                                    "valve_in2": valve_in2, 
                                                    "valve_out": valve_out, 
                                                    "valve_pump_tank_B201": valve_pump_tank_B201, 
                                                    "valve_pump_tank_B202": valve_pump_tank_B202, 
                                                    "valve_pump_tank_B203": valve_pump_tank_B203, 
                                                    "valve_pump_tank_B204": valve_pump_tank_B204})
        
        print(res['cot'])
        print(res['valve_in0'])
        print(res['valve_in1'])
        valve_in0 = 1 if res['valve_in0'] else 0
        valve_in1 = 1 if res['valve_in1'] else 0
        valve_in2 = 1 if res['valve_in2'] else 0
        valve_out = 1 if res['valve_out'] else 0
        valve_pump_tank_B201 = 1 if res['valve_pump_tank_B201'] else 0
        valve_pump_tank_B202 = 1 if res['valve_pump_tank_B202'] else 0
        valve_pump_tank_B203 = 1 if res['valve_pump_tank_B203'] else 0
        valve_pump_tank_B204 = 1 if res['valve_pump_tank_B204'] else 0

        total_input_tokens += res.token_usage.prompt_tokens
        total_output_tokens += res.token_usage.completion_tokens
        itr_input_tokens = res.token_usage.prompt_tokens
        itr_output_tokens = res.token_usage.completion_tokens
        itr_token = res.token_usage.total_tokens
        total_tokens+=res.token_usage.total_tokens


        message.append(res['cot'])
        valve_in0_list.append(res['valve_in0'])
        valve_in1_list.append(res['valve_in1'])
        valve_in2_list.append(res['valve_in2'])
        valve_out_list.append(res['valve_out'])
        valve_pump_tank_B201_list.append(res['valve_pump_tank_B201'])
        valve_pump_tank_B202_list.append(res['valve_pump_tank_B202'])
        valve_pump_tank_B203_list.append(res['valve_pump_tank_B203'])
        valve_pump_tank_B204_list.append(res['valve_pump_tank_B204'])
        total_input_tokens_list.append(total_input_tokens)
        total_output_tokens_list.append(total_output_tokens)
        total_tokens_list.append(total_tokens)
        itr_input_tokens_list.append(itr_input_tokens)
        itr_output_tokens_list.append(itr_output_tokens)
        itr_token_list.append(itr_token)
        df = pd.read_csv('../data/ds1/ds1_hybrid_s.csv')
        print(B201_level, B202_level, B203_level, B204_level)
        df_history = pd.concat([df_history,df])

        # B201_level = df_history['mixer0.tank_B201.level'].iloc[-1]
        # B202_level = df_history['mixer0.tank_B202.level'].iloc[-1]
        # B203_level = df_history['mixer0.tank_B203.level'].iloc[-1]
        # B204_level = df_history['mixer0.tank_B204.level'].iloc[-1]
        # B201_level_list.append(df_history['mixer0.tank_B201.level'].iloc[-1])
        # B202_level_list.append(df_history['mixer0.tank_B202.level'].iloc[-1])
        # B203_level_list.append(df_history['mixer0.tank_B203.level'].iloc[-1])
        # B204_level_list.append(df_history['mixer0.tank_B204.level'].iloc[-1])
        setup['ds1']['model']['modules']['mixer0']['init_states']['B201_level']=B201_level#df_history['mixer0.tank_B201.level'].iloc[-1]
        setup['ds1']['model']['modules']['mixer0']['init_states']['B202_level']=B202_level#df_history['mixer0.tank_B202.level'].iloc[-1]
        setup['ds1']['model']['modules']['mixer0']['init_states']['B203_level']=B203_level#df_history['mixer0.tank_B203.level'].iloc[-1]
        setup['ds1']['model']['modules']['mixer0']['init_states']['B204_level']=B204_level#df_history['mixer0.tank_B204.level'].iloc[-1]
        setup['ds1']['model']['modules']['mixer0']['init_states']['valve_in0_input']= 1 if res['valve_in0'] else 0
        setup['ds1']['model']['modules']['mixer0']['init_states']['valve_in1_input']= 1 if res['valve_in1'] else 0
        setup['ds1']['model']['modules']['mixer0']['init_states']['valve_in2_input']= 1 if res['valve_in2'] else 0
        setup['ds1']['model']['modules']['mixer0']['init_states']['valve_out_input']= 1 if res['valve_out'] else 0
        setup['ds1']['model']['modules']['mixer0']['init_states']['valve_pump_tank_B201_input']=1 if res['valve_pump_tank_B201'] else 0
        setup['ds1']['model']['modules']['mixer0']['init_states']['valve_pump_tank_B202_input']=1 if res['valve_pump_tank_B202'] else 0
        setup['ds1']['model']['modules']['mixer0']['init_states']['valve_pump_tank_B203_input']=1 if res['valve_pump_tank_B203'] else 0
        setup['ds1']['model']['modules']['mixer0']['init_states']['valve_pump_tank_B204_input']=1 if res['valve_pump_tank_B204'] else 0
        with open("mixer_sim.json", "w") as json_file:
            json.dump(setup, json_file, indent=4)
    df = pd.DataFrame({ 'message': message,
                        'B201_level': B201_level_list,
                        'B202_level': B202_level_list,
                        'B203_level': B203_level_list,
                        'B204_level': B204_level_list,
                        'valve_in0': valve_in0_list,
                        'valve_in1': valve_in1_list,
                        'valve_in2': valve_in2_list,
                        'valve_out': valve_out_list,
                        'valve_pump_tank_B201': valve_pump_tank_B201_list,
                        'valve_pump_tank_B202': valve_pump_tank_B202_list,
                        'valve_pump_tank_B203': valve_pump_tank_B203_list,
                        'valve_pump_tank_B204': valve_pump_tank_B204_list,
                        'total_input_tokens': total_input_tokens_list,
                        'total_output_tokens': total_output_tokens_list,
                        'total_tokens': total_tokens_list,
                        'itr_input_tokens': itr_input_tokens_list,
                        'itr_output_tokens': itr_output_tokens_list,
                        'itr_token': itr_token})
    df.to_csv('plant_op.csv', index=False)

        