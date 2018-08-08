import json

from elasticsearch import Elasticsearch

from ES_Manager import ES_Manager
import names
import random
import base64
import os

from Project.MyFlaskApp.validate import validate_date, validate_location

esm = ES_Manager('a7x')
path = 'C:\\Users\\nadav.ostrowsky\\PycharmProjects\\DHCS\\Project\\a7x jsons'
# directory = path + '\\songs'
# for filename in os.listdir(directory):
#     sub_directory = directory + '\\' + filename
#     for sub_filename in os.listdir(sub_directory):
#         file_name = sub_directory + '\\' + sub_filename
#         with open(file_name, 'r') as f:
#             json_str = f.read()
#             try:
#                 esm.new_song(json_str)
#             except Exception as e:
#                 pass
# directory = path + '\\albums'
# for filename in os.listdir(directory):
#     file_name = directory + '\\' + filename
#     with open(file_name, 'r') as f:
#         json_str = f.read()
#         try:
#             esm.new_album(json_str)
#         except:
#             pass
# directory = path + '\\concerts'
# for filename in os.listdir(directory):
#     file_name = directory + '\\' + filename
#     with open(file_name, 'r') as f:
#         json_str = f.read()
#         try:
#             esm.new_concert(json_str)
#         except:
#             pass



# es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
# #
# # es.indices.delete(index='album', ignore=[400, 404])
#
# results = esm.get_album_distribution('2018')
# print results
# print
# for res in results:
#     print res
# print
# print len(results)
#
#


print validate_location("Lover Kemping, Sopron, Hungary  ")