
import jetson.inference
import jetson.utils

net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)
camera = jetson.utils.gstCamera(320, 240, "/dev/video0")  # using V4L2
display = jetson.utils.glDisplay()

while display.IsOpen():
	img, width, height = camera.CaptureRGBA()
	detections = net.Detect(img, width, height)
	display.RenderOnce(img, width, height)
	#display.SetTitle("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))

	for det in detections:
		print(det.ClassID, det.Confidence, det.Left, det.Top, det.Area)