#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Auth0r : afang
# nice day mua! :P
# desc:

# imports

chars = "1f8b0800c76db2550003edcf310ac2401085e1a9738a6ded6676372b78053b73821489480281b822dede35a545ac4210feaf790c33c59b7e6cafb2312d528c4b16dfa91abc980f75b063329f444da39938ddbad8c7e39edbd93999a729afddfddaffa94b796bb8e5fc72cdb3eb4a9c97e174a8f66e060000000000000000000000000058f30643cc4d0e00280000"

i = 0
strr = ""
while i < len(chars):

    temp = chars[i] + chars[i+1]
    k = chr(int(temp,16))
    strr += k
    i += 2

w = open("flag",'wb')
w.write(strr)


