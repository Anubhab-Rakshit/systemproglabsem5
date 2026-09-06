.MODEL SMALL
.STACK 100H
.DATA
    arr DB 10, 20, 30, 40, 50
    key DB 30
    found DB 0
.CODE
MAIN PROC
    MOV AX, @DATA
    MOV DS, AX

    ; Linear search
    MOV CX, 5
    MOV SI, OFFSET arr
    MOV AL, key
SEARCH:
    CMP AL, [SI]
    JE FOUND_IT
    INC SI
    LOOP SEARCH
    JMP END_PROG
FOUND_IT:
    MOV found, 1
END_PROG:
    MOV AH, 4CH
    INT 21H
MAIN ENDP
END MAIN
