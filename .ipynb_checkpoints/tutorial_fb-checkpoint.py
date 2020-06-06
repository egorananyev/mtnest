import cv2 as cv
import numpy as np

class FBackDemo:
    def __init__(self):
        # self.capture = cv.CaptureFromCAM(0)
        self.capture = cv.VideoCapture(cv.samples.findFile("asm2.mp4"))
        self.mv_step = 16
        self.mv_scale = 1.5
        self.mv_color = (0, 255, 0)
        self.cflow = None
        self.flow = None
        
        cv.namedWindow( "Optical Flow", 1 )

        print( "Press ESC - quit the program\n" )

    def draw_flow(self, flow, prevgray):
        """ Returns a nice representation of a hue histogram """

        cv.CvtColor(prevgray, self.cflow, cv.CV_GRAY2BGR)
        for y in range(0, flow.height, self.mv_step):
            for x in range(0, flow.width, self.mv_step):
                fx, fy = flow[y, x]
                cv.Line(self.cflow, (x,y), (int(x+fx),int(y+fy)), self.mv_color)
                cv.Circle(self.cflow, (x,y), 2, self.mv_color, -1)
        cv.ShowImage("Optical Flow", self.cflow)

    def run(self):
        first_frame = True
        
        while True:
            
            res, frame = self.capture.read()
            # frame = cv.queryFrame( self.capture )

            if first_frame:
                # gray = cv.CreateImage(cv.GetSize(frame), 8, 1)
                gray = cv.cvtColor(frame, cv.COLOR_BGR2HSV)                
                # prev_gray = cv.CreateImage(cv.GetSize(frame), 8, 1)
                prev_gray = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
                # flow = cv.CreateImage(cv.GetSize(frame), 32, 2)
                flow = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
                # self.cflow = cv.CreateImage(cv.GetSize(frame), 8, 3)
                self.cflow = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
                
            # cv.cvtColor(frame, gray, cv.CV_BGR2HSV)
            cv.bitwise_and(frame, gray)
            print(np.size(prev_gray))
            print(np.size(gray))
            print(np.size(flow))
            
            if not first_frame:
                # cv.calcOpticalFlowFarneback(prev_gray, gray, flow,
                #     pyr_scale=0.5, levels=3, winsize=15,
                #     iterations=3, poly_n=5, poly_sigma=1.2, flags=0)
                cv.calcOpticalFlowFarneback(prev_gray, gray, flow, 0.5, 3, 20, 5, 7, 1.2, 0)
                self.draw_flow(flow, prev_gray)
                c = cv.WaitKey(7)
                if c in [27, ord('q'), ord('Q')]:
                    break
                    
            prev_gray, gray = gray, prev_gray        
            first_frame = False

if __name__=="__main__":
    demo = FBackDemo()
    demo.run()