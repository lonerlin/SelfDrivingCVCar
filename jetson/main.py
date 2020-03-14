from multiprocessing import Process,Pipe
from objcet_detection import object_detection


def main():
    conn1,conn2 = Pipe()
    od = object_detection(conn1, conn2, 15)



if __name__ == "__main__":
    main()