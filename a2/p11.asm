.MODEL SMALL
.STACK 100H
.DATA
    arr DB 5, 2, 9, 1, 3
.CODE
MAIN PROC
    MOV AX, @DATA
    MOV DS, AX

    ; Selection sort logic
    MOV CX, 4
OUTER:
    MOV SI, OFFSET arr
    MOV DX, CX
INNER:
    MOV AL, [SI]
    CMP AL, [SI+1]
    JLE SKIP
    XCHG AL, [SI+1]
    MOV [SI], AL
SKIP:
    INC SI
    DEC DX
    JNZ INNER
    LOOP OUTER

    MOV AH, 4CH
    INT 21H
MAIN ENDP
END MAIN
