import sys
import os
import requests
import re

def get_dir_name(regex, url):
        result = re.findall(regex, url)
        dir_name ="_".join(result[0])
        print(dir_name)
        return dir_name

def create_dir(name):
        try:
                print('Creating directory', name)
                os.mkdir(name)
                print('Created directory', name)
        except FileExistsError:
                print('Unable to create!', name, 'already exists!')
        return name

def download_image(img_url, file_name):
        r = requests.get(img_url)
        with open(file_name, 'wb') as f:
                f.write(r.content)

def html_file(web_url):
        result = requests.get(web_url)
        if result.ok is False:
                sys.exit(1)
        result = result.text
        return result


def process():
        main_dir = create_dir('dimik_pub')
##        print(type(main_dir))
##        print(main_dir)
        html_text = html_file('http://dimik.pub')
        data_pat = re.compile(r'<div class="book-cover">\s*<a href="(.*?)">\s*<img src="(.*?)">.*?<h2 class="sd-title"><.*?>(.*?)<', re.S)
        dir_pat = re.compile(r'book/(\d+)/(\w+)-(\w+)-')
        result = data_pat.findall(html_text)

        for item in result:
                name = item[2]
                url = item[0]
                img_url = item[1]

                dir_name = main_dir + '/' + get_dir_name(dir_pat, url)
                file_name = dir_name + '/' + 'information.txt'
                photo_name = dir_name + '/' + 'image.jpg'

                create_dir(dir_name)

                with open(file_name, 'w') as f:
                        f.write(name+'\n')
                        f.write(url+'\n')
                        f.write(img_url+'\n')

                download_image(img_url, photo_name)

if __name__ == '__main__':
        process()

