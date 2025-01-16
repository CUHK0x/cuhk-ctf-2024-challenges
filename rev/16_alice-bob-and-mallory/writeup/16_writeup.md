## Alice, Bob and Mallory
> Author: chemistrying \
> Category: rev \
> Expected Difficulty: 2 \
> Final Points: 131 \
> Solves: 10/38 (Secondary), 17/44 (CUHK), 7/8 (Invited Teams)
> 
> You are Mallory. One day, you see Alice happily presents her square-root program to Bob, which seems to function properly and no longer disappoints her mother. However, you want to make her sad and get her flag, which is her family's heirloom. Please hack her program and get the valuable heirloom.

First, this challenge is written in C. You can find it out by trial and error (putting the executable to different decompilers).

Suppose I use online decompilers like [this](https://dogbolt.org/) one, after some waiting time and analyse the decompiled code, plus some trial and error through locally running the executable / netcatting to the remote, you can see the code structure is roughly something like this:
1. The program requests a number $N$
2. The program validates the number and find the value $K$ using `math.h`'s `sqrt` function if the number is valid
3. If $K^2 \leq N$, then the program terminates, else it continues until you successfully send 100 unique numbers such that $K^2 > N$
4. If you succeed, you will get the flag

First, it is important to notice that the program uses `math.h`'s `sqrt`, which you can notice by looking at the differences of the lines of code of the function. You can try that out by coding custom `sqrt` function and using `math.h`'s sqrt function.

Second, it is necessary to transform $K$ into a mathematical formula, which is $K = \lfloor\sqrt{N}\rfloor$.

The problem of using `math.h`'s `sqrt` function is that it might contain error due to floating point representation errors. Decimal numbers (aka floating point numbers) uses [IEEE 754 standard](https://en.wikipedia.org/wiki/Double-precision_floating-point_format) to represent real numbers. In short, **the 0s and 1s cannot accurately represent all real numbers**. Since `math.h`'s `sqrt` uses `double` to evaluate square root, the final answer is only an **approximation** to the real number.

Now, we consider a very large square number $M$. Consider $\sqrt{M - 1}$, since $M$ is very large, $\sqrt{M - 1} \approx \sqrt{M}$. Therefore, the program might evaluate the answer of $\lfloor\sqrt{M - 1}\rfloor$ to $\lfloor\sqrt{M}\rfloor$ (which is obviously not the same) due to the fact that $\sqrt{M - 1} \approx \sqrt{M}$. For example, it calculate the squaure root value to $4.999999999999999999999999...$ (I make it up), which is closely equal to $5$, so the program thinks it is supposed to be a $5$, and return $5$ even when you do a floor operation. This error often appears in large values (like $\geq 10^9$).

So the solution is to first precompute 100 unique values which appears the above approximation error, and then send these 100 numbers to the remote.

Solve script:
```c
#include <stdio.h>
#include <math.h>

int main() {
    long long arr[100] = {0};
    int ptr = 0;
    for (long long i = 1; i <= 100 * 1000 * 1000; i++) {
        long long n = i * i - 1;
        long long n2 = (long long)sqrt(n);
        if (n2 * n2 > n) {
            arr[ptr] = n;
            ptr++;
            if (ptr == 100) {
                putchar('[');
                for (int j = 0; j < 100; j++) {
                    printf("%lld", arr[j]);
                    if (j != 99) {
                        printf(", ");
                    } else {
                        putchar(']');
                        putchar('\n');
                    }
                }
                return 0;
            }
        }
    }
    return 0;
}
```

```py
from pwn import *

ans = [4503599761588224, 4503599895805955, 4503600030023688, 4503600164241423, 4503600298459160, 4503600432676899, 4503600566894640, 4503600701112383, 4503600835330128, 4503600969547875, 4503601103765624, 4503601237983375, 4503601372201128, 4503601506418883, 4503601640636640, 4503601774854399, 4503601909072160, 4503602043289923, 4503602177507688, 4503602311725455, 4503602445943224, 4503602580160995, 4503602714378768, 4503602848596543, 4503602982814320, 4503603117032099, 4503603251249880, 4503603385467663, 4503603519685448, 4503603653903235, 4503603788121024, 4503603922338815, 4503604056556608, 4503604190774403, 4503604324992200, 4503604459209999, 4503604593427800, 4503604727645603, 4503604861863408, 4503604996081215, 4503605130299024, 4503605264516835, 4503605398734648, 4503605532952463, 4503605667170280, 4503605801388099, 4503605935605920, 4503606069823743, 4503606204041568, 4503606338259395, 4503606472477224, 4503606606695055, 4503606740912888, 4503606875130723, 4503607009348560, 4503607143566399, 4503607277784240, 4503607412002083, 4503607546219928, 4503607680437775, 4503607814655624, 4503607948873475, 4503608083091328, 4503608217309183, 4503608351527040, 4503608485744899, 4503608619962760, 4503608754180623, 4503608888398488, 4503609022616355, 4503609156834224, 4503609291052095, 4503609425269968, 4503609559487843, 4503609693705720, 4503609827923599, 4503609962141480, 4503610096359363, 4503610230577248, 4503610364795135, 4503610499013024, 4503610633230915, 4503610767448808, 4503610901666703, 4503611035884600, 4503611170102499, 4503611304320400, 4503611438538303, 4503611572756208, 4503611706974115, 4503611841192024, 4503611975409935, 4503612109627848, 4503612243845763, 4503612378063680, 4503612512281599, 4503612646499520, 4503612780717443, 4503612914935368, 4503613049153295]

conn = remote('localhost', 50016)

for i in range(100):
    conn.send(bytes(str(ans[i]) + '\n', "ascii"))
print(conn.recvall().decode("ascii"))
```

Flag: **`cuhk24ctf{Un0_tH3_r3v_trIck_AsT1Ey_oF_hqckin9_c_or_cpp_meTh}`**