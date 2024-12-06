from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from typing import TypedDict


# Define the agent states
class AgentState(TypedDict):
    messages: list

# Patient Scheduling Agent


def patient_scheduling_agent(state, config):
    """schedules an appointment for the patient"""
    # Simulate appointment scheduling logic
    patient_name = state["messages"][-1]["content"]
    department = "radiology"  # For simplicity, hardcode a department
    return {
        "messages": [{"content": f"Scheduled appointment for {patient_name} in {department}"}]
    }

# Diagnosis Assistance Agent


def diagnosis_assistance_agent(state, config):
    """provides diagnosis assistance for the patient"""
    # Simulate diagnosis assistance based on patient history
    patient_name = state["messages"][-1]["content"]
    diagnosis = f"Diagnosis assistance for {
        patient_name} based on medical history"
    return {
        "messages": [{"content": diagnosis}]
    }

# Resource Allocation Agent


def resource_allocation_agent(state, config):
    """allocates resources to the patient"""
    # Simulate checking if resources are available
    department = "radiology"  # Hardcoded department
    resource_available = True  # Simulating resource availability
    if resource_available:
        return {
            "messages": [{"content": f"Resource available for {department} department"}]
        }
    else:
        return {
            "messages": [{"content": "No resources available"}]
        }

# Define a conditional edge selector function


def continue_selector(state: AgentState):
    # This function returns the name of the next node based on conditions
    # For now, it always returns 'resource_allocation' to simulate 'continue'
    return "resource_allocation"


# Define conditional edges
conditional_edge_selector = ConditionalEdgeSelector(
    source="patient_scheduling",  # Source node
    selector_fn=continue_selector,  # Selector function
    edges={
        "resource_allocation": "resource_allocation",  # Target node for 'continue'
    }
)

# Initialize agents and workflows
patient_scheduling_node = ToolNode(
    [patient_scheduling_agent])  # Wrap in a list
diagnosis_assistance_node = ToolNode(
    [diagnosis_assistance_agent])  # Wrap in a list
resource_allocation_node = ToolNode([resource_allocation_agent])
# Build the state graph workflow
workflow = StateGraph(AgentState)
workflow.add_node("patient_scheduling", patient_scheduling_node)
workflow.add_node("diagnosis_assistance", diagnosis_assistance_node)
workflow.add_node("resource_allocation", resource_allocation_node)

# Define edges for communication between agents
'''workflow.add_edge("patient_scheduling", "resource_allocation", continue_condition="continue")
workflow.add_edge("resource_allocation", "diagnosis_assistance", continue_condition="continue")'''
workflow.add_conditional_edge_selector(conditional_edge_selector)
workflow.add_conditional_edge_selector(conditional_edge_selector)

# Compile and run the workflow
app = workflow.compile()

# Simulate an initial patient scheduling request
patient_name = "John Doe"
response = app.invoke({"messages": [{"content": patient_name}]})

# Print the response from the workflow
print(response["messages"][-1]["content"])
