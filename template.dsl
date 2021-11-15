@dsl-rule
scope: func
watch: [a, c]
assume: [a >= 1, c < 10]

@dsl-rule
scope: .*int_add.*
regex: True
watch: [b]
ensure: [b < 100]

@dsl-rule
scope: func
nesting: [0]
watch: [var0, var1]
require: [var0 >= var1]

@dsl-rule
scope: func
watch: [iterates]
require: [iter(iterates) != 5]

@dsl-rule
scope: signed_int_add
check: [integer-overflow, divzero]

@dsl-rule
scope: signed_int_add_restricted_invalid
watch_op: add
watch: [var1, var2]
require: [var1 + var2 >= var1 and var1 + var2 >= var2]
