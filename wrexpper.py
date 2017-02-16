import sys
import subprocess
import time

print("wrexpper --- the wrexp wrapper")


commands = []
servers = dict()

def check_commands():
    command_file = sys.argv[1]
    print("Reading commands from " + command_file)
    with open(command_file, 'r') as cf:
        for command in cf:
            commands.append(command.rstrip())
    print(str(len(commands)) + " commands found")
    with open(command_file, 'w'): pass

def check_servers():
    for server in sys.argv[2:]:
        (server, amount) = server.split(':')
        servers[server] = int(amount)
    print("Initialising " + str(len(servers)) + " servers:")
    print("slots\thost")
    for server in servers:
        print(str(servers.get(server, 0)) + "\t" + server)

def deploy_commands():
    for server in servers:
        s = subprocess.check_output(["wrexp", "ps", server], universal_newlines=True)
        nr_tasks = int((len(s.split("\n"))-2)/2)
        print(server + " [" + str(nr_tasks) + "/" + str(servers.get(server,0)) + "]")
        if commands and nr_tasks < servers.get(server, 0):
            new_task = commands.pop()
            #print("\tDeploying " + new_task)
            remote_task = ("ssh " + server + " nohup " + new_task + " &").split(" ")
            print("\tDeploying " + str(remote_task))
            subprocess.Popen(remote_task)
            print("\t" + str(len(commands)) + "tasks remaining")

minutes_passed = 0
check_servers()
while True:
    if minutes_passed % 5 == 0:
        check_commands() # every 5 min
    deploy_commands()    # every minute
    
    if not commands:
        break
    
    time.sleep(60)
    minutes_passed += 1

