@dsl-rule
scope: func
watch: [a]
assume: a >= 1

@dsl-rule
scope: .*func.*
regex: True
watch: [b]
ensure: b < 100

@dsl-rule
scope: func
nesting: [0]
watch: [var0, var1]
require: var0 >= var1

@dsl-rule
scope: func
watch: [iterates]
require: iter(iterates) != 5

@dsl-rule
scope: may-vul
check: [integer-overflow, divzero]

@dsl-rule
scope: may-vul
watch_op: add
watch: [var1, var2]
require: var1 + var2 >= var1 and var1 + var2 >= var2
