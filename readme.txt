Instruction

1. To put in the folder:
	file "my_requests.py"
	folder "in_out"
2. In the folder "in_out":
	to put file/files "bed_ID*.txt"
	If you have one big file with numbers like "200084502" you can cut this file to small files. For this rename your file in "big_file.txt" and run "cut_file()" from "my_requests.py"

3. Run "main_test()" from "my_requests.py" using the range of file, for example "0" and "0", or "1" and "20". It depends on the quantity of your files in the folder "in_out".

4. The result of this script is a list of files named "output*.txt" and "output*.xml". If you wish to compile the files "output*.txt" in one file, run "build_file()" from "my_requests.py" using the range of file.

5. You will get "big_file_output.txt" with list of projects and the file “SuperSeries.txt” with list of “strange” projects.


