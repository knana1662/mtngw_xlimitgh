from django.core.cache import cache

def generate_cache(key=None,values_or_values=None,condition=None,timeout=None):
    ...
    if condition=="set":
        ...
        if timeout == None:
            return cache.set(key, values_or_values, pow(100,20))
        else:
            return cache.set(key, values_or_values, timeout)

    elif condition=="get":
        ...
        return cache.get(key)

    elif condition=="get_or_set":
        ...
        if timeout == None:
            return cache.get_or_set(key, values_or_values, pow(100,20))
        else:
            return cache.get_or_set(key, values_or_values, timeout)