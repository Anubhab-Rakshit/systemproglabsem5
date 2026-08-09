.MODEL SMALL
.STACK 100H

.DATA
    arr DB 12,45,7,89,23,56
    n   EQU 6

    msg1 DB 'Second Minimum = $'
    msg2 DB 13,10,'Second Maximum = $'

    secondMin DB ?
    secondMax DB ?

.CODE
MAIN PROC
    MOV AX, @DATA
    MOV DS, AX

    ; --------------------------------
    ; Find minimum and second minimum
    ; --------------------------------

    MOV SI, 0

    MOV AL, arr[SI]       ; minimum
    MOV BL, AL

    MOV AL, arr[SI]       ; second minimum
    MOV BH, AL

    INC SI
    MOV CX, n-1

MIN_LOOP:
    MOV AL, arr[SI]

    ; Check if AL < minimum
    CMP AL, BL
    JAE CHECK_SECOND_MIN

    ; Old minimum becomes second minimum
    MOV BH, BL
    MOV BL, AL
    JMP NEXT_MIN

CHECK_SECOND_MIN:
    CMP AL, BH
    JAE NEXT_MIN

    ; Avoid duplicate minimum
    CMP AL, BL
    JE NEXT_MIN

    MOV BH, AL

NEXT_MIN:
    INC SI
    LOOP MIN_LOOP

    MOV secondMin, BH

    ; --------------------------------
    ; Find maximum and second maximum
    ; --------------------------------

    MOV SI, 0

    MOV AL, arr[SI]
    MOV DL, AL            ; maximum

    MOV AL, arr[SI]
    MOV DH, AL            ; second maximum

    INC SI
    MOV CX, n-1

MAX_LOOP:
    MOV AL, arr[SI]

    ; Check if AL > maximum
    CMP AL, DL
    JBE CHECK_SECOND_MAX

    ; Old maximum becomes second maximum
    MOV DH, DL
    MOV DL, AL
    JMP NEXT_MAX

CHECK_SECOND_MAX:
    CMP AL, DH
    JBE NEXT_MAX

    ; Avoid duplicate maximum
    CMP AL, DL
    JE NEXT_MAX

    MOV DH, AL

NEXT_MAX:
    INC SI
    LOOP MAX_LOOP

    MOV secondMax, DH

    ; --------------------------------
    ; Display second minimum
    ; --------------------------------

    LEA DX, msg1
    MOV AH, 09H
    INT 21H

    MOV AL, secondMin
    CALL PRINT_NUM

    ; --------------------------------
    ; Display second maximum
    ; --------------------------------

    LEA DX, msg2
    MOV AH, 09H
    INT 21H

    MOV AL, secondMax
    CALL PRINT_NUM

    ; Exit
    MOV AH, 4CH
    INT 21H

MAIN ENDP


; --------------------------------
; Print unsigned number in AL
; --------------------------------

PRINT_NUM PROC

    MOV AH, 00H
    MOV BL, 10
    DIV BL

    ; If quotient is zero
    CMP AL, 00H
    JE PRINT_ONES

    ; Print tens digit
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