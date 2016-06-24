using System;
using System.IO.Pipes; 	// NamedPipeServerStream

public class test  {

	private static string working_directory;
	private static string name = "PlayerController1";
	public static System.IO.StreamReader pipe_reader;
	public static System.IO.StreamWriter pipe_writer;

	public static void Main() {
		awake();
		start();
	}

	private static void awake() {

		pipe pipe_ = Communication.InitializeCommunication(name);
		pipe_reader = pipe_.reader;
		pipe_writer = pipe_.writer;
		pipe _pipe_ = Communication.InitializeCommunication("PlayerController2");
	
	}

	private static void start() {
		string initialization_daemon_reply = Shell.RunShellCommand(
			"src/python/daemons/initialization_daemon.py","query temp");
		if(initialization_daemon_reply == "Daemon is running") {
			// first object whose start method is called
			Console.WriteLine("Daemon is still running");
			Shell.RunShellCommand(
				"src/python/daemons/initialization_daemon.py","stop temp");
			// run the main Python script now
		} else {
			Console.WriteLine("Daemon has already been stopped");
		}
	}
}	