package main

import (
	"fmt"
	"math/rand"
)

// @assume: a <= 25;
func testPre(a uint8) uint8 {
	a *= 10
	return a
}

func genRans() []int {
	var rans []int
	for i := 0; i < 5; i++ {
		rans = append(rans, rand.Intn(20))
	}
	return rans
}

// @ensure: a + b > a;
func main() {
	var a, b uint8
	a = 25
	a = testPre(a)
	b = 10
	d := genRans()
	fmt.Println(d)
	// @forall: d $ _el <= 20

	c := a + b
	fmt.Printf("c is: %v, type is: %T\n", c, c)
	// @require: c > a && c > b;
}
