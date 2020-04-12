
class Object:
    """
        一个识别物体的增强对象。
        主要是添加了分类的中英文，同时保留了原来的位置，宽、高，面积，中心点等信息。
        对应COCO数据集
    """
    def __init__(self, detection):
        self.Names = ['unlabeled', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck',
                      'boat', 'traffic light', 'fire hydrant', 'street sign', 'stop sign', 'parking meter', 'bench',
                      'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'hat',
                      'backpack', 'umbrella', 'shoe', 'eye glasses', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis',
                      'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
                      'tennis racket', 'bottle', 'plate', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
                      'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut',
                      'cake', 'chair', 'couch', 'potted plant', 'bed', 'mirror', 'dining table', 'window', 'desk',
                      'toilet', 'door', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave',
                      'oven', 'toaster', 'sink', 'refrigerator', 'blender', 'book', 'clock', 'vase', 'scissors',
                      'teddy bear', 'hair drier', 'toothbrush']
        self.Chinese_names = ['无标号', '人', '自行车', '车', '摩托车', '飞机', '公共汽车', '火车', '卡车', '船', '红绿灯', '消防栓', '路标', '停车标志',
                              '咪表', '长凳', '鸟', '猫', '狗', '马', '羊', '牛', '大象', '熊', '斑马', '长颈鹿', '帽子', '背包', '雨伞', '鞋',
                              '眼镜', '手提包', '领带', '手提箱', '飞盘', '滑雪板', '滑雪板', '球', '风筝', '棒球棒', '棒球手套', '滑板', '冲浪板',
                              '网球拍', '瓶', '盘子', '酒杯', '杯', '叉', '刀', '勺子', '碗', '香蕉', '苹果', '三明治', '橙色', '西兰花', '胡萝卜',
                              '热狗', '披萨', '甜甜圈', '蛋糕', '椅子', '沙发上', '盆栽植物', '床上', '镜子', '餐桌', '窗口', '桌子', '厕所', '门',
                              '电视', '笔记本电脑', '鼠标', '遥控', '键盘', '手机', '微波', '烤箱', '烤面包机', '水槽', '冰箱', '搅拌机', '书', '时钟',
                              '花瓶', '剪刀', '泰迪熊', '头发干燥器', '牙刷']

        self.class_id = detection[0]
        self.name = self.Names[self.class_id]
        self.chinese = self.Chinese_names[self.class_id]
        self.confidence = detection[1]
        self.left = detection[2]
        self.right = detection[3]
        self.top = detection[4]
        self.bottom = detection[5]
        self.area = detection[6]
        self.center = detection[6]
        self.width = self.right - self.left
        self.height = self.bottom - self.top

    @staticmethod
    def get_list(detections):
        """
            接受由子线程传输进来的识别信息，封装成一个Object list。
        :param detections: 子线程传输过来的原始信息
        :return: 一个Object对象列表
        """
        package = []
        for det in detections:
            package.append(Object(det))
        return package


if __name__ == 'main()':
        pass
