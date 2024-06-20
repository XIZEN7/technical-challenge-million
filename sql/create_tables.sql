/**
 * create tables
 */
drop table if exists public.departments;
create table public.departments(
	id int primary key
	,department text
);

drop table if exists public.jobs;
create table public.jobs(
	id int primary key
	,job text
);

drop table if exists public.employees;
create table public.employees(
	id int primary key
	,name text
	,datetime timestamp with time zone
	,department_id int references departments(id)
	,job_id int references jobs(id)
);

/**
* create views
**/
create or replace view vst_hires_by_department_and_job as 
select d.department
  ,j.job
  ,count(distinct e."name") filter(where to_char(e.datetime, 'Q')::int = 1) Q1
  ,count(distinct e."name") filter(where to_char(e.datetime, 'Q')::int = 2) Q2
  ,count(distinct e."name") filter(where to_char(e.datetime, 'Q')::int = 3) Q3
  ,count(distinct e."name") filter(where to_char(e.datetime, 'Q')::int = 4) Q4
from employees e 
join departments d on e.department_id = d.id 
join jobs j on e.job_id = j.id
where to_char(e.datetime, 'YYYY') = '2021'
group by 1,2
order by d.department asc, j.job asc;

create or replace view vst_hires_by_department_and_job as 
select d.department
  ,j.job
  ,count(distinct e."name") filter(where to_char(e.datetime, 'Q')::int = 1) Q1
  ,count(distinct e."name") filter(where to_char(e.datetime, 'Q')::int = 2) Q2
  ,count(distinct e."name") filter(where to_char(e.datetime, 'Q')::int = 3) Q3
  ,count(distinct e."name") filter(where to_char(e.datetime, 'Q')::int = 4) Q4
from employees e 
join departments d on e.department_id = d.id 
join jobs j on e.job_id = j.id
where to_char(e.datetime, 'YYYY') = '2021'
group by 1,2
order by d.department asc, j.job asc;

create or replace view vst_hires_above_mean as 
with all_hires as (select d.id
					  ,d.department
					  ,count(1) hires
					from employees e 
					join departments d on e.department_id = d.id 
					where to_char(e.datetime, 'YYYY') = '2021'
					group by 1,2)
  ,avg_hires as (select avg(hires) avg_hires from all_hires)
select *
from all_hires ah
where ah.hires > (select avg_hires from avg_hires)
order by hires desc;