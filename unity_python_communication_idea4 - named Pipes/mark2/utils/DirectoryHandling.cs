using System;

public class DirectoryHandling {
	public static string GetCwd() {
		string[] working_directory_list = StringHandling.split(System.IO.Directory.GetCurrentDirectory());
		string working_directory = "";
		for(int i=0;i<working_directory_list.Length;i++) {
			string temp_string = "";
			for(int j=0;j<working_directory_list[i].Length;j++) {
				// if(working_directory_list[i][j] == ' ') {
				// 	temp_string += '\\';
				// }
				temp_string += working_directory_list[i][j];
			}
			working_directory += temp_string + '/';
		}

		// editing the working directory to remove the last '/' that causes the problem
		// when using - System.IO.Directory.SetCurrentDirectory(working_directory)
		string edited_working_directory = "";
		for(int i=0;i<working_directory.Length;i++) {
			if(!((i == working_directory.Length - 1) & (working_directory[i] == '/'))) {
				edited_working_directory += working_directory[i];
			}
		}
		return edited_working_directory;
	}
}