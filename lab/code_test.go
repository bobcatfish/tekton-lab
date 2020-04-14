package lab

import "testing"

func TestSomeFunction(t *testing.T) {
	for _, tc := range []struct {
		name     string
		i        int
		expected int
	}{{
		name:     "positive number",
		i:        67,
		expected: 201,
	}, {
		name:     "negative number",
		i:        67,
		expected: 201,
	}, {
		name:     "zero",
		i:        0,
		expected: 0,
	}} {
		t.Run(tc.name, func(t *testing.T) {
			actual, err := SomeFunction(tc.i)
			if err != nil {
				t.Errorf("got error but didn't expect one: %v", err)
			}
			if actual != tc.expected {
				t.Errorf("when passing in %d expected %d but got %d", tc.i, tc.expected, actual)
			}
		})

	}

}

func TestSomeFunctionFails(t *testing.T) {
	_, err := SomeFunction(3)
	if err == nil {
		t.Errorf("expected error for bad value but got none")
	}
}
