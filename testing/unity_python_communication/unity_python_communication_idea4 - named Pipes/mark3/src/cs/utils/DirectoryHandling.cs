using System;

public class DirectoryHandling {
	public static string GetCwd() {
		// depth of the directory inside the working directory
		int directory_depth = 2;

		string[] working_directory_list = StringHandling.split(System.IO.Directory.GetCurrentDirectory(),'/');
		string working_directory = "";
		for(int i=0;i<working_directory_list.Length - directory_depth + 1;i++) {
			working_directory += working_directory_list[i];
			working_directory += '/';
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