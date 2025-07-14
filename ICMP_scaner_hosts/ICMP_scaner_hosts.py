import argparse # Библиотека аргуменнтов командной строки
from icmplib import async_multiping #  Библиотека с работой ICMP ping-зпросами
import asyncio # Библиотека асинхронности

# Арггументы
parser = argparse.ArgumentParser()
parser.add_argument("--hosts", "-i", type=str, required=True, help="IP или диапазон (192.168.1.1, 192.168.1.1-100 или 192.168.1.0/24)")
args = parser.parse_args()

# Генерация списка IP из диапазона или одиночного адреса
def generate_hosts(hosts_arg):
    # Если формат 192.168.1.1-100
    if '-' in hosts_arg: 
        base_ip, range_part = hosts_arg.rsplit('.', 1)
        start, end = map(int, range_part.split('-'))
        return [f"{base_ip}.{i}" for i in range(start, end + 1)]
    ## 
    # Если 24 маска
    elif '/24' in hosts_arg:
        base = hosts_arg.replace('/24', '').rstrip('0')
        return [f"{base}{i}" for i in range(1, 255)]
    # Если 16 маска
    elif '/16' in hosts_arg:
        base = hosts_arg.replace('/16', '').rstrip('0')
        return [f"{base}{x}.{y}" for x in range(256) for y in range(1, 255)]
    # Если одиночный IP
    else:
        return [hosts_arg]
    
hosts = generate_hosts(args.hosts)
##################################################################################
# Асинхронное сканироване методом ICMP Ping Sweep
##Отправка Echo Request -> Ты живой?
##Ожидане ответа Echo Reply -> Да живой!
async def icmp_scan_hosts(hosts):
    results = await async_multiping(hosts)
    live_hosts = [host.address for host in results if host.is_alive]
    print(f"Колиество активных хостов (ICMP Ping Sweep):{len(live_hosts)}")
    for ip in live_hosts:
        print(ip)

# Запускаем сканирование
asyncio.run(icmp_scan_hosts(hosts))
####################################################################################
