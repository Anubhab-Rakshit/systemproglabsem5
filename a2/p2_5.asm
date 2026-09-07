.MODEL SMALL
.STACK 100H
.DATA
    msg1 DB 'Enter 16-bit dividend: $'
    msg2 DB 'Enter 8-bit divisor: $'
    msg3 DB 'Quotient: $'
    msg4 DB 'Remainder: $'
    dividend DW ?
    divisor DB ?
.CODE
MAIN PROC
    MOV AX, @DATA
    MOV DS, AX

    LEA DX, msg1
    MOV AH, 09H
    INT 21H
    CALL GET_NUM
    MOV dividend, AX
    CALL NEWLINE

    LEA DX, msg2
    MOV AH, 09H
    INT 21H
    CALL GET_NUM
    MOV divisor, AL
    CALL NEWLINE

    MOV AX, dividend
    DIV divisor
    
    MOV BX, AX

    LEA DX, msg3
    MOV AH, 09H
    INT 21H
    MOV AL, BL
    MOV AH, 0
    CALL PRINT_NUM
    CALL NEWLINE

    LEA DX, msg4
    MOV AH, 09H
    INT 21H
    MOV AL, BH
    MOV AH, 0
    CALL PRINT_NUM
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
