from typing import TypedDict, List, Union
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage

# Define the state structure


class HospitalState(TypedDict):
    messages: List[str]
    patient_data: dict
    appointment_status: Union[str, None]

# Patient Scheduling Agent logic


def patient_scheduling(message: HumanMessage, config):
    # Parse the state out of the initial message
    # assuming you used str() to create the message earlier
    initial_state = eval(message.content)

    state = {
        "messages": initial_state["messages"],
        "patient_data": initial_state["patient_data"],
        "appointment_status": initial_state["appointment_status"]
    }

    '''if state["appointment_status"] == "Scheduled":
        return {"messages": state["messages"] + ["Appointment already scheduled"]}

    # Simulate scheduling logic
    patient_name = state["patient_data"].get("name", "Unknown")
    department = state["patient_data"].get("department", "General")
    time_slot = "10:00 AM"  # This could be dynamically fetched
    state["appointment_status"] = f"Appointment for {patient_name} in {department} at {time_slot}"

    return {"messages": state["messages"] + [state["appointment_status"]]}'''

    # Extract state from the config
    state = config.get("state", {})

    if state.get("appointment_status") == "Scheduled":
        return {"messages": state.get("messages", []) + [{"content": "Appointment already scheduled"}]}

    # Simulate scheduling logic
    patient_name = state.get("patient_data", {}).get("name", "Unknown")
    department = state.get("patient_data", {}).get("department", "General")
    time_slot = "10:00 AM"  # This could be dynamically fetched
    state["appointment_status"] = f"Appointment for {
        patient_name} in {department} at {time_slot}"
    state["messages"] = state.get(
        "messages", []) + [{"content": state["appointment_status"]}]

    return state

# Resource Allocation Agent logic


def resource_allocation(state, config):
    # Simulate resource checking logic
    department = state["patient_data"].get("department", "General")
    resources_available = {"Radiology": 3, "Pharmacy": 5, "General": 2}

    if resources_available.get(department, 0) > 0:
        return {"messages": state["messages"] + [f"Resources available for {department}"]}
    else:
        return {"messages": state["messages"] + [f"No resources available for {department}"]}

# Diagnosis Assistance Agent logic


def diagnosis_assistance(state, config):
    # Simulate a diagnostic suggestion
    patient_history = state["patient_data"].get(
        "history", "No history provided")
    diagnosis = f"Suggested diagnosis based on history: {patient_history}"
    return {"messages": state["messages"] + [diagnosis]}


def decide_to_finish(state, config):
    if state["messages"] == "resource_allocation":
        return "resource_allocation"
    elif state["messages"] == "diagnosis_assistance":
        return "diagnosis_assistance"
    else:
        return None


# Workflow setup
workflow = StateGraph(HospitalState)

'''def edge_condition(state):
     return "Appointment" not in state["messages"][-1]
 workflow.add_edge("PatientScheduling", "ResourceAllocation", condition=edge_condition)'''

# Adding nodes
workflow.add_node("PatientScheduling", patient_scheduling)
workflow.add_node("ResourceAllocation", resource_allocation)
workflow.add_node("DiagnosisAssistance", diagnosis_assistance)

'''# Workflow transitions
workflow.set_entry_point(patient_scheduling)
workflow.add_edge("PatientScheduling", "ResourceAllocation")
workflow.add_conditional_edges(condition=lambda state: "Appointment" not in state["messages"][-1])
workflow.add_edge("ResourceAllocation", "DiagnosisAssistance", cond=lambda state: "Resources available" in state["messages"][-1])
workflow.add_edge("DiagnosisAssistance", END)'''

# Workflow transitions
workflow.set_entry_point("PatientScheduling")
workflow.add_edge("PatientScheduling", "ResourceAllocation")
workflow.add_edge("ResourceAllocation", "DiagnosisAssistance")
workflow.add_edge("DiagnosisAssistance", END)
workflow.add_conditional_edges(
    "PatientScheduling",
    decide_to_finish,
    {
        "ResourceAllocation": "ResourceAllocation",
        "DiagnosisAssistance": "DiagnosisAssistance"
    }

)
if __name__ == "__main__":
    # Compile and run
    app = workflow.compile()

    # Input data
    initial_state = {
        "messages": [{"content": "Schedule a patient"}],
        "patient_data": {"name": "John Doe", "department": "Radiology", "history": "Chronic headaches"},
        "appointment_status": None,
    }

    # Create a HumanMessage from the initial state
    # Convert initial_state to string
    initial_message = HumanMessage(content="schedule a patient")

    # Invoke the workflow
    response = app.invoke({"messages": initial_state['messages'],
                           "patient_data": initial_state['patient_data'],
                           "appointment_status": initial_state['appointment_status']
                           })
    # response = app.invoke({"messages": [{"content": "Schedule a patient"}]})
    for message in response["messages"]:
        print(message)
