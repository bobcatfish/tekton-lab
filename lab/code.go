package lab

import "fmt"

// SomeFunction returns i multiplied by 3, unless i itself is 3,
// which is obviously an error.
func SomeFunction(i int) (int, error) {
	if i == 3 {
		return 0, fmt.Errorf("%d is a very bad number", i)
	}
	return i * 3, nil
}
