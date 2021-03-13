package main

import "fmt"

import "time"

func main() {
	message := make(chan int)
	go func() {
		process(1, 6, "3s", message)
	}()
	go func() {
		process(2, 8, "2s", message)
	}()
	for {
		time.Sleep(1000 * time.Second)
	}
}

func process(id int, incr int, tick string, message chan int) {
	duration, _ := time.ParseDuration(tick)
	ticker := time.NewTicker(duration)
	counter := 0
	for {
		select {
		case m := <-message:
			fmt.Println("old counter was ", counter)
			fmt.Println("received a message")
			counter = Max(counter, m) + 1
			fmt.Println("new counter ", counter)
		case t := <-ticker.C:
			fmt.Println("Current time: ", t)
			counter = counter + incr
			if counter == 16 {
				message <- counter
			}
			fmt.Printf("Process %d | Current Counter: %d\n", id, counter)
		}
	}
}

// Max returns the larger of x or y.
func Max(x, y int) int {
	if x < y {
		return y
	}
	return x
}
