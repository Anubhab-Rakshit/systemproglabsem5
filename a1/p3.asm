.MODEL SMALL
.STACK 100H

.DATA
    msg1 DB 'First hexadecimal number: 25H',13,10,'$'
    msg2 DB 'Second hexadecimal number: 37H',13,10,'$'
    msg3 DB 'Sum = $'

    num1 DB 25H
    num2 DB 37H

.CODE
MAIN PROC
    MOV AX, @DATA
    MOV DS, AX

    LEA DX, msg1
    MOV AH, 09H
    INT 21H

    LEA DX, msg2
    MOV AH, 09H
    INT 21H

    ; Add numbers
    MOV AL, num1
    ADD AL, num2

    ; Store result
    MOV BL, AL

    ; Display message
    LEA DX, msg3
    MOV AH, 09H
    INT 21H

    ; Display hexadecimal result
    MOV AL, BL
    CALL PRINT_HEX

    ; Exit
    MOV AH, 4CH
    INT 21H

MAIN ENDP


; ------------------------------------
; Procedure to print AL as hexadecimal
; ------------------------------------

PRINT_HEX PROC

    PUSH AX
    PUSH BX

    MOV BL, AL

    ; Print upper nibble
    MOV CL, 04H
    SHR AL, CL
    CALL PRINT_HEX_DIGIT

    ; Print lower nibble
    MOV AL, BL
    AND AL, 0FH
    CALL PRINT_HEX_DIGIT

    POP BX
    POP AX

    RET

PRINT_HEX ENDP


PRINT_HEX_DIGIT PROC

    CMP AL, 09H
    JBE DIGIT

    ADD AL, 07H

DIGIT:
    ADD AL, 30H

    MOV DL, AL
    MOV AH, 02H
    INT 21H

    RET

PRINT_HEX_DIGIT ENDP

END MAIN