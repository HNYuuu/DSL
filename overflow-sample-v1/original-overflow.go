package main

import (
	"fmt"
	"math/rand"
)

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

func main() {
	var a, b uint8
	a = 25
	a = testPre(a)
	b = 10
	d := genRans()
	fmt.Println(d)

	c := a + b
	fmt.Printf("c is: %v, type is: %T\n", c, c)
}
