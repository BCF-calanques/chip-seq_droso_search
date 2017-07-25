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
	
def main():
	
	Entrez.email = 'alexey.solovyev@etu.univ-amu.fr'
	
	my_file = open('bed_ID.txt')
	my_output = open('output.txt', 'w')
	
	
	my_output.write('<?xml version="1.0" encoding="UTF-8" ?>' + '\n')
	
	for line in my_file.readlines():
		print(get_xml_file_by_id(line))
		text_for_file = line[0:9] + " " + str(get_xml_file_by_id(line)) + '\n'
		my_output.write(text_for_file)
	
	my_file.close()
	my_output.close()   

	
	my_id = "200097956"


	xml_file = get_xml_file_by_id(my_id).text
	#print(xml_file)
	   
	my_file = open('snake.xml', 'w')
	text_for_file = xml_file
	text_for_file = text_for_file.encode('ascii', 'ignore').decode('ascii')
	#print(text_for_file)
	my_file.write(text_for_file)
	my_file.close()


	mapping = []

	j = 0
	my_file = open('snake.xml')
	for line in my_file:
		print ("what i see"+ line)
		if '<Item Name="Accession" Type="String">' in line:
			print(get_gseID(line))
			
		j+=1
		if j > 10: break
	my_file.close()
	string_of_request1 = requests.get('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=gds&id=200099461')
	print(string_of_request1.content)
	
	tree = ET.parse('snake.xml')
	root = tree.getroot()
	
	print(root.tag)
	print(root.attrib)
	
	for child in root:
		print(child.tag, child.attrib)
	
	return
	
	
	
	#print(response.content) print(get_gseID(line))

	#print()
	#print(response.text)

	#print()
	#print(response.url)

	#res2 = requests.get("https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM2644385")

	#print()
	#print(res2.text)
	#j = 0
	#for i in response.text:
	#    print ("what i see", i)
	#    j+=1
	#    if j > 5: break


	#j = 0
	#f = open('snake.txt')
	#for line in f:
	#    print ("what i see", line)
	#    j+=1
	#    if j > 10: break
	#f.close()

	#j = 0
	#f = open('snake.txt')
	#for line in f:
	#    print ("what i see", line)
	#    j+=1
	#    if j == 5 :
	#         lag_line()
	#    if j > 10: break
	#f.close()

from Bio import Entrez
import requests
import xml.dom.minidom
import xml.etree.ElementTree as ET


if __name__ == "__main__":
    main()
