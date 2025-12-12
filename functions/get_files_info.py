import os



def get_files_info(working_directory, directory="."):

    try:
        #get the full path and check it's in the correct working dir
        fullpath = os.path.join(working_directory, directory)
        fullpath = os.path.abspath(fullpath)
        if not fullpath.startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(fullpath):
            return f'Error: "{directory}" is not a directory'
       # get the contents of directory
        dirlisting = os.listdir(fullpath)
        filelist = ''
        for file in dirlisting:
            fsize = os.path.getsize(os.path.join(fullpath, file))
            diryn = os.path.isdir(os.path.join(fullpath, file))
            filelist += (f'- {file}: file_size={fsize} bytes, is_dir={diryn}\n')

        return filelist

    except Exception as errmes:
        return f"Error: {errmes}"
