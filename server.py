import socket
import time
import threading
import heapq
import numpy as np
# === Configuration ===
SERVER_PORT = 4000
CLIENT_PORTS = [5001, 5002, 5003]
FLOW_WEIGHTS = {5001: 1, 5002: 2, 5003: 4}  # Example weights
CAPACITY = 20  # packets per second
BUFFER_SIZE = 100  # max number of packets in queue

# === Data Structures ===
packet_queue = []  # Min-heap sorted by VFT
queue_lock = threading.Lock()
virtual_time_lock = threading.Lock()
last_last_vft = {port: [] for port in CLIENT_PORTS}
last_vft = {port: 0 for port in CLIENT_PORTS}
virtual_time = 0

# === Socket Setup ===
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("127.0.0.1", SERVER_PORT))

def compute_vft(flow_id):
    weight = FLOW_WEIGHTS[flow_id]
    with virtual_time_lock:
        base = max(virtual_time, last_vft[flow_id])
    vft = base + 1 / (CAPACITY * weight)
    last_last_vft[flow_id].append(last_vft[flow_id])
    last_vft[flow_id] = vft


    return vft


def receiver():
    global virtual_time
    global packet_queue
    while True:
        data, addr = sock.recvfrom(1024)
        arrival_time = time.time()
        flow_id = addr[1]

        if flow_id not in FLOW_WEIGHTS:
            continue  # Unknown flow

        vft = compute_vft(flow_id)

        with queue_lock:
            #if packet_queue:
            #print('r',packet_queue)
            if len(packet_queue) >= BUFFER_SIZE:
                # DropTail: Remove packet with highest VFT if it's larger than new packet's
                packet_queue.sort(key=lambda x: x[0])
                if packet_queue[-1][0] > vft:
                    #packet_queue.pop()
                    vft_r, arrival_time_r, data_r, addr_r = packet_queue.pop()
                    # print(f"dropped {addr_r[1]}: {data_r.decode()}")
                    # print(len(packet_queue),vft_r,vft,addr[1])
                    last_vft[addr_r[1]]=last_last_vft[addr_r[1]].pop()
                    #print(packet_queue)
                    heapq.heapify(packet_queue)
                    heapq.heappush(packet_queue, (vft, arrival_time, data, addr))
                    if len(packet_queue) == 0:
                        with virtual_time_lock:
                            virtual_time = max(virtual_time,arrival_time)  # safely update virtual time

                # else: drop the incoming packet silently
                else:
                    # print(f"dropped {addr[1]}: {data.decode()}")
                    # print(len(packet_queue),vft,packet_queue[-1][0],packet_queue[-1][3][1],packet_queue[-1][2].decode())
                    last_vft[flow_id]=last_last_vft[flow_id].pop()
            else:
                # if packet_queue:
                #     print(packet_queue)
                heapq.heappush(packet_queue, (vft, arrival_time, data, addr))
                if len(packet_queue) == 0:
                    with virtual_time_lock:
                        virtual_time = max(arrival_time,virtual_time)  # safely update virtual time

                #print(len(packet_queue))

def server():
    global virtual_time
    start_time = 0
    while True:
        with queue_lock:
            if packet_queue:
                #print('s',packet_queue)
                vft, arrival_time, data, addr = heapq.heappop(packet_queue)
                with virtual_time_lock:
                    virtual_time = max(virtual_time, vft)
                
            else:
                continue  # No packets to serve
            
            
        sock.sendto(data, addr)
        print(f"Echoed to {addr[1]}: {data.decode()}")
        elapsed = time.perf_counter() - start_time
        print(elapsed)
        start_time = time.perf_counter()
        interval = max(1/CAPACITY, 0)  # 100 ms
        start = time.perf_counter()
        # Sleep for most of the interval
        time.sleep(interval - 0.005)  # Sleep for 995 ms
        # Busy-wait for the last ~5 ms
        #for accuracy
        while (time.perf_counter() - start) < interval:
            pass
        
        

def main():
    print("WFQ Server started...")
    threading.Thread(target=receiver, daemon=True).start()
    threading.Thread(target=server, daemon=True).start()
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
