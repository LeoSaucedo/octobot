CREATE TABLE Transactions (
  id uuid not null primary key,
  transaction_id not null,
  group_name text not null,
  purchaser text not null,
  debtor string not null,
  amount real not null,
  is_paid boolean not null,
  memo text not null,
  ip_addr text not null
);