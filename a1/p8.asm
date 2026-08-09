.MODEL SMALL
.STACK 100H

.DATA
    arr DB 25,12,45,7,63,18
    n   EQU 6

    maxVal DB ?
    minVal DB ?

    msg1 DB 'Maximum = $'
    msg2 DB 13,10,'Minimum = $'

.CODE
MAIN PROC
    MOV AX, @DATA
    MOV DS, AX

    ; Initialize maximum and minimum
    MOV AL, arr[0]
    MOV maxVal, AL
    MOV minVal, AL

    MOV SI, 1
    MOV CX, n-1

LOOP_ARRAY:

    MOV AL, arr[SI]

    ; Check maximum
    CMP AL, maxVal
    JBE CHECK_MIN

    MOV maxVal, AL

CHECK_MIN:
    CMP AL, minVal
    JAE NEXT_ELEMENT

    MOV minVal, AL

NEXT_ELEMENT:
    INC SI
    LOOP LOOP_ARRAY

    ; Display maximum
    LEA DX, msg1
    MOV AH, 09H
    INT 21H

    MOV AL, maxVal
    CALL PRINT_NUM

    ; Display minimum
    LEA DX, msg2
    MOV AH, 09H
    INT 21H

    MOV AL, minVal
    CALL PRINT_NUM

    ; Exit
    MOV AH, 4CH
    INT 21H

MAIN ENDP


PRINT_NUM PROC

    MOV AH, 00H
    MOV BL, 10
    DIV BL

    CMP AL, 00H
    JE PRINT_ONES

    ADD AL, 30H
    MOV DL, AL
    MOV AH, 02H
    INT 21H

PRINT_ONES:
    MOV AL, AH
    ADD AL, 30H
    MOV DL, AL
    MOV AH, 02H
    INT 21H

    RET

PRINT_NUM ENDP

END MAIN