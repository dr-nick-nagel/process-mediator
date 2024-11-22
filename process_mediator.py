import queue
import subprocess
import time
import sys
import os
from threading import Thread

class ProcessDirector :
    '''
    Responsible for spawning and directing processes to 
    execute python scripts. 
    '''
    def __init__ ( self ) : 
        self.processes = [] 
        self.t_queue = queue.Queue()

    def launch_process( self, python_script, cmd_ln_args ) : 
        '''
        Launch a process and add it to your list given...

        arguments: 
            python_script: name of script to launch
            cmd_lin_args: a sequence of command line 
            arguments...

        returns: the new process id. The client should hold onto it.
        '''
        launch_sequence = [ sys.executable, python_script ] + cmd_ln_args

        proc = subprocess.Popen(
            launch_sequence,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        self.processes.append( proc )

        t = Thread(
            target=self.read_proc_output,
            args=[proc.pid]
        )
        t.daemon = True
        t.start()

        return proc.pid

    def terminate_children( self ) : 
        '''
        Dispose of all spawned child processes
        '''
        for i in range( len( self.processes ) - 1, -1, -1 ) : 
            target = self.processes[i]
            target.terminate()
            target.wait()
            if target.returncode is not None:
                self.processes.pop( i )

    def read_proc_output( self, pid ) : 
        '''
        Read-loop target for read thread. Reads stdout of child 
        process given the process ID. Note: The pid enables the
        director to determine which pipe to read...

        Arguments: 
            pid: The pid (process id) of the process 
            (should be obtained on launch...) 
        '''
        for process in self.processes :
            if process.pid == pid :
                proc = process
        while True: 
            # sleep. otherwise you work too hard and heat up the box...
            time.sleep( 0.02 )

            output = proc.stdout.readline()
            if not output :
                continue
            self.t_queue.put( output )

    def send_input(self, pid, input_text):
        '''
        Send input to the specified process.

        Arguments:
          pid: Process id to send to
          input_text: text to send
        '''
        for process in self.processes :
            if process.pid == pid :
                proc = process
        proc.stdin.write(input_text + '\n')
        # proc.stdin.write(input_text)
        proc.stdin.flush()

    def process_q ( self ) : 
        '''
        This is the function clients should call to get data
        from the `process mediator`. The queue is expected to
        hold data accumulated since the last dequeue operation...
        '''
        output = ""
        while not self.t_queue.empty () :
            output += self.t_queue.get()
        return output
    
    def terminate( self, pid ) :
        '''
        Kill the specified process given ...

        Arguments: 
            pid : process id (obtained at launch)
        '''
        for i, process in enumerate( self.processes ) :
            if process.pid == pid :
                target = process
                target_idx = i
                break
        if not target :
            return
        target.terminate()
        target.wait()
        if target.returncode is not None:
            self.processes.pop( target_idx )


if __name__ == "__main__" : 
    print( "----    START TEST     ----" )
    CWD = os.getcwd()
    TEST_SCRIPT_NAME = CWD + "/nn_testscript.py"
    pd = ProcessDirector()
    test_proc_1_pid = pd.launch_process( TEST_SCRIPT_NAME, [ "TEST INSTANCE 1" ] )
    test_proc_2_pid = pd.launch_process( TEST_SCRIPT_NAME, [ "TEST INSTANCE 2" ] )

    print("TESTING. WAITA MINNIT...")
    time.sleep( 5 )
    print( f"Q SIZE PRE: {pd.t_queue.qsize()}" )
    test_output = pd.process_q()
    print( test_output )
    print( f"Q SIZE POST: {pd.t_queue.qsize()}" )
    
    pd.terminate_children()
    print( "----    END   TEST     ----" )
