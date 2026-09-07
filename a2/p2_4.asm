.MODEL SMALL
.STACK 100H
.DATA
    msg1 DB 'Enter first 32-bit number: $'
    msg2 DB 'Enter second 32-bit number: $'
    msg3 DB 'Result: $'
    n1_hi DW 0
    n1_lo DW 0
    n2_hi DW 0
    n2_lo DW 0
    res0 DW 0
    res1 DW 0
    res2 DW 0
    res3 DW 0
.CODE
MAIN PROC
    MOV AX, @DATA
    MOV DS, AX

    LEA DX, msg1
    MOV AH, 09H
    INT 21H
    CALL GET_32_DEC
    MOV n1_hi, DX
    MOV n1_lo, AX
    CALL NEWLINE

    LEA DX, msg2
    MOV AH, 09H
    INT 21H
    CALL GET_32_DEC
    MOV n2_hi, DX
    MOV n2_lo, AX
    CALL NEWLINE

    ; Multiply 32-bit * 32-bit -> 64-bit
    MOV res0, 0
    MOV res1, 0
    MOV res2, 0
    MOV res3, 0

    ; n1_lo * n2_lo
    MOV AX, n1_lo
    MOV BX, n2_lo
    MUL BX
    MOV res0, AX
    MOV res1, DX

    ; n1_hi * n2_lo
    MOV AX, n1_hi
    MOV BX, n2_lo
    MUL BX
    ADD res1, AX
    ADC res2, DX
    ADC res3, 0

    ; n1_lo * n2_hi
    MOV AX, n1_lo
    MOV BX, n2_hi
    MUL BX
    ADD res1, AX
    ADC res2, DX
    ADC res3, 0

    ; n1_hi * n2_hi
    MOV AX, n1_hi
    MOV BX, n2_hi
    MUL BX
    ADD res2, AX
    ADC res3, DX

    LEA DX, msg3
    MOV AH, 09H
    INT 21H
    CALL PRINT_64_DEC
    CALL NEWLINE

    MOV AH, 4CH
    INT 21H
MAIN ENDP

GET_32_DEC PROC
    ; Reads a 32-bit decimal number into DX:AX
    PUSH BX
    PUSH CX
    PUSH SI
    PUSH DI
    MOV SI, 0 ; high word
    MOV DI, 0 ; low word
READ_32:
    MOV AH, 01H
    INT 21H
    CMP AL, 13
    JE END_G32
    CMP AL, 32
    JE END_G32
    SUB AL, '0'
    MOV AH, 0
    PUSH AX ; save digit

    ; Multiply SI:DI by 10
    MOV AX, DI
    MOV BX, 10
    MUL BX
    MOV DI, AX
    MOV CX, DX

    MOV AX, SI
    MUL BX
    ADD AX, CX
    MOV SI, AX

    POP AX ; pop digit
    ADD DI, AX
    ADC SI, 0
    JMP READ_32
END_G32:
    MOV DX, SI
    MOV AX, DI
    POP DI
    POP SI
    POP CX
    POP BX
    RET
GET_32_DEC ENDP

PRINT_64_DEC PROC
    ; Prints the 64-bit value stored in res3:res2:res1:res0
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX

    MOV CX, 0
DIV_LOOP64:
    ; Divide res3:res2:res1:res0 by 10
    MOV BX, 10
    MOV DX, 0
    
    MOV AX, res3
    DIV BX
    MOV res3, AX
    
    MOV AX, res2
    DIV BX
    MOV res2, AX
    
    MOV AX, res1
    DIV BX
    MOV res1, AX
    
    MOV AX, res0
    DIV BX
    MOV res0, AX
    
    PUSH DX ; Remainder
    INC CX
    
    ; Check if res3:res2:res1:res0 == 0
    MOV AX, res0
    OR AX, res1
    OR AX, res2
    OR AX, res3
    JNZ DIV_LOOP64

PRINT_LOOP64:
    POP DX
    ADD DL, '0'
    MOV AH, 02H
    INT 21H
    LOOP PRINT_LOOP64

    POP DX
    POP CX
    POP BX
    POP AX
    RET
PRINT_64_DEC ENDP

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
