#!/usr/bin/env python
# -*- coding: utf-8 -*-
import zipfile
import os


class Zip:  # 需要生成一个以哈希命名的zip文件,并且返回文件的路径/文件名(保证每个人生成的压缩包不会被覆盖)
    @classmethod
    def zip(cls, path_name, name):
        startdir = path_name
        name =  name+".zip"
        file_name = path_name + "/" +name
        print("开始压缩")
        z = zipfile.ZipFile(file_name, 'w', zipfile.ZIP_DEFLATED)  # 文件名
        for dirpath, dirname, filenames in os.walk(startdir):
            fpath = dirpath.replace(startdir, '')
            fpath = fpath and fpath + os.sep or ''
            for filename in filenames:
                if filename != name:  # 如果它不叫这个名字,则给他搞进去
                    z.write(os.path.join(dirpath, filename), fpath + filename)
        z.close()
