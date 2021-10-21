from dns.resolver import query
from mcstatus import MinecraftServer


def testNgrokPort(sub, port) -> bool:
    print(f'Now testing: {sub}, {port}')
    try: 
        server = MinecraftServer.lookup(f"{sub}.tcp.ngrok.io:{port}")
        status = server.status(1)
        hitlist = open("hitlist", "a")
        print("hit")
        try:
            query = server.query(1)
            hitlist.write(f'--- New Query Hit ----------------------------------\n')
            hitlist.write(f'Branch: {sub}, Port: {port}, Version: {query.software.version}, Ping: {status.latency}\n')
            try:
                  hitlist.write(f'Motd: {query.motd}\n')
            except:
                  hitlist.write(f'Motd: ~~~~CONTAINS UNICODE, CAN NOT DISPLAY~~~~\n')
            hitlist.write(f'Plugins: {query.software.plugins}\n')
            hitlist.write(f'Players: {query.players.online}/{query.players.max}\n')
            for name in query.players.names:
                hitlist.write(f'{name}\n')
            hitlist.write(f'----------------------------------------------------\n')
        except:
            hitlist.write(f'--- New Status Hit ---------------------------------\n')
            hitlist.write(f'Branch: {sub}, Port: {port}, Version: {status.version.name}, Ping: {status.latency}\n')
            try:
                hitlist.write(f'Motd: {status.description}\n')
            except:
                hitlist.write(f'Motd: ~~~~CONTAINS UNICODE, CAN NOT DISPLAY~~~~\n')
            hitlist.write(f'Players: {status.players.online}/{status.players.max}\n')
            hitlist.write(f'----------------------------------------------------\n')
        hitlist.close()
    except:
        return False
    return True


subnets = [2, 4, 6, 8, 0]

#The Test - Set True to run
if True:
    for sub in subnets:
        for port in range(10000, 20000):
            testNgrokPort(sub, port)
    print("Completed Scans")