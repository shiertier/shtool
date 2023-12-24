#shzip.py
import argparse
import os
import pyzipper
from . import shcheck

def zip_file(file_path, output_directory=None, password="shiertier"):
    password = password.encode('utf-8') if password else None
    if output_directory is None:
        output_directory = os.getcwd()
    shcheck.is_file(file_path)
    shcheck.is_directory(output_directory)
    try:
        file_name, file_extension = os.path.splitext(os.path.basename(file_path))
        zipfile_name = f"{file_name}.zip"
        zip_file_path = os.path.join(output_directory, zipfile_name)
        with pyzipper.AESZipFile(zip_file_path, 'w', compression=pyzipper.ZIP_LZMA, encryption=pyzipper.WZ_AES) as zipf:
            if password:
                zipf.setpassword(password)
            zipf.write(file_path, arcname=file_name)
        print(f"文件 '{file_path}' 已加密并保存到 '{zip_file_path}'.")
    except Exception as e:
        print(f"发生了一个错误: {str(e)}")
        exit()

def zip_directory(directory_path, output_directory=None, password="shiertier"):
    password = password.encode('utf-8') if password else None
    if output_directory is None:
        output_directory = os.getcwd()
    shcheck.is_directory(directory_path)
    shcheck.is_directory(output_directory)
    try:
        directory_name = os.path.basename(directory_path)
        zipfile_name = directory_name + '.zip'
        zip_file_path = os.path.join(output_directory, zipfile_name)
        with pyzipper.AESZipFile(zip_file_path, 'w', compression=pyzipper.ZIP_LZMA, encryption=pyzipper.WZ_AES) as zipf:
            if password:
                zipf.setpassword(password)
            for root, _, files in os.walk(directory_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, directory_path)
                    zipf.write(file_path, arcname=arcname)
        print(f"路径 '{directory_name}' 已加密并保存到 '{zip_file_path}'.")
    except Exception as e:
        print(f"发生了一个错误: {str(e)}")
        exit()

def unzip_zipfile(zip_path, output_directory=None, password="shiertier"):
    password = password.encode('utf-8') if password else None
    shcheck.is_zip_file(zip_path)
    if output_directory is None:
        output_directory = os.getcwd()
    shcheck.is_directory(output_directory)
    with pyzipper.AESZipFile(zip_path, 'r', compression=pyzipper.ZIP_LZMA, encryption=pyzipper.WZ_AES) as zipf:
        if password:
            zipf.setpassword(password)
        zipf.extractall(output_directory)

        
def main():
    parser = argparse.ArgumentParser(description="Encrypt, compress, and decrypt specified archives.")
    parser.add_argument("-u", "--unzip", metavar="DIRECTORY_PATH", help="Unzip specified directory")
    parser.add_argument("-z1", "--zipfile", metavar="FILE_PATH", help="Zip specified file")
    parser.add_argument("-z", "--zipdirectory", metavar="DIRECTORY_PATH", help="Zip specified directory")
    parser.add_argument("-p", "--password", metavar="PASSWORD", default="shiertier",
                        help="Set password for encryption (default: shiertier)")
    parser.add_argument("-n", "--nopassword", action="store_true",
                        help="Perform compression or decompression without password")
    parser.add_argument("-o", "--output", metavar="OUTPUT_DIRECTORY_PATH", default=None,
                        help="Specify output path for compressed or decompressed files")

    args = parser.parse_args()
    
    if args.nopassword and args.password:
        print("错误: -n/--nopassword and -p/--password 不能同时使用.")
        exit()
        
    password = args.password if not args.nopassword else None
    
    if sum(1 for flag in [args.unzip, args.zipfile, args.zipdirectory] if flag) != 1:
        print("错误: 选项必须指定其中之一且仅能指定一个：-u/--unzip, -z1/--zipfile, -z/--zipdirectory.")
        exit()

    try:
        if args.unzip:
            unzip_zipfile(args.unzip, args.output, password)

        elif args.zipfile:
            zip_file(args.zipfile, args.output, password)

        elif args.zipdirectory:
            zip_directory(args.zipdirectory, args.output, password)

    except Exception as e:
        print(f"发生错误: {str(e)}")
        exit()

if __name__ == "__main__":
    main()
