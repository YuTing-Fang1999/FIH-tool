import os

def get_file_path_c7(project_path, file_path):
    return project_path + file_path

def get_file_path_c6(project_path, file_path):
    if not os.path.exists(project_path+'/src'):
        return project_path+'/src'
    project_name = os.listdir(project_path+'/src')[0]
    path = project_path + '/src/' + project_name + file_path
    
    if not os.path.exists(path):
        return path
    
    for f in os.listdir(path):
        if "snapshot" in f :
            path += f + '/'
            break
    for f in os.listdir(path):
        if ".h" in f :
            path += f 
            break
    return path