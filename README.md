# 2048 Solver
Use this solver to solve any 2048 game!

## Supports
- Currently Mac/Linux only, because I work only on its OS. If anyone wants Windows support, I will help with implementing it.
- Mobile support **isn't planned** because it isn't possible to simulate key presses there (without help of computer). 
- This solver works only on 4x4 field, but working with larger fields is planned.

## Before usage
- This project uses Tesseract to find numbers on the 2048 field. You'll need not only tot pip install it, but also **brew install**,
    more info in its repository: https://github.com/tesseract-ocr/tesseract.
- To select field, this project uses keyboard module, that **requires root rights**. 
    To run the code on Mac/Linux, paste *sudo python src/main.py* (with this repository as current working directory)

## Usage
After you run this successfully, instructions will pop up in terminal!