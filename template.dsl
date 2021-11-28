@dsl-rule
scope: signed_int_add
watch: [flag]
assume: [flag >= 10]

@dsl-rule
scope: .*int_add.*
regex: True
watch: [c]
ensure: [c <= 2147483647]

@dsl-rule
scope: test_nesting
nesting: [0]
watch: [b]
require: [b < 6]

@dsl-rule
scope: test_nesting
nesting: [4, 1]
watch: [d]
require: [d < 100]

@dsl-rule
scope: func
watch: [iterates]
require: [iter(iterates) != 5]

@dsl-rule
scope: div_zero_vul
check: [divzero]

@dsl-rule
scope: test_watch_op
watch_op: add
watch: [var1, var2]
require: [var1 + var2 >= var1 and var1 + var2 >= var2]
