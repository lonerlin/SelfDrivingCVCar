# 事件驱动模型，让程序更简单
如果你认真阅读main.py函数，你就会发现它过于复杂，整体程序比较长。有没有更加现代，更加面向对象的写法呢？答案当然是有。
## 一个处理基本任务的父类

其实，整个程序的框架基本是固定的，所以在car路径下，定义了一个类CarBase，它实现了程序最基本的部分，包括一些对象的初始化，
主循环的构造和最后的对象销毁，资源释放。用户在编写小车控制程序时，直接继承该类。   
在子类中，你只需按需新建一些对象，如巡线对象，寻找十字路口对象。然后将这些对象添加到任务对象列表中。

## 事件触发与回调函数
如果你认真阅读cv目录下面的各个文件的源代码，你会发现它们都继承了car路径下的Base类，Base类提供一个event_function的属性和
一个execute方法，execute方法用于在循环中执行具体的任务，比如FollowLine，它的execute就是执行查找白线的中心点（实际上是封
装了对get_offset函数的调用），FindIntersection的execute执行的是寻找路口（封装了对is_intersection的调用）等等，但是
execute除了对实际执行函数的调用之外，还会触发对event_function的调用，相当于触发了一个事件。   
但是在基类的event_function是一个变量，它值是None，为何可以作为一个事件函数呢？Python本身提供了这么一个特性，变量可以是一个
函数，既然是一个函数，那么就可以把变量当成函数来调用。    
每个继承了Base的类，都有这么个event_function的变量，那它的具体得值（其实就是一个函数），你仔细阅读car_main.py中的以下代码：
```python

...

# 寻找路口对象，事件处理函数中会返回一个intersection_number参数，你也可以通过fi.intersection_number调用这个属性
        self.fi = FindIntersection(radius=150, threshold=4, repeat_count=2, delay_time=1.6)
        
        # 回调函数的具体指向就是e_find_intersection
        self.fi.event_function = self.e_find_intersection
        CarMain.task_list.append(self.fi)

...
    # 发现路口的事件处理函数
    def e_find_intersection(self, **kwargs):
        """
            发现路口时触发本事件
        """
        if self.fi.intersection_number == 1:
            self.car_controller.turn(True, 1.2)
        if self.fi.intersection_number == 5:
            self.car_controller.turn(False, 1)
        if self.fi.intersection_number == 6:
            self.car_controller.turn(True, 1.3)
        if self.fi.intersection_number == 10:
            self.car_controller.turn(False, 1)
        if self.fi.intersection_number == 11:
            self.car_controller.stop()
        pass
        number = kwargs['intersection_number']
        print("intersection_number{}".format(number))

```

 我们新建一个FindIntersection的实例fi，然后让fi的属性指向e_find_intersection，在循环中我们重复调用fi.execute()
 ，当fi对象找到路口时，event_function会被调用，因为event_function的具体值是函数e_find_intersection，所以最后
 e_find_intersection会得到执行。
 
 ## 程序循环中的对象时怎么被执行的？
 仔细阅读car_main.py的代码，你会发现,每个新建的对象都会被添加到CarMain的task_list中，比如下面的程序：
 ```python
CarMain.task_list.append(self.fi)
```
task_list中保存了我们新建的所有对象，然后我们在基类中遍历task_list，逐一执行对象的execute方法，这样就实现了对所有对象的执行。
```python
# 循环任务列表，按顺序执行，ImageInit需要先于其他cv下面的对象执行
            for task in CarBase.task_list:
                tmp = []
                if isinstance(task, ImageInit):     # 没办法弄成一样，所以写了两个if
                    self.available_frame = task.execute(self.original_frame)
                elif isinstance(task, FindRoadblock):
                    task.execute(self.original_frame, None)
                else:
                    tmp.append(self.render_frame)
                    task.execute(self.available_frame, tmp)
            # 实际的小车控制操作由update控制
            self.car_controller.update()
```

## 使用事件驱动模型的优缺点
习惯于面向编程的人，可能更接受这样的编程方式，你在使用的过程中，会用到继承，多态等等的技术。我们设计比赛的初衷，就是通过比赛，
让更多的人去接触，了解，学习各种新的技术，提高自己的编程水平，处理问题的能力。所以，我认为提供一个事件驱动模型的程序，是非常
有必要的，我也很期待更多的人去理解，使用这种方式来编程。     
当然，整个程序还有很多不如意的地方，也不是一个完全面向的编程，中间很多不合理的地方，这是我个人水平太差导致的。无论如何，我希望
抛砖引玉，更多人能写出更完美的程序！