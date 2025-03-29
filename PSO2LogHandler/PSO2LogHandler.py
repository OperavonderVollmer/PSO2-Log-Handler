from OperaPowerRelay import opr
from LogFileMonitor import LogFileMonitor as lfm
from OPRSpeaks import OPRSpeaks as ops, OPRSpeaksModels as opsm
from typing import Iterator
import queue
import os
import traceback
import time
import threading

def initialize() -> None:    
    opr.print_from("PSO2 Log Handler - Initialize", "Starting PSO2 Log Handler...", 1)
    lfm.initialize(os.path.abspath(__file__))
    ops.initialize(filepath=os.path.abspath(__file__))

def deinitialize() -> None:
    os.system('cls')
    opr.print_from("PSO2 Log Handler - Deinitialize", "Stopping PSO2 Log Handler...")
    lfm.deinitialize()
    ops.deinitialize()


def get_output_queue() -> Iterator[str]:
    while True:  
        try:
            yield lfm.OUTPUT_QUEUE.get(timeout=1) 
        except queue.Empty:
            continue
        except Exception as e:
            error_message = traceback.format_exc()
            opr.print_from("OPR-Speaks - Main", f"FAILED: Unexpected Error: {error_message}")
            break


def filter_users(user: str) -> bool:
    if user in BLACKLIST_USERS:
        return False
    return True

def filter_context(context: str) -> bool:
    if context in BLACKLIST_CONTEXT:
        return False  
    return True  

def filter_id(id_: str) -> bool:
    if id_ in BLACKLIST_ID:
        return False
    return True

def process_logs(line: str, verbose: bool = False) -> str:
    
    """
    Process a single log line and return the processed message if any.

    Args:
        line (str): The log line to process.
        verbose (bool, optional): Whether to print the log line details. Defaults to False.

    Returns:
        str: The processed message if any, otherwise None.
    """
    global CURRENT_CONTEXT

    log_string = line[0].split('\t')
    
    date, msg_id, context, sender_id, sender, msg = log_string

    if verbose:
        print(f"Date: {date} | ID: {sender_id} | Context: {context} | Msg ID: {msg_id} | Sender: {sender} | Msg: {msg}")

    if not filter_context(context.strip()) or not filter_id(sender_id.strip()) or not filter_users(sender.strip()):
        opr.print_from("PSO2 Log Handler - Main", f"Filtered Message: {msg}", 1)
        return


    message = f"{sender} "

    if CURRENT_CONTEXT != context:
        CURRENT_CONTEXT = context
        message += f"from {context} chat "

    message += f"says {msg}"

    opr.print_from("PSO2 Log Handler - Main", f"Processed Message: {message}")
    return message


def speak_thread(TTS: opsm.TTS_Model) -> None:

    if not DEBUG_MODE:
        os.system('cls')

    opr.print_from("PSO2 Log Handler - Speak Thread", "Starting to monitor Log File Monitor Outputs")
    retry_count = 0

    opr.print_from("PSO2 Log Handler - Speak Thread", "Now monitoring (Ctrl+C to exit)...")
    while True:
        try:
            for line in get_output_queue():

                processed = process_logs(line)

                if processed:
                    TTS.Say(processed)

        except KeyboardInterrupt:
            break

        except Exception as e:
            error_message = traceback.format_exc()
            opr.print_from("PSO2 Log Handler - Main", f"FAILED: Unexpected Error: {error_message}")
            
            retry_count += 1
            if retry_count >= 5:
                opr.print_from("PSO2 Log Handler - Main", "FAILED: Max retries reached. Exiting...")
                break

            opr.print_from("PSO2 Log Handler - Main", f"Retrying in 5 seconds... ({retry_count}/5)")
            time.sleep(5)

def quickstart_lfm() -> None:

    """
    Starts the quickstart wizard for Log File Monitor.
    This function starts the quickstart wizard for Log File Monitor, which allows the user to quickly create a new monitor. 
    The user is prompted to select a path from the list of saved paths, and then to enter the monitor name,and encoding. 
    The wizard then adds the monitor to the list of quickstart monitors and saves it to the quickstart.json file. 
    If the user chooses not to add the monitor, the wizard will exit. 
    If the user chooses to add the monitor, the wizard will add it to the list of quickstart monitors and save it to the quickstart.json file.

    Parameters
    ----------

    None

    Returns
    -------

    None
    """

    if not DEBUG_MODE:
        os.system('cls')

    opr.print_from("PSO2 Log Handler - Quickstart", "Quickstart Log File Monitor...")

    quickstart = opr.load_json("PSO2 Log Handler - Quickstart", os.path.dirname(os.path.abspath(__file__)), "quickstart.json")

    while True:
        decision = opr.input_from("PSO2 Log Handler - Quickstart", f"\nThere are {len(quickstart)} quickstart monitors configured. \n\nWould you like to create a quickstart? (y/n)")
        if decision.lower() == "y":
            while True:
                name = opr.input_from("PSO2 Log Handler - Quickstart Wizard | Add", "Monitor Name")
                
                opr.print_from("PSO2 Log Handler - Quickstart Wizard | Add", "Select a path", 1)

                PATHS = lfm.PATHS

                for i, path in enumerate(PATHS.keys(), 1):
                    opr.print_from("PSO2 Log Handler - Quickstart Wizard | Add", f"[{i}]: {path}")
                
                while True:        
                    choice = opr.input_from("PSO2 Log Handler - Quickstart Wizard | Add", f"Select a path (1-{len(PATHS)})")
                    if choice.isdigit() and int(choice) in range(1, len(PATHS) + 1):
                        break
                    opr.print_from("PSO2 Log Handler - Quickstart Wizard | Add","Invalid selection. Please enter a valid number.")


                path = list(PATHS.keys())[int(choice) - 1] 

                while True:
                    en_choice = opr.input_from("LogFileMonitor - Wizard | Add", f"Please select an encoding: [1] UTF-8 | [2] UTF-16 | [3] UTF-32")
                    if en_choice in ["1", "2", "3"]:
                        break
                    opr.print_from("LogFileMonitor - Wizard | Add", "Invalid input")

                encoding = ["utf-8", "utf-16", "utf-32"][int(en_choice) - 1]
                

                opr.print_from("PSO2 Log Handler - Quickstart Wizard | Add", f"Name: {name} | Path: {path} | Encoding: {encoding}")                

                decision = opr.input_from("PSO2 Log Handler - Quickstart Wizard | Add", "Is this correct? (y/n)")
                if decision.lower() == "y":            
                    quickstart[len(quickstart) + 1] = {"name": name, "path": path, "encoding": encoding}
                    opr.save_json("PSO2 Log Handler - Quickstart", os.path.dirname(os.path.abspath(__file__)), quickstart, "quickstart.json")    

        else:
            break

    
    if quickstart:
        for monitor in quickstart.values():
            opr.print_from("PSO2 Log Handler - Quickstart", f"Quickstart Monitor: {monitor['name']} | {monitor['path']} | {monitor['encoding']}", 1)
            decision = opr.input_from("PSO2 Log Handler - Quickstart", "Do you want to start this monitor? (y/n)")
            if decision.lower() == "y":
                lfm._add_monitor(mode="2", name=monitor["name"], path=monitor["path"], _encoding=monitor["encoding"])

CURRENT_CONTEXT = ""
BLACKLIST_CONTEXT = ["PUBLIC"]
BLACKLIST_USERS = []
BLACKLIST_ID = ["11618426"]
DEBUG_MODE = False


SPEAK_THREAD = None

if __name__ == "__main__":

    initialize()
    try:
        quickstart_lfm()
        
        TTS = opsm.TTS_Factory(ops.OUTPUT_DEVICE[0], "1")

        TTS.Start()

        SPEAK_THREAD = threading.Thread(target=speak_thread, daemon=True, args=(TTS,))
        SPEAK_THREAD.start()
        
        time.sleep(2)

        lfm.wizard_interface()

        TTS.Stop()

    except KeyboardInterrupt:
        pass
    except Exception as e:
        error_message = traceback.format_exc()
        opr.print_from("PSO2 Log Handler - Main", f"FAILED: Unexpected Error: {error_message}")
        
    deinitialize()