# Bridge Hand JSON Generator

Using github actions to schedule the generation of fresh bridge hands - stored as a json file to be accessed as an API.

Bridge scores presented using "High Card Points" and a ["Bergen Adjustment 3"](https://www.bridgewebs.com/ocala/Hand%20Evaluation.pdf) mechanism. Hands are separated into skewed and/or random generated based on the score.

Using the extremely accomplished [endplay package](https://endplay.readthedocs.io/en/latest/index.html) to generate and evaluate hands.

Hands returned as a dot separated string of `Spades`, `Hearts`, `Diamonds`, `Clubs` eg. "9863.92.95.KQT72"

Uses github actions described by [Python Engineer](https://www.python-engineer.com/posts/run-python-github-actions/)
