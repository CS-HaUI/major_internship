import time
import customtkinter
import cv2
from PIL import Image

from config.config_system import *


class App(customtkinter.CTk):
    def __init__(self, camera=None):
        super().__init__()
        self.example_image = cv2.imread("dataset\\2.jpg")

        self.camera = cv2.VideoCapture(0)
        self.ctk_image = None

        self.title("Nhận diện biển số xe")
        self.geometry(f"{WIDTH}x{HEIGHT}+10+10")
        self.resizable(False, False)

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.control = customtkinter.CTkFrame(self, corner_radius=0, width=SIZE_CONTROL)
        self.detect_frame = customtkinter.CTkFrame(self, corner_radius=0, width=WIDTH - SIZE_CONTROL)
        self.register_frame = customtkinter.CTkFrame(self, corner_radius=0, width=WIDTH - SIZE_CONTROL)
        self.information_frame = customtkinter.CTkFrame(self, corner_radius=0, width=WIDTH - SIZE_CONTROL)

        self.top_df = customtkinter.CTkFrame(self.detect_frame, corner_radius=0, height=TOP_SIZE)
        self.bottom_df = customtkinter.CTkFrame(self.detect_frame, corner_radius=0, height=HEIGHT - TOP_SIZE)
        self.video_frame = customtkinter.CTkFrame(self.top_df, corner_radius=5, width=VIDEO_WIDTH)
        self.information = customtkinter.CTkFrame(self.top_df, corner_radius=0, width=WIDTH - VIDEO_WIDTH)

        # ----------------- SELECT FRAME ----------------------------------
        self.detect_image = customtkinter.CTkImage(Image.open(DETECT_PATH))
        self.register_image = customtkinter.CTkImage(Image.open(REGISTER_PATH))
        self.search_image = customtkinter.CTkImage(Image.open(SEARCH_PATH))

        # FRAME DETECTION
        self.detect_button = customtkinter.CTkButton(self.control, corner_radius=0, height=40, border_spacing=10,
                                                     text="Nhận diện",
                                                     fg_color="transparent", text_color=("gray10", "gray90"),
                                                     hover_color=("gray70", "gray30"),
                                                     image=self.detect_image, anchor="w", command=self.detect_event)
        self.detect_button.grid(row=1, column=0, sticky="ew")

        # FRAME REGISTER
        self.register_button = customtkinter.CTkButton(self.control, corner_radius=0, height=40, border_spacing=10,
                                                       text="Đăng kí",
                                                       fg_color="transparent", text_color=("gray10", "gray90"),
                                                       hover_color=("gray70", "gray30"),
                                                       image=self.register_image, anchor="w",
                                                       command=self.register_event)
        self.register_button.grid(row=2, column=0, sticky="ew")

        # FRAME CHECK CAR IN DATABASE
        self.information_button = customtkinter.CTkButton(self.control, corner_radius=0, height=40, border_spacing=10,
                                                          text="Nhà xe",
                                                          fg_color="transparent", text_color=("gray10", "gray90"),
                                                          hover_color=("gray70", "gray30"),
                                                          image=self.search_image, anchor="w",
                                                          command=self.information_event)
        self.information_button.grid(row=3, column=0, sticky="ew")
        # ----------------- SELECT FRAME ----------------------------------

        self.control.grid(row=0, column=0, sticky="nsew")
        self.detect_frame.grid(row=0, column=1, sticky='nsew')
        self.top_df.pack(side='top', fill='both', expand=True)
        self.bottom_df.pack(side='bottom', fill='both', expand=True)

        self.video_frame.pack(side='left', fill='both', expand=True)
        self.information.pack(side='right', fill='both', expand=True)

        self.display_video = customtkinter.CTkLabel(self.video_frame, text="", compound="left")
        self.display_video.pack()

    def update_video(self):
        """
        get current frame of stream video
        """
        # res, frame = self.camera.read()
        res, frame = True, self.example_image
        if res is not None:
            # ---------------- FPS ------------------
            # global start_time, frame_count
            # frame_count += 1
            # elapsed_time = time.time() - start_time
            # if elapsed_time > 1:
            #     fps = frame_count / elapsed_time
            #     print(fps)
            #     frame_count = 0
            #     start_time = time.time()
            # ---------------- FPS ------------------
            self.ctk_image = customtkinter.CTkImage(
                Image.fromarray(
                    cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                ),
                size=(600, 400)
            )
            self.display_video.configure(image=self.ctk_image)
        else:
            self.camera.release()
            cv2.destroyAllWindows()
        self.after(10, self.update_video)

    def set_current_frame(self, name):
        """
        :param name: name of current frame
        :return:
        """
        self.detect_button.configure(fg_color=("gray75", "gray25") if name == "detect" else "transparent")
        self.register_button.configure(fg_color=("gray75", "gray25") if name == "register" else "transparent")
        self.information_button.configure(fg_color=("gray75", "gray25") if name == "information" else "transparent")
        # show selected frame
        if name == "detect":
            self.detect_frame.grid(row=0, column=1, sticky='nsew')
        else:
            self.detect_frame.grid_forget()

        if name == "register":
            self.register_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.register_frame.grid_forget()
        if name == "information":
            self.information_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.information_frame.grid_forget()

    def detect_event(self):
        self.set_current_frame("detect")

    def register_event(self):
        self.set_current_frame("register")

    def information_event(self):
        self.set_current_frame("information")


if __name__ == "__main__":
    start_time = time.time()
    frame_count = 0
    app = App()
    app.update_video()
    app.mainloop()
