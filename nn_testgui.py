import tkinter as tk
import subprocess
import threading
import queue
import sys
import os

sys.path.insert(1, '/home/nick/project/nn_webcast/nnrtc')

from process_mediator import ProcessDirector

# class ProcessManager:
#     def __init__(self, script_name):
#         self.script_name = script_name
#         self.process = None
#         self.output_queue = queue.Queue()

#     def start_process(self):
#         """Start the process and thread to read output."""

#         print( f"====\nSTART PROCESS: {self.script_name}" )

#         # TODO: RESUME HERE! LOOK AT SUBPROCESSES IN PYTHON AND HOW IT WORKS...
#         # OPTION 1: USE THIS GUI AND INTEGRATE THE CURRENT TEST HARNESS AND nnfilexfer.py OR...
#         # OPTION 2: USE THE CURRENT TEST HARNESS AND INTEGRATE THIS GUI AND nnfilexfer.py...
#         # FLIP A FUCKIN' COIN AND PRAY...
#         # https://docs.python.org/3/library/subprocess.html#subprocess.Popen


#         self.process = subprocess.Popen(
#             [sys.executable, self.script_name, "Instance TBD"],
#             stdin=subprocess.PIPE,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             text=True,
#             bufsize=1  # line-buffered
#         )
#         threading.Thread(target=self.read_output, daemon=True).start()

#     def read_output(self):
#         """Read process output and put it in the queue."""
#         for line in self.process.stdout:
#             self.output_queue.put(line)
#         self.process.stdout.close()

#     def send_input(self, input_text):
#         """Send input to the process."""
#         if self.process:
#             self.process.stdin.write(input_text + '\n')
#             self.process.stdin.flush()

#     def get_output(self):
#         """Get the output from the queue if available."""
#         output = []
#         while not self.output_queue.empty():
#             output.append(self.output_queue.get())
#         return ''.join(output)

# Main application class with tkinter GUI
class App:
    def __init__( self, root ):
        self.root = root
        self.root.title("Read/Write Process Thread Example")
        # Instantiate a 'process mediator'
        self.process_mediator = ProcessDirector()
        # Create GUI elements
        self.text_output = tk.Text(root, wrap='word', height=20, width=40)
        self.text_output.pack(pady=5)
        self.entry_input = tk.Entry(root)
        self.entry_input.pack(pady=5)
        self.start_button1 = tk.Button( 
            root, 
            text="Launch Subprocess", 
            command=lambda:self.start_process( TEST_SCRIPT )
        )
        self.start_button1.pack( side=tk.LEFT, padx=5 )

        self.send_button1 = tk.Button(
            root, 
            text="Send Input", 
            command=self.send_input
        )
        self.send_button1.pack(side=tk.LEFT, padx=5)

        # Start updating output display
        self.update_output()

    def start_process(self, script_name):
        """Start the specified process."""
        self.subProcId = self.process_mediator.launch_process( 
            script_name, 
            ["TEST_PROCESS"] 
        )

    def send_input( self ):
        """Send input to the selected process."""
        input_text = self.entry_input.get()
        self.process_mediator.send_input( self.subProcId, input_text ) 
        self.entry_input.delete(0, tk.END)

    def update_output(self):
        """Update output view(s)."""
        if  hasattr( self, 'subProcId' ) :
            output = self.process_mediator.process_q()
            self.text_output.insert( tk.END, output )
        self.root.after(100, self.update_output)  # Update every 100ms

if __name__ == "__main__":
    TEST_SCRIPT = "nn_testscript.py"
    root = tk.Tk()
    print( "====    START GUI TEST    ====" )
    app = App(root)
    root.mainloop()
    print( "====    END GUI TEST    ====" )
