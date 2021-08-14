import os
import sys
import subprocess
import shutil

FFMPEG_COMMAND = ("ffmpeg", "-i")

def create_mp3_file_name(mp4_file_path:str, dest_directory:str)->str:
    file_name = os.path.splitext(os.path.basename(mp4_file_path))[0]
    if(dest_directory[-1] is os.sep):
        dest_directory = dest_directory[0:-1]
    return "{}.{}".format(os.path.join(dest_directory, file_name), "mp3")

def mp4_to_mp3(src_file: str, dest_directory: str):
    command = list(FFMPEG_COMMAND)
    command.append(src_file)

    dest_file_name = create_mp3_file_name(src_file, dest_directory)
    command.append(dest_file_name)

    subprocess.run(command)
    print("Convert {} to {}", src_file, dest_file_name)


def create_directory_tree(src_directory_path:str, dest_directory_path:str, file_function=None):
    for name in os.listdir(src_directory_path):
        if(os.path.isfile(os.path.join(src_directory_path, name))):
            if(file_function is not None):
                file_function(os.path.join(src_directory_path, name), dest_directory_path)
            else:
                shutil.copyfile(os.path.join(src_directory_path, name), os.path.join(dest_directory_path, name))

        elif(os.path.isdir(os.path.join(src_directory_path, name))):
            os.mkdir(os.path.join(dest_directory_path, name))
            create_directory_tree(os.path.join(src_directory_path, name), os.path.join(dest_directory_path, name), file_function)


if __name__ == '__main__':
    args = sys.argv

    if(len(args) < 4):
        raise ValueError("Usage: python {} <Source Directory> <Dest Directory>",args[0])

    src_path = args[1]
    dest_path = args[2]

    create_directory_tree(src_path, dest_path)