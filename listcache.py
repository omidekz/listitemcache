from expiringdict import ExpiringDict
from typing import Union


def create_cache(max_len: int = None, ttl: int = None) -> Union[dict, ExpiringDict]:
    parameters = {
    }
    if max_len:
        parameters['max_len'] = max_len
    if ttl:
        parameters['max_age_seconds'] = ttl
    if parameters:
        return ExpiringDict(**parameters)
    return dict()


def items_cache(max_len: int = None, ttl: int = None, key: callable = None, algorithm: callable = None) -> callable:

    def decorator(function):
        function.key = key or hash
        function.algorithm = algorithm
        function.cache = create_cache(max_len, ttl)

        def wrapper(*args):
            cache_result = list()
            function_call_params = list()
            for index, item in enumerate(args):
                item_key = function.key(item)
                if item_key in function.cache:
                    cache_result.append((index, function.cache[item_key]))
                else:
                    function_call_params.append(item)
            function_result = list(function(*function_call_params))
            for index, arg in enumerate(function_call_params):
                function.cache[function.key(arg)] = function_call_params[index]

            for item in cache_result:
                function_result.insert(item[0], item[1])
            return function_result
        return wrapper
    return decorator
