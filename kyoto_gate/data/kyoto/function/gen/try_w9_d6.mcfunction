# Try a 9x6 house here (macro args passed through to the builder)
execute store result score #blocked ky.var run function kyoto:gen/check_w9_d6
execute if score #blocked ky.var matches 1 run return 0
scoreboard players set #stilt ky.var 0
execute if score #blocked ky.var matches 2 run scoreboard players set #stilt ky.var 1
$function kyoto:gen/build_w9_d6 {f:$(f),front:"$(front)",roof:"$(roof)",seed:$(seed),rot:"$(rot)",win:$(win),wall:"$(wall)",interior:"$(interior)"}
return 1
