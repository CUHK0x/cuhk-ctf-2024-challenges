## Burpmon
> Author: chemistrying \
> Category: web \
> Expected Difficulty: 1 \
> Final Points: 100 \
> Solves: 25/38 (Secondary), 38/44 (CUHK), 8/8 (Invited Teams)
> 
> Gammamon

This is a basic HTTP request tampering problem.

If you first click the get flag button, it requests your to give some chocolate.

If you open BurpSuite and check your HTTP requests (or check the page source code), you will see that we initially send `food=chili&amount=1`.

We can then change the food from `chili` to `chocolate`.

Next, it requests more chocolate. Therefore, you should change the amount to something larger. As long as you have chocolate more than $2^{64} - 1$, you will pass this test.

After that, it said you're not `Hiro` but instead something else (let's call it `X` for simplicity).

If you observe your HTTP request in BurpSuite, you will see that your `User-Agent` in header section of the request is the same as `X`. Therefore, you can just replace that part to `Hiro`.

Then, it said you're accepting other languages (let's call it `Y` for simplicity) instead of Japanese. 

If you once again observe your HTTP reuqest in BurpSuite, you will see that your `Accept-Language` is `Y`. Therefore, you can replace that part to `Japanese`.

However, it said your `Accept-Language` should follow the `"locale code"` format. If you google `japanese locale code`, you will find that the locale code of Japanese is `ja-JP`. Just replace with this local code.

Finally, it requests you to use request method `BURP` to get the flag. Replace your `POST` request to `BURP`.

Flag: **`cuhk24ctf{Did_U_BURP_to_GET_FLAG_frum_gammAAAAAAAAAAAAAAAAAAAAAAAAAmon_asdflk;dkjfkl;j}`**