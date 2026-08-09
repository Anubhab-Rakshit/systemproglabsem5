.MODEL SMALL
.STACK 100H

.DATA
    msg DB 13,10,'Program is running...',13,10
        DB 'Continue? (Y/N): $'

    byeMsg DB 13,10,'Program terminated.$'

.CODE
MAIN PROC
    MOV AX, @DATA
    MOV DS, AX

START_LOOP:

    ; Display message
    LEA DX, msg
    MOV AH, 09H
    INT 21H

    ; Read choice
    MOV AH, 01H
    INT 21H

    ; Convert lowercase to uppercase if necessary
    CMP AL, 'a'
    JB CHECK_CHOICE

    CMP AL, 'z'
    JA CHECK_CHOICE

    SUB AL, 20H

CHECK_CHOICE:

    CMP AL, 'Y'
    JE START_LOOP

    CMP AL, 'N'
    JE QUIT

    ; Invalid input -> ask again
    JMP START_LOOP

QUIT:

    LEA DX, byeMsg
    MOV AH, 09H
    INT 21H

    MOV AH, 4CH
    INT 21H

MAIN ENDP
END MAIN