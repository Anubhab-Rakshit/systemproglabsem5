.MODEL SMALL
.STACK 100H

.DATA
    msg1 DB 'Enter first number: $'
    msg2 DB 13,10,'Enter second number: $'

    lessMsg DB 13,10,'Second number is LESS than the first.$'
    notLessMsg DB 13,10,'Second number is NOT less than the first.$'

    first DB ?
    second DB ?

.CODE
MAIN PROC
    MOV AX, @DATA
    MOV DS, AX

    ; Read first number
    LEA DX, msg1
    MOV AH, 09H
    INT 21H

    MOV AH, 01H
    INT 21H

    SUB AL, 30H
    MOV first, AL

    ; Read second number
    LEA DX, msg2
    MOV AH, 09H
    INT 21H

    MOV AH, 01H
    INT 21H

    SUB AL, 30H
    MOV second, AL

    ; Compare
    MOV AL, second
    CMP AL, first

    JB SECOND_LESS

    ; Second >= first
    LEA DX, notLessMsg
    MOV AH, 09H
    INT 21H
    JMP EXIT

SECOND_LESS:
    LEA DX, lessMsg
    MOV AH, 09H
    INT 21H

EXIT:
    MOV AH, 4CH
    INT 21H

MAIN ENDP
END MAIN