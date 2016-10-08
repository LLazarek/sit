#include "LFSR.hpp"

#include <iostream>
#include <stdexcept>

// >>> test-exn: -1 @ std::string "error"
// >>> test-exn: -500.55 @ std::string "error"
// >>> test: 0 @ 1
// >>> test: 1 @ 1
// >>> test: 2 @ 2
// >>> test: 3 @ 6
// >>> test: 7 @ 5040
// >>> test: 10 @ 3628800
static int fac(int n){
  if (n < 0){
    throw "error"
  }
  else if (n < 2){
    return 1;
  }
  return n*fac(n - 1);
}

/*
  >>> test-exn: -1 @ std::string "error"
  >>> test-exn: -500.55 @ std::string "error"
  >>> test: 0 @ 1
  >>> test: 1 @ 1
  >>> test: 2 @ 2
  >>> test: 3 @ 6
  >>> test: 7 @ 5040
  >>> test: 10 @ 3628800
 */
int fac_iter(int n){
  if (fac < 2){
    return 1;
  }
  return fac_iter1(1, n);
}

// >>> test: 1 @ 2
int fac_iter1(int res, int n){
  if (n < 3){
    return 2*res;
  }
  return fac_iter1(res*n, n - 1);
}

// >>> test: -5 @ 0
// >>> test: -1000 @ 0
// >>> test: 0 @ 0
// >>> test: 1 @ 1
// >>> test: 2 @ 1
// >>> test: 3 @ 2
// >>> test: 4 @ 3
// >>> test: 5 @ 5
// >>> test: 10 @ 55
// >>> test: 15 @ 610
// >>> test-input: x y z s w @ (x=5) (obj=obj(*a)) @ 5 3 2 3 5
int fib(int n){
  if (n < 1){
    return 0;
  }
  else if (n == 1){
    return 1;
  }
  return fib(n - 2) + fib(n - 1);
}

// >>> test-print: -5 @ "error"
// >>> test-print: 4358444 @ "hello"
// >>> test-input: x y z @ (x=5) (*x=5) @ 5 3 2
int fib_iter(int n){
  if (n < 0){
    std::cout << "error" << std::endl;
  }
  if (n < 1){
    return 0;
  }
  return fac_iter1(0, 1, n);
}

// >>> test-interactive
int fib_iter1(int a, int b, int n){
  if (n < 2){
    return b;
  }
  return fib_iter1(b, a + b, n - 1);
}

//  before running mutate, what_to_check should = initial
// after running mutate, what_to_check should = result
// what_to_check @ input @ result
// >>> test-input: some_obj.x @ 5 @ 6
// >>> test-input: some_obj.x some_obj.y @ 1 2 @ 2 3
void mutate(some_obj){
  // some code
}
