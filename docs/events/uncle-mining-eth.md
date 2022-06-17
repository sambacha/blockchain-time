---
created: 2022-06-17T09:42:33 (UTC -07:00)
tags: []
source: https://bitslog.com/2016/04/28/uncle-mining-an-ethereum-consensus-protocol-flaw/
author: 
---

# Uncle Mining, an Ethereum Consensus Protocol Flaw | Bitslog

> A year ago I was hired by Eth Dev Ltd through Coinspect to perform a security audit on the Ethereum design. One of our findings was that the uncle reward strategy in Ethereum was weird, and could l…

A year ago I was hired by Eth Dev Ltd through [Coinspect](https://coinspect.com/) to perform a security audit on the Ethereum design. One of our findings was that the uncle reward strategy in Ethereum was weird, and could lead to miners abusing the uncle rewards to almost triple the money supply. We discovered this problem because I had been working on the same problem for a long time, and posting in cryptocurrency mailing lists and [in this blog](https://bitslog.wordpress.com/2014/05/02/decor/) about a variation of Nakamoto consensus protocol called [DECOR+](https://bitslog.wordpress.com/2014/05/07/decor-2/), that is based on sharing block rewards between competing blocks. At that time I explained the flaw and suggested to limit the number of uncles to prevent an unbounded money supply function. I assumed the Ethereum core team would pick the DECOR+ protocol sooner or later, but Ethereum has now gone through several programmed hard-forks, and the problem still remains.

Last week, and the night before a [presentation](http://blockchaintechlab.com/timetable/2016/4/11/rootstock) of the RSK (a.k. Rootstock) smart-contract platform,  I decided to explore the problem a little more, and I found to my surprise that the uncle mining strategy theoretically works in Ethereum at very low thresholds, and therefore the current Ethereum consensus protocol is certainly not incentive compatible. Uncle mining strategy consist of forcing you own blocks into uncles (blocks not in the best chain) in order to earn uncle rewards while preventing your blocks from contributing to the block difficulty adjustments. Uncle mining is a greedy strategy (or even it can be considered dishonest), as the greedy miners get monetary compensations while providing less of the expected service to the network: uncle mining does contribute to securing the network due to GHOST weighting, but does not contribute to increasing the network transaction processing power.

Before publishing this post, I exchanged e-mails with Vitalik Buterin to check the math and make sure the problem exists. I’m now more confident that the problem does exists, although we disagreed on the severity. My duty now is to report it to the Ethereum community. The good news is that fixing it is easy, but the bad news is that it requires a hard-fork. Ethereum team will soon hard-fork to replace the current consensus protocol altogether with the new shiny Casper proof-of-stake consensus algorithm, so maybe that’s going to be a good moment to fix it.

The uncle mining problem is not exactly a security vulnerability, since no ether is stolen. However, it can bee seen as an unfair advantage, a design flaw, and a risk to the stability of the network. Things can get complicated if the majority of miners engage in uncle mining without coordination.

The theoretical results show that under certain optimal conditions uncle mining is profitable when the miner hashing power is over 12.5%. The practical threshold where uncle mining is profitable given the current efficiency of the Ethereum network is debatable. The debate goes around to what extent the optimality assumptions must be weakened to match the current network state.  I have discussed this with Vitalik Buterin, and we don’t agree: I suspect the actual threshold is near 20%, while Vitalik thinks this is in the 20%-37% range (without considering long term effects). I will present both points of view.

If you are an Ethereum user or company, you should protect the network from this eventual attack. To protect the network, users mining through open pools should refrain from using a pool if it starts uncle mining, or if the total uncle rate becomes larger than the uncle mining threshold (20% using my criteria) plus the inefficiency of the network floor (7%), approximately 27%. This is a deterrent for uncle mining in public mining pools, but not in private mining pools. In fact, there are other reasons why uncle mining in public pools may not work as expected.

There is a higher risk of uncle mining towards the Casper switch date, since miners owning huge amounts of GPUs may be incentivized to take advantage of it, as the arrival of the Casper deadline marks the end of their GPU mining business on Ethereum.

The problem benefits slightly more new large dishonest miners rather than pre-existent pools, because pre-existing pools must wait for a downward difficulty adjustment in order to start profiting from the dishonest strategy. As an example, an honest pool having 25% of the hashing power that turns dishonest undergoes an initial loss of about 500 USD during the first hour, and then it begins earning an additional 500 USD for every following hour (the ROI is 2 hours).

This analysis presented here is based on my knowledge of the Ethereum protocol and may contain inaccuracies (although no central flaw has been observed). Also I’ve not tried uncle mining myself, neither in a simulated net nor in the real network, so be aware that the strategies I propose in this post could not work exactly as expected. Please send me your comments if you find errors in this post  and I’ll review it.

One of the solutions to the design problem in Ethereum is to replace uncle rewards by reward sharing, as specified by the DECOR+ protocol described in this post. I’m preparing a paper on the [DECOR+](https://bitslog.wordpress.com/2014/05/02/decor/) protocol, and also the DECOR+ protocol has become one of the backbones of the [RSK smart contract platform](http://www.rootstock.io/). So soon you’ll be able analyze it theoretically and see working in practice.

## **Ethereum Consensus Protocol**

The core of Ethereum consensus protocol is a variation of the [GHOST consensus protocol](https://eprint.iacr.org/2013/881.pdf) which in turn is a variation of the Nakamoto consensus protocol. In GHOST, solved blocks that are not part of the best chain (stale blocks) can become _uncles_ when they are referenced by blocks in the best chain. The references are stored in a new field in the each block header. When an uncle is referenced, the branch that referenced the uncle increases its weight by the same amount as the uncle was part of the best chain. The best chain is selected as the branch with higher weight. In the two following figures, the best chain switches from the A branch to the B branch, but for different reasons. In figure 1, the branch B is chosen after receiving B3 because it is longer. In figure 2, it is chosen after receiving B2 because it has higher weight.

![LongestChain.png](https://bitslog.files.wordpress.com/2016/04/longestchain.png?w=620)

_Figure 1: Bitcoin. Longest branch prevails (assuming equal difficulty). When B3 arrives, the B branch is chosen as the best chain, as it is longer._

![GHOST.png](https://bitslog.files.wordpress.com/2016/04/ghost.png?w=620)

_Figure 2: Ethereum, heaviest branch prevails (GHOST).  When B2 arrives, the B branch is chosen as the best chain, since the uncle C1 counts as another block in the branch weight._

In GHOST uncles have no other function and their transaction content is ignored. But Ethereum does more with uncles: uncles are paid a reward that is created from thin air specifically for that purpose. The reward is n/8  of the current block subsidy, where n=7 if the uncle is included in a nephew block, 6 if it is included the a child of the nephew, etc. After 6 childs, stale blocks cannot be referenced anymore. In the case shown in figure 2, the miner of block C1 receives ⅞ of the subsidy of block B2.

## **Uncle mining**

The mining strategy I propose is simply to mine uncles instead of blocks extending the best chain. To mine uncles only, a miner must make sure that the block he solves is not included in the best chain (the chain with higher weight). For example, the miner start mining a normal child but then wait until all peers have received a competing block (at the same height) before broadcasting the sibling mined. The uncle mining strategy could be considered selfish, and be compared to the [selfish-mining strategy](https://www.cs.cornell.edu/~ie53/publications/btcProcFC.pdf), but later in this post we’ll see that uncle mining also benefits the remaining miners. It can be considered selfish if “self” represents all the miners, since the strategy increases all miners revenue but decreases the performance of the network (transactions per second) so Ethereum non-miner users are harmed.

**Uncle mining algorithm (strategy 1)**

1.  Let B be the best chain tip (the “tip” is the last added block on a chain)
2.  Start mining block C , being C a child of B.
3.  If solution for block C is found, store child C (but do not broadcast)
4.  If most of my peers have a block different from C at the block height of C:
    1.  retrieve all child blocks stored and broadcast
    2.  Go to step 1
5.  Go to step 3

This uncle strategy 1 (without modifications) works under 5 conditions:

1.  The remaining miners are honest (not performing uncle mining)
2.  There is no limit in the number of uncles allowed per block.
3.  The mining reward is constant per block.
4.  The hashing rate has stabilized so that there are no difficulty adjustments.
5.  Miners do not switch  between mining pools.

To analyze the performance of this uncle mining strategy more easily, we also add two assumptions:

1.  Uncles are most of the times included in a nephew block (and they are never left out), so the uncle reward is generally 7/8 of the block reward.
2.  Uncle inclusion reward is negligible.

We’ll show that even if we break any of these pre-conditions and even without the assumptions, once the hashing power is over a certain threshold (which is below 50%) there is usually a modified uncle mining strategy that is better than the honest one. For example, the limit of two uncles referenced per block does not prevent an uncle mining strategy.

First we’ll show a simple example of how this uncle-mining strategy works. Suppose that a malicious miner X (or mining pool) has 25% of the total mining hashing power. Suppose also that there are no uncle blocks produced by the network (ideal setup).

Then the honest mining strategy can be represented by the following “average” cyclic mining pattern in figure 3.

![25](https://bitslog.files.wordpress.com/2016/04/25.png?w=620)

_Figure 3__: “__Average” Mining Pattern for honest miners (light-blue miner has 25%__)_

We say that it’s an average mining pattern even if mining does not generate this exact periodical pattern. If we split the mined blockchain in slices of 4 blocks each, the randomness of the mining process may create patterns where the dishonest miner solves two or more blocks and others where it does not solve any (in the “average” pattern, the dishonest miner solves only one).  However, we can still characterize this mining state by the average (most probable) pattern depicted in figure 3, which corresponds to the average payout.  If the reward per block is R, clearly miner X receives R\*0.25 per block on average.

Now we present the uncle mining  pattern in figure 4.

_![25u.png](https://bitslog.files.wordpress.com/2016/04/25u2.png?w=620)_

_Figure 4: Uncle  mining pattern_

In this pattern the block B1 is a sibling of the block A1, and it is referenced by a child block A2 of the best chain (in orange). Because B1 does not count in the difficulty calculation for establishing mining target difficulty, and because we assume the blockchain is in a stable state, the difficulty of this blockchain state must be lower than of the average state. If assume without loss of generality that the average state difficulty is 1, then the uncle mining state difficulty is ¾. Also we can easily see that the pattern repeats every 3 blocks of the best chain, not 4. Therefore, the rate of this pattern is 4/3 of the rate of the average pattern. Note that the GHOST blockchain weight does not vary from the average pattern to the uncle mining pattern, but the GHOST weight is not what drives the mining difficulty in Ethereum, [but block timestamps are](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-2.mediawiki).

As we assumed the uncle was always included and was generally included in the nephew block, then the average uncle reward is close to 7/8 (although in practice is will always be slightly lower). Therefore, the revenue of miner X per pattern is 7/8 every 3 blocks, or R\*7/8\*1/3 ~=R\*0.29.

So the uncle mining strategy provides (0.29-0.25)/0.25=16% more revenue for miner X.

If the hashing power of X is P (as a factor of the total hashing power), then under the conditions listed, this uncle mining strategy generates a revenue of R\*7/8\*P/(1-P). Since the honest mining strategy obtains a reward of R\*P, then the increase of revenue for the malicious miner as a factor of the honest revenue is 7/(8\*(1-P))-1. This is positive if P > 1/8. In other words, this strategy should be selected by any rational miner if his hashing power is greater than 12.5% of the network hashing power.

**But the dishonest miners have also increased the honest miners revenue! Why would they do that?**

If we analyze the revenue of a honest miner having 25% of the hashing power, we see the dishonest miner has helped the honest miners increase its revenue from R\*0.25 to R\*0.33. This is because mining in Ethereum is not a [zero-sum game](https://en.wikipedia.org/wiki/Zero-sum_game), miners in Ethereum are not competing, but incentivized to form an organization.

One may argue against the benefit of the strategy of uncle mining by noting that by increasing the money supply, dishonest miners are increasing the monetary inflation rate, which indirectly makes their recently earned coins less valuable. But this an indirect and much weaker effect. If the main incentive for the dishonest miner is selling the earned ether, then I don’t see why wouldn’t they perform uncle  mining, even if it also benefits the remaining honest miners.

If the dishonest miner is not a mining pool but a private miner, and the strategy of the dishonest miner is to increase the percentage of ether owned over the total ether in existence compared to other miners, over a long period of mining, and assuming the other miners are also private miners hoarding their rewards, all in order to be able to have higher returns when Casper (proof-of-stake) mining is in effect, then maybe behaving honestly is better. Honest mining keeps the balance between miners stakes. But the efficient market hypothesis implies that proof-of-stake mining will not be profitable, because the entry barrier to Casper mining is low  (just buy enough ether and create a bond). Therefore, dishonest PoW mining seems the best plan now.

Now we can see how some of the conditions and assumptions affect the uncle mining strategy.

**What if the remaining miners are dishonest and also follow the uncle mining strategy?**

If all remaining miners are also dishonest, and if there is no limit in the number of uncles to reference in a block, then clearly we can reach a tragedy of the commons and the network would stall. But Ethereum limits the number of uncles per block to at most 2. The current average number of uncles per block (as of block 1362900) is [as low as 7%](https://stats.etherchain.org/dashboard/db/uncles?theme=light). This means that there is plenty of uncle space so that 60% of the network hashing power can turn dishonest without uncle competition between dishonest parties. The [current](https://stats.etherchain.org/dashboard/db/uncles?theme=light) 7% uncle rate also means that no mining pool is doing uncle mining right now, since uncle rate must reach 12.5% to make us suspect a miner is profiting from it. Note that the best strategy for a miner turning dishonest is not to switch completely and instantaneously to uncle mining, but to do it gradually so that the best chain keeps increasing while the difficulty drops.

If the uncle rate is high enough so that uncle mining strategies compete with each other, then a modification of the previous strategy can prevent competition and assure a steady revenue from uncle mining as shown by figure 5.

![40u2](https://bitslog.files.wordpress.com/2016/04/40u2.png?w=620)

_Figure 5: Uncle strategy 2 for miner having 40% of the hashing power_

This strategy is a modification of strategy 1, but also mines blocks in the best chain referencing self-solved uncles whenever these uncles are unreferenced by the remaining miners.

**Uncle mining algorithm (strategy 2)**

1.  Let B be the best chain tip
2.  If at least one locally found block has not been referenced by other blocks in the best chain for a depth greater than k:
    1.  Start mining a child C of B normally, referencing the missing siblings (max 2 siblings).
    2.  If a solution for C is found:
        1.  Broadcast the locally solved blocks (if not broadcasted before)
        2.  Broadcast the solved block C referencing the solved blocks
        3.  Remove the referenced blocks from local storage (if present)
        4.  Go to step 1
    3.  If B is no longer the best chain tip:
        1.  Go to step 1
    4.  Go to step 2b
3.  If all locally stored valid blocks have been referenced by mined blocks:
    1.  Start mining block C, being C  a child of B.
    2.  If solution for block C is found:
        1.  Locally store the block C (but do not broadcast)
    3.  If most of my peers have a sibling of C in their best chain:
        1.  retrieve all locally stored blocks and broadcast all of them
        2.  Go to step 1
    4.  Go to step 3a
4.  Go to step 3

This strategy does rely on some of the conditions 1 (remaining miners are honest, and unlimited uncles). The best value for k has not been analyzed in this article (k may be a constant but can also depend on the number of unreferenced self-mined uncles).

To compute a back-of-the-envelope approximation on the additional revenue the dishonest miner can make we can further assume:

1.  The uncle space is saturated
2.  Miners never reference uncles created by other miners
3.  Each dishonest miner creates 2 uncle blocks per best chain block
4.  The uncle payout is 5/8 (instead of 7/8) because uncles are not immediately referenced, but only referenced at depth 3, on average.

Even if the maximum uncle reference depth in Ethereum is 7, we present a pattern having period 6 to avoid delaying uncle references too much (because uncle payout depends on this). The resulting periodic pattern that takes advantage of the strategy 2 is depicted in figure 6.

![minu2](https://bitslog.files.wordpress.com/2016/04/minu2.png?w=620)

_Figure 6: (Almost) best pattern allowing uncle  mining of 2 uncles in a dishonest network_

Considering this pattern, it can be seen that the strategy 2 only works if P >= 3/8. In other words, the dishonest miner must control 37% of the hashing power (the reason is because the periodic pattern in figure 6 contains 8 total blocks, and 3 belong to miner X). Note that this back-of-the-envelope computation (and the minimum pattern) is only an approximation, since the best pattern depends on the value (or function) k.

Since the hashing rate will be 8/6 faster than the honest state, the expected earnings for X from this uncle mining pattern is R\*8/6\*(1+2\*5/8)/6=R\*0.5. That means that a dishonest miner having 37% of the mining hashing power can earn approximately (0.5-0.37)/0.37=35% more.

**From Theory to Practice. What is the actual practical threshold?**

By evaluating the current state and efficiency of the Ethereum network I suspect the uncle mining threshold is close to 20%. Vitalik has raised several objections to this figure, which I list below and I try to address  (original Vitalik objections have  been minimally edited to reduce space):

Objection 1: Not all uncles immediately get included in the earliest possible block, and so they often get lower rewards than the maximum. Empirically, we see (eg. from [etherscan statistics](http://etherscan.io/charts/uncles)) that the average uncle reward is ~3.28 ETH (close to 5/8). This raises the threshold to ~34.5%.

Partial Refutation: Propagating a block takes 2 seconds in Ethereum. Therefore miners should be including the uncle immediately in the following block. There must be a problem in Ethereum clients related to uncle propagation, or else uncles that are being captured by etherscan are “special” in some way.  What is happening now is that uncle referencing is delayed because one of the following reasons:

1.  uncles are consuming more block space and that delays transmission
2.  uncles are consuming more CPU during verification
3.  uncles are being created by a minority of miners with poor connectivity
4.  mining pool management applications do not update immediately workers when a new uncle is received, but they do update their workers immediately when the best chain has been modified. Polling for new block templates is either not done or done only at a low rate.
5.  there is an attack ongoing where some miners are blocking uncles from propagating or avoiding referencing them.

In any except the last two cases, I suppose the greedy miner can just increase the uncle rewards to ⅞ by having efficient and robust network connectivity.If the reason is 4, then clearly uncles will be delayed one block unless they are sent milliseconds before the pool software ask for a new template but after the pool software has been notified of the new best chain block. If this is the cause of the lower than expected average uncle reward, then uncle mining threshold will be close to 25%.

The statistics in [http://etherscan.io/charts/blocks](http://etherscan.io/charts/blocks) show that the current block reward is close to 5.01 eth so transaction fees are less than 1%.  If the reason of uncle inclusion delay is their size/CPU, then the attacker can just mine empty uncles. If this is the case (and I suppose it is) then the dishonest miner can expect the uncle reward to be still close to 7/8.

Objection 2: If you try to mine uncles, then ~7% of the time you will fail for the same reason why normal miners make an uncle (ie. unexpected block). You can think of this failure mode as being knocked down one rung on the ladder, so subtract another 7%.

Partial Refutation: While is it true that the delay in broadcasting a block makes that blocks less probable to be referenced by a nephew, the delay is much less than a rung in the ladder. A full rung would be a delay of an average block interval (12 seconds) while the current delay is comparable to the network propagation time, and the later can be reduced by the attacker by increasing its network connectivity. Therefore I concede a 3% reduction in profit here.

Objection 3: If you’re uncle mining at 35.5%, then ~17.5% of the time you’ll create three uncles before the next block gets created, so one of those three blocks will be knocked down further.

Refutation: First, our uncle mining strategy is not “uncle mining”, but normal child mining while keeping the block secret for some time until it becomes stale. So the best strategy in the lucky case a miner mines two children of a parent is just to start mining a grandchild of one of the children referencing the other child as an uncle. If you find a solution to the grandchild, then  publish all three. This basically extends the best chain of the network by 2 blocks. Two things are accomplished: if gives the miner 2 full rewards, and assures the miner a full 7/8 uncle reward. Also the miner can probably tweak the dates to prevent difficulty adjustments.

Objection 4: If you are carrying out this attack as part of a pool, then you are increasing others’ revenues along with your own. Hence, you are actually **creating an incentive** for miners to leave your pool. If you’re doing it as a solo miner, then of course it doesn’t apply, unless you have investors in which case you are a kind of pool in an economic sense.

Granted: Yes. That’s why I say that the strategy is probably good for a new private miner that starts mining, and not so good for a mining pool.

Objection 5: This analysis assumes that miners are a static set. In reality, increasing the mining reward will bring new miners in.

Partially granted: This is probably the only reason why uncle mining may not be good idea in the mid/long term (more than 2 months). But not in the short term, not with current ether volatility. As an example, the price of ether now is 6 times more than in January. The peak was in March (15 times more than January). But since March the price is declining (lost 50% of its value) but the hashrate has risen 300% during the decline period ([http://etherscan.io/charts/hashrate](http://etherscan.io/charts/hashrate)). That means that mining engagement response to a price increase/decrease has at least a 2 months delay. Therefore the uncle miner should not expect any change related to its behaviour before two months. However, after two months, the uncle miner (and any other miner) will see a decrease in its revenue that could cancels out its previous profit. I agree with V.B. that this objection does not apply in the months right before a PoS switch, when no new miners will be brought. Also this objection does not apply if the uncle miner is willing to switch to other more profitable cryptocurrencies when Ethereum becomes unprofitable, which is what multi-pools often do.

**Assuming a 20% uncle mining threshold,  how serious is the problem?**

The current hashrate distribution in Ethereum is [heavily centralized](https://etherchain.org/statistics/miners). The [dwarftpool](https://dwarfpool.com/) has 40.7% of the hashing power,  followed by [ethpool](http://ethpool.org/) having 16.2%. So dwarfpool is the only pool with enough resources to perform the uncle mining attack. Luckily this is a public mining pools, so miners could move away from them if they become dishonest. Therefore the problem can be contained, if individual miners want it. Another important property of uncle mining is that it is evident, and can be [tracked](https://ethstats.net/). Because the current average [number of uncles per block](https://stats.etherchain.org/dashboard/db/uncles?theme=light) is as low as 7%, we know no mining pool is currently taking advantage of the problem. If we assume that 7% is the current inherent inefficiency of the network, then if the uncle rate reaches 27% (20%+7%) for more than two hours it would mean that there is high probability a pool (or combination of pools) is doing uncle mining. Users should monitor the uncle rate and take action if that happens. Also the Ethereum core developers can prepare to deploy a hard-fork in case uncle mining is being performed.

**How to solve this flaw?**

First of all we should note that Ethereum algorithm used to compute difficulty is based only on [parent block time](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-2.mediawiki). Basically it increases the difficulty in a small step if the parent block was too close and decreases the difficulty if it was too far away. It does not take into account the chain weight. Contrary, [Bitcoin difficulty](https://en.bitcoin.it/wiki/Difficulty) adjusting algorithm takes the last 2016 blocks and adjusts the difficulty so the next 2016 blocks are created in 14 days on average, using the first and last block timestamps (but also has a subtle [bug](http://bitcoin.stackexchange.com/questions/20597/where-exactly-is-the-off-by-one-difficulty-bug)). If Ethereum had used an algorithm similar to Bitcoin’s but based on the chain weight (weight/time), then mining uncles would not increase the rate of the best chain, and uncle mining would be prevented.

I propose three different ways to solve the uncle mining problem:

1.  Computing a chain difficulty by taking into account uncles. This is done by changing the current Ethereum difficulty algorithm and establishing a new algorithm that computes difficulty based on the total weight of a branch over the time taken by such branch.
2.  Reduce the maximum uncle reward to 1/2.
3.  Switching the consensus protocol to DECOR+.

The first and second solutions do not work well if the subsidy is much lower than mining fees: in that case the uncle reward does not provide any meaningful payment. As this is the Ethereum long term plan, I suppose this solution is not the best for Ethereum. The third solution works in any case (but pushing the best chain forward having low subsidy and low transaction fees is still an open problem in cryptocurrency design)

## **DECOR+**

In a nutshell the DECOR+ strategy is to share the block reward between all miners that have solved a block of the same height. As in Ethereum, uncles are referenced on-chain, by a special field in each block header (e.g. UncleList\[\]) that contains only uncle headers (or other parent or grand-parent sibling blocks). The transaction information of uncles is not included. The reward is split after a coinbase maturity period (when uncles can be referenced in UncleList\[\] fields), using the following criteria:

1.  The full reward of a conflicting block must pay a _forward pressure fee (e.g. 0.6%)_. This can be fixed or made variable depending on difficulty adjustments that occurred in the last uncle inclusion interval. If not such difficulty adjustment event has occurred, this fee can be set to zero. The forward pressure fee must be burned.
2.  From what is left, if the conflicting block and sibling headers do not obey a selection rule (see below) a _punishment fee_ is subtracted (e.g. 10%). The punishment fee must be burned.
3.  From what is left, a factor of the remaining (e.g. 10%) is the _publisher’s fee_, and it is shared in equal parts between the miners that included uncle headers for a specifi block.
4.  The remaining is the _reward share_ and it is split in equal parts between the miners that solved the sibling blocks (including the miner of the block in the best chain and the miners that solved the uncle headers).

The selection rule says that miners must always choose the parent block that has higher reward (subsidy plus transaction fees). If both have the same, then they must choose one with lower header hash. The selection rule imply that nodes do not obey the first seen rule. The first seen rule (in Bitcoin) stipulates that if a node receives two competing blocks, and both extend the best chain, they must chose the first one received (and verified), and discard the second. In DECOR+ nodes may change the best chain tip if a competing block is received and has higher reward. This also implies that single-block confirmations in DECOR+ are weaker than single block confirmations in Ethereum, but only before the network propagation time has elapsed (about 3 seconds in Ethereum). After that moment, single-block confirmations in DECOR+ are stronger than single-block confirmations in Ethereum, since normally in DECOR+ there should not be two competing branches, while in Ethereum there might be (but this fact is known to the network, due to uncle header propagation).

The forward pressure creates an incentive to move forward in the block-chain by extending it in the cases where the network difficulty has increased. This is to prevent miners creating uncles at lower difficulty and higher reward. Note that nothing prevents miners from mining uncles if sibling blocks have rare huge rewards (by means of transaction fees) compared to the fees that can be collected from the transaction pool. Nevertheless, in this condition disappears as soon as the huge reward is split between miners and each sibling reward share becomes lower than a block reward at the tip of the best chain.

The exact percentages for each kind of fee can be changed. For example, to incentivize miners to have better network connectivity, the punishment fee can be increased. To incentivize miners to broadcast uncle headers, the publisher’s fee can be increased. If the sharing steps are performed as described (first forward pressure fee, then punishment fee, then publishers fee, and last sibling blocks sharing) then the right incentives will prevail.

The RSK (a.k.a. [Rootstock](http://www.rootstock.io/)) smart-contract platform uses DECOR+, and the follow slide in figure 7 from my last RSK presentation compares the protections on Bitcoin, Ethereum and RSK platforms have against theoretical uncle/selfish mining strategies (practical thresholds vary).

![BitcoinEthereumRSK.png](https://bitslog.files.wordpress.com/2016/04/bitcoinethereumrsk.png?w=620)

_Figure 7: Theoretical uncle/selfish mining thresholds for Bitcoin, Ethereum and RSK_

**Incentive for miners to switch from honest to dishonest strategies**

Difficulty adjustments in Ethereum are progressive and slow ([Homestead](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-2.mediawiki) hard-fork release increased the speed of downward adjustments). Ethereum allows each block to perform a [positive or negative adjustment](http://ethereum.stackexchange.com/questions/1880/how-is-the-mining-difficulty-calculated-on-ethereum) of a factor of at most 1/2048 of the previous difficulty. The average number of blocks required to stabilize the difficulty after a drop of 25% is 589 blocks (approximately 2 hours, but tweaking the time field can reduce this a bit). This means that a pool having 25% of the hashing power that is honest and turns dishonest must wait approximately 1 hour (294 blocks at a 25% slower rate) mining at a loss until it starts getting higher profits. During that period, we assume the dishonest miner rewards become approximately 7/8 of average rewards. The following table summarizes the cost for the miner to switch from honest to dishonest using the uncle mining strategy 1, assuming current ETH/USD exchange rate.

<table><tbody><tr><td>Honest profit (294 blocks)</td><td>Dishonest profit</td><td>Initial Loss</td></tr><tr><td>73.5 rewards =<p>367.5 ETH =</p><p>3307 USD</p></td><td>64.31 rewards =<p>321.5 ETH =</p><p>2894 USD</p></td><td>413 USD (12%)</td></tr></tbody></table>

This dishonest miner undergoes an initial loss of not more than 500 USD during the first hour, and then it begins earning an additional 500 USD for every following hour (the ROI is 2 hours). This is not the optimal switching strategy, but it is close to.

## **Conclusion**

In this post we’ve analyzed a flaw in Ethereum consensus protocol related to uncle rewards that incentivize miners having more than 12.5% of the hashing power to do uncle mining. The practical threshold where uncle mining becomes profitable is between 12.5% and 37%, and more network analysis is required to find out the current threshold. Uncle mining is in some ways similar to “selfish” mining, but the word “selfish” here is misleading  since, over certain threshold, uncle mining benefits all miners. Also the the same flaw allows the majority of miners in collusion to almost triple the money supply. The flaw is not critical, but should not be disregarded. Although this post does not present a formal analysis of the optimal strategy nor provides formal proof, it shows two easy to understand uncle mining strategies that are clearly better than the honest strategy. Finally we propose three solutions: the first solution is based on changing how block difficulty is computed, the second based on reducing the uncle reward, and the third based on changing how uncle and block rewards are computed (DECOR+ protocol). Only the last works when the block subsidy is low. We’re preparing an academic paper on DECOR+ that I hope will soon be published (thanks to Philippe Camacho).

Finally, we’ve a working implementation of DECOR+ in the [RSK smart-contract platform](http://www.rootstock.io/) soon to be open-sourced and launched. Also DECOR+ can be implemented in Bitcoin through a soft-fork, although the need for DECOR+ is higher only when block rate is  also higher.

This entry was posted on April 28, 2016, 1:51 am and is filed under [Uncategorized](https://bitslog.com/category/uncategorized/). You can follow any responses to this entry through [RSS 2.0](https://bitslog.com/2016/04/28/uncle-mining-an-ethereum-consensus-protocol-flaw/feed/ "RSS 2.0"). You can [leave a response](https://bitslog.com/2016/04/28/uncle-mining-an-ethereum-consensus-protocol-flaw/#respond), or [trackback](https://bitslog.com/2016/04/28/uncle-mining-an-ethereum-consensus-protocol-flaw/trackback/) from your own site.
