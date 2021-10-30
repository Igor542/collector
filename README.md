# TgFinance

Simple telegram chat bot to track money spendings.

## Commands (prototype)

Command                                 | acK   | Example                   | Description
--------------------------------------- | ----- | ------------------------- | ------------
`/register [@user...]`                  |       |                           | Register new users
`/set option`                           | ?     |                           | Set some options
`/ack` / `/nack`                        |       |                           | Agree / disagree with the last command
`/stat`                                 |       |                           | Show current statistic
`/log [num_last_tx]`                    |       | `/log 10`                 | Show last `num_last_tx` transactions. 0 for all. Default: 10
`/payment [a2a]`                        |       |                           | Show payment routes with minimized number of transactions, unless `a2a` modifier is used.
`/reset`                                | +     |                           | Full reset
`/[g]+ <value> [@user...] [comment]`    |       | `/+ 10.3 @u1 @u2 Dinner`  | Register `value` spending across mention users. No user means all. `g` modifier to spread between groups and not users.
`/[g]- <value> [@user...] [comment]`    | +     | `/g- 4 Lunch refund`      | Register `value` refund.
`/cancel <tx> [comment]`                | +     | `/cancel 13 no surfing`   | Cancel `tx` transaction (see `/log`).
`/= [@user1...] [comment]`              | +     | `/= @u1 @u2`              | Register pay-off between all or mentioned users.
`/join @user` / `/disjoin`              | +     | `/join @u3`               | Form a group of users. All transactions are spread between users in group (no matter if one or many users are mentioned).
