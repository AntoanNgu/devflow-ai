
## Validation steps

1. Format: does the text match the pattern of github.com/owner/repo? (no network call needed, just a text check)
2. Exists: does github have this repo
3. Public: can DevFlow access it without credentials
4. Size: is it under the limit
5. Tag exists: if the user passed a tag or commit, is it real

Reasoning: This order was chosen based on cost. For the first bullet, if the user submits a repo URL that is invalid this would avoid having DevFlow from running on something other than a repo For steps 2-5. After checking for a valid url, devflow needs to know if this repo actually exist and can be accessed, as well as the size of the repo to avoid processing repos that are too large. Lastly check for tags or commits from the user that are valid, which all happen through Github's API, before cloning

## Cloning and checking out

* checking out a specific tag, to record the exact code that was ingested. Without pinning, evals would fail whenever the repo changes, even when DevFlow was right. If DevFlow only records the latest code, questions about the older versions of the code would be inaccurate
* Record the commit hash even if the user does not pass a tag, if a user asked why something happened, without the hash there would be no record of what version latest meant at ingestion time

## Filtering 

When filtering files such as `node_modules/` or `.git/`, two things are taken into account: cost and speed, and retrieval quality. Having fewer files to chunk, embed, and store makes processing faster and cheaper. When retrieving, chunks are ranked by how closely they match what the user is asking for, so without filtering, the top chunks could be library code instead of the user’s project. Retrieval quality is then improved with less noise competing with the code the user is asking for.

## Background job

1. User submits a URL. DevFlow runs the fast format check, then creates a repo record in the database with a new ID and status = pending
2. DevFlow reponds with the ID
3. slow work runs in the background (more checks, clone, filter, chunk, store), updating the status as it goes
4. the user checks GET /repos/{ID} to see the current status

Background job prevents user from having to wait on the same screen until the repo is done being processed. Additionally if a response was lost, the user would still be able to check on the status of their repo

## Status order

* submitted, github checks run (`pending`)
* Since cloning requires the entire repo to be downloaded over the network, it gets its own status (`cloning`)
* Filtering, chunking, storing are steps that happen almost instantly so they have shared status (`processing`)
* Storing will be split into its own status, since every chunks needs its own API call (`embedding`)
* If those steps are successful (`complete`)
* If a step failed, store failed step in `error` with the reason and step (`failed`)

## Access control

* Every request for a repo ID checks who's asking before returning anything
* If the repo's `user_id`is not matched with the logged-in-user's ID, the users get back `404 Not Found` so a repo's existence is not revealed
* This applies to every endpoint that takes a repo ID,  not just `GET/repo/{id}` since search and chat will need it to 

## Tables

Users

* Unique user ID (`id`)
* E-mail (`email`)
* Date created (`created_at`)
* Password hash (`password_hash`)

Repos

* Unique ID for repo URL (`id`)
* User ID (`user_id`)
* The GitHub URL submitted(`repo_url`)
* Any tags, if the user submitted any (e.g., v1.2.4) (`requested_ref`)
* Commit hash - exact commit ingested, which is filled in after checkout (`commit_hash`)
* Status (`status`)
* When it was created (`created_at`)

Chunks

* Each row in this table represents a piece of code in the repo
* unique ID (`id`)
* repo ID (`repo_id`)
* file path (`file_path`)
* content (`content`)
* where the chunk sits in the file (line numbers) (`start_line`, `end_line`

Embeddings

* foreign key to `chunks.id` (`chunk_id`)
* name of the embedding model (`model`)
* the vector itself (`embedding`)
* `chunk_id` + `model` together identify a row, since one chunk has at most one vector per model

## Why

Foreign keys such as repos.user_id should point to users.id, and chunks.repo_id should point to repos.id in the case that a user decides to change their email in the future and do not want to lose the repos they have already submitted in the past.

Having a separate table for embeddings saves the trouble of having to overwrite old vectors when switching embedding models. If in the future, I decide to switch embedding models, having a separate table for vectors allows for the two models to sit side-by-side for an eval comparison, at the cost of having every search needing one extra join.

Repos often contain several files with the same name, which could lead to false passes in retrieval, having file path included in the tables keeps the chunks unambiguous.
