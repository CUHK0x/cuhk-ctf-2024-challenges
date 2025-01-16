# Whisper

## Keys
- A user supplied format string vulnerability (`chall.c:59`)
- Understanding workings of `printf`, including:
   - `$` Positional arguments
   - Format argument types (`%s` used here)
- Flag placed in `s[15]`, but the input for index is properly validated
  to not allow reading `s[15]`
- Random number initialized with `srand(0)`, leading to same behavior
  every time.

## Abstract
The program gives the user two options:
1. *Get a whisper*:
   Allows the user to enter an index in [0, 14], and read the message at
   that index with `printf`.
2. *Write a whisper*:
   Writes a user supplied message randomly to one of the message buffers `s`,
   except the flag.
3. (Other numbers):
   The program exits gracefully.

## Solve
We craft a user formatted string to read the flag string specifically.

Using `printf` numbered positional argument feature:
> `%1$d` outputs the first argument passed to `printf`, `%2$d` outputs the
  second argument passed to `printf`, and so on. By x86_64 function calling
  convention, arguments starting from the 6th are pushed onto the stack. `printf`
  assumes they are pushed to the top of the stack sequentially, 6th argument
  at the top (at `$rsp`), then 7th, and so on. There are no checks if whether
  there are actually arguments pushed.

We can read arbitrary values at arbitrary locations of the stack, if we have control
of the format string.

Observe that the flag string is stored in a `malloc`ed memory, and a pointer
is kept on the stack (`chall.c:29,35`). We want `printf` to leak the flag string,
so we craft the format string to use *that* pointer to print out our flag string.

One solution that may be came up with is to simply tell `printf` to print out
strings with everything on the stack:
```
%6$s%7$s%8$s...
```
but this will SEGFAULT the program prematurely as not all values on the stack are
valid pointers.

Therefore, we should compute the offset we need to read the flag precisely.
Throwing the program into debug mode, we can see the addresses of the stack pointer and the `char*` array (you can do this with a regular binary too):
```
-exec p $rsp
$1 = (void *) 0x7fffffffd150
-exec p &s
$2 = (char *(*)[16]) 0x7fffffffd170
```

We know that the flag is s[15], each pointer is 8 bytes (64-bits) on a 64-bit computer,
so we have `&(s[15]) == 0x7fffffffd1e8`. At the same time, each argument to `printf` is
8 bytes as well, and `printf` starts counting from `$rsp` for the 6th argument and so forth,
so we have the position be:
```
(0x7fffffffd1e8-0x7fffffffd150)/8+6 => 25
```
Hence `%25$s` will print the flag.

Now `rand` is deterministic given the constant random seed. By testing, the first whisper
will be written to the 1 index. We write our whisper (just 5 characters!) and get the flag:
```
It is very quiet here. Please, lowly whisper your message.
<if you say the right word, you might get surprises.>
1. Get a whisper
2. Write a whisper
Enter your choice: 2
Whisper something:
%25$s
1. Get a whisper
2. Write a whisper
Enter your choice: 1
Pick a whisper: 1
cuhk24ctf{tHE_QUieTer_Y0u_@Re_the_MORe_yoU_hEar}
```

## Motivation
As a (sort of) antonym to `scream`, this is deliberately made as a
*much* easier version to it. This challenge was originally a UAF
(Use After Free), but I realized it's hard to make UAFs that are
easy. Even the *easy* UAF challenge in Magpie I plan to *reference*, creatively named `free`, requires some code review. I switched and make this instead, in light of the fewer easy `pwn` challenges.
