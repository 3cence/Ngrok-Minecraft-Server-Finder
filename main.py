from mcstatus import MinecraftServer
from threading import Thread
from openpyxl import workbook, worksheet
from openpyxl.reader.excel import load_workbook

def testNgrokPort(sub, port) -> bool:
    print(f'Now testing: {sub}, {port}')
    try: 
        server = MinecraftServer.lookup(f"{sub}.tcp.ngrok.io:{port}")
        status = server.status(1)
        print("Hit")
        wb = load_workbook(f'Subnets/{sub}.xlsx')
        ws = wb.active
        ws.append([sub, port, status.version.name, status.description, status.players.online, status.players.max])
        wb.save(f'Subnets/{sub}.xlsx')
        hitlist = open('hitlist', 'a')
        hitlist.write(f"New hit on Subnet {sub}, Port {port}\n")
        hitlist.close()
    except:
        return False
    return True


def testNgrokSubnet(subnet):
    for port in range(10000, 20000):
        testNgrokPort(subnet, port)



subnets = [0, 2, 4, 6, 8]
threads = []

for sub in subnets:
    threads.append(Thread(target=testNgrokSubnet, args=(sub,)))

for t in threads:
    t.start()

for t in threads:
    t.join()