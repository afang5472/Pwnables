bits 16

; open file handle
mov ah, 3Dh ; open file
mov al, 0h  ; 0 read file
; dx contains ptr to filename
;mov dx, file

int 21h

; read A:\FLAG.TXT
mov bx, ax ; handle we get when opening a file
mov ah, 3Fh ; read file
mov cx, 20 ; number of bytes to read
; dx contains pointer to buffer
int 21h

; let's try to use the fancy print
;pop dx
;push dx
; dx contains pointer to buffer
;mov dx, file
mov cx, ax ; len to print
mov bx, 1 ; stdout
mov ah, 40h ; write file/device
int 21h

mov ah, 0x4c
int 21h            ; exit
