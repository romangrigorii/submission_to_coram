import zmq
import time
from collections import Counter, deque

class_counter = Counter()
class_queue = deque()

time_horizon = 10
report_time_interval = 10

def time_report(time_horizon):
    time_lower_bond = time.time() - time_horizon
    for ii in list(class_queue):
        if (ii[0]<time_lower_bond):
            class_queue.popleft()
        else:
            break
    class_counter = dict(Counter([q[1] for q in class_queue]))
    print(f"In the last {time_horizon} the classifier identified: ")
    for q in class_counter:
        print(f"class {q} detected {class_counter[q]} times")
    
def main() -> None:
    # socket set up
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    server = "tcp://localhost:9876"
    socket.connect(server)
    print(f"Connected to clasifier server: {server}")
    print("Reporting image classification results:")
    # misc variables
    request_id = 0    
    ts = time.time()
    # run continuously
    while(1):
        socket.send_string("Classify latest image")
        message = socket.recv().__str__()
        if len(message)>0:
            #print(f"Classification result: {request_id} -> [ {message} ]")
            class_queue.append((int(time.time()), message))
        else:
            print(f"Request unsuccesful.")
        request_id+=1
        if (time.time() - ts) > report_time_interval:
            time_report(time_horizon)
            ts = time.time()
        #input("Press enter to classify latest image")

if __name__ == "__main__":
    main()




