using System;
	
public class Shell {
	public static string RunShellCommand(string command, String arguments) {

		System.Diagnostics.ProcessStartInfo startInfo = new System.Diagnostics.ProcessStartInfo () {
			FileName = command,
			Arguments = arguments,
			UseShellExecute = false,
			RedirectStandardOutput = true,
			RedirectStandardError = true,
		};

		System.Diagnostics.Process proc = new System.Diagnostics.Process () {
			StartInfo = startInfo,
		};

		proc.Start ();
		proc.WaitForExit ();
		string return_string = "";
		while(! proc.StandardOutput.EndOfStream) {
			return_string += proc.StandardOutput.ReadLine();
		}
		return return_string;
	} 
}