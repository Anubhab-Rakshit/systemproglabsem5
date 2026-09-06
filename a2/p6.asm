.MODEL SMALL
.STACK 100H
.DATA
    fib DB 10 DUP(?)
.CODE
MAIN PROC
    MOV AX, @DATA
    MOV DS, AX

    MOV SI, OFFSET fib
    MOV AL, 0
    MOV [SI], AL
    INC SI
    
    MOV BL, 1
    MOV [SI], BL
    INC SI
    
    MOV CX, 8
L1:
    MOV DL, AL
    ADD DL, BL
    MOV [SI], DL
    INC SI
    MOV AL, BL
    MOV BL, DL
    LOOP L1

    MOV AH, 4CH
    INT 21H
MAIN ENDP
END MAIN
