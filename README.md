NamecoinHashrateDistribution
============================

Scripts for calculating Namecoin hashrate distribution.

These scripts use the Blockchain.info API to get hashrate distribution for Bitcoin over the past 100 blocks, and converts to Namecoin based on the ratio of Bitcoin and Namecoin network hashrate.  Percentages should sum to 100.

It is recommended to only run this script every 15 minutes to avoid overloading API's.

Code is licensed under AGPLv3.
