## Block Validation (EVM)

[source](https://github.com/ethereum/wiki/blob/c02254611f218f43cbb07517ca8e5d00fd6d6d75/Block-Protocol-2.0.md#block-validation-algorithm)

- Check the following:

* Is there an object, which is a block, in the database with `block.prevhash` as its hash? Let `parent` be that block.
* Is the proof of work on the block valid?
* Is the proof of work on all uncle headers valid?
* Are all uncles unique and actually uncles (ie. children of the parent of the parent, but not the parent)?
* Is `block.timestamp <= now + 900` and is `block.timestamp >= parent.timestamp`?
* Is `block.number == parent.number + 1`?
* Is `block.difficulty == adjust_difficulty(parent.difficulty,timestamp,parent.timestamp)`?
* Is `block.transaction_hash = TRIEHASH(transaction_list)`?
* Is `block.stacktrace_hash = TRIEHASH(stacktrace)`?
* Is `block.uncle_hash = H(uncle_list)`?
