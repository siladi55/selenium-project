#coding=utf-8

x = 99

def maker(n):
    k = 8
    def f2(x):
        # nonlocal k
        # k += 1
        print ('%s的%s次方结果：%s'%(x, n, x**n + k))
        return x**n + k
    return f2

if __name__ == '__main__':
    from functools import wraps, partial
    from functools import wraps


    def singleton(cls):
        _instances = {}  # 容器字典，存储每个类对应生成的实例

        @wraps(cls)
        def wrapper(*args, **kwargs):
            # 检查类是否_instances的key；如果是，直接返回生成过的实例
            key = '<{}_{}_{}>'.format(cls.__name__, args, kwargs)
            print key
            if key not in _instances:
                _instances[key] = cls(*args, **kwargs)
            return _instances[key]

        return wrapper


    @singleton
    class Foo(object):
        def __init__(self, a=0):
            self.a = a


    # 测试
    foo1 = Foo(1)
    foo2 = Foo(1)
    print foo1.a  # Out: 1
    print foo2.a  # Out: 1
    print id(foo1) == id(foo2)  # 结果为True，两个实例id相等，证明这个类确实是单例的

    foo3 = Foo(3)
    print id(foo3) == id(foo1)


"""    单例模式的实现（线程友好）
import threading
class Singleton(object):
    _instance_lock = threading.Lock()

    def __init__(self):
        pass
        
    def __new__(cls, *args, **kwargs):
        if not hasattr(Singleton, "_instance"):
            with Singleton._instance_lock:
                if not hasattr(Singleton, "_instance"):
                    Singleton._instance = object.__new__(cls)  
        return Singleton._instance
--------------------------------方法二，装饰器
def Singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton


@Singleton
class A(object):
    a = 1

    def __init__(self, x=0):
        self.x = x    
        
-------------------------------方法三，模块
class Singleton(object):
    def foo(self):
        pass
singleton = Singleton()
使用from module import singleton
    
"""
