.MODEL SMALL
.STACK 100H
.DATA
    msg1 DB 'Enter a 4-bit binary number (e.g. 1010): $'
    msg2 DB 'Decimal equivalent: $'
    msg3 DB 'Enter a decimal number (0-15): $'
    msg4 DB 'Binary equivalent: $'
    bin_str DB 10 DUP('$')
.CODE
MAIN PROC
    MOV AX, @DATA
    MOV DS, AX

    LEA DX, msg1
    MOV AH, 09H
    INT 21H
    
    ; Read 4 characters
    MOV CX, 4
    MOV AH, 01H
    MOV BX, 0
READ_BIN:
    INT 21H
    SUB AL, '0'
    SHL BX, 1
    MOV AH, 0
    ADD BX, AX
    MOV AH, 01H
    LOOP READ_BIN
    CALL NEWLINE

    LEA DX, msg2
    MOV AH, 09H
    INT 21H
    MOV AX, BX
    CALL PRINT_NUM
    CALL NEWLINE

    LEA DX, msg3
    MOV AH, 09H
    INT 21H
    CALL GET_NUM
    MOV BX, AX
    CALL NEWLINE

    LEA DX, msg4
    MOV AH, 09H
    INT 21H
    
    MOV CX, 4
PRINT_BIN:
    ROL BL, 1
    MOV DL, BL
    AND DL, 1
    ADD DL, '0'
    MOV AH, 02H
    INT 21H
    LOOP PRINT_BIN
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
