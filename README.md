# eTimeDecorator v1.0.0 (Elapsed Time Decorator)

eTimeDecorator is a set of 3 decorators for Python 3.x and PyPy3 to measure the execution time of a function that records the minimum, average and maximum elapsed time of functions that execute hundreds/thousands of times per second. It also works with asyncio.

![](https://raw.githubusercontent.com/rabuchaim/etimedecorator/main/example.png)

## Installation

```
pip install etimedecorator
```

## Decorators

- **`@elapsedTimeDecorator`**: It is a very simple decorator and displays the execution time of the decorated function. It is not suitable for functions that are called hundreds or thousands of times per second.
    - Output: *Elapsed Time for method_name(): 0.000001228 sec*

- **`@elapsedTimeAverageDecorator(window_size:int=1000,decimal_places:int=9)`**:

    This decorator is already suitable for reentrant functions with thousands of executions per second. Accepts the 'window_size' parameters that indicate after how many executions the minimum, average and maximum execution time statistics will be displayed. You can also define the number of decimal places to be displayed in statistics using the 'decimal_places' parameter, by default the number of decimal places is 9.

    - Output: *Elapsed Time for method_name() - 1000 calls - Min:0.000000454 / Avg:0.000000597 / Max:0.000038203*

- **`@elapsedTimePercentileDecorator(window_size:int=1000,decimal_places:int=9)`**

    This decorator is also suitable for reentrant functions with thousands of executions per second but displays the percentile calculation of the functions' execution time. Accepts the 'window_size' parameters that indicate after how many executions the minimum, average and maximum execution time statistics will be displayed. You can also define the number of decimal places to be displayed in statistics using the 'decimal_places' parameter, by default the number of decimal places is 9. *Because percentile calculation requires an ordered list of execution times, this method is slightly slower than the @elapsedTimeAverageDecorator method.*

    - Output: *Elapsed Time for method_name() 1000 calls - Min:0.000000517 Avg:0.000000750 Max:0.000022660 - 50%:0.000000624 75%:0.000000688 90%:0.000001000 99%:0.000002410*


## Usage example

Let's imagine an application that converts integers to IP addresses. If you are considering sporadic executions, you can use any of these functions, but if they are executed hundreds or thousands of times per second, you need to evaluate which of these functions performs best.

Here we have 3 ways to do this and we will measure which of these 3 ways performs better in our example. We will use the 'ipaddress' library and another function that uses 'socket' and 'struct', and a *roots* function do this calc. Let's run each of them 4000 times and evaluate performance after every 1000 runs using randomic numbers without cache. It will also be executed another 8000 times with asyncio.

We will only read the returned value and will not print anything on the screen. 

```python
import ipaddress, socket, struct, random, asyncio
from etimedecorator import elapsedTimeDecorator, elapsedTimeAverageDecorator, elapsedTimePercentileDecorator

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

##──── Now use ipaddress and socket-struct with ASYNCIO 
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

asyncio.run(example_async())

```
Output:
```bash
Elapsed Time for roots_int2ip(): 0.000003090 sec
Elapsed Time for roots_int2ip(): 0.000002067 sec
Elapsed Time for roots_int2ip(): 0.000000862 sec
Elapsed Time for roots_int2ip(): 0.000000771 sec
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Elapsed Time for ipaddress_int2ip() - 1000 calls - Min:0.000000967 / Avg:0.000001179 / Max:0.000025965
Elapsed Time for ipaddress_int2ip() - 1000 calls - Min:0.000000967 / Avg:0.000001758 / Max:0.000150562
Elapsed Time for ipaddress_int2ip() - 1000 calls - Min:0.000000963 / Avg:0.000001299 / Max:0.000150562
Elapsed Time for ipaddress_int2ip() - 1000 calls - Min:0.000000935 / Avg:0.000001079 / Max:0.000150562
Elapsed Time for struct_int2ip() 1000 calls - Min:0.000000413 Avg:0.000000514 Max:0.000041898 - 50%:0.000000451 75%:0.000000462 90%:0.000000474 99%:0.000000826
Elapsed Time for struct_int2ip() 1000 calls - Min:0.000000410 Avg:0.000000444 Max:0.000041898 - 50%:0.000000432 75%:0.000000441 90%:0.000000450 99%:0.000000505
Elapsed Time for struct_int2ip() 1000 calls - Min:0.000000410 Avg:0.000000513 Max:0.000041898 - 50%:0.000000500 75%:0.000000510 90%:0.000000521 99%:0.000000591
Elapsed Time for struct_int2ip() 1000 calls - Min:0.000000410 Avg:0.000000532 Max:0.000041898 - 50%:0.000000501 75%:0.000000526 90%:0.000000548 99%:0.000000928
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Elapsed Time for async_ipaddress_int2ip() - 1000 calls - Min:0.000000135 / Avg:0.000000354 / Max:0.000017034
Elapsed Time for async_ipaddress_int2ip() - 1000 calls - Min:0.000000133 / Avg:0.000000283 / Max:0.000017034
Elapsed Time for async_ipaddress_int2ip() - 1000 calls - Min:0.000000133 / Avg:0.000000339 / Max:0.000017034
Elapsed Time for async_ipaddress_int2ip() - 1000 calls - Min:0.000000120 / Avg:0.000000350 / Max:0.000024730
Elapsed Time for async_struct_int2ip() 1000 calls - Min:0.000000132 Avg:0.000000179 Max:0.000007117 - 50%:0.000000168 75%:0.000000173 90%:0.000000177 99%:0.000000210
Elapsed Time for async_struct_int2ip() 1000 calls - Min:0.000000132 Avg:0.000000231 Max:0.000011292 - 50%:0.000000170 75%:0.000000178 90%:0.000000186 99%:0.000001282
Elapsed Time for async_struct_int2ip() 1000 calls - Min:0.000000132 Avg:0.000000291 Max:0.000011292 - 50%:0.000000187 75%:0.000000194 90%:0.000000205 99%:0.000001917
Elapsed Time for async_struct_int2ip() 1000 calls - Min:0.000000132 Avg:0.000000456 Max:0.000015390 - 50%:0.000000277 75%:0.000000288 90%:0.000000463 99%:0.000004349
```
The percentile indicated in the fields 50%, 75%, 90% and 99% means that 50% of executions are below the indicated value, in the other field it indicates that 75% of executions are below the indicated value, and so on.

As we can see, the function struct_int2ip() is faster than the ipaddress_int2ip() and roots_int2ip() function. All of this was measured without having to place codes and make calculations in the middle of the function code. When putting it into production, just comment or delete the decorator call.

And in the last 8000 executions, we can see that with asyncio the average elapsed time was much better than synchronously, and we can also see that the two functions async_ipaddress_int2ip() and async_struct_int2ip() obtained practically the same performance.

This decorator uses the time.monotonic() function which is not impacted by machine time changes.

## Sugestions, feedbacks, bugs...

E-mail me: ricardoabuchaim at gmail.com
