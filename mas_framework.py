from queue import Queue
from threading import Thread
from db import add_patient, fetch_patient, setup_database

# Define a base agent class


class Agent(Thread):
    def __init__(self, name, inbox):
        super().__init__()
        self.name = name
        self.inbox = inbox

    def send_message(self, recipient_inbox, message):
        recipient_inbox.put((self.name, message))

    def run(self):
        while True:
            sender, message = self.inbox.get()
            if message == "STOP":
                break
            self.handle_message(sender, message)

    def handle_message(self, sender, message):
        pass

# Patient Scheduling Agent


class SchedulingAgent(Agent):
    def __init__(self, inbox):
        super().__init__("Scheduler", inbox)

    def handle_message(self, sender, message):
        if message["type"] == "schedule":
            print(f"{self.name}: Scheduling appointment for {
                  message['data']['name']}.")
            add_patient(**message['data'])
        elif message["type"] == "fetch":
            patient = fetch_patient(
                message['data']['name'], message['data']['dob'])
            print(f"{self.name}: Retrieved patient record: {patient}.")

# Diagnosis Assistance Agent


class DiagnosisAgent(Agent):
    def __init__(self, inbox):
        super().__init__("Diagnosis", inbox)

    def handle_message(self, sender, message):
        print(f"{self.name}: Assisting with diagnosis for {message}.")

# Resource Allocation Agent


class ResourceAgent(Agent):
    def __init__(self, inbox):
        super().__init__("ResourceAllocator", inbox)

    def handle_message(self, sender, message):
        print(f"{self.name}: Allocating resources for {message}.")


if __name__ == "__main__":
    setup_database()

    # Create inboxes
    scheduler_inbox = Queue()
    diagnosis_inbox = Queue()
    resource_inbox = Queue()

    # Create agents
    scheduler = SchedulingAgent(scheduler_inbox)
    diagnosis = DiagnosisAgent(diagnosis_inbox)
    resource_allocator = ResourceAgent(resource_inbox)

    # Start agents
    scheduler.start()
    diagnosis.start()
    resource_allocator.start()
    while True:
        choice = int(input(
            "Enter 1 for new patient \n Enter 2 for old patient \n Enter 3 for exiting the code \n"))
        if choice == 1:
            name2, dob2, medical_history, contact = [
                i for i in input("enter new patient details(name , dob ,medical history, contact): ").split(",")]
            # Simulate messages
            scheduler.send_message(scheduler_inbox, {
                "type": "schedule",
                "data": {
                    "name": name2,
                    "dob": dob2,
                    "medical_history": medical_history,
                    "contact": contact
                }
            })
        if choice == 2:
            name1, dob1 = [i for i in input(
                "retreiving patient details(name , dob): ").split(",")]
            scheduler.send_message(scheduler_inbox, {
                "type": "fetch",
                "data": {
                    "name": name1,
                    "dob": dob1
                }
            })
        if choice == 3:
            print("Quitting the program")
            break

    # Stop agents
    scheduler.send_message(scheduler_inbox, "STOP")
    diagnosis.send_message(diagnosis_inbox, "STOP")
    resource_allocator.send_message(resource_inbox, "STOP")
