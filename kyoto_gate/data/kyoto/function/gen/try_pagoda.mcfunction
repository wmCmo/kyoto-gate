# Try the pagoda here. Returns 1 if built.
execute store result score #blocked ky.var run function kyoto:gen/check_w9_d9
execute if score #blocked ky.var matches 1.. run return 0
$function kyoto:gen/build_pagoda {rot:"$(rot)"}
return 1
