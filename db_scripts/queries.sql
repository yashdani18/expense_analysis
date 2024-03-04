select group_name, sum(cost)
from exp_groups g, expenses e
where g.group_id = e.group_id
and e.description <> 'Payment'
and e.description <> 'Settle all balances'
group by e.group_id ;

select * from expenses e, exp_groups g where e.group_id = g.group_id and g.group_name like '%san%';

select * from expenses where extract(month from created_at) = 12;

select count(*) from expenses;

select sum(cost), extract(month from created_at) as months
from expenses 
group by months;

select u.user_id, first_name, group_name
from users u, exp_groups g, users_groups ug
where u.user_id = ug.user_id and g.group_id = ug.group_id and first_name like '%yash%';


select sum(paid_share), sum(owed_share), sum(net_balance) from shares where user_id = 32703372;

SELECT * FROM expense_manager.shares;

select sum(owed_share), (sum(owed_share) / 24) from shares where user_id = 32703372;
select sum(owed_share), (sum(owed_share) / 12) from shares where user_id = 46379417;

select sum(owed_share), (sum(owed_share) / 12) from shares where user_id = 43357520;

select sum(paid_share), sum(owed_share), sum(net_balance) 
from shares s, expenses e 
where user_id = 32703372 
and s.expense_id = e.expense_id 
and extract(MONTH from e.created_at) in (1, 12);

select sum(paid_share), sum(owed_share), sum(net_balance), extract(month from e.created_at) as months
from shares s, expenses e 
where user_id = 32703372 
and s.expense_id = e.expense_id
group by months
order by months;