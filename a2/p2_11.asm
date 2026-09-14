.MODEL SMALL
.STACK 100H
.DATA
    arr_sel DW 5 DUP(?)
    arr_ins DW 5 DUP(?)
    msg_input DB 'Enter 5 numbers for the array:', 13, 10, '$'
    msg_elem DB 'Element: $'
    msg_sel DB 'Array after Selection Sort: $'
    msg_ins DB 'Array after Insertion Sort: $'
.CODE
MAIN PROC
    MOV AX, @DATA
    MOV DS, AX

    LEA DX, msg_input
    MOV AH, 09H
    INT 21H

    MOV CX, 5
    MOV SI, 0
READ_ARRAY:
    LEA DX, msg_elem
    MOV AH, 09H
    INT 21H
    CALL GET_NUM
    
    MOV arr_sel[SI], AX
    MOV arr_ins[SI], AX
    
    CALL NEWLINE
    ADD SI, 2
    LOOP READ_ARRAY

    ; =======================
    ; Selection Sort Logic
    ; =======================
    MOV CX, 4               ; Outer loop count
    MOV DI, 0               ; Pointer i (byte offset)
SEL_OUTER_LOOP:
    MOV BX, DI              ; min_ptr = i
    MOV SI, DI
    ADD SI, 2               ; j = i + 1

SEL_INNER_LOOP:
    MOV AX, arr_sel[SI]     ; arr[j]
    MOV DX, arr_sel[BX]     ; arr[min_idx]

    CMP AX, DX
    JGE NOT_LESS
    MOV BX, SI              ; min_idx = j
NOT_LESS:
    ADD SI, 2
    CMP SI, 10
    JL SEL_INNER_LOOP

    ; Swap arr[i] and arr[min_idx]
    MOV AX, arr_sel[DI]
    MOV DX, arr_sel[BX]
    MOV arr_sel[DI], DX
    MOV arr_sel[BX], AX

    ADD DI, 2
    LOOP SEL_OUTER_LOOP

    ; Print Selection Sorted Array
    LEA DX, msg_sel
    MOV AH, 09H
    INT 21H

    MOV CX, 5
    MOV SI, 0
PRINT_SEL:
    MOV AX, arr_sel[SI]
    CALL PRINT_NUM
    MOV DL, ' '
    MOV AH, 02H
    INT 21H
    ADD SI, 2
    LOOP PRINT_SEL
    CALL NEWLINE

    ; =======================
    ; Insertion Sort Logic
    ; =======================
    MOV DI, 2               ; i = 1 (second element, 2 bytes)
INS_OUTER_LOOP:
    MOV AX, arr_ins[DI]     ; AX = key
    MOV SI, DI
    SUB SI, 2               ; SI = j = i - 1

INS_INNER_LOOP:
    CMP SI, 0
    JL INS_PLACE            ; If j < 0, break
    
    MOV DX, arr_ins[SI]
    CMP DX, AX
    JLE INS_PLACE           ; If arr[j] <= key, break

    ; arr[j+1] = arr[j]
    MOV arr_ins[SI+2], DX
    
    SUB SI, 2
    JMP INS_INNER_LOOP

INS_PLACE:
    ; arr[j+1] = key
    MOV arr_ins[SI+2], AX

    ADD DI, 2
    CMP DI, 10              ; i < 5 (10 bytes)
    JL INS_OUTER_LOOP

    ; Print Insertion Sorted Array
    LEA DX, msg_ins
    MOV AH, 09H
    INT 21H

    MOV CX, 5
    MOV SI, 0
PRINT_INS:
    MOV AX, arr_ins[SI]
    CALL PRINT_NUM
    MOV DL, ' '
    MOV AH, 02H
    INT 21H
    ADD SI, 2
    LOOP PRINT_INS
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
