
import jetson.inference
import jetson.utils

net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)
camera = jetson.utils.gstCamera(320, 240, "0")  # using V4L2
display = jetson.utils.glDisplay()

while display.IsOpen():
	img, width, height = camera.CaptureRGBA()
	detections = net.Detect(img, 320, 240)
	display.RenderOnce(img, 320, 240)
	#display.SetTitle("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))