#!/usr/bin/python

import os
import sys
import string

"""
os.path.basename():
return the filename without all parent directories

os.listdir():
return the whole directory for the input directory

os.path.isdir():
return whether a input string is a dir or not


str.replace(a, b):
Inside the str. Replace the substring a with string b

"""


class tree_cmd(object):
	def __init__(self):
		self.dir_count = 0
		self.file_count = 0
		pass

	def get_tree(self, target_dir, option):
		target_list = self.get_list(target_dir, 0, option)
		#print target_list
		tree_list = []
		curr_layer = 0
		is_last_dir = [False]

		for i in range(len(target_list)):
			# process each path from the top layer iterately
			complete_filepath = target_list[i]
			filename = os.path.basename(complete_filepath)
			relative_filepath = complete_filepath.replace(target_dir, '')
			#print relative_filepath
			if complete_filepath == target_dir:
				# the root directory
				tree_list.append(complete_filepath + ' r')
				continue
			else:
				# inside a directory
				# layer starts from 1
				# is_last_layer[layer]
				names = relative_filepath.split('/')
				curr_layer = len(names)
				#if "screen-shot.png" in relative_filepath:
				print relative_filepath, curr_layer

				if len(is_last_dir) == curr_layer: # make len(is_last_dir) == curr_layer+1
					is_last_dir.append(False)
				else:
					is_last_dir[curr_layer] = False

				name = '|-- ' + filename
				# add a '`' to the last file in a directory
				pos = name.find('&')
				if pos >= 0:
					is_last_dir[curr_layer] = True
					tmp_pos = name.index('|')
					name = name[0:tmp_pos] + '`' + name[tmp_pos+1:pos]

				for j in reversed(range(1, curr_layer)): # curr_layer = 1 -> no indent
					if is_last_dir[j]:
						name = '    ' + name
					else:
						name = '|   ' + name
				tree_list.append(name)

		# print the formatted output
		for i in range(len(tree_list)):
			print tree_list[i]
		print "\n%d directories, %d files" %(self.dir_count, self.file_count)
		return

	def get_list(self, target_dir, layer, op):
		target_file_list = []
		if layer == 0:
			# add the root directory
			target_file_list.append(target_dir)
		# sort all names
		files = sorted(os.listdir(target_dir))
		last_file = None
		for file in files:
			if file[0] == '.':
				# filter out all invisible files
				continue
			
			complete_file = os.path.join(target_dir, file)
			if os.path.isdir(complete_file):
				# this is a dir
				self.dir_count += 1
				target_file_list.append(complete_file + ' *')
				target_file_list += self.get_list(complete_file, layer+1, op)
				last_file = complete_file + ' *'
			elif op == '-d':
				self.file_count += 1
				pass
			else:
				# this is a file
				self.file_count += 1
				target_file_list.append(complete_file)
				last_file = complete_file

		if last_file != None:
			marked_file = last_file + '&'
			pos = target_file_list.index(last_file)
			target_file_list[pos] = marked_file
		return target_file_list

	def show_helper(self, cmd):
		print 'Linux Tree Command:'
		print '    ' + cmd + 'dir'
		print 'For example:'
		print '    ' + cmd + '/Users/jianfeng/'
		return


def tree_cmd_tester():

	t = tree_cmd()

	if len(sys.argv) < 2:
		t.show_helper(sys.argv[0])
	else:
		op = None	
		target_dir = None
		if len(sys.argv) == 2:
			target_dir = sys.argv[1]
		elif len(sys.argv) == 3:
			op = sys.argv[1]
			target_dir = sys.argv[2]

		t.get_tree(target_dir, op)
	return


if __name__ == '__main__':
	tree_cmd_tester()