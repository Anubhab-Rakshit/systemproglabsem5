Assignment 3 - Simulator Test Cases
Here are comprehensive input sets for each of the scripts to thoroughly test their features, including edge cases!

p3_1.py - One Pass Assembler (Calculator)
Tests standard math, register-to-register operations, and edge cases like dividing by zero.

Input Sequence:

text

LOAD R1, 10
LOAD R2, 0
ADD R1, 5
SUB R1, 2
MUL R1, R1
DIV R1, R2
LOAD R2, 3
DIV R1, R2
PRINT R1
EXIT
(Notice how the DIV R1, R2 catches the Divide by Zero error safely before you load 3 into R2!)

p3_2.py - Two Pass Assembler (Loop Constructs)
Tests single loops, nested loops (FOR inside WHILE), and symbol table generation accuracy.

Input Sequence:

text

LOAD R1, 0
WHILE R1 < 10
ADD R1, 1
FOR R2 = 0, R2 < 5, R2++
ADD R3, 2
ENDFOR
ENDWHILE
COMPILE
(When you type COMPILE, watch how Pass 1 builds the symbol table with L_START and L_END labels, and Pass 2 translates them into accurate JMP memory addresses.)

p3_3.py - Macro Processor
Tests macro definition, argument substitution, and expanding macros inside normal code.

Input Sequence:

text

MACRO ADD_THREE &A, &B, &C
LOAD R1, &A
ADD R1, &B
ADD R1, &C
MEND
LOAD R2, 0
ADD_THREE 5, 10, 15
ADD_THREE X, Y, Z
COMPILE
(Notice how Pass 1 stores the MACRO in the MNT and MDT tables without executing it, and Pass 2 flawlessly expands the variables via the Argument List Array!)

p3_4.py - Text Editor Simulator
A sequence of menu choices to test appending, out-of-bounds deletion, and file saving/loading.

Action Sequence:

Select 2 (Append) -> Type Line 1
Select 2 (Append) -> Type Line 2
Select 3 (Insert) -> Index: 0, Text: Header
Select 1 (View) -> You should see Header, Line 1, Line 2
Select 4 (Delete) -> Index: 99 -> Should catch Out of Bounds error
Select 4 (Delete) -> Index: 1 -> Deletes Line 1
Select 5 (Save) -> Filename: test_doc.txt
Select 7 (Clear)
Select 6 (Open) -> Filename: test_doc.txt -> File loaded!
Select 1 (View) -> You should see your text restored.
Select 8 (Exit)
p3_5.py - Bangla Phonetic Keyboard
Tests phonetic combinations, vowels, raw numbers, and unmapped spaces/punctuation.

Input Sequence:

text

ami banglay gan gai
k kotha bolche?
amader desh 123
EXIT
p3_6.py - Hindi Phonetic Keyboard
Tests Devanagari translation mappings and punctuation passthrough.

Input Sequence:

text

mera nam kya hai
tum kaise ho?
1234
EXIT
p3_7.py - Linker & Loader

How many object modules do you want to link together?: 3

--- Define Object Module 1 ---
Enter name: main.o
Enter size: 200
Enter an EXPORTED symbol name: (Just press Enter)
Enter an IMPORTED symbol name: MATH_ADD
At what relative offsets is 'MATH_ADD' referenced?: 50, 120
Enter an IMPORTED symbol name: (Just press Enter)

--- Define Object Module 2 ---
Enter name: math.o
Enter size: 150
Enter an EXPORTED symbol name: MATH_ADD
At what relative offset is 'MATH_ADD' located?: 40
Enter an EXPORTED symbol name: (Just press Enter)
Enter an IMPORTED symbol name: SYS_PRINT
At what relative offsets is 'SYS_PRINT' referenced?: 100
Enter an IMPORTED symbol name: (Just press Enter)

--- Define Object Module 3 ---
Enter name: sys.o
Enter size: 300
Enter an EXPORTED symbol name: SYS_PRINT
At what relative offset is 'SYS_PRINT' located?: 10
Enter an EXPORTED symbol name: (Just press Enter)
Enter an IMPORTED symbol name: (Just press Enter)


