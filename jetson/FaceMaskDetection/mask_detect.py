import cv2
import numpy as np
from utils.anchor_generator import generate_anchors
from utils.anchor_decode import decode_bbox
from utils.nms import single_class_non_max_suppression
from load_model.keras_loader import load_keras_model, keras_inference


class MaskDetect:

    def __init__(self, width=320, height=240):
        self.image_width = width
        self.image_height = height
        self.model = model = load_keras_model('models/face_mask_detection.json', 'models/face_mask_detection.hdf5')
        # anchor configuration
        feature_map_sizes = [[33, 33], [17, 17], [9, 9], [5, 5], [3, 3]]
        anchor_sizes = [[0.04, 0.056], [0.08, 0.11], [0.16, 0.22], [0.32, 0.45], [0.64, 0.72]]
        anchor_ratios = [[1, 0.62, 0.42]] * 5

        # generate anchors
        self.anchors = generate_anchors(feature_map_sizes, anchor_sizes, anchor_ratios)

        # for inference , the batch size is 1, the model output shape is [1, N, 4],
        # so we expand dim for anchors to [1, anchor_num, 4]
        self.anchors_exp = np.expand_dims(self.anchors, axis=0)

        self.id2class = {0: 'Mask', 1: 'NoMask'}

    def inference(self,
                  image,
                  conf_thresh=0.5,
                  iou_thresh=0.4,
                  target_shape=(160, 160),
                  ):
        '''
        Main function of detection inference
        :param image: 3D numpy array of image
        :param conf_thresh: the min threshold of classification probabity.
        :param iou_thresh: the IOU threshold of NMS
        :param target_shape: the model input size.
        :param draw_result: whether to daw bounding box to the image.
        :param show_result: whether to display the image.
        :return:
        '''
        # image = np.copy(image)
        output_info = []
        height, width, _ = image.shape
        image_resized = cv2.resize(image, target_shape)
        image_np = image_resized / 255.0  # 归一化到0~1
        image_exp = np.expand_dims(image_np, axis=0)

        y_bboxes_output, y_cls_output = keras_inference(self.model, image_exp)
        # remove the batch dimension, for batch is always 1 for inference.
        y_bboxes = decode_bbox(self.anchors_exp, y_bboxes_output)[0]
        y_cls = y_cls_output[0]
        # To speed up, do single class NMS, not multiple classes NMS.
        bbox_max_scores = np.max(y_cls, axis=1)
        bbox_max_score_classes = np.argmax(y_cls, axis=1)

        # keep_idx is the alive bounding box after nms.
        keep_idxs = single_class_non_max_suppression(y_bboxes,
                                                     bbox_max_scores,
                                                     conf_thresh=conf_thresh,
                                                     iou_thresh=iou_thresh,
                                                     )

        for idx in keep_idxs:
            conf = float(bbox_max_scores[idx])
            class_id = bbox_max_score_classes[idx]
            bbox = y_bboxes[idx]
            # clip the coordinate, avoid the value exceed the image boundary.
            xmin = max(0, int(bbox[0] * width))
            ymin = max(0, int(bbox[1] * height))
            xmax = min(int(bbox[2] * width), width)
            ymax = min(int(bbox[3] * height), height)
            output_info.append([class_id, conf, xmin, ymin, xmax, ymax])
            # if draw_result:
            #     if class_id == 0:
            #         color = (0, 255, 0)
            #     else:
            #         color = (255, 0, 0)
            #     cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, 2)
            #     cv2.putText(image, "%s: %.2f" % (self.id2class[class_id], conf), (xmin + 2, ymin - 2),
            #                 cv2.FONT_HERSHEY_SIMPLEX, 0.8, color)

        # if show_result:
        #     Image.fromarray(image).show()
        return output_info

    def render(self, image, output_info):
        for idx in output_info:
            if idx[0] == 0:
                color = (0, 255, 0)
            else:
                color = (255, 0, 0)
            cv2.rectangle(image, (idx[2], idx[3]), (idx[4], idx[5]), color, 2)
            cv2.putText(image, "%s: %.2f" % (self.id2class[idx[0]], idx[1]), (idx[2] + 2, idx[3] - 2),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color)

    def detect(self, image, render_image=None):
        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        info = self.inference(img, target_shape=(self.image_width, self.image_height))
        if render_image is not None:
            self.render(render_image, info)
        return info
