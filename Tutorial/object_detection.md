# 目标检测
目标检测，也叫目标提取，是一种基于目标几何和统计特征的图像分割，它将目标的分割和识别合二为一，其准确性和实时性是整个系统的一项重要能力。
尤其是在复杂场景中，需要对多个目标进行实时处理时，目标自动提取和识别就显得特别重要。(百度百科)
当前，目标检测是人工智能一个热门的研究方向，也有着广泛的应用。如现在汽车的行人检测和预防碰撞系统（PCS），自适应巡航系统（ACC）都会使用
到目标检测技术。
## 比赛中的目标检测任务要求
无人驾驶小车比赛任务中有以下几个要求：   
  - 进入车站，检测到有人等车，停车5秒。
  - 在斑马线前，检测到有行人等待过斑马线，必须礼让行人。
  - 在行进的过程中，如果检测到路中间有障碍物，比如一个水瓶，必须执行避障动作，避开障碍物行驶。
  - 检测到停车标志，停车。   
  
以上比赛任务，可以转换为小车行进过程的通过实时图像的目标检测来实现对各种对象的查找和识别，同事结合CarController对象实现小车的控制。
    
## 目标检测的具体实现
目标检测理论性较强，这里省略了具体的理论分析。只介绍系统实现的方法。我们探索了多种模型，框架，甚至于硬件。最后使用了一个独立的摄像头，
以英伟达提供的Jetson Inference作为编程的接口，Mobilenet作为模型，兼顾了检测成功率，速度，和编程的简易性。
系统封装了Recognition类，实现了目标检测的基本操作，Recognition提供了get_objects用于返回检测到的目标对象的一个列表，同时提供了，
object_appeared方法，用于协助用户快速判断所需要的对象是否出现。另外，封装了Object辅助类，该类保存了目标对象的ID，中英文名称，位置，
宽、高，面积，中心点等信息，object还封装了两个相关的静态方法，get_list，get_object_id 用于生成对象列表，转换名字等功能。

### Recognition方法详细说明:
```python
__init__(self, device="/dev/video0", width=320, height=240, frequency=40, display_window=True)

    初始化识别类，此处应注意，如果指定摄像头的宽和高摄像头本身不支持，必定会出现错误。
    以下语句可以检测摄像头的分辨率：v4l2-ctl --list-formats-ext
    :param device: 指定摄像头（/dev/video?）
    :param width: 指定摄像头宽度
    :param height: 指定摄像头高度
    :param frequency:检测的频率，默认每秒40帧(相当于不限制检测频率)
    :param display_window:是否开始监视窗口，默认是

get_objects(self)
        
    在循环中不停的调用本函数来刷新识别到的物体，当刷新速率超过设定的识别帧率（frequency）时，会返回一个空的列表（list）
    :return: 返回一个包含Object对象的列表。

object_appeared(self, appeared_id, object_width_threshold=60, delay_time=10)
        
    根据输入的目标ID，目标宽度，延迟时间 检测所需目标是否出现并符合设定条件。
    目标ID根据COCO数据集定义。object_appeared用于协助检测对象是否出现。
    :param appeared_id:需要检测的目标ID
    :param object_width_threshold:目标的宽度是否超过阈值
    :param delay_time:两次检测时间间隔（避免重复检测到同一对象）
    :return:当目标对象出现并符合设定的条件返回TRUE，否则返回FALSE

close(self):

    关闭子线程，必须显式关闭，否则识别子进程将不会自动退出。
        
execute(self, frame, render_frame_list)
        
    用于事件的触发
                      
```
### Object 方法的详细说明：
```python
属性：
class_id ：ID
name ：英文名称
chinese ：中文名称
confidence ：未知
left ：对象左外边距边界的偏移
right ：对象右外边距边界的偏移
top ： 上外边距边界与其包含块上边界之间的偏移
bottom ： 下外边距边界与其包含块下边界之间的偏移
area ： 面积
center ： 中心
width ： 对象的宽
height ： 对象的高

——————————————————————————————————————————————————
@staticmethod # 静态方法
    get_list(detections)
        
        受由子线程传输进来的识别信息，封装成一个Object list。
        :param detections: 子线程传输过来的原始信息
        :return: 一个Object对象列表
        
@staticmethod # 静态方法
    get_object_id(name):
     
        根据名称查询对象的id，如果对象不存在列表中，返回-1。
        :param name: 中文或者英文名
        :return: id
        
```

## 一个目标检测的简单实例
以下实例演示了如何初始化Recognition，并在循环中打印出识别的对象信息，完整的程序请下载examples路径下的[object_detection.py](https://github.com/lonerlin/SelfDrivingCVCar/blob/testing/jetson/examples/object_detection.py) 文件
```python

...

OD_CAMERA = '/dev/video1'        # 物体检测摄像头
OD_CAMERA_WIDTH = 320            # 识别视频高度
OD_CAMERA_HEIGHT = 240           # 识别视频高度

# 新建一个识别对象，用于识别操作，程序中的识别对象只能有一个
# 指定设备，指定窗口的宽度和高度，是否打开识别显示窗口（默认是打开）
recognition = Recognition(device=OD_CAMERA, width=OD_CAMERA_WIDTH, height=OD_CAMERA_HEIGHT, display_window=True)

# 新建一个计时器对象，用于程序结束的计时，设置时间为60秒
timer = CarTimer(interval=60)

# 计时没有结束之前一直循环
while not timer.timeout():
    # get_objects函数返回的是包含0个以上的Object对象列表，
    targets = recognition.get_objects()
    # 如果列表中有对象存在，那么迭代循环 打印对象的属性
    if targets:
        for obj in targets:
            print("发现对象 id：{}，名称：{}，面积：{}，高度：{}，宽度：{}"
                  .format(obj.class_id, obj.chinese, obj.area, obj.height, obj.width))

# 循环结束必须调用close（）函数，结束识别窗口，否则窗口将一直打开
recognition.close()
```
假设你现在需要判断一个人是否出现在场地中，条件是：人的宽度超过30个像素（重复出现两个人的间隔设定为五秒），你可以在修改一下上面的程序：
```python

...

OD_CAMERA = '/dev/video1'        # 物体检测摄像头
OD_CAMERA_WIDTH = 320            # 识别视频高度
OD_CAMERA_HEIGHT = 240           # 识别视频高度

# 新建一个识别对象，用于识别操作，程序中的识别对象只能有一个
# 指定设备，指定窗口的宽度和高度，是否打开识别显示窗口（默认是打开）
recognition = Recognition(device=OD_CAMERA, width=OD_CAMERA_WIDTH, height=OD_CAMERA_HEIGHT, display_window=True)

# 新建一个计时器对象，用于程序结束的计时，设置时间为60秒
timer = CarTimer(interval=60)

# 计时没有结束之前一直循环
while not timer.timeout():
    
    # 只需要调用object_appeared，写出人的ID，宽度，延迟时间。
    if recognition.object_appeared(appeared_id=1, object_width_threshold=30, delay_time=5):
        print("前方发现一个人！")

# 循环结束必须调用close（）函数，结束识别窗口，否则窗口将一直打开
recognition.close()

```
## 在做目标检测时需要注意的一些问题
    1. 目标检测单独使用一个摄像头，其他任务公用一个摄像头
    2. 系统采用的是应用最为广泛的COCO数据集，该数据能检测90个目标，具体的目标名称和编号请参考下文。
    3. 结束Recognition的使用，必须调用其方法close,否则程序不能正常退出。
    4. 目标检测技术有一定的成功率，会受到灯光，摄像头角度，物体角度等等的限制，无论哪种模型，都不可能做到100%
    5. 在比赛中，如果是检测人，要注意场地周围的参赛者，裁判员等人员有可能被检测到，从而影响程序的准确性。
    
## COCO数据集的目标编号和中英文名称：
    0,unlabeled,没有标签
    1,person,人
    2,bicycle,自行车
    3,car,车
    4,motorcycle,摩托车
    5,airplane,飞机
    6,bus,公共汽车
    7,train,火车
    8,truck,卡车
    9,boat,船
    10,traffic light,红绿灯
    11,fire hydrant,消防栓
    12,street sign,路标
    13,stop sign,停车标志
    14,parking meter,停车费
    15,bench,板凳上
    16,bird,鸟
    17,cat,猫
    18,dog,狗
    19,horse,马
    20,sheep,羊
    21,cow,牛
    22,elephant,大象
    23,bear,熊
    24,zebra,斑马
    25,giraffe,长颈鹿
    26,hat,帽子
    27,backpack,背包
    28,umbrella,伞
    29,shoe,鞋
    30,eye glasses,眼镜
    31,handbag,手提包
    32,tie,领带
    33,suitcase,手提箱
    34,frisbee,飞盘
    35,skis,滑雪板
    36,snowboard,滑雪板
    37,sports ball,体育球
    38,kite,风筝
    39,baseball bat,棒球棒
    40,baseball glove,棒球手套
    41,skateboard,滑板
    42,surfboard,冲浪板
    43,tennis racket,网球拍
    44,bottle,瓶
    45,plate,板
    46,wine glass,酒杯
    47,cup,杯
    48,fork,叉
    49,knife,刀
    50,spoon,勺子
    51,bowl,碗
    52,banana,香蕉
    53,apple,苹果
    54,sandwich,三明治
    55,orange,橙
    56,broccoli,西兰花
    57,carrot,胡萝卜
    58,hot dog,热狗
    59,pizza,披萨
    60,donut,甜甜圈
    61,cake,蛋糕
    62,chair,椅子
    63,couch,沙发上
    64,potted plant,盆栽植物
    65,bed,床上
    66,mirror,镜子
    67,dining table,餐桌
    68,window,窗口
    69,desk,桌子上
    70,toilet,厕所。。。
    71,door,门
    72,tv,电视
    73,laptop,移动PC
    74,mouse,鼠标
    75,remote,远程
    76,keyboard,键盘
    77,cell phone,手机
    78,microwave,微波
    79,oven,烤箱
    80,toaster,烤面包机
    81,sink,水槽
    82,refrigerator,冰箱
    83,blender,搅拌机
    84,book,书
    85,clock,时钟
    86,vase,花瓶
    87,scissors,剪刀
    88,teddy bear,泰迪熊
    89,hair drier,头发干燥器
    90,toothbrush,牙刷