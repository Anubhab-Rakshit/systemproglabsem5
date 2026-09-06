.MODEL SMALL
.STACK 100H
.DATA
    dividend DW 0050H
    divisor DB 05H
    quotient DB ?
    remainder DB ?
.CODE
MAIN PROC
    MOV AX, @DATA
    MOV DS, AX

    MOV AX, dividend
    DIV divisor
    MOV quotient, AL
    MOV remainder, AH

    MOV AH, 4CH
    INT 21H
MAIN ENDP
END MAIN
