.MODEL SMALL
.STACK 100H
.DATA
    hrs DB ?
    mins DB ?
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

    ; Get Time
    MOV AH, 2CH
    INT 21H
    MOV hrs, CH
    MOV mins, CL

    MOV AL, hrs
    CALL PRINT_NUM
    
    MOV DL, ':'
    MOV AH, 02H
    INT 21H

    MOV AL, mins
    CALL PRINT_NUM

    MOV AH, 4CH
    INT 21H
MAIN ENDP
END MAIN
