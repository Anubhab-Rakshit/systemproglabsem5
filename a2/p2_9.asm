.MODEL SMALL
.STACK 100H
.DATA
    arr DW 5 DUP(?)
    msg_input DB 'Enter 5 numbers in SORTED order:', 13, 10, '$'
    msg_elem DB 'Element: $'
    msg_search_lin DB 'Enter number to search (Linear Search): $'
    msg_search_bin DB 'Enter number to search (Binary Search): $'
    msg_found DB 'Found!', 13, 10, '$'
    msg_not_found DB 'Not Found!', 13, 10, '$'
    search_key DW ?
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

    ; Linear Search
    LEA DX, msg_search_lin
    MOV AH, 09H
    INT 21H
    CALL GET_NUM
    MOV search_key, AX
    CALL NEWLINE

    MOV CX, 5
    MOV SI, OFFSET arr
    MOV AX, search_key
LIN_SEARCH:
    CMP AX, [SI]
    JE LIN_FOUND
    ADD SI, 2
    LOOP LIN_SEARCH

    LEA DX, msg_not_found
    MOV AH, 09H
    INT 21H
    JMP BINARY_SEARCH_START
LIN_FOUND:
    LEA DX, msg_found
    MOV AH, 09H
    INT 21H

BINARY_SEARCH_START:
    ; Binary Search
    LEA DX, msg_search_bin
    MOV AH, 09H
    INT 21H
    CALL GET_NUM
    MOV search_key, AX
    CALL NEWLINE

    MOV BX, 0    ; low index
    MOV DX, 4    ; high index
BIN_SEARCH_LOOP:
    CMP BX, DX
    JG BIN_NOT_FOUND
    
    ; mid = (low + high) / 2
    MOV AX, BX
    ADD AX, DX
    SHR AX, 1    ; AX = mid index
    
    MOV SI, AX
    SHL SI, 1    ; word offset
    ADD SI, OFFSET arr
    MOV CX, [SI] ; CX = arr[mid]
    
    MOV AX, search_key
    CMP AX, CX
    JE BIN_FOUND
    JL SEARCH_LEFT
    
    ; SEARCH_RIGHT: low = mid + 1
    MOV BX, AX
    INC BX
    JMP BIN_SEARCH_LOOP
    
SEARCH_LEFT:
    ; high = mid - 1
    MOV DX, AX
    DEC DX
    JMP BIN_SEARCH_LOOP
    
BIN_NOT_FOUND:
    LEA DX, msg_not_found
    MOV AH, 09H
    INT 21H
    JMP DONE
BIN_FOUND:
    LEA DX, msg_found
    MOV AH, 09H
    INT 21H

DONE:
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
