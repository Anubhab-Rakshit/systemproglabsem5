.MODEL SMALL
.STACK 100H
.DATA
    num DB 2
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
    MOV DL, ' '
    MOV AH, 02H
    INT 21H
    RET
PRINT_NUM ENDP

MAIN PROC
    MOV AX, @DATA
    MOV DS, AX

    MOV num, 2
OUTER:
    MOV AL, num
    CMP AL, 100
    JG DONE
    
    ; check if prime
    MOV BL, 2
INNER:
    CMP BL, num
    JE IS_PRIME
    MOV AH, 0
    MOV AL, num
    DIV BL
    CMP AH, 0
    JE NOT_PRIME
    INC BL
    JMP INNER

IS_PRIME:
    MOV AL, num
    CALL PRINT_NUM

NOT_PRIME:
    INC num
    JMP OUTER
DONE:
    MOV AH, 4CH
    INT 21H
MAIN ENDP
END MAIN
