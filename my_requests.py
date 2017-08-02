#!/usr/bin/env python3

from Bio import Entrez
import requests, requests_ftp
import xml.dom.minidom
import xml.etree.ElementTree as ET
import xml.etree.ElementTree as xml
import os, sys
from getpass import getpass
import ftplib, os, socket
from ftplib import FTP
import urllib, urllib3




def lag_line(): #test of cursor
    k=0
    for l in f:
        print("what i see from procedure", l)
        k +=1
        if k >2: break
    return

def get_xml_file_by_id(my_id = "200099461"):
	Entrez.email = 'alexey.solovyev@etu.univ-amu.fr'
	string_of_request = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=gds&id=' + my_id
	response = requests.get(string_of_request, timeout=1.001)
	
	return response
	
def get_gseID(line = '<Item Name="Accession" Type="String">GSE97956</Item>'):	
	my_from = line.index("GSE")
	my_till = line.rindex("</Item>")
	test = line[my_from:my_till]
	return test
	
def array_samples(my_file_xml, my_num):
	fuse = 0
	my_ind = 1
	rep = {}
	while my_ind <= my_num:
		if fuse > 600: break
		line1 = my_file_xml.readline()
		line2 = my_file_xml.readline()
		line3 = my_file_xml.readline()
		line4 = my_file_xml.readline()
		my_from = line1.index("GSM")
		my_till = line1.rindex("</Item>")
		my_number_of_sample = line1[my_from:my_till]
		my_from = line2.index('String')
		my_till = line2.rindex("</Item>")
		my_title_of_sample = line2[my_from+8:my_till]
		
		rep[my_number_of_sample] = my_title_of_sample
#		print ('what i see', my_number_of_sample, my_title_of_sample, fuse)
		fuse += 1
		my_ind += 1
		if '<Item Name="Relations" Type="List">' in line1: break
	return rep

def cut_file():
	my_big_file = open(os.path.join(os.path.dirname(__file__),'.','in_out','big_file.txt'))
	
	my_little_output = open(os.path.join(os.path.dirname(__file__),'.','in_out','bed_ID1.txt'), 'w')
	fuse_tmp = 0
	ind_file = 2
	for i in my_big_file.readlines():
		my_little_output.write(i)
		print(i, str(fuse_tmp))
		if fuse_tmp > 18:
			my_little_output.close()
			my_little_output = open(os.path.join(os.path.dirname(__file__),'.','in_out','bed_ID' + str(ind_file)+'.txt'), 'w')
			ind_file += 1
			fuse_tmp = -1
		fuse_tmp += 1


#	my_output = open('output.xml', 'w')
#	my_file.close()
	my_little_output.close()
	my_big_file.close() 
	return		

def build_file():
	
	first_file = int(input("Number of first file "))
	last_file = int(input("Number of last file "))
	big_output = open('./in_out/big_file_output.txt', 'w')
	
	for ind_tmp in range (first_file, last_file+1):
		input_tmp = open('./in_out/output' + str(ind_tmp) + '.txt')
		for l in input_tmp.readlines():
			text_for_file = l
			big_output.write(text_for_file)
		input_tmp.close()
	
	big_output.close()
	return

def main_test():
	first_file = int(input("Number of first file "))
	last_file = int(input("Number of last file "))
	for ind_tmp in range (first_file, last_file+1):
		name_of_proc_file = './in_out/bed_ID' + str(ind_tmp) + '.txt'
		name_of_xml_file = './in_out/output' + str(ind_tmp) + '.xml'
		name_of_txt_file = './in_out/output' + str(ind_tmp) + '.txt'
		print(name_of_proc_file)
		main(name_of_proc_file, name_of_xml_file, name_of_txt_file, ind_tmp)
	return

def main(name_of_proc_file = './in_out/bed_ID0.txt', name_of_xml_file = './in_out/output0.xml', name_of_txt_file = './in_out/output0.txt', count = 0):
	
	Entrez.email = 'alexey.solovyev@etu.univ-amu.fr'
	
#	my_file = open('bed_ID.txt')
#	my_output = open('output.xml', 'w')
#	my_output_txt = open('output.txt', 'w')

	my_file = open(name_of_proc_file)
	my_output = open(name_of_xml_file, 'w')
	my_output_txt = open(name_of_txt_file, 'w')
	my_output_big = open("./in_out/SuperSeries.txt", 'a')
	
	
	my_output.write('<?xml version="1.0" encoding="UTF-8" ?>' + '\n')
	my_output.write('<!DOCTYPE TableResult PUBLIC "-//NLM//DTD TableResult v1 //EN" "written by Solovyev Alexey">' + '\n')
	my_output.write('<TableResult>' + '\n')
	my_output.write('\t' + '<Item Name="Examples" Type="List">'+ '\n')
	#my_output.write('<DocSum>' + '\n')
	#my_output.write('</DocSum>' + '\n')
	
	global_count = 1

	for line_input in my_file.readlines():
		

#		my_output.write('\t\t' +'<Item Name="Exp" Type="Structure">'+ '\n')
#		text_for_file = '\t\t\t' + '<Id>' + line_input[0:9] + '</Id>'  + '\n'
#		my_output.write(text_for_file)

		acc_2000 = line_input[0:9]
		my_id = line_input[0:9]
		
		xml_file = get_xml_file_by_id(my_id).text
		
		my_f = open('snake.xml', 'w')
		text_for_file = xml_file
		text_for_file = text_for_file.encode('ascii', 'ignore').decode('ascii')
		my_f.write(text_for_file)
		my_f.close()
		
		number_of_line = 0
		my_file_xml = open('snake.xml')
		for l_tmp in my_file_xml: number_of_line += 1
		my_file_xml.close()	
		
				
		tree = ET.parse('snake.xml')
		root = tree.getroot()
		my_acc = root[0][1].text
		print()
		print(str(global_count) + " I begin to process the project",my_id, my_acc)
		global_count += 1
		
#		try:
#			how_samles = nt(root[0][19].text)
#		except:
#			print('I do not see folder ftp.ncbi.nlm.nih.gov' + wdir + ' so I pass this project')
#			ftp.quit()
#			continue
		

		if int(root[0][19].text) > 99:
			text_for_file = acc_2000 + " " + my_acc + '\n'
			my_output_big.write(text_for_file)
			print("This project is Super Series, I've added it in SuperSeries.txt")
			continue
		
		host = "ftp.ncbi.nlm.nih.gov"
			
		wdir_root = "/geo/series/" + my_acc[0:len(my_acc)-3]+ "nnn/" + my_acc + "/"
		print(wdir_root)
#		wdir = "/geo/series/" + my_acc[0:5]+ "nnn/" + my_acc + "/suppl/"
		wdir = wdir_root + "suppl/"
		
		
		
		
		ftp = FTP(host, 'anonymous', 'anonymous')
		ftp.set_pasv(1)

#		list_files = ftp.nlst(wdir)
		
		try:
			list_files = ftp.nlst(wdir)
		except:
			print('I do not see folder ftp.ncbi.nlm.nih.gov' + wdir + ' so I pass this project')
			ftp.quit()
			continue
		
		
		
#		print(len(list_files))
#		print(list_files)
		list_files_clear = []
		i_see_bed = False
	
		my_source = "ftp.ncbi.nlm.nih.gov" + "/geo/series/" + my_acc[0:5]+ "nnn/" + my_acc + "/suppl/" + my_acc + "_RAW.tar"
		for sim_files in list_files:
			my_from = sim_files.index("/suppl/")
			list_files_clear.append(sim_files[my_from+7:])
			if ".bed." in sim_files[my_from+7:] : 
				i_see_bed = True
				my_source = "ftp.ncbi.nlm.nih.gov" + sim_files
#				print(my_source)
#		print(list_files_clear)
		
		ind_filelist_txt = False
		bed_in_file = False
		

		
		if "filelist.txt" in list_files_clear: ind_filelist_txt = True
		
		if not i_see_bed and not ind_filelist_txt : 
			print ('I do not see any bed-files, nor filelist.txt so I pass this project')
			ftp.quit()
			continue
		
		if not i_see_bed and ind_filelist_txt: 
			print ('I do not see any bed-file, but I see filelist.txt so I load it')
			string_search = 'ftp://ftp.ncbi.nlm.nih.gov/geo/series/' + my_acc[0:5]+ 'nnn/' + my_acc + '/suppl/filelist.txt'
#			urllib.urlretrieve(string_search, 'filelist.txt')

			ftp1 = ftplib.FTP("ftp.ncbi.nlm.nih.gov")
			ftp1.login("anonymous", "anonymous")
			ftp1.cwd("/geo/series/"+my_acc[0:5] +"nnn/" + my_acc + "/suppl")


			try:
				ftp1.retrbinary("RETR " + "filelist.txt" ,open('filelist.txt', 'wb').write)
			except:
				print("Error")
			
			ftp1.quit()
			
			my_f_tmp = open('filelist.txt')
			for bed in my_f_tmp:
				if ".bed." in bed : bed_in_file = True
			my_f.close()	
			if not bed_in_file :
				print ("There are not any bed-files in the filelist.txt so I pass this project")
				ftp.quit()
				continue
		
		ftp.quit()
		
#		path = 'geo/series/GSE97nnn/GSE97956/suppl/'
		
		my_output_txt.write('\n')
		
		my_output.write('\t\t' +'<Item Name="Exp" Type="Structure">'+ '\n')
		text_for_file = '\t\t\t' + '<Id>' + acc_2000 + '</Id>'  + '\n'
		my_output.write(text_for_file)
		my_output_txt.write(acc_2000 + '|')
		
		
		text_for_file = '\t\t\t' + '<Accession>' + root[0][1].text + '</Accession>' + '\n'
		my_output.write(text_for_file)
		my_output_txt.write(root[0][1].text + '|')

		text_for_file = '\t\t\t' + '<OverallDesign>' + root[0][4].text + '</OverallDesign>' + '\n'
		my_output.write(text_for_file)
		
		
		text_for_file = '\t\t\t' + '<File>' + my_source + '</File>' + '\n'
		my_output.write(text_for_file)
		my_output_txt.write(my_source + '|')




		my_file_xml = open('snake.xml')
		samples = {}
		j = 0
#		for line in my_file_xml:

		while j <= number_of_line:
			line_xml = my_file_xml.readline()
			if '<Item Name="Samples" Type="List">' in line_xml: 
				print ("Number of samples for this project is", str(root[0][19].text))
				line_1 = my_file_xml.readline()
				samples = array_samples(my_file_xml, int(root[0][19].text))
#				my_output.write('\t\t\t' + str(array_samples(my_file_xml, int(root[0][19].text)))+'\n')
				my_output_txt.write('|' + str(samples)+'|')
				my_output.write('\t\t\t' + '<Item Name="Samples" Type="List">'+ '\n')
				ensemble_sample = set()
				sample_number = 0
				for sam in samples:
					my_output.write('\t\t\t\t' + '<Item Name="Sample" Type="Structure">'+ '\n')
					my_output.write('\t\t\t\t\t' + '<Item Name="Accession" Type="String">' + sam + '</Item>' + '\n')
					my_output.write('\t\t\t\t\t' + '<Item Name="Title" Type="String">' + samples[sam] + '</Item>' + '\n')
#					my_output_txt.write(samples[sam] + ',')
#					my_output.write('\t\t\t\t' + '</Item>'+ '\n')
					
					html_file = requests.get("https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=" + sam)

					my_f_html = open('snake.html', 'w')
					text_for_file = html_file.text
					text_for_file = text_for_file.encode('ascii', 'ignore').decode('ascii')
					my_f_html.write(text_for_file)
					my_f_html.close()
					
					gsm_html = open('snake.html')
							
					fuse_tis = 0
					fuse_tis_bool = 0
					fuse_tis_bool1 = 0
					
					test1 = " "
					test7 = " "
					test2 = " "
					
					while (fuse_tis_bool+fuse_tis_bool1<2) and fuse_tis < 1000:
						fuse_tis += 1
						l_html = gsm_html.readline()
#						print("new line" + l_html)
						

						if "<td nowrap>Source name</td>" in l_html:
							line_gsm_1 = gsm_html.readline()
#							for i in range(6): line_gsm_7 = gsm_html.readline()
#							
							fuse_tis_bool = 1

							my_from = line_gsm_1.index('<td style="text-align: justify">')
							my_till = line_gsm_1.rindex("<br></td>\n")
							test1 = line_gsm_1[my_from+32:my_till]
#							print(test1)
							
						if ">tissue:" in l_html:
							line_gsm_7 = gsm_html.readline()
							line_gsm_7 = l_html
							
							fuse_tis_bool1 = 1
#							print(line_gsm_7)
							
							my_from = line_gsm_7.index('>tissue:')
							my_till = line_gsm_7.index("<br>")
							test7 = line_gsm_7[my_from+9:my_till]
#							print("this tissue" + test7)
						
						if ">source:" in l_html:
							line_gsm_2 = gsm_html.readline()
							line_gsm_2 = l_html
							
							fuse_tis_bool1 = 1
							
							my_from = line_gsm_2.index('>source:')
							my_till = line_gsm_2.index("<br>")
							test2 = line_gsm_2[my_from+9:my_till]

			

							
#							try:
#								my_from = line_gsm_7.index('<td style="text-align: justify">tissue: ')
#							except:
#								print ("No tissue")
#								break
								
#							my_from = line_gsm_7.index('<td style="text-align: justify">tissue: ')
#							my_till = line_gsm_7.index("<br>")
#							test7 = line_gsm_7[my_from+40:my_till]
							
					sample_number += 1
					if (fuse_tis_bool+fuse_tis_bool1>1) : print("Sample number " + str(sample_number)+ " " + test1 + " " + test7 + " " + test2)
					
					gsm_html.close()
					
					if test1 <> " ": ensemble_sample.add(test1)
					if test7 <> " ": ensemble_sample.add(test7)
					if test2 <> " ": ensemble_sample.add(test2)
					
					my_output.write('\t\t\t\t\t' + '<Item Name="SourceName" Type="String">' + test1 + '</Item>' + '\n')
					my_output.write('\t\t\t\t\t' + '<Item Name="Tissue" Type="String">' + test7 + '</Item>' + '\n')
					my_output.write('\t\t\t\t' + '</Item>'+ '\n')
#					my_output_txt.write('|')
					
				my_output.write('\t\t\t' + '</Item>'+ '\n')
				list_ensemble_sample = []
				for tmp in ensemble_sample : list_ensemble_sample.append(tmp)
				my_output.write('\t\t\t' + '<Item Name="AnsembleSource" Type="String">' + str(list_ensemble_sample) + '</Item>' + '\n')
				my_output_txt.write(str(list_ensemble_sample) + '|\n')
			j+=1
#		my_output_txt.write('|')
		my_file_xml.close()	
		
		
#		html_file = requests.get("https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM2644385")
		
#		my_f_html = open('snake.html', 'w')
#		text_for_file = html_file.text
#		text_for_file = text_for_file.encode('ascii', 'ignore').decode('ascii')
#		my_f_html.write(text_for_file)
#		my_f_html.close()
		
#		gsm_html = open('snake.html')
				
#		fuse_tis = 0
#		fuse_tis_bool = True
#		while fuse_tis_bool and fuse_tis < 500:
#			fuse_tis += 1
#			l_html = gsm_html.readline()
#			print (l_html)
#			if "<td nowrap>Source name</td>" in l_html:
#				line_gsm_1 = gsm_html.readline()
#			
#				fuse_tis_bool = False
#				my_from = line_gsm_1.index('<td style="text-align: justify">')
#				my_till = line_gsm_1.rindex("<br></td>\n")
#				test = line_gsm_1[my_from+32:my_till]
#				print(test)
		
#		gsm_html.close()	
		
	
	
		
#		for child in root:
#			print(child.tag, child.attrib,root[0][1].text)
#			
#			text_for_file = '\t\t' + '<Accession>' + root[0][1].text + '</Accession>' + '\n'
#			my_output.write(text_for_file)
#			
#			for child1 in child:
#				
#				if child1.tag != 'Id': print('Print from cicle', child1.tag, child1.attrib, child1.attrib['Name'],)
				
		
		
		text_for_file = '\t\t' + '</Item>' + '\n'
		my_output.write(text_for_file)	
		
	
	my_output.write('</TableResult>')
	
	my_file.close()
	my_output.close()  
	my_output_txt.close()  
	my_output_big.close()
	
#    appt = ET.Element("appointment")
#    root.append("TableResult", "begin")
#    begin = ET.SubElement(appt, "begin")
#    begin.text = "1181251680"
#    uid = ET.SubElement(appt, "uid")
#    uid.text = "040000008200E000"
#    state = ET.SubElement(appt, "state")
    
    
#    tree = ET.ElementTree(root)

	
#	my_id = "200097956"


#	xml_file = get_xml_file_by_id(my_id).text
	#print(xml_file)
	   
#	my_file = open('snake.xml', 'w')
#	text_for_file = xml_file
#	text_for_file = text_for_file.encode('ascii', 'ignore').decode('ascii')
#	#print(text_for_file)
#	my_file.write(text_for_file)
#	my_file.close()


#	mapping = []


	return
	
	
	




if __name__ == "__main__":
#   main()
#	cut_file()
	main_test()
#	build_file()
    
