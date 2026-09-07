.MODEL SMALL
.STACK 100H
.DATA
    arr DW 50, 20, 90, 10, 30
    msg1 DB 'Array before sort: 50 20 90 10 30', 13, 10, '$'
    msg2 DB 'Array after sort: $'
.CODE
MAIN PROC
    MOV AX, @DATA
    MOV DS, AX

    LEA DX, msg1
    MOV AH, 09H
    INT 21H

    MOV CX, 4
OUTER:
    MOV SI, OFFSET arr
    MOV DX, CX
INNER:
    MOV AX, [SI]
    CMP AX, [SI+2]
    JLE SKIP
    XCHG AX, [SI+2]
    MOV [SI], AX
SKIP:
    ADD SI, 2
    DEC DX
    JNZ INNER
    LOOP OUTER

    LEA DX, msg2
    MOV AH, 09H
    INT 21H

    MOV CX, 5
    MOV SI, OFFSET arr
PRINT_ARR:
    MOV AX, [SI]
    CALL PRINT_NUM
    MOV DL, ' '
    MOV AH, 02H
    INT 21H
    ADD SI, 2
    LOOP PRINT_ARR

    CALL NEWLINE
    MOV AH, 4CH
    INT 21H
MAIN ENDP

; Utility Procedures
GET_NUM PROC
    PUSH BX
    PUSH CX
    PUSH DX
    MOV BX, 0
    MOV CX, 10
    MOV AH, 01H
READ_CHAR:
    INT 21H
    CMP AL, 13
    JE END_GET_NUM
    CMP AL, 32
    JE END_GET_NUM
    SUB AL, '0'
    MOV AH, 0
    PUSH AX
    MOV AX, BX
    MUL CX
    POP DX
    ADD AX, DX
    MOV BX, AX
    MOV AH, 01H
    JMP READ_CHAR
END_GET_NUM:
    MOV AX, BX
    POP DX
    POP CX
    POP BX
    RET
GET_NUM ENDP

PRINT_NUM PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    CMP AX, 0
    JGE POSITIVE
    PUSH AX
    MOV DL, '-'
    MOV AH, 02H
    INT 21H
    POP AX
    NEG AX
POSITIVE:
    MOV CX, 0
    MOV BX, 10
DIV_LOOP:
    MOV DX, 0
    DIV BX
    PUSH DX
    INC CX
    CMP AX, 0
    JNE DIV_LOOP
PRINT_LOOP:
    POP DX
    ADD DL, '0'
    MOV AH, 02H
    INT 21H
    LOOP PRINT_LOOP
    POP DX
    POP CX
    POP BX
    POP AX
    RET
PRINT_NUM ENDP

NEWLINE PROC
    PUSH AX
    PUSH DX
    MOV DL, 13
    MOV AH, 02H
    INT 21H
    MOV DL, 10
    MOV AH, 02H
    INT 21H
    POP DX
    POP AX
    RET
NEWLINE ENDP
END MAIN
