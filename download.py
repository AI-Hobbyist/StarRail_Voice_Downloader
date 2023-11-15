from pathlib import Path
from subprocess import Popen
from hashlib import md5
from glob import glob
import re, json, os, argparse

dl = "ZH|EN|JP|KR"
skip = "VO_"
index = Path("./data/index.json").read_text(encoding="utf-8")

def get_versions():
    sup_ver = glob("./data/hashlist/*.txt")
    ver_list = []
    for vers in sup_ver:
        versions = os.path.basename(vers).replace(".txt","")
        ver_list.append(versions)
    ver = '|'.join(ver_list)
    return ver
versions = get_versions()

def is_in(want,content):
    if re.findall(want,content):
        return True
    else:
        return False

def hash_dl(hash,file):
    file_content = Path(f"{output_path}/{file}").read_bytes()
    fmd5 = md5(file_content)
    fmd5 = fmd5.hexdigest()
    if fmd5 == hash:
        return True
    else:
        return False
    
def dl_pck(version,dl_path,file_name):
        dl_link = f"https://autopatchcn.bhsr.com/asb/V{version}Live/{dl_path}/client/Windows/AudioBlock/{file_name}"
        p = Popen(f'".\lib\wget.exe" -P "{output_path}" {dl_link} -c',shell=True)
        p.wait()

def read_hash(lang_need,content):
    md5list = []
    for line in open(content):
        if is_in(lang_need,line) == True and is_in(skip,line) == False:
            line = line.replace("\n","")
            md5list.append(line)
    return md5list

def download(output,version,lang):
    content = Path(f"./data/hashlist/{version}.txt")
    dl_path = json.loads(index)
    if lang == "ZH":
        lang_need = "Chinese"
    elif lang == "EN":
        lang_need = "English"
    elif lang == "JP":
        lang_need = "Japanese"
    else:
        lang_need = "Korean"
    md5list = read_hash(lang_need,content)
    for file in md5list:
        file_info = json.loads(file)
        file_path = file_info['Path']
        file_hash = file_info['Md5']
        file_name = os.path.basename(file_path)
        output_file = Path(f"{output}/{file_name}")
        if is_in(lang_need,file_path):
            if output_file.exists() == False:
                if Path(output_path).exists() == False:
                    os.makedirs(output)
                dl_pck(version,dl_path[version],file_path)
            elif hash_dl(file_hash,file_name) == False:
                dl_pck(version,dl_path[version],file_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ver', type=str, help=f'版本({versions})', required=True)
    parser.add_argument('--lang', type=str, help=f'语言({dl})', required=True)
    parser.add_argument('--dst', type=str, help='下载目录', required=True)
    args = parser.parse_args()
    output_path = args.dst
    if is_in(versions,args.ver) == True:
        if is_in(dl,args.lang):
            download(output_path,args.ver,args.lang)
        else:
            print(f"不支持的语言。目前支持：{dl}")
            exit()
    else:
        print(f"不支持的版本，目前支持：{versions}")
        exit()