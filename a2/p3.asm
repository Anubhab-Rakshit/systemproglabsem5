.MODEL SMALL
.STACK 100H
.DATA
    num1 DB 2
    num2 DB 98
    comma DB ', ', '$'
    newline DB 13, 10, '$'
.CODE
PRINT_NUM PROC
    MOV AH, 0
    MOV BL, 10
    DIV BL
    ADD AL, '0'
    MOV DL, AL
    MOV BH, AH
    MOV AH, 02H
    INT 21H
    MOV AL, BH
    ADD AL, '0'
    MOV DL, AL
    MOV AH, 02H
    INT 21H
    RET
PRINT_NUM ENDP

MAIN PROC
    MOV AX, @DATA
    MOV DS, AX

    MOV CX, 24
L1:
    MOV AL, num1
    CALL PRINT_NUM

    LEA DX, comma
    MOV AH, 09H
    INT 21H

    MOV AL, num2
    CALL PRINT_NUM

    LEA DX, newline
    MOV AH, 09H
    INT 21H

    ADD num1, 2
    SUB num2, 2
    LOOP L1

    MOV AH, 4CH
    INT 21H
MAIN ENDP
END MAIN
