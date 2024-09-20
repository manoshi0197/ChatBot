import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import chatbot
from chatbot import *

class ChatApplication:
    def __init__(self, window):
        self.window = window
        window.title("Chat window for covid-19")
        window.geometry("800x800")
        window.resizable(True, True)
        window.configure(bg='#f8f8f8')

        # Create a frame to hold the message display and entry widgets
        self.frame1 = tk.Frame(window, bg='#f8f8f8')
        self.frame1.grid(column=0, row=0, padx=10, pady=10, sticky="nsew")
        self.frame1.rowconfigure(1, weight=1)

        # Create a label to display the title
        self.heading_name_chatbot = tk.Label(self.frame1, text="Chat Application", font=("Times New Roman", 28, "bold"), fg="#0C1F40", bg='#f8f8f8')
        self.heading_name_chatbot.grid(column=0, row=0, padx=10, pady=10, sticky="w")

        # Create a frame to hold the message display widgets
        self.frame2_content = tk.Frame(self.frame1, bg='#f8f8f8')
        self.frame2_content.grid(column=0, row=1, padx=10, pady=10, sticky="nsew")
        self.frame2_content.rowconfigure(0, weight=1)
        self.frame2_content.columnconfigure(0, weight=1)

        """ # Create a scrolled text box to display messages
        self.conversation_scroll = scrolledtext.ScrolledText(self.frame2_content, width=50, height=20, font=("Times New Roman", 12), bg='#f8f8f8', fg='#0C1F40')
        self.conversation_scroll.grid(column=0, row=0, sticky="nsew") """

        # Create a frame to hold the message entry widgets
        self.first_message_frame2 = tk.Frame(self.frame1, bg='#f8f8f8')
        self.first_message_frame2.grid(column=0, row=2, padx=10, pady=10, sticky="nsew")

         # Create a scrolled text box to display messages
        self.conversation_scroll = scrolledtext.ScrolledText(self.frame2_content, width=50, height=20, font=("Times New Roman", 12), bg='#f8f8f8', fg='white')
        self.conversation_scroll.grid(column=0, row=0, sticky="nsew")
        
        # Add a scrollbar to the message display widget
        self.scrollbar = ttk.Scrollbar(self.frame2_content, orient="vertical", command=self.conversation_scroll.yview)
        self.scrollbar.grid(column=1, row=0, sticky="ns")
        self.conversation_scroll.config(yscrollcommand=self.scrollbar.set, wrap="word")


        # Create a text box to enter messages
        self.message_input = tk.Entry(self.first_message_frame2, width=50, font=("Times New Roman", 12), bd=0, highlightthickness=1, highlightbackground='#0C1F40')
        self.message_input.grid(column=0, row=0, padx=10, pady=10, sticky="w")

        # Create a button to send messages
        self.send_button = tk.Button(self.first_message_frame2, text="Send", font=("Times New Roman", 12, "bold"), bg='#0C1F40', fg='white', bd=0, highlightthickness=1, highlightbackground='#0C1F40', command=self.send_message)
        self.send_button.grid(column=1, row=0, padx=10, pady=10, sticky="e")
        """ window.bind('<Return>',self.send_message) """

    

    def send_message(self):
        message = self.message_input.get()
        self.message_input.delete(0, tk.END)

        # Create a jumbotron-style message container
        frame2_content = tk.Frame(self.conversation_scroll, bg='#f8f8f8', bd=1, relief='solid', highlightthickness=1, highlightbackground='#0C1F40')
        frame2_content.pack(fill='x', padx=10, pady=5, anchor='nw')

        # Add the message to the message container
        message_label = tk.Label(frame2_content, text="You: " + message, font=("Times New Roman", 12), bg='#f8f8f8', fg='#0C1F40')
        message_label.pack(side='left', padx=5, pady=5, anchor='nw')

        # Scroll the message display to the bottom
        self.conversation_scroll.see(tk.END)
        botResponse = chatbot.response(message);
        self.bot_message(botResponse);

    def bot_message(self,userMessage):
        message = userMessage
        self.message_input.delete(0, tk.END)

        # Create a jumbotron-style message container
        frame2_content = tk.Frame(self.conversation_scroll, bg='#f8f8f8', bd=1, relief='solid', highlightthickness=1, highlightbackground='#0C1F40')
        frame2_content.pack(fill='x', padx=10, pady=5, anchor='nw')

        # Add the message to the message container
        message_label = tk.Label(frame2_content, text="BOT: " + message, font=("Times New Roman", 12), bg='#f8f8f8', fg='#0C1F40')
        message_label.pack(side='left', padx=5, pady=5, anchor='nw')

        # Scroll the message display to the bottom
        self.conversation_scroll.see(tk.END)


root = tk.Tk()
chat_app = ChatApplication(root)
root.mainloop()

        