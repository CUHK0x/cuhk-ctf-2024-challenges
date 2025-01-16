# Key Points / Vulnerabilities
- No filepath input validation on the input file name, allowing users to enter a path `../data/` uploading into `data` directory, where `yaml` files are stored.
- `os.path.normpath` terminates path at null byte, bypassing file extension filter (Python <3.11.3)
- The use of `r+` mode to write the yaml files allows the payload to be **partially** modified and can add the signature at the beginning of the file, making the file loadable by `yaml.load`.
- `yaml.load` uses `yaml.Loader` to load the yaml file, which permits construction of arbitrary Python objects, consequently RCE.
- `PIL.Image` calls ensures the uploaded image as a proper image, but it does not test whether the image type is indeed a `PNG` or `JPEG`.
- Theoretically, there can be a race condition between an image upload with a worker and another that tries to create a yaml file, the file header can be overwritten by the new *non-existent* friend to get a successful object load. (Solution 2, not tested)

# Exploit 1 (Simpler solution)
1. Construct some payload with an image header, so that the image can be recognized by `PIL.Image`. We can use tools such as *pixload* to inject our payload into a proper image file.

   Count the length of the newly serialized `pyyaml` object, and construct our payload so that the payload comes right after the overwritten part, as an attribute of the original object.
   *See solve script for payload.*
2. Upload the file with a filename in the likes of `../static/<name>.yaml\0.png`, with
   `<name>` matching the name given in the `full_name` field of the form.
3. Use the list image page to trigger a call to load the object containing the payload.
4. Enjoy sweet RCE.

# Exploit 2 (Harder, unproven solution)
We upload a malicious `yaml` like the simpler solution, but to overwrite the existing file, we use the *add-a-friend* feature. This feature will create a new `yaml` file for the friend if he/she does not already exists.
In theory, if an image upload happens right after the *add-a-friend* feature is used,
there is a chance that the feature will overwrite the "image" with an empty `Friend`
object. However, the time frame should be short and it's much harder to execute.

# Design notes
- [x] Writable permission to `/flag` might allow the attacker to overwrite the
  flag. Make sure to remove write perms.
- [x] Using a random name for flag, such as `/flag-c0ffeeaaaa` to force them to
  look around a bit more, instead of reading the flag directly.
- [ ] Might need an instance based (i.e. one instance per team) so they don't
  vandalize it

# Exploit notes
- For some reason modifying the filename in a POST request intercepted from the browser in Burp causes *the image to be tried to decode as utf-8*[^2]. Sending a request with `requests` in Python works.

# Issues
- In my experience, just by appending a `pyyaml` object behind the image headers
  in the payload have never worked, it will always trigger some parsing error from
  `pyyaml` when loading. Can have more testing if anyone is interested.

[^1]: The safe alternative is *`SafeLoader`*, which does not have the ability to
serialize python objects, preventing RCE.

[^2]: This is just my guess, based on the `b'\xef\xbf\xbd'`s that appear in the file stream.
