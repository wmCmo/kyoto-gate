# Dispatch on #w / #hd to the size-specific try function (house args in storage kyoto:tmp house)
# Returns 1 if a house was built.
execute if score #w ky.var matches 5 if score #hd ky.var matches 5 run return run function kyoto:gen/try_w5_d5 with storage kyoto:tmp house
execute if score #w ky.var matches 5 if score #hd ky.var matches 6 run return run function kyoto:gen/try_w5_d6 with storage kyoto:tmp house
execute if score #w ky.var matches 7 if score #hd ky.var matches 5 run return run function kyoto:gen/try_w7_d5 with storage kyoto:tmp house
execute if score #w ky.var matches 7 if score #hd ky.var matches 6 run return run function kyoto:gen/try_w7_d6 with storage kyoto:tmp house
execute if score #w ky.var matches 9 if score #hd ky.var matches 5 run return run function kyoto:gen/try_w9_d5 with storage kyoto:tmp house
execute if score #w ky.var matches 9 if score #hd ky.var matches 6 run return run function kyoto:gen/try_w9_d6 with storage kyoto:tmp house
return 0
