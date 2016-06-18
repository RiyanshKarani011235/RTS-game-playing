using System;
using System.IO.Pipes; 	// NamedPipeServerStream

public class test  {

	private static string name = "PlayerController1";
	public static System.IO.StreamReader pipe_reader;
	public static System.IO.StreamWriter pipe_writer;

	public static void Main() {
		awake();
	}

	private static void awake() {

		NamedPipeServerStream read_pipe;
		NamedPipeServerStream write_pipe;
		// System.IO.StreamReader pipe_reader;
		// System.IO.StreamWriter pipe_writer;

		// setting up and cleaning the working directory
		string initialization_daemon_reply;
		try {
			initialization_daemon_reply = Shell.RunShellCommand(
				"src/python/daemons/initialization_daemon.py","query temp");
		} catch(System.ComponentModel.Win32Exception) {
			// changing working_directory
			string working_directory =  DirectoryHandling.GetCwd();
			System.IO.Directory.SetCurrentDirectory(working_directory);	
			Console.WriteLine(working_directory);
			// cleaning up previous daemons
			Shell.RunShellCommand("src/python/daemons/utils/cleanup_daemons.py",""); 
			initialization_daemon_reply = Shell.RunShellCommand(
				"src/python/daemons/initialization_daemon.py","query temp");
		}
		if(initialization_daemon_reply == "Daemon is not running") {
			// clean /tmp/unity folder before using
			Shell.RunShellCommand("src/python/daemons/utils/cleanup_daemons.py","");
			// if you get an error here, it means that the file is not executable
			Console.WriteLine("Daemon is not running.\nCleaning /tmp/unity directory");
			Shell.RunShellCommand("rm","-r /tmp/unity");
			Shell.RunShellCommand("mkdir","/tmp/unity");

			Shell.RunShellCommand(
				"src/python/daemons/initialization_daemon.py","start temp");
		} else {
			Console.WriteLine("Daemon is already running");
		}

		// initialization of pipes
		string write_pipe_path = "/tmp/unity/" + name + "_unity_object_write_pipe";
		string read_pipe_path = "/tmp/unity/" + name + "_unity_object_read_pipe";
		Shell.RunShellCommand("mkfifo",read_pipe_path);
		Shell.RunShellCommand("mkfifo",write_pipe_path);
		read_pipe = new NamedPipeServerStream(read_pipe_path,PipeDirection.In);
		write_pipe = new NamedPipeServerStream(write_pipe_path,PipeDirection.Out);

		// open the pipe and wait for Python to connect
		Shell.RunShellCommand("src/python/daemons/unity_communication_daemon.py","start " + objectName);
		read_pipe.WaitForConnection();
		Console.WriteLine("read pipe is now open");
		write_pipe.WaitForConnection();
		Console.WriteLine("write pipe is now open");

		pipe_reader = new System.IO.StreamReader(read_pipe);
        pipe_writer = new System.IO.StreamWriter(write_pipe);

		// handshaking
		Console.WriteLine("got a signal : " + pipe_reader.ReadLine());  // READ
		pipe_writer.WriteLine("hello there\n");
		pipe_writer.Flush();											// WRITE
		Console.WriteLine("data has been written. Waiting for reply");
		Console.WriteLine(pipe_reader.Read());							// READ
		Console.WriteLine("connected");
		Log("connected");
	
	}

}	