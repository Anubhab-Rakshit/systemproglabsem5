.MODEL SMALL
.STACK 100H
.DATA
    num1 DW 1234H
    num2 DW 1000H
    sum DW ?
    diff DW ?
.CODE
MAIN PROC
    MOV AX, @DATA
    MOV DS, AX

    ; Add
    MOV AX, num1
    ADD AX, num2
    MOV sum, AX

    ; Subtract
    MOV AX, num1
    SUB AX, num2
    MOV diff, AX

    ; Exit
    MOV AH, 4CH
    INT 21H
MAIN ENDP
END MAIN
