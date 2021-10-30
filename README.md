# TgFinance

Simple telegram chat bot to track money spending and help with payments.

## Commands (prototype)

Command                                 | acK   | Description
--------------------------------------- | ----- | ------------
`/register [@user...]`                  |       | Register a user.
`/join @user` / `/disjoin`              | +     | Form a group of users. All transactions are split between users in one group. <br> Ex: `/join @u3`
`/ack` / `/nack`                        |       | Agree / disagree with the last command.
`/stat`                                 |       | Show current statistics.
`/log [num_tx]`                         |       | Show last `num_tx` transactions. 0 for all. Default: 10.
`/payment [a2a]`                        |       | Show payments with minimized transaction number, unless `a2a` modifier is used.
`/[g]+ <value> [@user...] [comment]`    |       | Register `value` spending across all or mention users. `g` modifier to split between groups instead of users. <br> Ex: `/+ 10.3 @u1 @u2 Dinner`
`/cancel <tx> [comment]`                | +     | Cancel `tx` transaction (see `/log`). <br> Ex: `/cancel 13 no surfing`
`/= [@user1...] [comment]`              | +     | Register pay-off between all or mentioned users. <br> Ex: `/= @u1 @u2`
`/reset`                                | +     | Full reset.

## Model

1. Money are equally split between all or mentioned users at a given transaction.
2. When groups are used, money are equally split between the groups first,
   and then equally split withing the groups between users. Example:
   - Users: u1, u2, (u3, u4). Users (3) and (4) form a group.
   - If u1 calls `/+ 60`, then all users will owe u1 15.
   - If u1 calls `/g+ 60`, then all u2 owes u1 20, and u3 and u4 owe u1 10.
3. Cancel is treated as a transaction with inverse values and extended comment:
   `Cancel <tx>. <comment>`.
