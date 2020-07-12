import os
import time
import random
import json
import multiprocessing as mp
from multiprocessing.pool import Pool
import socket
import logging
logging.basicConfig(level=logging.INFO)


def scan_ip_range(max_processes, ip_range, result_queue):
    q = mp.Queue(100)
    flag = mp.Value('i', 0)

    def put_queue(queue: mp.Queue, ip_range):
        start_ip, end_ip = ip_range.split('-')
        ip_stage_list = start_ip.split('.')[:3]
        for i in range(int(start_ip.split('.')[3]), int(end_ip.split('.')[3])):
            ip_addr = ".".join(ip_stage_list + [str(i)])
            if queue.full():
                logging.debug('Queue is full, sleeping 1 second...')
                time.sleep(1) 
            else:
                logging.debug(f'{ip_addr} has been putted into the Queue')
                queue.put(ip_addr)
        flag = 1
        logging.debug(f'put_queue completed, flag is now {flag}')

    def process_ping(queue: mp.Queue):
        logging.debug(f'Process {os.getpid()} started processing...')
        while True:
            if queue.empty() and flag:
                logging.debug(f'Queue is empty, process {os.getpid()} is exiting...')
                break
            elif queue.empty() and flag==0:
                logging.debug(f'Queue is empty currently, process {os.getpid()} will wait 1 seconds to retrieve data...')
                time.sleep(1)
            else:
                ip_addr = queue.get()
                logging.debug(f'Process {os.getpid()} is processing {ip_addr}......')
                result = os.popen(f'ping {ip_addr} -c 3').read()
                if result.find('3 packets transmitted, 3 received, 0% packet loss') >= 0:
                    result_queue.put(ip_addr)
                    logging.info(f'{ip_addr} is pingable!')

    p = mp.Process(target=put_queue, args=(q, ip_range))
    p.start()

    ping_process = None
    for c in range(max_processes):
        ping_process = mp.Process(target=process_ping, args=(q, ))
        time.sleep(random.randint(1, 2))
        ping_process.start()
    ping_process.join()

def scan_ports(max_processes, ip_addr, result_queue):

    def scan_ports(queue: mp.Queue, ip_addr, step, available_ports):
        logging.debug(f'Process {os.getpid()} started processing...')
        while True:
            if queue.empty():
                logging.debug(f'Queue is empty, process {os.getpid()} is exiting...')
                break
            else:
                start_port = queue.get()
                logging.debug(f'Process {os.getpid()} is processing {start_port} ~ {start_port+step}......')
                for p in range(start_port, start_port+step):
                    try:
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                            s.connect((ip_addr, p))
                            logging.info(f'Port {p} is available')
                            available_ports.put(p)
                    except Exception:
                        logging.debug(f'Port {p} cannot be connected')


    step = 1000
    q = mp.Queue(700)
    for i in range(1, 65536, step):
        q.put(i)
    
    available_ports = result_queue

    scan_process = None
    for _ in range(max_processes):
        scan_process = mp.Process(target=scan_ports, args=(q, ip_addr, step, available_ports))
        time.sleep(random.randint(1, 2))
        scan_process.start()
    
    scan_process.join()


if __name__ == '__main__':
    logging.debug('父进程开始')
    parent_start_time = time.time()
    cpu_count = mp.cpu_count()
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--num', type=int, default=cpu_count, help='指定并发数量')
    parser.add_argument('-f', '--fangfa', choices=['ping', 'tcp'], required=True, help='指定进行 ping 测试或进行 tcp 端口扫描')
    parser.add_argument('-ip', '--ipaddr', required=True, help='连续 IP 地址支持 192.168.0.1-192.168.0.100 写法')
    parser.add_argument('-v', '--verbose', action='count', default=0, help='打印程序执行时间')
    parser.add_argument('-w', '--write', default=None, help='扫描结果进行保存')
    args = parser.parse_args()


    result_queue = mp.Queue(100)

    if args.fangfa == 'ping':
        scan_ip_range(args.num, args.ipaddr, result_queue)
    else:
        scan_ports(args.num, args.ipaddr, result_queue)
    
    result_list = []
    
    while True:
        if result_queue.empty():
            break
        else:
            result_list.append(result_queue.get())
    
    if args.write:
        with open(args.write, 'w') as f:
            json.dump(result_list, f)
            logging.info(f'result has been written to {args.write} successfully')
            

    logging.debug('父进程结束！')
    parent_end_time = time.time()
    if args.verbose:
        logging.info(f'程序运行时长为{parent_end_time-parent_start_time}秒')