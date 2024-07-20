#!/usr/bin/env python3
import ipaddress, socket, struct, random, asyncio
from etimedecorator import elapsedTimeDecorator, elapsedTimeAverageDecorator, elapsedTimePercentileDecorator

async def example_async():
    tasks = [ async_ipaddress_int2ip(random.randrange(16777216, 3758096383))
        for _ in range(4000)
    ]
    results = await asyncio.gather(*tasks)

    tasks = [ async_struct_int2ip(random.randrange(16777216, 3758096383))
        for _ in range(4000)
    ]
    results = await asyncio.gather(*tasks)

@elapsedTimeAverageDecorator(window_size=1000)
async def async_ipaddress_int2ip(iplong)->str:
    return str(ipaddress.ip_address(iplong))

@elapsedTimePercentileDecorator(window_size=1000)
async def async_struct_int2ip(iplong)->str:
    return socket.inet_ntoa(struct.pack('>L', iplong))

@elapsedTimeDecorator
def roots_int2ip(iplong):
    return f"{(iplong >> 24) & 0xFF}.{(iplong >> 16) & 0xFF}.{(iplong >> 8) & 0xFF}.{iplong & 0xFF}"

@elapsedTimeAverageDecorator(window_size=1000)
def ipaddress_int2ip(iplong)->str:
    return str(ipaddress.ip_address(iplong))

@elapsedTimePercentileDecorator(window_size=1000)
def struct_int2ip(iplong)->str:
    return socket.inet_ntoa(struct.pack('>L', iplong))

##──── Using the roots method 
ip = roots_int2ip(random.randrange(16777216,3758096383))
ip = roots_int2ip(random.randrange(16777216,3758096383))
ip = roots_int2ip(random.randrange(16777216,3758096383))
ip = roots_int2ip(random.randrange(16777216,3758096383))

print("- "*40)

##──── Using ipaddress library 
for I in range(4000):
    ip = ipaddress_int2ip(random.randrange(16777216,3758096383)) # from 1.0.0.0 to 223.255.255.255
    
##──── Using socket-struct libraries
for I in range(4000):
    ip = struct_int2ip(random.randrange(16777216,3758096383)) # from 1.0.0.0 to 223.255.255.255

print("- "*40)

asyncio.run(example_async())
