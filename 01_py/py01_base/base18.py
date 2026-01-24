#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/1/14 20:35
# Module    : base18.py
# explain   : 类 和 对象 ， https://docs.python.org/zh-cn/3.10/tutorial/classes.html


# 1、初识类和对象
class MyClass(object):
    def __init__(self):
        print("创建了一个MyClass对象")


mc = MyClass()
print(mc, id(mc))


# 2、类属性和实例属性
class Student(object):
    # school是类属性，每一个实例对象的都是这个值
    school = "北京一中"

    def __init__(self, name, age):
        self.name = name
        self.age = age


s1 = Student("zhangsan", 18)
print(s1)
# 给实例对象添加一个属性，注意：只有这个对象才有这个属性，其他对象没有这个属性
s1.height = 180
print(s1.height)
# del可以删除某个对象的某个属性
del s1.height
# AttributeError: 'Student' object has no attribute 'height'
# print(s1.height)
print(s1.school)  # 北京一中

s2 = Student("lisi", 18)
print(s2.school)  # 北京一中
# 以下报错说明height属性只添加到了s1对象
# AttributeError: 'Student' object has no attribute 'height'
# print(s2.height)

# 实例对象.类属性：表示修改这个对象的类属性，其他对象的对应类属性还是原来的不变
s1.school = "上海一中"
print(s1.school)  # 上海一中
print(s2.school)  # 北京一中

# 用类名修改类属性
Student.school = "广州一中"
print(s1.school)  # 上海一中， 这里还是原来的上海一中，说明，如果某个实例对象已经修改过类属性了，那么这个实例对象的类属性就无法通过”类名.类属性“进行修改了
print(s2.school)  # 广州一中

print("=" * 50)

# 3、类中的方法
# 下面分析py类中的三种方法的区别，实例方法、类方法、静态方法
"""
| 类型   | 第一个参数  | 装饰器             | 能访问           |
| ---- | ------ | --------------- | ------------- |
| 实例方法 | `self` | 无               | 实例属性          |
| 类方法  | `cls`  | `@classmethod`  | 类属性           |
| 静态方法 | 无      | `@staticmethod` | 啥都访问不了（除非写类名） |
"""


# object 是 py对象的超类
# (object)表示Person这个类继承自 object 类
class Person(object):
    # continent 是 Person 类的类属性，由带有 @classmethod 装饰器的类方法访问
    count = 0

    # __init__ 是每一个对象都需要一个构造方法
    # __init__ 是实例化对象的初始方法，
    # __init__ 是每一个类必须的，当然如果你不实现，那么py会给你一个默认实现
    def __init__(self, name, age):
        self.name = name
        self.age = age
        Person.count += 1

    # 如果类里面的某个方法要想成为实例方法，那么这个方法的第一个参数必须是self，这个self参数的值有py传入
    # 【【【self 就是当前调用这个方法的对象实例本身】】】
    # 实例对象会作为实例方法的第一个参数被传入当前方法
    def what_self(self):
        print(f"实例方法的self是什么？？？{id(self)}, self实际就是当前调用这个实例方法的实例对象的地址")

    # 如果想定义一个类方法，而非实例方法，那么方法的第一个参数不再是self了
    # 而是cls表示class类，并且必须在该方法上加一个装饰器@classmethod
    # 类方法可以访问类属性
    @classmethod
    def say_hi(cls):
        print(f"欢迎来到Person类 {cls.count} ！！！")

    # 定义一个静态方法，既不能访问实例属性，也不能访问类属性
    # 静态方法没有self，也没有cls
    # 定义静态方法必须加@staticmethod装饰器
    # 静态方法由：类名.静态方法名 来访问
    @staticmethod
    def do_something(msg):
        print(f"do_something: msg={msg}")


p1 = Person("zhangsan", 18)
p2 = Person("lisi", 18)
print(p1.count, p1.count)
p1.what_self()
Person.what_self(p2)

p1.say_hi()
p2.say_hi()
Person.say_hi()

Person.do_something("你好世界")


class MyClass:
    """A simple example class"""
    i = 12345

    def f(self):
        return 'hello world'

    # 构造函数
    # 当创建一个MyClass实例对象的时候被调用
    def __init__(self):
        print("创建新对象")

    # 析构函数
    # 当前对象被 del 或 程序结束 的时候会被调用
    # 注意：如果程序运行过程中不手动调用del mc删除这个类的实例对象，那么在程序结束前一定会调用__del__
    # 如果部手动调用del，则类似于 after_destroy 方法，即程序销毁前执行的方法，由py解释器执行
    # 可以理解为类的实例对象内存地址被释放之前执行的一个方法
    def __del__(self):
        print("对象被销毁")


mc = MyClass()
print(MyClass.i)
print(MyClass.f(mc))
print(MyClass.__doc__)
# del mc
# 创建一个对象，但是不持有这个对象的地址，那么py解释器会立即销毁他，因为就算你不销毁，以后也无法访问到这块内存了，
# 所有以下一句调用完构造函数之后会立即调用析构函数【创建完成之后立即销毁】
MyClass()

print("=" * 20 + "5、继承" + "=" * 30)


class Animal(object):
    def __init__(self, name):
        self.name = name

    # 封装
    def eat(self):
        print(f"Animal {self.name} 正在吃饭哦")


class Dog(Animal):
    def __init__(self, name, addr):
        super().__init__(name)
        self.addr = addr

    def wangwangwang(self):
        print(f"{self.addr} 的 {self.name} 正在狂叫不止~~~")

    # 方法重写
    def eat(self):
        print(f"Dog {self.name} 正在疯狂干饭...")


class Fish(Animal):
    def __init__(self, name, weight):
        super().__init__(name)
        self.weight = weight

    def swimming(self):
        print(f"{self.weight} kg 的 {self.name} 正在游泳")

    # 方法重写
    def eat(self):
        print(f"Fish {self.name} 正在找小虾米吃...")


dog = Dog("Tom", "上海")
dog.eat()
dog.wangwangwang()

fish = Fish("小鱼儿", 5)
fish.eat()
fish.swimming()

print("\n")


# 多态，子类对象指向父类引用, 同一种行为具有多种不同的表现形式，【同一个接口（方法），不同对象，表现出不同行为】
# 多态的前提条件：要由继承关系，并且子类要重写父类的方法

# 定义一个方法来使用多态，这个方法接收Animal及其所有子类对象
# 当我们传入的对象不同时，其表现出的行为也不同，这个就是多态
# 运行时动态绑定（Dynamic Dispatch）
def make_animal_eat(animal: Animal):
    animal.eat()


make_animal_eat(dog)
make_animal_eat(fish)


# 此外py中有一个叫做鸭子类型的说法，
# 鸭子类型：【【【不关心对象“是什么类”，只关心对象“能不能干这件事”】】】不通过对象的类型（isinstance），而是通过对象是否具备所需的方法或行为来决定是否可用
# 对于上述的多态实现就可以利用这个原理，用其它拥有eat方法的对象来实现make_animal_eat的多态，即其实不需要是Animal类的子类，也能调用make_animal_eat实现多态
# 但是前提是这个类的对象必须由 eat()方法
class Robot:
    def eat(self):
        print("充电中...")


make_animal_eat(Robot())

print("\n")


# 多重继承，又称协作式多继承
# 要想实现协作式多继承，必须实现的三条铁律（重点）
# ✅ 规则 1：被多继承的父类中的__init__ 必须接收 **kwargs 参数
# ✅ 规则 2：被多继承的父类中的__init__必须调用 super().__init__(**kwargs)
# ✅ 规则 3：子类在调用super().__init__的时候必须使用关键字传参
# ✅ 规则 4：每一个类只初始化“自己负责的属性”
class BaseA(object):
    def __init__(self, name, **kwargs):
        print("BaseA.__init__.1")
        super().__init__(**kwargs)
        self.name = name
        print("BaseA.__init__.2")

    def funca(self):
        print(f"funca 被 {self.name} 执行 ")


class BaseB(object):

    # 为什么以下去除, **kwargs和注释super().__init__之后还可以正常运行？
    # 答：根据ClassC.__mro__可知，BaseB.__init__会被BaseA.__init__调用
    # 而在BaseA.__init__里面调用super().__init__(**kwargs)会将age参数传入BaseB.__init__
    # 因此在BaseB.__init__里面实际就没用到**kwargs参数了，同时也不需要再将**kwargs向后传递了
    # 因此这里可以将**kwargs相关的去除，无影响
    # 从上面的分析中，我们可以得出结论，即多继承时继承的顺序（如ClassC(BaseA, BaseB)）对是否要加**kwargs至关重要：
    # 即如果如果要继承的后面的父类不需要传递参数，那么对应的那个父类就可以不要写**kwargs
    # 注意：不需要写**kwargs的父类写在后面

    # 从上面的分析中，我们也可以得出一个结论：即__init__方法的最佳实际是声明的时候最后要解释**kwargs，并且在初始化父类super().__init__的时候将**kwargs向后传递，如此之后这个类无论在那里被继承都可以不用修改了，可以直接使用
    # 定义的最佳实践：def __init__(self, age, **kwargs):
    # 初始化父类的最佳实践：super().__init__(**kwargs)
    # def __init__(self, age, **kwargs):
    def __init__(self, age):
        print("BaseB.__init__.1")
        # super().__init__(**kwargs)
        self.age = age
        print("BaseB.__init__.2")

    def funcb(self):
        print(f"funcb 被 {self.age} 执行 ")


class ClassC(BaseA, BaseB):
    def __init__(self, name, age, addr):
        super().__init__(name=name, age=age)
        self.addr = addr

    def funcc(self):
        print(f"name={self.name},age={self.age},addr={self.addr} 正在执行 funcc")


# 查看ClassC的MRO（方法解析顺序）
# mro是ClassC类的super()方法的调用顺序
# ClassC → BaseA → BaseB → object
# (<class '__main__.ClassC'>, <class '__main__.BaseA'>, <class '__main__.BaseB'>, <class 'object'>)
# 以上元组的解释：在ClassC中调用super().__init__实际调用的是BaseA中的__init__方法
print(ClassC.__mro__)

c = ClassC("zhangsan", 18, "北京")
c.funcc()
c.funcb()
c.funca()
"""
BaseA.__init__.1
BaseB.__init__.1
BaseB.__init__.2
BaseA.__init__.2
name=zhangsan,age=18,addr=北京 正在执行 funcc
funcb 被 18 执行 
funca 被 zhangsan 执行 
"""


# 受保护变量 和 私有变量
# 受保护变量：以一个下划线_开头的变量，这中变量时约定的私有变量，
# 私有变量：当类中的某个变量不希望被外部使用时，就要使用私有变量, 私有变量的变量名以两个下划线__开头，如：__tmp, __age
# 受保护的变量还是可以被访问的，只不过py开发者们约定俗成以一个下划线_开头的变量外界不能去修改他，但是如果你强行修改或访问还是可以的
# 而私有变量是不可以被访问的
# 以两个下划线__开头的变量py会对其进行改写，如__addr  →  _TestClass1__addr，即实际在py的元数据里面存的是_TestClass1__addr这个变量
class TestClass1:
    def __init__(self, name, age, addr):
        self.name = name
        self._age = age
        self.__addr = addr

    def get_addr(self):
        return self.__addr

    def func(self, *args):
        self.__private_func(*args)

    def __private_func(self, *args):
        print("我是私有函数", *args)


tc = TestClass1("张三", 18, "北京")
print(tc.name)
print(tc._age)
# AttributeError: 'TestClass1' object has no attribute '__addr'
# print(tc.__addr)
print(tc.get_addr())
print(tc.__dict__)
# 访问被改写后的变量名
print(tc._TestClass1__addr)  # 'TestClass1' 的未解析的特性引用 '_TestClass1__addr'
tc.func(1, 2, 3, )
# AttributeError: 'TestClass1' object has no attribute '__addr'
# tc.__private_func(1, 2, 3, )


# 定义存数据结构，即model类，没有实现方法的
# 要引入一个包dataclasses里面的装饰器dataclass，from dataclasses import dataclass
# 被@dataclass装饰器装饰的类即为存数据模型类，没有相关方法
# 非常适合：DTO / VO、配置对象、ORM 前的数据模型、API 返回对象、临时数据结构
from dataclasses import dataclass


@dataclass
class Employee:
    name: str
    dept: str
    salary: int


# @dataclass装饰器会为Employee类生成以下内容
"""
    def __init__(self, name: str, dept: str, salary: int):
        self.name = name
        self.dept = dept
        self.salary = salary

    def __repr__(self):
        return f"Employee(name={self.name!r}, dept={self.dept!r}, salary={self.salary!r})"

    def __eq__(self, other):
        if not isinstance(other, Employee):
            return NotImplemented
        return (
            self.name == other.name and
            self.dept == other.dept and
            self.salary == other.salary
        )
"""

e1 = Employee("zhangsan", "财务部", 1800)
e2 = Employee("zhangsan", "人事部", 1800)
print(e1, e1.name, e1.dept, e1.salary)
print(e2, e2.name, e2.dept, e2.salary)
