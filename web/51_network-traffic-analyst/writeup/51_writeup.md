## Network Traffic Analyst
> Author: chemistrying \
> Category: web \
> Expected Difficulty: 1 \
> Final Points: 100 \
> Solves: 21/38 (CUHK), 26/44 (Secondary), 7/8 (Invited Teams)
> 
> Are you a qualified network traffic analyst? Solve this challenge to find out.

This is a basic HTTP traffic analysing problem.

For any problems that requires traffic analysing, you should make use of Burpsuite to do the problem.

After opening the Burpsuite, click the Proxy tab and use the browser given to access to the challenge website. You can see two kinds of traffic: HTTP traffic (in HTTP history tab) and Websocket traffic (in Websocket history tab).

You should click both to see whether there are incoming traffic from the webserver.

After some inspection, you will find that there is a websocket traffic with content like this:
```json
{
    "op": "flag1",
    "content": "cuhk24ctf{C@pture_Th3_C1ty_With_Ur_Trafik_Ann@1y5ing_SqkilLs}"
}
```

Congratuations, you've got the flag for this challenge.
