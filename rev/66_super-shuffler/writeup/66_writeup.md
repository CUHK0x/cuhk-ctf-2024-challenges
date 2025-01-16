# Keys / Vuln
- Hidden "Cards" available in the caller stack frame
- Accepting user input as index without bounds checking, allowing random memory access.
- Even when we are only allowed to swap with the first item, because we have unlimited swaps,
  so we can still construct an arbitrary *lucky* sequence (Insert Inductive proof here)

# Program logic
0. Sets I/O buffering to 0.
1. Initializes *extra cards* in the main stack frame buffer.
2. Initializes *regular cards* (0-9JQK, i.e. a quarter playing cards stack) and shuffle them
3. Asks a user for a number input as index, and swaps the first card with the indexed card.
   (0-indexed)
4. Repeat step 3 until user enters '`bet`'.
5. Checks the hand of 8 cards against a lucky number. If the hand is *lucky* (i.e. hand is
   equal to the lucky number), then print the flag. Otherwise exits.

# Solve steps
1. Input a number that refers to the `extra_cards` and swap with the first item.
2. Swap the item to the right position.
3. Repeat steps 1 and 2, finally swapping the first item. If a card is shuffled to the back
   of the deck, do two same swaps to reveal the card without modifying the sequence.
4. After the target sequence is constructed, enter the word `bet` to exit the loop and check
   for win status
5. Flag GET!
