.MODEL SMALL
.STACK 100H
.DATA
    arr DW 5 DUP(?)
    msg_input DB 'Enter 5 numbers for the array:', 13, 10, '$'
    msg_elem DB 'Element: $'
    msg_after DB 'Array after Selection Sort: $'
.CODE
MAIN PROC
    MOV AX, @DATA
    MOV DS, AX

    LEA DX, msg_input
    MOV AH, 09H
    INT 21H

    MOV CX, 5
    MOV SI, OFFSET arr
READ_ARRAY:
    LEA DX, msg_elem
    MOV AH, 09H
    INT 21H
    CALL GET_NUM
    MOV [SI], AX
    CALL NEWLINE
    ADD SI, 2
    LOOP READ_ARRAY

    ; Selection Sort Logic
    MOV CX, 4               ; Outer loop count (n-1 passes)
    MOV DI, OFFSET arr      ; Pointer i
OUTER_LOOP:
    MOV BX, DI              ; min_ptr = i
    MOV SI, DI
    ADD SI, 2               ; j_ptr = i + 1

INNER_LOOP:
    MOV AX, [SI]            ; AX = arr[j]
    MOV DX, [BX]            ; DX = arr[min_idx]

    CMP AX, DX
    JGE NOT_LESS            ; If arr[j] >= arr[min_idx], skip
    MOV BX, SI              ; min_idx = j
NOT_LESS:
    ADD SI, 2
    CMP SI, OFFSET arr + 10 ; 5 elements = 10 bytes offset
    JL INNER_LOOP

    ; Swap arr[i] and arr[min_idx]
    MOV AX, [DI]
    MOV DX, [BX]
    MOV [DI], DX
    MOV [BX], AX

    ADD DI, 2
    LOOP OUTER_LOOP

    ; Print Sorted Array
    LEA DX, msg_after
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
