#!/usr/bin/env python3
"""Elapsed Time Decorator v1.0.0"""
"""
     _____ _                ____                           _
  __|_   _(_)_ __ ___   ___|  _ \  ___  ___ ___  _ __ __ _| |_ ___  _ __
 / _ \| | | | '_ ` _ \ / _ \ | | |/ _ \/ __/ _ \| '__/ _` | __/ _ \| '__|
|  __/| | | | | | | | |  __/ |_| |  __/ (_| (_) | | | (_| | || (_) | |
 \___||_| |_|_| |_| |_|\___|____/ \___|\___\___/|_|  \__,_|\__\___/|_|

    Author.: Ricardo Abuchaim - ricardoabuchaim@gmail.com
    License: MIT
    Github.: https://github.com/rabuchaim/etimedecorator
    Issues.: https://github.com/rabuchaim/etimedecorator/issues
    PyPI...: https://pypi.org/project/etimedecorator/  ( pip install etimedecorator )

"""
import time

__all__ = ['elapsedTimeDecorator','elapsedTimeAverageDecorator','elapsedTimePercentileDecorator']

##──── Decorator to get the elapsed time of a function ───────────────────────────────────────────────────────────────────────────
def elapsedTimeDecorator(method):
    """Displays statistics for each execution determined by the window_size parameter
    
    Output on every call: Elapsed Time for method_name(): 0.000003485 sec
    """
    def decorated_method(*args, **kwargs):
        try:
            startTime = time.monotonic()
            result = method(*args, **kwargs)
            print(f'\033[33mElapsed Time for {method.__name__}(): %.9f sec'%(time.monotonic()-startTime)+"\033[0m")
            return result
        except Exception as ERR:
            print('\033[91m'+f"[ELAPSED_TIME_EXCEPTION] {method.__name__}(): {str(ERR)}"+'\033[0m')
    return decorated_method

##──── a decorator to show the minimum_time, maximum_time and average_time time between requests ─────────────────────────────────
def elapsedTimeAverageDecorator(window_size:int=1000,decimal_places:int=9):
    """Displays statistics for each set of executions determined by the window_size parameter.
    
    Useful only for functions that have tens/hundreds of executions per second.
    
    Prints the output  below each 'window_size' cals:
    
    - Elapsed Time for method_name() - 1000 calls - Min:0.000001479 / Avg:0.000002905 / Max:0.000067696
    
    """
    history = []
    min_time, max_time = 1000000000, 0.0

    def decorator(method):
        nonlocal history, min_time, max_time

        def decorated_method(*args, **kwargs):
            nonlocal history, min_time, max_time
            startTime = time.monotonic()
            try:
                result = method(*args, **kwargs)
                elapsedTime = time.monotonic()-startTime
                min_time = elapsedTime if elapsedTime < min_time else min_time
                max_time = elapsedTime if elapsedTime > max_time else max_time
                history.append(elapsedTime)
                if len(history) >= window_size:
                    averageTime = sum(history) / len(history)
                    history.clear()
                    print(f'\033[32;1mElapsed Time for {method.__name__}() - {window_size} calls - Min:{f"%.{decimal_places}f"%(min_time)} / Avg:{f"%.{decimal_places}f"%(averageTime)} / Max:{f"%.{decimal_places}f"%(max_time)}\033[0m')
                return result
            except Exception as ERR:
                print('\033[91m'+f"[AVERAGE_ELAPSED_TIME_EXCEPTION] {method.__name__}(): {str(ERR)}"+'\033[0m')

        return decorated_method

    return decorator

##──── a decorator to show the percentile of elapsed time between requests ───────────────────────────────────────────────────────
def elapsedTimePercentileDecorator(window_size:int=1000,decimal_places:int=9):
    """Displays statistics for each set of executions determined by the window_size parameter.
    
    Useful only for functions that have tens/hundreds of executions per second.
    
    Prints the output like below each 'window_size' cals:
    
    - Elapsed Time for method_name() 1000 calls - Min:0.000000650 Avg:0.000000946 Max:0.000039139 - 50%:0.000000794 75%:0.000001049 90%:0.000001162 99%:0.000001632
    
    """    
    history = []
    min_time, max_time = 1000000000, 0.0    

    def decorator(method):
        nonlocal history, min_time, max_time

        def percentile(percentile):
            k = (len(history) - 1) * percentile / 100
            f = int(k)
            c = f + 1
            if f == c or c >= len(history):
                return history[f]
            return history[f] * (c - k) + history[c] * (k - f)

        def decorated_method(*args, **kwargs):
            nonlocal history, min_time, max_time
            startTime = time.monotonic()
            try:
                result = method(*args, **kwargs)
                elapsedTime = time.monotonic()-startTime
                min_time = elapsedTime if elapsedTime < min_time else min_time
                max_time = elapsedTime if elapsedTime > max_time else max_time
                history.append(elapsedTime)
                if len(history) >= window_size:
                    averageTime = sum(history) / len(history)
                    history = sorted(history)
                    percentile_line = f"- 50%:{f'%.{decimal_places}f'%percentile(50)} 75%:{f'%.{decimal_places}f'%percentile(75)} 90%:{f'%.{decimal_places}f'%percentile(90)} 99%:{f'%.{decimal_places}f'%percentile(99)}"
                    print(f'\033[38;2;255;140;0;1mElapsed Time for {method.__name__}() {window_size} calls - Min:{f"%.{decimal_places}f"%(min_time)} Avg:{f"%.{decimal_places}f"%(averageTime)} Max:{f"%.{decimal_places}f"%(max_time)} {percentile_line}\033[0m')
                    history.clear()
                return result
            except Exception as ERR:
                print('\033[91m'+f"[AVERAGE_ELAPSED_TIME_EXCEPTION] {method.__name__}(): {str(ERR)}"+'\033[0m')

        return decorated_method

    return decorator