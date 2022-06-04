# TgFinance

Simple telegram chat bot to track money spending and help with payments.

## Commands (prototype)

Command                                    | Type     | Description
------------------------------------------ | -------- | ------------
`/register`                                | User mgt | Register a user.
`/join @user` / `/disjoin`                 | User mgt | Form a group of users. All transactions are split between users in one group. <br> Ex: `/join @u3`
`/stat`                                    | Info     | Show current statistics.
`/spent [<tx/date_from> [<tx/date_to>]]`   | Info     | Show logical spending between dates or transactions.
`/spent c [<tx/date_from> [<tx/date_to>]]` | Info     | Show cash (real) spending between dates or transactions.
`/log [@user or me] [num_tx]`              | Info     | Show last `num_tx` transactions (must be positive integer number, default: 10) for a given @user, self (`me`), or all if omitted. <br> Ex: `/log me 10`.
`/payment`                                 | Info     | Show pay-offs.
`/add <value> [@user...] [comment]`        | Action   | Register `value` spending across all or mentioned users. <br> Ex: `/add 10.3 @u1 @u2 Dinner`
`/g_add <value> [@user...] [comment]`      | Action   | Register `value` spending across groups of all or mentioned users. <br> Ex: `/g_add 10.3 @u1 @u2 House`
`/cancel <tx> [comment]`                   | Action   | Cancel `tx` transaction (see `/log`). <br> Ex: `/cancel 13 no surfing`
`/compensate [comment]`                    | Action   | Register pay-off between all users.

## Model

1. Money are equally split between all or mentioned users at a given transaction.
2. When groups are used, money are equally split between the groups first,
   and then equally split withing the groups between users. Example:
   - Users: u1, u2, (u3, u4). Users (3) and (4) form a group.
   - If u1 calls `/add 60`, then all users will owe u1 15.
   - If u1 calls `/g_add 60`, then all u2 owes u1 20, and u3 and u4 owe u1 10.
3. Cancel is treated as a transaction with inverse values and extended comment:
   `Cancel <tx>. <comment>`.
