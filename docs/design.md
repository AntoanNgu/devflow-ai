
Validation steps

1. Format: does the text match the pattern of github.com/owner/repo? (no network call needed, just a text check)
2. Exists: does github have this repo
3. Public: can DevFlow access it without credentials
4. Size: is it under the limit
5. Tag exists: if the user passed a tag or commit, is it real

Reasoning: This order was chosen based on cost. For the first bullet, if the user submits a repo URL that is invalid this would avoid having DevFlow from running on something other than a repo For steps 2-5, after checking for a valid url devflow needs to know if this repo actually exist and can be accessed, as well as the size of the repo to avoid processing repos that are too large. Lastly check for tags or commits from the user that are valid, which all happen through Github's API, before cloning

Cloning and checking out

* checking out a specific tag, to record the exact code that was ingested. Without pinning, evals would fail whenever the repo changes, even when DevFlow was right. If DevFlow only records the latest code questions about the older versions of the code would be inaccurate
* Record the commit hash even if the user does not pass a tag, if a user asked why something happened, without the hash there would be no record of what version latest meant at ingestion time
