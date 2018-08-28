#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
import csv
import datetime


input_file = sys.argv[1]
DATE = "2018-08-28T"
TZONE = "+0100"

with open(input_file) as infile:
    data = csv.reader(infile, delimiter=',')
    for row in list(data)[1:]:
        #         boat,atempt nb, start, end, datafile, class
        boat = row[0]
        attempt = row[1]
        starttime = datetime.datetime.strptime(DATE+row[2]+ TZONE, "%Y-%m-%dT%H:%M%z")
        endtime = datetime.datetime.strptime(DATE+row[3]+ TZONE, "%Y-%m-%dT%H:%M%z")
        data_file = row[4]
        boat_class = row[5]
        splited_filename = boat + "_" + boat_class + "_attempt" + attempt + ".csv"

        with open(data_file) as data_file_reader: 
            data_reader = csv.reader(data_file_reader, delimiter=',')
            with open(splited_filename, 'w') as data_file_writer:
                data_writer = csv.writer(data_file_writer, delimiter=',')
                data_writer.writerow(next(data_reader))
                for in_data_row in data_reader:
                    in_time = datetime.datetime.strptime(in_data_row[0], "%Y-%m-%dT%H:%M:%S%z")
                    if (in_time > starttime) and (in_time < endtime):
                        data_writer.writerow(in_data_row)
        print("File " + splited_filename + " written")
        
