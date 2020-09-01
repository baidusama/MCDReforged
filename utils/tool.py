# -*- coding: utf-8 -*-
import importlib.machinery
import importlib.util
import os
import re
import sys
import threading
from colorama import Fore, Back, Style
from utils import constant


def start_thread(func, args, name=None):
	thread = threading.Thread(target=func, args=args, name=name)
	thread.setDaemon(True)
	thread.start()
	return thread


def load_source(path, name=None):
	if name is None:
		name = path.replace('/', '_').replace('\\', '_').replace('.', '_')
	spec = importlib.util.spec_from_file_location(name, path)
	module = importlib.util.module_from_spec(spec)
	sys.modules[name] = module
	spec.loader.exec_module(module)
	return module


def list_file(folder, suffix):
	ret = []
	for file in os.listdir(folder):
		file_path = os.path.join(folder, file)
		if os.path.isfile(file_path) and file_path.endswith(suffix):
			ret.append(file_path)
	return ret


def touch_folder(folder):
	if not os.path.isdir(folder):
		os.makedirs(folder)


def unique_list(l):
	ret = list(set(l))
	ret.sort(key=l.index)
	return ret


def remove_suffix(text: str, suffix: str):
	pos = text.rfind(suffix)
	return text[:pos] if pos >= 0 else text


def get_all_base_class(cls):
	if cls is object:
		return []
	ret = [cls]
	for base in cls.__bases__:
		ret.extend(get_all_base_class(base))
	return unique_list(ret)


def clean_minecraft_color_code(text):
	return re.sub('§[\w0-9]', '', str(text))


def clean_console_color_code(text):
	return re.sub(r'\033\[(\d+(;\d+)?)?m', '', text)


def format_plugin_file_name(file_name):
	file_name = remove_suffix(file_name, constant.DISABLED_PLUGIN_FILE_SUFFIX)
	file_name = remove_suffix(file_name, constant.PLUGIN_FILE_SUFFIX)
	file_name += constant.PLUGIN_FILE_SUFFIX
	return file_name


def format_plugin_file_name_disabled(file_name):
	return format_plugin_file_name(file_name) + constant.DISABLED_PLUGIN_FILE_SUFFIX


def version_compare(v1, v2):
	"""
	Compare which version number is newer
	suffixes begin with "-" like "-alpha", "-beta" will be ignored

	:param v1: a version number like "0.4.5-alpha" or "1.2.0.10086"
	:param v2: the same as v1
	:return: a int. 1: v1 is newer; 0: they are the same; -1: v2 is newer
	"""
	def split_version(v):
		return tuple([int(x) for x in v.split('-')[0].split('.')])

	def cmp(a, b):
		if a < b:
			return -1
		elif a > b:
			return 1
		else:
			return 0
	v1 = split_version(v1)
	v2 = split_version(v2)
	for i in range(min(len(v1), len(v2))):
		if v1[i] != v2[i]:
			return cmp(v1[i], v2[i])
	else:
		return cmp(len(v1), len(v2))
