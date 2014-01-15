NamecoinHashrateDistribution
============================

Scripts for calculating Namecoin hashrate distribution.

These scripts use the Blockchain.info API to get hashrate distribution for Bitcoin over the past 100 blocks, and converts to Namecoin based on the ratio of Bitcoin and Namecoin difficulty.  Hashrate percentages will sum to less than 100% because of smaller pools which are not included in the list.

It is recommended to only run this script every 15 minutes to avoid overloading API's.

Code is licensed under AGPLv3.
