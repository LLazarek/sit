#include <iostream>
#include <stdexcept>

class Obj {
public:
  int x, y;
};

static int fac(int n);
int fac_iter(int n);
int fac_iter1(int res, int n);
int fib(int n);
int fib_iter(int n);
int fib_iter1(int a, int b, int n);
void mutate(Obj &some_obj);

// >>> test-exn: -1 @ cstr "error"
// >>> test-exn: -500.55 @ cstr "error"
// >>> test: 0 @ 1
// >>> test: 1 @ 1
// >>> test: 2 @ 2
// >>> test: 3 @ 6
// >>> test: 7 @ 5040
// >>> test: 10 @ 3628800
static int fac(int n){
  if (n < 0){
    throw "error";
  }
  else if (n < 2){
    return 1;
  }
  return n*fac(n - 1);
}

/*
  >>> test-exn: -1 @ cstr "error message"
  >>> test-exn: -500.55 @ cstr "error message"
  >>> test: 0 @ 1
  >>> test: 1 @ 1
  >>> test: 2 @ 2
  >>> test: 3 @ 6
  >>> test: 7 @ 5040
  >>> test: 10 @ 3628800
 */
int fac_iter(int n){
  if (n < 0){
    throw "error message";
  }
  if (n < 2){
    return 1;
  }
  return fac_iter1(1, n);
}

// >>> test: 1 1 @ 2
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
// >>> test: 16 @ 16
int fib(int n){
  if (n < 1){
    return 0;
  }
  else if (n == 1){
    return 1;
  }
  return fib(n - 2) + fib(n - 1);
}

// >>> test-exn: -5 @ cstr "error"
// >>> test-exn: -1000 @ cstr "error"
// >>> test-exn: n @ (n = 0) @ cstr "error"
// >>> test: 0 @ 0
// >>> test: 1 @ 1
// >>> test: 2 @ 1
// >>> test: 3 @ 2
// >>> test: 4 @ 3
// >>> test: 5 @ 5
// >>> test: 10 @ 55
// >>> test: 15 @ 610
int fib_iter(int n){
  if (n < 0){
    throw "error";
  }
  if (n < 1){
    return 0;
  }
  return fib_iter1(0, 1, n);
}

/*
  >>> test: 2 b 1 @ (b = 1) @ 1
  >>> test: 0 1 n @ (n = 5) @ 5
 */
int fib_iter1(int a, int b, int n){
  if (n < 2){
    return b;
  }
  return fib_iter1(b, a + b, n - 1);
}


//  before running mutate, what_to_check should = initial
// after running mutate, what_to_check should = result
// what_to_check @ input @ result
// >>> test-input: some_obj.x @ (Obj tmp = Obj()) (some_obj = tmp) (some_obj.x = 5) @ 6
// >>> test-input: some_obj.x some_obj.y @ (Obj tmp = Obj()) (some_obj = tmp) (some_obj.x = 5) (some_obj.y = 1) @ 6 2
// >>> test-input: some_obj.y @ (Obj anobj = Obj()) (some_obj = anobj) (some_obj.y = -5) @ -4
void mutate(Obj &some_obj){
  some_obj.x++;
  some_obj.y++;
}
