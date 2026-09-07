.MODEL SMALL
.STACK 100H
.DATA
    msg1 DB 'Enter first number: $'
    msg2 DB 'Enter second number: $'
    msg3 DB 'Enter third number: $'
    msg_gcd DB 'GCD is: $'
    msg_lcm DB 'LCM is: $'
    n1 DW ?
    n2 DW ?
    n3 DW ?
.CODE
MAIN PROC
    MOV AX, @DATA
    MOV DS, AX

    LEA DX, msg1
    MOV AH, 09H
    INT 21H
    CALL GET_NUM
    MOV n1, AX
    CALL NEWLINE

    LEA DX, msg2
    MOV AH, 09H
    INT 21H
    CALL GET_NUM
    MOV n2, AX
    CALL NEWLINE

    LEA DX, msg3
    MOV AH, 09H
    INT 21H
    CALL GET_NUM
    MOV n3, AX
    CALL NEWLINE

    ; Calculate final GCD
    MOV AX, n1
    MOV BX, n2
    CALL GCD
    MOV BX, n3
    CALL GCD
    
    PUSH AX ; Save final GCD
    LEA DX, msg_gcd
    MOV AH, 09H
    INT 21H
    POP AX
    CALL PRINT_NUM
    CALL NEWLINE

    ; Calculate final LCM
    MOV AX, n1
    MOV BX, n2
    CALL LCM
    MOV BX, n3
    CALL LCM

    PUSH AX ; Save final LCM
    LEA DX, msg_lcm
    MOV AH, 09H
    INT 21H
    POP AX
    CALL PRINT_NUM
    CALL NEWLINE

    MOV AH, 4CH
    INT 21H
MAIN ENDP

GCD PROC
    ; GCD of AX and BX using Division (Euclidean Algorithm)
    ; Result in AX
    CMP AX, 0
    JE GCD_B_RES
    CMP BX, 0
    JE GCD_DONE
GCD_LOOP:
    MOV DX, 0
    DIV BX
    CMP DX, 0
    JE GCD_B_RES
    MOV AX, BX
    MOV BX, DX
    JMP GCD_LOOP
GCD_B_RES:
    MOV AX, BX
GCD_DONE:
    RET
GCD ENDP

LCM PROC
    ; Calculates LCM of AX and BX, result in AX
    CMP AX, 0
    JE LCM_ZERO
    CMP BX, 0
    JE LCM_ZERO
    
    PUSH AX
    PUSH BX
    CALL GCD
    MOV CX, AX ; CX = GCD
    POP BX
    POP AX
    
    ; DX:AX = AX * BX
    MOV DX, 0
    MUL BX
    
    ; DX:AX / CX
    DIV CX
    RET
LCM_ZERO:
    MOV AX, 0
    RET
LCM ENDP

; Utility Procedures
GET_NUM PROC
    PUSH BX
    PUSH CX
    PUSH DX
    MOV BX, 0
    MOV CX, 10
    
SKIP_NON_DIGIT:
    MOV AH, 01H
    INT 21H
    CMP AL, 13
    JE END_GET_NUM
    CMP AL, '0'
    JB SKIP_NON_DIGIT
    CMP AL, '9'
    JA SKIP_NON_DIGIT
    
    SUB AL, '0'
    MOV AH, 0
    MOV BX, AX

READ_CHAR:
    MOV AH, 01H
    INT 21H
    CMP AL, 13
    JE END_GET_NUM
    CMP AL, 32
    JE END_GET_NUM
    CMP AL, '0'
    JB READ_CHAR
    CMP AL, '9'
    JA READ_CHAR
    
    SUB AL, '0'
    MOV AH, 0
    PUSH AX
    MOV AX, BX
    MUL CX
    POP DX
    ADD AX, DX
    MOV BX, AX
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
