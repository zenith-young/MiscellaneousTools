#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil


# File Operation

class FileSystemUtils:

    @staticmethod
    def init_folder(folder):
        if not os.path.exists(folder):
            os.makedirs(folder)
        else:
            FileSystemUtils.remove_all_files_and_folders(folder)

    @staticmethod
    def is_file(path):
        return os.path.isfile(path)

    @staticmethod
    def is_dir(path):
        return os.path.isdir(path)

    @staticmethod
    def get_file_name(file):
        return os.path.split(file)[1].split('.')[0]

    @staticmethod
    def get_file_ext(file):
        return os.path.splitext(file)[1]

    @staticmethod
    def list_all_files_recursively(folder):
        result = []
        for root, dirs, files in os.walk(folder):
            for name in files:
                result.append(os.path.join(root, name))
        return result

    @staticmethod
    def list_all_folders_recursively(folder):
        result = []
        for root, dirs, files in os.walk(folder):
            for name in dirs:
                result.append(os.path.join(root, name))
        return result

    @staticmethod
    def remove_all_files_and_folders(folder):
        for file in FileSystemUtils.list_all_files_recursively(folder):
            os.remove(file)
        for folder in FileSystemUtils.list_all_folders_recursively(folder):
            os.removedirs(folder)

    @staticmethod
    def copyFilesToFolder(source_files, target_folder):
        for file in source_files:
            shutil.copy(file, target_folder)
