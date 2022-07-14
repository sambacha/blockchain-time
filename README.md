---
title: On the usage of Time in Blockchains
type: monograph
version: draft
summary: deterministic time tables and accounting
---


## Ethereum Genesis 

>**Note**    
> Jul-30-2015 03:26:13 PM +UTC is not the 'true' timestamp for the genesis block. 

[see https://github.com/ethereum/go-ethereum/issues/17042#issuecomment-559414137](https://github.com/ethereum/go-ethereum/issues/17042#issuecomment-559414137)

So, etherscan does show the genesis: etherscan.io/block/0 -- but they must have put some hack into place to make it show up as (Jul-30-2015 03:26:13 PM +UTC) -- because AFIK the actual timestamp on the genesis is all zeroes, which is 1970. Unless I'm mistaken, there's no error in geth here, possibly etherscan.

The same holds when querying a node running Parity: timestamp for block 0 is 0. On the other hand, etherscan.io shows Jul-30-2015 03:26:13 PM +UTC as timestamp for the genesis block. It would be nice to have a consistent view, or at least an explanation like "0 is correct, etherscan is just extrapolating".

[source, frontiner genesis: https://raw.githubusercontent.com/ethereum/ethereumj/develop/ethereumj-core/src/main/resources/genesis/frontier.json](https://raw.githubusercontent.com/ethereum/ethereumj/develop/ethereumj-core/src/main/resources/genesis/frontier.json)


### Blockchain Time: On the subject of Time and its Implementations on-chain and off-chain

> Resources for utilizing time on-chain
  * [Blockchain Time: On the subject of Time and its Implementations on-chain and off-chain](#blockchain-time--on-the-subject-of-time-and-its-implementations-on-chain-and-off-chain)
  * [Background](#background)
    + [time2posix](#time2posix)
    + [strftime()](#strftime--)
    + [TimeZones](#timezones)
    + [Valid ISO 8601 date or time formats](#valid-iso-8601-date-or-time-formats)
    + [Daylight Savings Changes](#daylight-savings-changes)
- [CalSystems](#calsystems)
- [Seconds](#seconds)
- [UNIX](#unix)
- [Time Stamp Formats](#time-stamp-formats)
- [Time Stamp Conventions](#time-stamp-conventions)
- [Julian-Gregorian Adoption Dates](#julian-gregorian-adoption-dates)
  * [References](#references)


## Block Timestamp Manipulation

> [source: sigmaprime blog ](https://blog.sigmaprime.io/solidity-security.html#keyless-eth:~:text=such%20a%20transaction.-,12.%20Block%20Timestamp%20Manipulation,but%20it%20is%20something%20to%20be%20aware%20of%20when%20developing%20contracts.,-Real%2DWorld%20Example)

Block timestamps have historically been used for a variety of applications, such as entropy for random numbers (see the Entropy Illusion section for further details), locking funds for periods of time and various state-changing conditional statements that are time-dependent. Miner's have the ability to adjust timestamps slightly which can prove to be quite dangerous if block timestamps are used incorrectly in smart contracts.

Some useful references for this are: The Solidity Docs, this Stack Exchange Question.

### The Vulnerability
`block.timestamp` or its alias `now` (depreciated) can be manipulated by miners if they have some incentive to do so. Let's construct a simple game, which would be vulnerable to miner exploitation,


```solidity
// roulette.sol:
contract Roulette {
    uint public pastBlockTime; // Forces one bet per block

    constructor() public payable {} // initially fund contract

    // fallback function used to make a bet
    function () public payable {
        require(msg.value == 10 ether); // must send 10 ether to play
        require(now != pastBlockTime); // only 1 transaction per block
        pastBlockTime = now;
        if(now % 15 == 0) { // winner
            msg.sender.transfer(this.balance);
        }
    }
}
```

This contract behaves like a simple lottery. One transaction per block can bet 10 ether for a chance to win the balance of the contract. The assumption here is that, block.timestamp is uniformly distributed about the last two digits. If that were the case, there would be a 1/15 chance of winning this lottery.

However, as we know, miners can adjust the timestamp, should they need to. In this particular case, if enough ether pooled in the contract, a miner who solves a block is incentivised to choose a timestamp such that block.timestamp or now modulo 15 is 0. In doing so they may win the ether locked in this contract along with the block reward. As there is only one person allowed to bet per block, this is also vulnerable to front-running attacks.

> **Note** 
> block timestamps are monotonically increasing and so miners cannot choose arbitrary block timestamps (true for Ethereum1)

In practice, block timestamps are monotonically increasing and so miners cannot choose arbitrary block timestamps (they must be larger than their predecessors). They are also limited to setting blocktimes not too far in the future as these blocks will likely be rejected by the network (nodes will not validate blocks whose timestamps are in the future).

### Preventative Techniques

Block timestamps should not be used for entropy or generating random numbers - i.e. they should not be the deciding factor (either directly or through some derivation) for winning a game or changing an important state (if assumed to be random).

Time-sensitive logic is sometimes required; i.e. unlocking contracts (timelocking), completing an ICO after a few weeks or enforcing expiry dates. It is sometimes recommend to use block.number (see the Solidity docs) and an average block time to estimate times; .i.e. 1 week with a 10 second block time, equates to approximately, 60480 blocks. Thus, specifying a block number at which to change a contract state can be more secure as miners are unable to manipulate the block number as easily. The BAT ICO contract employed this strategy.

This can be unnecessary if contracts aren't particularly concerned with miner manipulations of the block timestamp, but it is something to be aware of when developing contracts.



### Equation 

<img src="https://render.githubusercontent.com/render/math?math=UnixTime%3D(JD%5Bmo%2C%20day%20%2Cyr%5D-2440588)*86400">

### UNIX Background

#### time2posix

IEEE Std 1003.1-1988 (`POSIX.1`) legislates that a time_t value of
536457599 shall correspond to "Wed Dec 31 23:59:59 GMT 1986." This
effectively implies that POSIX time_t's cannot include leap seconds and,
therefore, that the system time must be adjusted as each leap occurs.

#### strftime()

The C and POSIX standards define for the strftime() function and the
date utility a notation for defining date and time representations. Here
are some examples, of how they can be used to produce ISO 8601 output:

```bash
format string 	output
%Y-%m-%d 	      1999-12-31
%Y-%j 	        1999-365
%G-W%V-%u      	1999-W52-5
%H:%M:%S      	23:59:59
```

[JSON Schema `date-time`](https://json-schema.org/latest/json-schema-validation.html#RFC3339)
```bash
date --rfc-3339=seconds | sed 's/ /T/'
> 2021-03-29T19:12:08-07:00
```

#### TimeZones

```bash
date -u +"%Y-%m-%d %H-%M-%SZ"
date -u +"%Y-%m-%dT%H:%MZ"
```

Z and +00:00 are the same (mostly). For purposes of translating time,
they both mean UTC. However England is +00:00 in winter and +01:00 in
summer (BST). Z is UTC, while +00:00 is GMT.

GNU `date` `date -I` is the same as ` date +%F`, and `-Iseconds` and
`Iminutes` also include time with UTC offset.

```bash
date +%F # -I or +%Y-%m-%d
date +%FT%T%z # -Iseconds or +%Y-%m-%dT%H:%M:%S%z
date +%FT%H:%M # -Iminutes or +%Y-%m-%dT%H:%M%z
date -u +%FT%TZ
```

#### Valid ISO 8601 date or time formats

```bash
20130503T15 (%Y%m%dT%M)
2013-05 (%Y%m)
2013-W18 (%Y-W%V)
2013-W18-5 (%Y-W%V-%u)
2013W185 (%YW%V%u)
2013-123 (%Y-%j, ordinal date)
2013 (%Y)
1559 (%H%M)
15 (%H)
15:59:24+03 (UTC offset doesn't have to include minutes)
```

```bash
$ date -u -Iseconds
$ date -u '+%Y-%m-%dT%k:%M:%S%z'
```

#### Daylight Savings Changes

| **From**                   | **To**                  | **On**                     | **At**                      | **Action**  | \*\*\*\*                   |
| -------------------------- | ----------------------- | -------------------------- | --------------------------- | ----------- | -------------------------- |
| 1918                       | 1919                    | last Sunday                | in March                    | 02:00 local | go to daylight saving time |
| in October                 | return to standard time |                            |                             |             |                            |
| 1942 only                  | February 9th            | go to “war time”           |                             |             |                            |
| 1945 only                  | August 14th             | 23:00 UT                   | rename “war time” to “peace |             |                            |
| time;” clocks don’t change |                         |                            |                             |             |                            |
| September 30th             | 02:00 local             | return to standard time    |                             |             |                            |
| 1967                       | 2006                    | last Sunday                | in October                  |             |                            |
| 1973                       | in April                | go to daylight saving time |                             |             |                            |
| 1974 only                  | January 6th             |                            |                             |             |                            |
| 1975 only                  | February 23rd           |                            |                             |             |                            |
| 1976                       | 1986                    | last Sunday                | in April                    |             |                            |
| 1987                       | 2006                    | first Sunday               |                             |             |                            |
| 2007                       | present                 | second Sunday in March     |                             |             |                            |
| first Sunday in November   | return to standard time |                            |                             |             |                            |

## CalSystems

| **cal_system** | **AverageYear(Days)**   | **ErrorPerYear(Days)** | **ErrorRatio** | **CylcePeriod** | **1-DayShift** | **100-yearError(Days)** |
| -------------- | ----------------------- | ---------------------- | -------------- | --------------- | -------------- | ----------------------- |
| 365            | 365                     | 0\.2422                | 6\.63 xx10\-4  | 1,508           | 4\.129         | 24\.22                  |
| Julian         | 365\.25                 | \-0\.0078              | 2\.14 xx10\-5  | 46,826          | 128\.2         | 0\.78                   |
| Gregorian      | 365\.2425               | \-0\.0003              | 8\.2 xx10\-7   | 1,200,000       | 3,333\.30      | 0\.03                   |
| 4000           | 365\.24225              | \-0\.00005             | 1\.4 xx10\-7   | 7,300,000       | 20,000         | 0\.005                  |
| 2//900         | 365\.2422               | \-0\.000022            | 6\.1 xx10\-8   | 16,000,000      | 45,000         | 0\.002                  |
| Jalaali        | 365\.242424             | \-0\.000224            | 6\.1 xx10\-7   | 1,600,000       | 4,460          | 0\.02                   |
| 31//128        | 365\.24218750 \.0000125 | 0 \.0000125            | 3\.4 xx10\-8   | 29,000,000      | 80,000         | 0\.001                  |

## Seconds

| **Layman time**               | **Seconds** |
| ----------------------------- | ----------- |
| 1 minute                      | 60          |
| 5 minutes                     | 300         |
| 10 minutes                    | 600         |
| 30 minutes                    | 1800        |
| 1 hour                        | 3600        |
| 2 hours                       | 7200        |
| 4 hours                       | 14400       |
| 6 hours                       | 21600       |
| 8 hours                       | 28800       |
| 12 hours                      | 43200       |
| 1 day                         | 86400       |
| 2 days                        | 172800      |
| 3 days                        | 259200      |
| 4 days                        | 345600      |
| 5 days                        | 432000      |
| 6 days                        | 518400      |
| 1 week                        | 604800      |
| 2 weeks                       | 1209600     |
| 4 weeks                       | 2419200     |
| 1 month \(30 days\)           | 2592000     |
| 1 month \(avg\. 30\.44 days\) | 2629743     |
| 1 month \(31 days\)           | 2678400     |
| 1 year \(365 days\)           | 31536000    |
| 1 year \(avg\. 365\.24 days\) | 31556926    |
| leap year \(366 days\)        | 31622400    |

## UNIX

| **Regular date** | **Unix timestampGMT/UTC** |
| ---------------- | ------------------------- |
| 1930, January 1  | \-1262304000              |
| 1931, January 1  | \-1230768000              |
| 1932, January 1  | \-1199232000              |
| 1933, January 1  | \-1167609600              |
| 1934, January 1  | \-1136073600              |
| 1935, January 1  | \-1104537600              |
| 1936, January 1  | \-1073001600              |
| 1937, January 1  | \-1041379200              |
| 1938, January 1  | \-1009843200              |
| 1939, January 1  | \-978307200               |
| 1940, January 1  | \-946771200               |
| 1941, January 1  | \-915148800               |
| 1942, January 1  | \-883612800               |
| 1943, January 1  | \-852076800               |
| 1944, January 1  | \-820540800               |
| 1945, January 1  | \-788918400               |
| 1946, January 1  | \-757382400               |
| 1947, January 1  | \-725846400               |
| 1948, January 1  | \-694310400               |
| 1949, January 1  | \-662688000               |
| 1950, January 1  | \-631152000               |
| 1951, January 1  | \-599616000               |
| 1952, January 1  | \-568080000               |
| 1953, January 1  | \-536457600               |
| 1954, January 1  | \-504921600               |
| 1955, January 1  | \-473385600               |
| 1956, January 1  | \-441849600               |
| 1957, January 1  | \-410227200               |
| 1958, January 1  | \-378691200               |
| 1959, January 1  | \-347155200               |
| 1960, January 1  | \-315619200               |
| 1961, January 1  | \-283996800               |
| 1962, January 1  | \-252460800               |
| 1963, January 1  | \-220924800               |
| 1964, January 1  | \-189388800               |
| 1965, January 1  | \-157766400               |
| 1966, January 1  | \-126230400               |
| 1967, January 1  | \-94694400                |
| 1968, January 1  | \-63158400                |
| 1969, January 1  | \-31536000                |
| 1970, January 1  | 0                         |
| 1971, January 1  | 31536000                  |
| 1972, January 1  | 63072000                  |
| 1973, January 1  | 94694400                  |
| 1974, January 1  | 126230400                 |
| 1975, January 1  | 157766400                 |
| 1976, January 1  | 189302400                 |
| 1977, January 1  | 220924800                 |
| 1978, January 1  | 252460800                 |
| 1979, January 1  | 283996800                 |
| 1980, January 1  | 315532800                 |
| 1981, January 1  | 347155200                 |
| 1982, January 1  | 378691200                 |
| 1983, January 1  | 410227200                 |
| 1984, January 1  | 441763200                 |
| 1985, January 1  | 473385600                 |
| 1986, January 1  | 504921600                 |
| 1987, January 1  | 536457600                 |
| 1988, January 1  | 567993600                 |
| 1989, January 1  | 599616000                 |
| 1990, January 1  | 631152000                 |
| 1991, January 1  | 662688000                 |
| 1992, January 1  | 694224000                 |
| 1993, January 1  | 725846400                 |
| 1994, January 1  | 757382400                 |
| 1995, January 1  | 788918400                 |
| 1996, January 1  | 820454400                 |
| 1997, January 1  | 852076800                 |
| 1998, January 1  | 883612800                 |
| 1999, January 1  | 915148800                 |
| 2000, January 1  | 946684800                 |
| 2001, January 1  | 978307200                 |
| 2002, January 1  | 1009843200                |
| 2003, January 1  | 1041379200                |
| 2004, January 1  | 1072915200                |
| 2005, January 1  | 1104537600                |
| 2006, January 1  | 1136073600                |
| 2007, January 1  | 1167609600                |
| 2008, January 1  | 1199145600                |
| 2009, January 1  | 1230768000                |
| 2010, January 1  | 1262304000                |
| 2011, January 1  | 1293840000                |
| 2012, January 1  | 1325376000                |
| 2013, January 1  | 1356998400                |
| 2014, January 1  | 1388534400                |
| 2015, January 1  | 1420070400                |
| 2016, January 1  | 1451606400                |
| 2017, January 1  | 1483228800                |
| 2018, January 1  | 1514764800                |
| 2019, January 1  | 1546300800                |
| 2020, January 1  | 1577836800                |
| 2021, January 1  | 1609459200                |
| 2022, January 1  | 1640995200                |
| 2023, January 1  | 1672531200                |
| 2024, January 1  | 1704067200                |
| 2025, January 1  | 1735689600                |
| 2026, January 1  | 1767225600                |
| 2027, January 1  | 1798761600                |
| 2028, January 1  | 1830297600                |
| 2029, January 1  | 1861920000                |
| 2030, January 1  | 1893456000                |
| 2031, January 1  | 1924992000                |
| 2032, January 1  | 1956528000                |
| 2033, January 1  | 1988150400                |
| 2034, January 1  | 2019686400                |
| 2035, January 1  | 2051222400                |
| 2036, January 1  | 2082758400                |
| 2037, January 1  | 2114380800                |
| 2038, January 1  | 2145916800                |


## Time Stamp Formats 

 **imestamp Format**           | **Example**                                            
-------------------------------|--------------------------------------------------------
 yyyy-MM-dd'T'HH:mm:ss*SSSZZZZ | 2018-08-20'T'13:20:10*633+0000                         
 yyyy MMM dd HH:mm:ss.SSS zzz  | 2017 Mar 03 05:12:41.211 PDT                           
 MMM dd HH:mm:ss ZZZZ yyyy     | Jan 21 18:20:11 +0000 2017                             
 dd/MMM/yyyy:HH:mm:ss ZZZZ     | 19/Apr/2017:06:36:15 -0700                             
 MMM dd, yyyy hh:mm:ss a       | Dec 2, 2017 2:39:58 AM                                 
 MMM dd yyyy HH:mm:ss          | Jun 09 2018 15:28:14                                   
 MMM dd HH:mm:ss yyyy          | Apr 20 00:00:35 2010                                   
 MMM dd HH:mm:ss ZZZZ          | Sep 28 19:00:00 +0000                                  
 MMM dd HH:mm:ss               | Mar 16 8:12:04                                         
 yyyy-MM-dd'T'HH:mm:ssZZZZ     | 2017-10-14T22:11:20+0000                               
 yyyy-MM-dd'T'HH:mm:ss.SSS'Z'  | 2017-07-01T14:59:55.711'+0000'2017-07-01T14:59:55.711Z 
 yyyy-MM-dd HH:mm:ss ZZZZ      | 2017-08-19 12:17:55 -0400                              
 yyyy-MM-dd HH:mm:ssZZZZ       | 2017-08-19 12:17:55-0400                               
 yyyy-MM-dd HH:mm:ss,SSS       | 2017-06-26 02:31:29,573                                
 yyyy/MM/dd*HH:mm:ss           | 2017/04/12*19:37:50                                    
 yyyy MMM dd HH:mm:ss.SSS*zzz  | 2018 Apr 13 22:08:13.211*PDT                           
 yyyy MMM dd HH:mm:ss.SSS      | 2017 Mar 10 1:44:20                                    
 yyyy-MM-dd HH:mm:ss,SSSZZZZ   | 2017-03-10 14:30:12,655+0000                           
 yyyy-MM-dd HH:mm:ss.SSS       | 2018-02-27 15:35:20                                    
 yyyy-MM-dd HH:mm:ss.SSSZZZZ   | 2017-03-12 13:11:34.222-0700                           
 yyyy-MM-dd'T'HH:mm:ss.SSS     | 2017-07-22'T'16:28:55.444                              
 yyyy-MM-dd'T'HH:mm:ss         | 2017-09-08'T'03:13:10                                  
 yyyy-MM-dd'T'HH:mm:ss'Z'      | 2017-03-12'T'17:56:22'-0700'                           
 yyyy-MM-dd'T'HH:mm:ss.SSS     | 2017-11-22'T'10:10:15.455                              
 yyyy-MM-dd'T'HH:mm:ss         | 2017-02-11'T'18:31:44                                  
 yyyy-MM-dd*HH:mm:ss:SSS       | 2017-10-30*02:47:33:899                                
 yyyy-MM-dd*HH:mm:ss           | 2017-07-04*13:23:55                                    
 yy-MM-dd HH:mm:ss,SSS ZZZZ    | 11-02-11 16:47:35,985 +0000                            
 yy-MM-dd HH:mm:ss,SSS         | 10-06-26 02:31:29,573                                  
 yy-MM-dd HH:mm:ss             | 10-04-19 12:00:17                                      
 yy/MM/dd HH:mm:ss             | 06/01/22 4:11:05                                       
 yyMMdd HH:mm:ss               | 150423 11:42:35                                        
 yyyyMMdd HH:mm:ss.SSS         | 20150423 11:42:35.173                                  
 MM/dd/yy*HH:mm:ss             | 08/10/11*13:33:56                                      
 MM/dd/yyyy*HH:mm:ss           | 11/22/2017*05:13:11                                    
 MM/dd/yyyy*HH:mm:ss*SSS       | 05/09/2017*08:22:14*612                                
 MM/dd/yy HH:mm:ss ZZZZ        | 04/23/17 04:34:22 +0000                                
 MM/dd/yyyy HH:mm:ss ZZZZ      | 10/03/2017 07:29:46 -0700                              
 HH:mm:ss                      | 11:42:35                                               
 HH:mm:ss.SSS                  | 11:42:35                                               
 HH:mm:ss,SSS                  | 11:42:35,173                                           
 dd/MMM HH:mm:ss,SSS           | 23/Apr 11:42:35,173                                    
 dd/MMM/yyyy:HH:mm:ss          | 23/Apr/2017:11:42:35                                   
 dd/MMM/yyyy HH:mm:ss          | 23/Apr/2017 11:42:35                                   
 dd-MMM-yyyy HH:mm:ss          | 23-Apr-2017 11:42:35                                   
 dd-MMM-yyyy HH:mm:ss.SSS      | 23-Apr-2017 11:42:36                                   
 dd MMM yyyy HH:mm:ss          | 23 Apr 2017 11:42:35                                   
 dd MMM yyyy HH:mm:ss*SSS      | 23 Apr 2017 10:32:35*311                               
 MMdd_HH:mm:ss                 | 0423_11:42:35                                          
 MMdd_HH:mm:ss.SSS             | 0423_11:42:35.883                                      
 MM/dd/yyyy hh:mm:ss a:SSS     | 8/5/2011 3:31:18 AM:234                                
 MM/dd/yyyy hh:mm:ss a         | 9/28/2011 2:23:15 PM                                   

## Time Stamp Conventions

| **Token** | **Date or Time Component**                                            | **Example**      |
|-----------|-----------------------------------------------------------------------|------------------|
| yyyy      | 4-digit year                                                          | 2012; 2016       |
| yy        | 2-digit year                                                          | 12; 16           |
| MMM       | 3-character month                                                     | Jan; Mar; Dec    |
| MM        | 1- or 2-digit month (in a year)                                       | 1; 01; 9; 09; 12 |
| dd        | 1- or 2-digit day (in a month)                                        | 1; 01; 16; 30    |
| a         | AM/PM (case insensitive)                                              | AM; PM; am; pm   |
| HH        | 1- or 2-digit hour (in a day, 0-23)                                   | 2; 02; 14; 23    |
| hh        | 1- or 2-digit hour (in a day, 1-12 with AM/PM)                        | 2; 02; 11; 12    |
| mm        | 1- or 2-digit minute (in an hour)                                     | 8; 08; 55        |
| ss        | 1- or 2-digit second (in a minute)                                    | 5; 05; 35        |
| SSS       | 1-3 digit subsecond or millisecond (in decimal)                       | 4; 58; 944       |
| zzz       | 3- letter time zone                                                   | UTC; PST; EDT    |
| ZZZZ      | RFC 822 time zone                                                     | -0900; +0500     |
| Z'        | Literal Z character                                                   | Z                |
| T'        | Literal T character                                                   | T                |
| epoch     | 10, 13, 16, 19 digit timestamp with optional . (dot) after 10 digits. | 1496756807       |


## Julian-Gregorian Adoption Dates

|                                                                                               Country                                                                                              |                                                           End Julian Calendar                                                           |                                                            Begin Gregorian Calendar                                                           |
|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|:---------------------------------------------------------------------------------------------------------------------------------------:|:---------------------------------------------------------------------------------------------------------------------------------------------:|
| Albania                                                                                                                                                                                            |                                                                                                                                Dec 1912 |                                                                                                                                      Dec 1912 |
| Austria<br> Tyrol<br> Carinthia, Styria                                                                                                                                                            | Oct 5, 1583<br>Dec 14, 1583                                                                                                             | Oct 16,1583<br>Dec 25, 1583                                                                                                                   |
| Belgium<br> Spanish Provinces<br> Liege                                                                                                                                                            | Dec 21, 1582<br>Feb 10,1583                                                                                                             | Jan 1, 1583<br>Feb 21,1583                                                                                                                    |
| Bulgaria                                                                                                                                                                                           |                                                                                                                             Nov 1, 1915 |                                                                                                                                  Nov 14, 1915 |
| China                                                                                                                                                                                              |                                                                                                                            Dec 18, 1911 |                                                                                                                                   Jan 1, 1912 |
| Canada<br> British Colonies<br> Nova Scotia                                                                                                                                                        | Sep 2, 1752<br>Sep 2, 1752                                                                                                              | Sep 14, 1752<br>Sep 14, 1752                                                                                                                  |
| Czech Republic - Bohemia / Moravia                                                                                                                                                                 |                                                                                                                             Jan 6, 1584 |                                                                                                                                  Jan 17, 1584 |
| Denmark<br> Faero Islands                                                                                                                                                                          | Feb 18, 1700<br>Nov 16, 1700                                                                                                            | March 1,1700<br>Nov 28, 1700                                                                                                                  |
| Egypt                                                                                                                                                                                              |                                                                                                                                    1875 |                                                                                                                                          1875 |
| Estonia                                                                                                                                                                                            |                                                                                                                             Feb 1, 1918 |                                                                                                                                  Feb 15, 1918 |
| Finland (part of Sweden)                                                                                                                                                                           |                                                                                                                            Feb 17, 1753 |                                                                                                                                 March 1, 1753 |
| France & Colonies<br> Alsace<br> Strasbourg                                                                                                                                                        | Dec 9, 1582<br>1648<br>Feb 5, 1682                                                                                                      | Dec 20, 1582<br>1648<br>Feb 16,1682                                                                                                           |
| Germany, Catholic Regions<br> Augsburg<br> Baden<br> Bavaria<br> Cologne<br> Julich<br> Mainz<br> Munster, Strasbourg<br> Trier<br> Wurzburg                                                       | Feb 13, 1583<br>Nov 16, 1583<br>Oct 5, 1583<br>Nov 3, 1583<br>Nov 2, 1583<br>Nov 11, 1583<br>Nov 16, 1583<br>Oct 4, 1583<br>Nov 4, 1583 | Feb 24, 1583<br>Nov 27, 1583<br>Nov 16, 1583<br>Nov 14, 1583<br>Nov 13, 1583<br>Nov 22, 1583<br>Nov 27, 1583<br>Oct, 15, 1583<br>Nov 15, 1583 |
| Germany, Protestant Regions<br> Hildesheim<br> Kurland<br> Minden<br> Neuburg<br> Osnabruck<br> Paderborn<br> Prussia<br> Westphalia<br> All Others                                                | Mar 15, 1631<br>1617<br>Feb 1, 1668<br>Dec 13, 1615<br>1624<br>June 16, 1585<br>Aug 22, 1610<br>July 1, 1584<br>Feb 18, 1700            | March 26, 1631<br>1617<br>Feb 12, 1668<br>Dec 24, 1615<br>1624<br>July 27, 1585<br>Sept 2, 1610<br>July 12, 1584<br>March 1, 1700             |
| Great Britain & colonies                                                                                                                                                                           | Sept 2, 1752                                                                                                                            | Sept 14, 1752                                                                                                                                 |
| Greece                                                                                                                                                                                             | Sept 14, 1916                                                                                                                           | Sept 28, 1916                                                                                                                                 |
| Holy Roman Empire                                                                                                                                                                                  |                                                                                                                             Jan 6, 1584 |                                                                                                                                  Jan 17, 1584 |
| Hungary<br> Transylvania                                                                                                                                                                           | Oct 21, 1587<br>Dec 14, 1590                                                                                                            | Nov 1, 1587<br>Dec 25, 1590                                                                                                                   |
| Iceland                                                                                                                                                                                            |                                                                                                                            Nov 16, 1700 |                                                                                                                                  Nov 28, 1700 |
| Ireland                                                                                                                                                                                            | Sept 2, 1752                                                                                                                            | Sept 14, 1752                                                                                                                                 |
| Italy                                                                                                                                                                                              |                                                                                                                              Oct 4,1582 |                                                                                                                                  Oct 15, 1582 |
| Japan                                                                                                                                                                                              |                                                                                                                                    1873 |                                                                                                                                          1873 |
| Latvia                                                                                                                                                                                             |                                                                                                                             Feb 1, 1918 |                                                                                                                                  Feb 15, 1918 |
| Lithuania                                                                                                                                                                                          |                                                                                                                             Feb 1, 1918 |                                                                                                                                  Feb 15, 1918 |
| Moravia (Czech Republic)                                                                                                                                                                           |                                                                                                                             Jan 6, 1584 |                                                                                                                                  Jan 17, 1584 |
| The Netherlands<br> Holland, North Brabant<br> Gelderland, Zutphen<br> Utrecht, Overijssel<br> Friesland, Groningen<br> Drente                                                                     | Dec 21, 1582<br>June 30, 1700<br>Nov 30, 1700<br>Dec 31, 1700<br>April 30, 1701                                                         | Jan 1, 1583<br>July 7, 1700<br>Dec 12, 1700<br>Jan 12, 1701<br>May 12, 1701                                                                   |
| Norway                                                                                                                                                                                             |                                                                                                                            Feb 18, 1700 |                                                                                                                                 March 1, 1700 |
| Poland<br> Silesia                                                                                                                                                                                 | Oct 4, 1582<br>Jan 12, 1584                                                                                                             | Oct 15, 1582<br>Jan 23, 1584                                                                                                                  |
| Portugal                                                                                                                                                                                           |                                                                                                                             Oct 4, 1582 |                                                                                                                                  Oct 15, 1582 |
| Romania<br> Transylvania                                                                                                                                                                           | March 31, 1919<br>Dec 14, 1590                                                                                                          | April 14, 1919<br>Dec 25, 1590                                                                                                                |
| Russia                                                                                                                                                                                             |                                                                                                                             Jan 31,1918 |                                                                                                                                  Feb 14, 1918 |
| Spain<br> American Colonies                                                                                                                                                                        | Oct 4, 1582<br>1584                                                                                                                     | Oct 15, 1582<br>1584                                                                                                                          |
| Sweden                                                                                                                                                                                             |                                                                                                                            Feb 17, 1753 |                                                                                                                                 March 1, 1753 |
| Switzerland<br> Catholic Cantons - Lucern, Uri, Schwyz, Zug, Freiburg, Solothurn<br> Wallis<br> Protestant - Zurich, Bern, Basel, Schaffhouse, Geneva, Thurgovia<br> Appenzell, Glarus, St. Gallen | Jan 11, 1584<br>Jan 11, 1584<br>Feb 28, 1655<br>Dec 31, 1700<br>Dec 31, 1700<br>1724                                                    | Jan 22, 1584<br>Jan 22, 1584<br>March 11, 1655<br>Jan 12, 1701<br>Jan 12, 1701<br>1724                                                        |
| Turkey                                                                                                                                                                                             |                                                                                                                                    1927 |                                                                                                                                          1927 |
| United States<br> British Colonies<br> Spanish Colonies<br> Alaska                                                                                                                                 | Sept 2, 1752<br>1584<br>Oct 5, 1867                                                                                                     | Sept 14, 1752<br>1584<br>Oct 18, 1867                                                                                                         |
| Yugoslavia                                                                                                                                                                                         |                                                                                                                           March 4, 1919 |                                                                                                                                March 18, 1919 |


### References

[https://pumas.nasa.gov/files/04_21_97_1.pdf](https://pumas.nasa.gov/files/04_21_97_1.pdf)
<br>
[Timestamps, Time-Zones, Time-Ranges, and Date-Formats#Timestamp_conventions](https://help.sumologic.com/03Send-Data/Sources/04Reference-Information-for-Sources/Timestamps%2C-Time-Zones%2C-Time-Ranges%2C-and-Date-Formats#Timestamp_conventions)
