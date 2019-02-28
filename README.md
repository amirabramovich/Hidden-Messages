# Hidden-Messages
## Steganography
From Wikipedia, the free encyclopedia.

Steganography is the practice of concealing a file, message, image, or video within another file, message, image, or video. 
The word steganography combines the Greek words steganos (στεγανός), meaning "covered, concealed, or protected", and graphein (γράφειν) meaning "writing".

Concealing and Revealing Data in Images
=======================================
Each pixel from RGB image is composed of 3 values which are 8-bit values (the range is 0–255).
The right-most bit is the least significant bit. 
Meaning, changing the rightmost bit will result a maximum 1 value change in a range of 256 (it represents less than 1%).
In conclusion, changing the rightmost bit it will have almost no impact on the final value. 

Usage:
```
python steg.py 
```
(make sure the program can run as exetuable)

Options:
-----
1. Conceal Data in an Image :
    Select any file in your computer by giving its path.
    Select strong password in order to encrypt the data.
    The program will encrypt the data before the hiding using SHA256.
    Note: it will cause slightly increase in file size.
    Select large enough image to store the file in its LSBs.
2. Extract Data from an Image :
    Select any image in your computer by giving its path.
    Write the password in order to decrypt the hidden data.
    Select a name for the output file, if the password was correct, your file will be extracted.

You can use any type of file and store it in any type of image.
The only one rule is that the image should be slightly bigger than File's size.
