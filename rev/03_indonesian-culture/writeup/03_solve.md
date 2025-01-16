## \[rev] Indonesian Culture

> Expected Difficulty: Freshmen (Level 1)
> Final Points: ???
> Solves: ??/?? (CUHK), ??/?? (Secondary), ??/?? (Invited Teams)
> 
> Sitting on the world's most populous island, One Indonesian programmer designed a program that updates the password daily. With a slow life pace in ASEAN countries, you should have no surprises on how to find the daily password.

This question serves as an introduction to the world of reverse engineering (rev), particularly the use of decompilers.

This time when inputting the `file IndonesianCulture` command to a Linux terminal, it is found that the given file is a Java class.

Using any Java decompilers (such as [decompiler.com](https://www.decompiler.com/)) to decompile the excutable (renaming the file to `IndonesianCulture.class` may be required), it is found the file contains a password with a hard-coded phrase`p3n9uinIsAw3s0ne`, and a varying part that varies with the current date.

Good thing is the date format is also hard-coded (dd/MM/yyyy), and that the default value of `date()` is set to the UNIX date at the moment the program is executed. So it is as easy as inputting the correct combinations for the password to the checker and it will return the flag to you.

*Note:
The date given in the password is corresponding to **UNIX time (UTC+0)**, not Hong Kong Time (UTC+8). Beware of the difference when running the code between 12AM and 8AM Hong Kong Time.*

Flag: **`cuhk24ctf{decompilers_R_ur_be5t_frd_iN_rev}`**
