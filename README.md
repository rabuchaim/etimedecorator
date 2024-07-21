# eTimeDecorator v1.0.1 (Elapsed Time Decorator)

eTimeDecorator is a set of 3 elapsed timer decorators for Python 3.x and PyPy3 to measure the execution time of a function that executes hundreds/thousands of times per second. It also works with asyncio. Records the minimum, average and maximum elapsed time of functions and calculates the percentile.

![](https://raw.githubusercontent.com/rabuchaim/etimedecorator/main/example.png)

## Installation

```
pip install etimedecorator
```

## Decorators

- **`@elapsedTimeDecorator(decimal_places:int=9,print_args:bool=False)`**: 

    It is a very simple decorator and displays the execution time of the decorated function. **It is not suitable** for functions that are called hundreds or thousands of times per second. You can also define the number of decimal places to be displayed in statistics using the `decimal_places` parameter, by default the number of decimal places is 9. And the `print_args` parameter prints the arguments (*args and **kwargs) passed to the function.
    
    - Output: *Elapsed Time for method_name(): 0.000001228 sec*

- **`@elapsedTimeAverageDecorator(window_size:int=1000,decimal_places:int=9,print_args:bool=False)`**:

    This decorator is already suitable for reentrant functions with thousands of executions per second. Accepts the `window_size` parameters that indicate after how many executions the minimum, average and maximum execution time statistics will be displayed. You can also define the number of decimal places to be displayed in statistics using the `decimal_places` parameter, by default the number of decimal places is 9. And the `print_args` parameter prints the arguments (*args and **kwargs) passed to the function.

    - Output: *Elapsed Time for method_name() - 1000 calls - Min:0.000000454 / Avg:0.000000597 / Max:0.000038203*

- **`@elapsedTimePercentileDecorator(window_size:int=1000,decimal_places:int=9,print_args:bool=False)`**

    This decorator is also suitable for reentrant functions with thousands of executions per second but displays the percentile calculation of the functions' execution time. Accepts the `window_size` parameters that indicate after how many executions the minimum, average and maximum execution time statistics will be displayed. You can also define the number of decimal places to be displayed in statistics using the `decimal_places` parameter, by default the number of decimal places is 9 *Because percentile calculation requires an ordered list of execution times, this method is slightly slower than the @elapsedTimeAverageDecorator method.*. And the `print_args` parameter prints the arguments (*args and **kwargs) passed to the function. 

    - Output: *Elapsed Time for method_name() 1000 calls - Min:0.000000517 Avg:0.000000750 Max:0.000022660 - 50%:0.000000624 75%:0.000000688 90%:0.000001000 99%:0.000002410*


## Usage example

Let's imagine an application that converts integers to IP addresses. If you are considering sporadic executions, you can use any of these functions, but if they are executed hundreds or thousands of times per second, you need to evaluate which of these functions performs best.

Here we have 3 ways to do this and we will measure which of these 3 ways performs better in our example. We will use the 'ipaddress' library and another function that uses 'socket' and 'struct', and a *roots* function do this calc. Let's run each of them 4000 times and evaluate performance after every 1000 runs using randomic numbers without cache. It will also be executed another 8000 times with asyncio.

We will only read the returned value and will not print anything on the screen. 

```python
import ipaddress, socket, struct, random, asyncio
from etimedecorator import elapsedTimeDecorator, elapsedTimeAverageDecorator, elapsedTimePercentileDecorator

@elapsedTimeDecorator()
def roots_int2ip(iplong):
    return f"{(iplong >> 24) & 0xFF}.{(iplong >> 16) & 0xFF}.{(iplong >> 8) & 0xFF}.{iplong & 0xFF}"

@elapsedTimeAverageDecorator(window_size=1000,print_args=True) # Will print the 'iplong' value passed to the function as *args
def ipaddress_int2ip(iplong)->str:
    return str(ipaddress.ip_address(iplong))

@elapsedTimePercentileDecorator(window_size=1000,print_args=True) # Will print the 'iplong' value passed to the function as **kwargs
def struct_int2ip(iplong=iplong)->str:
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
Elapsed Time for roots_int2ip(): 0.000002739 sec
Elapsed Time for roots_int2ip(): 0.000002334 sec
Elapsed Time for roots_int2ip(): 0.000001023 sec
Elapsed Time for roots_int2ip(): 0.000006749 sec
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Elapsed Time for ipaddress_int2ip((3509596061,)) - 1000 calls - Min:0.000000920 / Avg:0.000001123 / Max:0.000011491
Elapsed Time for ipaddress_int2ip((3292303103,)) - 1000 calls - Min:0.000000920 / Avg:0.000001339 / Max:0.000016721
Elapsed Time for ipaddress_int2ip((1861348088,)) - 1000 calls - Min:0.000000905 / Avg:0.000001128 / Max:0.000031977
Elapsed Time for ipaddress_int2ip((1955570310,)) - 1000 calls - Min:0.000000905 / Avg:0.000001010 / Max:0.000031977
Elapsed Time for struct_int2ip({'iplong':3734307021}) 1000 calls - Min:0.000000543 Avg:0.000000724 Max:0.000041515 - 50%:0.000000603 75%:0.000000622 90%:0.000000647 99%:0.000001843
Elapsed Time for struct_int2ip({'iplong':1647016321}) 1000 calls - Min:0.000000499 Avg:0.000000649 Max:0.000041515 - 50%:0.000000560 75%:0.000000573 90%:0.000000603 99%:0.000001737
Elapsed Time for struct_int2ip({'iplong':2504612232}) 1000 calls - Min:0.000000472 Avg:0.000000582 Max:0.000041515 - 50%:0.000000562 75%:0.000000580 90%:0.000000601 99%:0.000000983
Elapsed Time for struct_int2ip({'iplong':2341449854}) 1000 calls - Min:0.000000472 Avg:0.000000604 Max:0.000041515 - 50%:0.000000533 75%:0.000000564 90%:0.000000818 99%:0.000001142
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Elapsed Time for async_ipaddress_int2ip() - 1000 calls - Min:0.000000123 / Avg:0.000000253 / Max:0.000012031
Elapsed Time for async_ipaddress_int2ip() - 1000 calls - Min:0.000000116 / Avg:0.000000211 / Max:0.000012031
Elapsed Time for async_ipaddress_int2ip() - 1000 calls - Min:0.000000116 / Avg:0.000000248 / Max:0.000012031
Elapsed Time for async_ipaddress_int2ip() - 1000 calls - Min:0.000000116 / Avg:0.000000223 / Max:0.000015060
Elapsed Time for async_struct_int2ip() 1000 calls - Min:0.000000133 Avg:0.000000225 Max:0.000009146 - 50%:0.000000165 75%:0.000000170 90%:0.000000187 99%:0.000001524
Elapsed Time for async_struct_int2ip() 1000 calls - Min:0.000000136 Avg:0.000000198 Max:0.000011554 - 50%:0.000000165 75%:0.000000170 90%:0.000000174 99%:0.000000497
Elapsed Time for async_struct_int2ip() 1000 calls - Min:0.000000136 Avg:0.000000250 Max:0.000014483 - 50%:0.000000162 75%:0.000000170 90%:0.000000175 99%:0.000001503
Elapsed Time for async_struct_int2ip() 1000 calls - Min:0.000000136 Avg:0.000000306 Max:0.000018371 - 50%:0.000000174 75%:0.000000178 90%:0.000000184 99%:0.000003273
```
The percentile indicated in the fields 50%, 75%, 90% and 99% means that 50% of executions are below the indicated value, in the other field it indicates that 75% of executions are below the indicated value, and so on.

As we can see, the function struct_int2ip() is faster than the ipaddress_int2ip() and roots_int2ip() function. All of this was measured without having to place codes and make calculations in the middle of the function code. When putting it into production, just comment or delete the decorator call.

And in the last 8000 executions, we can see that with asyncio the average elapsed time was much better than synchronously, and we can also see that the two functions async_ipaddress_int2ip() and async_struct_int2ip() obtained practically the same performance.

This decorator uses the time.monotonic() function which is not impacted by machine time changes.

## Sugestions, feedbacks, bugs...

E-mail me: ricardoabuchaim at gmail.com
