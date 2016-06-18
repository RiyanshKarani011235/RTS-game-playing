public class StringHandling {

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
}