import struct
import numpy as np

from PIL import Image
from cipher import AESCipher


# Set the last bit of n to x
def set_bit(n, x):
	n &= -2
	if x:
		n |= 1
	return n

# Hide file into LSB bits of an image
def hide():
	# Open the binary file
	file_to_hide = raw_input("Enter path of file to hide:\n")
	f = open(file_to_hide, "rb")
	data = f.read()
	f.close()
	print "\033[92m" +'Hidden file size: {0} KB.'.format(round(len(data)/1024.0,2))+ "\033[0m"
		
	# Encrypt the binary file according the password
	password = raw_input("Enter password:\n")
	cipher = AESCipher(password)
	data = cipher.encrypt(data)
	
	# Pack the file's length in first 4 bytes, then the rest of the file.
	data = [ord(b) for b in struct.pack("i", len(data))] + [ord(b) for b in data]

	# Transform data from file_to_hide binary file into an array of bits
	data = np.array(data, dtype=np.uint8)
	hidden_file = np.unpackbits(data).tolist()
	
	# Append bits until multiple of 3
	while(len(hidden_file)%3):
		hidden_file.append(0)

	hidden_file_size = len(hidden_file)/(8.0*1024.0)
	print "\033[92m" +'Encrypted hidden file size: {0} KB.'.format(round(hidden_file_size,2))+ "\033[0m"
	
	# Open large enough image to hide the file in
	while(True):
		img_file = raw_input("Enter image path or exit:\n")
		if img_file == "exit":
			print "\033[92m" +'Bye Bye'+ "\033[0m"
			return
		img = Image.open(img_file)
		(width, height) = img.size
		hide_space = width*height*3.0/(8.0*1024.0) # max file_to_hide size
		print "\033[92m" +'Usable hiding space: {0} KB.'.format(round(hide_space,2))+ "\033[0m"
		
		if (hidden_file_size < hide_space - 4):
			break
		
		print "\033[91m" +'File too large for this image!'+ "\033[0m" , "\033[92m" +'Select different image!'+ "\033[0m"
	
	# Transform input image into RGB format
	rgb_img = img.convert("RGBA").getdata()
		
	# Create output image
	output_img = Image.new('RGBA',(width, height))
	data_img = output_img.getdata()

	index = 0
    # Iterate over all pixels of image and hide data
	for h in range(height):
		for w in range(width):
			(r, g, b, a) = rgb_img.getpixel((w, h))

			if index < len(hidden_file): # Change only the pixels which relates to hidden file
				r = set_bit(r, hidden_file[index])
				g = set_bit(g, hidden_file[index+1])
				b = set_bit(b, hidden_file[index+2])
			data_img.putpixel((w,h), (r, g, b, a))
			index += 3

	img_name = img_file.split('.', 1)[0]
	output_img.save(img_name + "-new.png", "PNG")
	
	print "\033[92m" +'{0} was hidden in {1}-new.png successfully!'.format(file_to_hide,img_name)+ "\033[0m"
        
# Extract data hidden to output file
def extract():
	img_file = raw_input("Enter image path:\n")
	img = Image.open(img_file)
	(width, height) = img.size
	rgb_img = img.convert("RGBA").getdata()

	# Extract LSBs
	hidden_bits = []
	for h in range(height):
		for w in range(width):
			(r, g, b, a) = rgb_img.getpixel((w, h))
			hidden_bits.append(r & 1)
			hidden_bits.append(g & 1)
			hidden_bits.append(b & 1)
			
        
	# Transform an array of bits into a binary file
	data = np.array(hidden_bits, dtype=np.uint8)
	hidden_file = "".join(map(chr, np.packbits(data).tolist()))
	hidden_file_size = struct.unpack("i", hidden_file[:4])[0]
	hidden_file = hidden_file[4: hidden_file_size + 4]

	# Decrypt the binary file according the password
	password = raw_input("Enter password:\n")
	cipher = AESCipher(password)
	hidden_file = cipher.decrypt(hidden_file)

	# Write decrypted data in output file
	output_name = raw_input("Enter output file name:\n")
	output_file = open(output_name, "wb")
	output_file.write(hidden_file)
	output_file.close()
	
	print "\033[92m" +'{0} was extracted from {1} successfully!'.format(output_name,img_file)+ "\033[0m"

def menu():
	print '\033[36m'+'\033[04m'+'\033[01m'+"Hide Files within Least Significant Bits of Images."+ "\033[0m"
	print '\033[36m'+"Author: Amir Abramovich"+ "\033[0m"
	print '\033[34m'+'\033[01m'+"Options:"+ "\033[0m"
	print '\033[33m'+"1 - Hide a file in an image" 
	print "2 - Extract file from an image" 
	print "3 - Exit" + "\033[0m"
	choice = raw_input("Please pick an option:\n")
	return choice

def main():
	choice = menu()	
	if choice == "1":		
		hide()
	elif choice == "2":
		extract()
	elif choice == "3":
		print "\033[92m" +'Bye Bye'+ "\033[0m"
	else:
		print "\033[91m" +'Invalid option'+ "\033[0m"
		main()
	
if __name__ == "__main__":
	main()
		
