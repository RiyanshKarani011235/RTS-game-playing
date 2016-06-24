
class object_class : 
    def __init__(self,name) : 
        self.name = name
    def __print__(self) : 
        # ensuring that the name is the first value printed
        print('name : ' + self.name)
        for element in self.__dict__.keys() : 
            if element != 'name' : 
                print(element + ' : ' + self.__dict__[element])

def parse_file(object_name,string) : 
    def remove_spaces(string) : 
        return_string = ''
        for character in string : 
            if character != ' ' : 
                return_string += character
        return return_string
    
    return_object = object_class(object_name)
    
    lines = string.split('\n')
    for line in lines : 
        name,value = [remove_spaces(string) for string in line.split('=')]
        setattr(return_object,name,value)
    return return_object

def read(file_path) : 
    string = ''
    with open(file_path) as file : 
        string += file.read()
    
    return_object = parse_file(file_path.split('/')[-1],string)
    return return_object