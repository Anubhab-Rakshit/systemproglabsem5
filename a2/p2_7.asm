.MODEL SMALL
.STACK 100H
.DATA
    msg1 DB 'Enter main string: $'
    msg2 DB 13, 10, 'Enter sub-string to delete: $'
    msg3 DB 13, 10, 'Resulting string: $'
    msg4 DB 13, 10, 'Sub-string not found.$'
    
    str_buf DB 50
    str_len DB ?
    str_data DB 50 DUP('$')
    
    sub_buf DB 50
    sub_len DB ?
    sub_data DB 50 DUP('$')
    
.CODE
MAIN PROC
    MOV AX, @DATA
    MOV DS, AX
    MOV ES, AX
    
    ; Print msg1
    LEA DX, msg1
    MOV AH, 09H
    INT 21H
    
    ; Read main string
    LEA DX, str_buf
    MOV AH, 0AH
    INT 21H
    
    ; Print msg2
    LEA DX, msg2
    MOV AH, 09H
    INT 21H
    
    ; Read sub-string
    LEA DX, sub_buf
    MOV AH, 0AH
    INT 21H
    
    ; Check if sub_len is 0
    CMP sub_len, 0
    JE PRINT_RESULT
    
    ; Check if str_len is 0
    MOV CL, str_len
    MOV CH, 0
    CMP CX, 0
    JE PRINT_RESULT
    
    MOV AL, sub_len
    MOV AH, 0
    MOV DX, AX ; DX = sub_len (using DX instead of BX because BX is used for addressing)
    
    MOV SI, 0 ; i = 0
SEARCH_LOOP:
    ; if i + sub_len > str_len, not found
    MOV AX, SI
    ADD AX, DX
    MOV BX, 0
    MOV BL, str_len
    CMP AX, BX
    JG NOT_FOUND
    
    ; Match inner loop
    MOV DI, 0 ; j = 0
MATCH_LOOP:
    CMP DI, DX
    JAE MATCH_FOUND ; matched entirely!
    
    ; Compare str_data[i+j] with sub_data[j]
    LEA BX, str_data
    ADD BX, SI
    ADD BX, DI
    MOV AL, [BX]
    
    LEA BX, sub_data
    ADD BX, DI
    MOV AH, [BX]
    
    CMP AL, AH
    JNE NO_MATCH
    
    INC DI
    JMP MATCH_LOOP
    
NO_MATCH:
    INC SI
    JMP SEARCH_LOOP
    
MATCH_FOUND:
    ; Shift left from i + sub_len to str_len
    MOV AX, SI
    ADD AX, DX
    MOV DI, AX ; DI = i + sub_len (source index)
    MOV BP, SI ; BP = i (dest index)
    
    MOV CX, 0
    MOV CL, str_len
    SUB CX, DI ; CX = bytes to move
    
    CMP CX, 0
    JE UPDATE_LEN
    
SHIFT_LOOP:
    LEA BX, str_data
    ADD BX, DI
    MOV AL, [BX]
    
    LEA BX, str_data
    ADD BX, BP
    MOV [BX], AL
    
    INC DI
    INC BP
    LOOP SHIFT_LOOP
    
UPDATE_LEN:
    ; str_len -= sub_len
    MOV AL, str_len
    SUB AL, sub_len
    MOV str_len, AL
    JMP PRINT_RESULT
    
NOT_FOUND:
    LEA DX, msg4
    MOV AH, 09H
    INT 21H
    JMP EXIT_PROG
    
PRINT_RESULT:
    LEA DX, msg3
    MOV AH, 09H
    INT 21H
    
    ; Add '$' at the new end of str_data
    MOV AL, str_len
    MOV AH, 0
    LEA BX, str_data
    ADD BX, AX
    MOV BYTE PTR [BX], '$'
    
    LEA DX, str_data
    MOV AH, 09H
    INT 21H
    
    ; Print newline
    MOV DL, 13
    MOV AH, 02H
    INT 21H
    MOV DL, 10
    MOV AH, 02H
    INT 21H
    
EXIT_PROG:
    MOV AH, 4CH
    INT 21H
MAIN ENDP
END MAIN
