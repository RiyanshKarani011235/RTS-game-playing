using System;

public class test  {

	private static string working_directory;

	private static void RunShellCommand(string working_directory, string command, String arguments) {

		System.Diagnostics.ProcessStartInfo startInfo = new System.Diagnostics.ProcessStartInfo () {
			FileName = command,
			Arguments = arguments,
		};

		System.Diagnostics.Process proc = new System.Diagnostics.Process () {
			StartInfo = startInfo,
		};

		proc.Start ();
		proc.WaitForExit ();
	}

	public static void Main() {
		awake();
	}

	private static void awake() {
		working_directory =  DirectoryHandling.GetCwd();
		System.IO.Directory.SetCurrentDirectory(working_directory);
		RunShellCommand(working_directory,"./src/python/test.py","");
	}
}