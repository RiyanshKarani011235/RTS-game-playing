
using System;
using System.IO;
using System.IO.Pipes; 	// NamedPipeServerStream
using System.Text;
using System.Threading;

public class pipeServer {
	
	public static void Main() {
		// NamedPipeServerStream pipeServer = new NamedPipeServerStream("/tmp/myfifo1",PipeDirection.In);
		// pipeServer.WaitForConnection();
		// Console.WriteLine("connected");
		// RunShellCommand("ls","");
		// Console.WriteLine("--------------------");
		// string[] split_string = split("users/ironstein/desktop/");
		// for(int i = 0;i<split_string.Length;i++) {
		// 	if(split_string[i] == "") {
		// 		Console.WriteLine("-");
		// 	} else {
		// 		Console.WriteLine(split_string[i]);
		// 	}
		// }
		// Console.WriteLine("------------------");
		// Console.WriteLine();
		// StreamReader ss = new StreamReader(pipeServer);
		// // while(true) {
		// 	String filename = ss.ReadLine();
		// 	Console.WriteLine("got a reply {0}",filename);
		// // }

		getcwd();
	}

	public static void RunShellCommand(string command, String arguments) {

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

	public static string[] split(string str) {
		int count = 0;

		// type = 0 -->  a/b/c/d
		// type = 1 --> /a/b/c/d
		// type = 2 -->  a/b/c/d/
		// type = 3 --> /a/b/c/d/
		int type = 0;
		if(str[0] == '/') {
			type = 1;
		}
		if(str[str.Length - 1] == '/') {
			if(type == 1) {
				type = 3;
			} else {
				type = 2;
			}
		}
		for(int i=0;i<str.Length;i++) {
			if(str[i] == '/') {
				count += 1;
			}
		}

		int return_array_length = count + 1;
		string[] return_array = new string[return_array_length];
		int return_array_string_index = 0;

		string temp_string = "";
		for(int i=0;i<str.Length;i++) {
			if((str[i] == '/') | (i == str.Length-1)) {
				if((str[i] == '/') & (i == str.Length-1)) {
					return_array[return_array_string_index + 1] = "";
				} else if(i == str.Length - 1) {
					temp_string += str[i];
				}
				return_array[return_array_string_index] = temp_string;
				return_array_string_index += 1;
				temp_string = "";
			} else {
				temp_string += str[i];
			}
		}

		return return_array;

	}

	public static string getcwd() {
		string[] working_directory_list = split(System.IO.Directory.GetCurrentDirectory());
		for(int i=0;i<working_directory_list.Length;i++) {
			Console.WriteLine(working_directory_list[i]);
		} 
		return "";
	}
}
