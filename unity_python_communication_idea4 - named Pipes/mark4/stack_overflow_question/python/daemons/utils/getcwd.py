
'''
returns the path of the the directory encompassing the 
"daemons" directory
'''

def getcwd() : 
    working_directory_list = __file__.split('/')
    working_directory = ''
    for element in working_directory_list : 
        if 'daemons' in element : 
            break
        else :  
            working_directory += element + '/'
    return working_directory 
    