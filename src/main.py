import tkinter as tk
from PIL import Image
from PIL import ImageTk
import requests
import threading
import json

class Window:
    def __init__(self, master):
        self.master = master
        self.TITLE = "News App"
        self.WIDTH = 1000
        self.HEIGHT = 600
        self.TOP = 50
        self.LEFT = 100
        self.API_KEY = ""

        self.init_window()

    def init_window(self):
        self.master.title(self.TITLE)
        self.master.geometry(f"{self.WIDTH}x{self.HEIGHT}+{self.LEFT}+{self.TOP}")
        self.master.config(bg="#343434")

        self.widgets()

    def widgets(self):
        self.heading = tk.Label(self.master, text="Top News By News App", font=("sans-serif", 24, "bold"), background="#343434", foreground="limegreen")
        self.heading.pack(pady=15, side=tk.TOP, fill=tk.X)

        self.frame = tk.Frame(self.master, background="#343434")
        self.scrollbar = tk.Scrollbar(self.frame)
        self.x_scrollbar = tk.Scrollbar(self.frame, orient=tk.HORIZONTAL)
        self.textView = tk.Text(self.frame, height=20, width=75, background="#232323", foreground="tomato", font=("Comic Sans MS", 15, "bold"), relief=tk.FLAT, selectbackground="hotpink", yscrollcommand=self.scrollbar.set, xscrollcommand=self.x_scrollbar.set, wrap=tk.WORD)
        self.scrollbar.config(command=self.textView.yview)
        self.x_scrollbar.config(command=self.textView.xview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.textView.pack(side=tk.LEFT)
        self.frame.pack(pady=20)

        self.get_news()

    def get_news(self):
        t1 = threading.Thread(target=self.getNews)
        t1.start()

    def getNews(self):
        resp = requests.get(f"https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey={self.API_KEY}")

        resp = json.loads(resp.text)
        self.img = []
        for i, j in enumerate(resp["articles"]):

            news_title = j["title"]
            news_description = j["description"]
            news_author = j["author"]
            news_url = j["url"]
            news_publish = j["publishedAt"]
            self.textView.insert(tk.END, f"\n{i+1}. {news_title}:-\n")
            self.textView.insert(tk.END, f"\t{news_description}\n\n")
            self.textView.insert(tk.END, f"\tAuthor:- {news_author}\n\n")
            self.textView.insert(tk.END, f"\tTo know more Visit:- {news_url}\n\n")
            self.textView.insert(tk.END, f"\tPublished At:- {news_publish}\n\n")
            try:
                imageFile = Image.open(requests.get(
                    j["urlToImage"], stream=True).raw)
                self.img.append(ImageTk.PhotoImage(image=imageFile))
            except:
                pass
            else:
                try:
                    self.textView.window_create(
                        tk.END, window=tk.Label(self.textView, image=self.img[i]))
                except:
                    pass

if __name__ == "__main__":
    window = tk.Tk()
    screen = Window(window)
    window.mainloop()
