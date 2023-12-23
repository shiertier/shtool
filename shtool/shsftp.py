#shsftp.py
import os
import paramiko
import threading
import time
import argparse
from . import shcheck

def sftp_transfer_thread(event, local_dirctory, remote_dirctory, url, port, username, password):
    shcheck.is_directory(local_dirctory)
    try:
        transport = paramiko.Transport((url, port))
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.chdir(remote_dirctory)
        files = sftp.listdir()
        for file in files:
            remote_file = os.path.join(remote_dirctory, file)
            local_file = os.path.join(local_dirctory, file)
            if not os.path.exists(local_file):
                sftp.get(remote_file, local_file)
                print(f"{local_file} 成功")
        sftp.close()
        transport.close()
    except Exception as e:
        print(f"sftp线程错误: {str(e)}")
        event.set()

def sftp_download_dirctory(local_dirctory, remote_dirctory, url, port, username, password):
    shcheck.is_directory(local_dirctory)
    shcheck.is_directory(remote_dirctory, False)
    try:
        transport = paramiko.Transport((url, port))
        transport.connect(username=username, password=password)

        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.chdir(remote_dirctory)
        files = sftp.listdir()
        os.makedirs(local_dirctory, exist_ok=True)

        thread_count = 3
        events = [threading.Event() for _ in range(thread_count)]
        threads = []

        for i in range(thread_count):
            t = threading.Thread(target=sftp_transfer_thread, args=(events[i], local_dirctory, remote_dirctory, url, port, username, password))
            threads.append(t)
            t.start()
            time.sleep(3)

        for event in events:
            event.wait()

        sftp.close()
        transport.close()

    except Exception as e:
        print(f"错误: {str(e)}")

def sftp_download_file(local_dirctory, remote_file, url, port, username, password):
    shcheck.is_directory(local_dirctory)
    shcheck.is_file(remote_file)
    try:
        transport = paramiko.Transport((url, port))
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        specific_file_name = os.path.basename(remote_file)
        local_file = os.path.join(local_dirctory, specific_file_name)
        sftp.get(remote_file, local_file)
        print(f"{local_file} 成功.")

        sftp.close()
        transport.close()

    except Exception as e:
        print(f"错误: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='SFTP下载工具')
    parser.add_argument("-u", '--url', type=str, help='SFTP的网址')
    parser.add_argument("-p", '--port', type=int, help='SFTP的端口')
    parser.add_argument("-n", '--name', type=str, help='SFTP的用户名')
    parser.add_argument("-pw", '--password', type=str, help='SFTP的密码')
    parser.add_argument("-f","--downfile", action='store_true', help='设置时保存指定文件')
    parser.add_argument("-d","--downdirectory", action='store_true', help='设置时保存指定目录')
    parser.add_argument("-s", '--save', type=str, help='保存的位置')
    args = parser.parse_args()

    if args.downfile:
        sftp_download_file(args.save, args.downfile, args.url, args.port, args.name, args.password)
    elif args.downdirectory:
        sftp_download_dirctory(args.save, args.downdirectory, args.url, args.port, args.name, args.password)
    else:
        print("错误: 请指定 --downfile 或 --downdirectory 中的一个选项。")

if __name__ == "__main__":
    main()
