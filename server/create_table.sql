CREATE TABLE Transactions (
  id uuid not null primary key,
  transaction_id not null,
  group_name text not null,
  purchaser text not null,
  debtor string not null,
  amount real not null,
  is_paid boolean not null,
  memo text not null,
  ip_addr text not null,
  timestamp datetime default current_timestamp
);

CREATE TABLE transaction_audit (
  id uuid not null primary key,
  transaction_id not null,
  request text not null,
  status text not null,
  error_msg text,
  timestamp datetime default current_timestamp
);