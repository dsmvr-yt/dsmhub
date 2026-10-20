-- Run in Supabase: SQL Editor > New query.
create table public.messages (
  id uuid primary key default gen_random_uuid(),
  channel text not null check (channel in ('general','games','movies')),
  user_id uuid not null default auth.uid() references auth.users(id) on delete cascade,
  name text not null default 'user' check (char_length(name) <= 40),
  text text not null check (char_length(text) between 1 and 500),
  created_at timestamptz not null default now()
);
create index messages_channel_created on public.messages (channel, created_at desc);

alter table public.messages enable row level security;
create policy "signed-in users read" on public.messages for select to authenticated using (true);
create policy "users insert own" on public.messages for insert to authenticated with check (user_id = auth.uid());
create policy "users delete own" on public.messages for delete to authenticated using (user_id = auth.uid());

-- Spam control: one message per second per user.
create function public.throttle_messages() returns trigger language plpgsql as $$
begin
  if exists (select 1 from public.messages where user_id = new.user_id and created_at > now() - interval '1 second') then
    raise exception 'Slow down';
  end if;
  return new;
end $$;
create trigger messages_throttle before insert on public.messages for each row execute function public.throttle_messages();

alter publication supabase_realtime add table public.messages;

-- Per-user synced data (favorites, recently played, movie embed).
create table public.user_data (
  user_id uuid not null default auth.uid() references auth.users(id) on delete cascade,
  key text not null check (key in ('fav','recent','movie')),
  value jsonb not null check (octet_length(value::text) < 20000),
  updated_at timestamptz not null default now(),
  primary key (user_id, key)
);
alter table public.user_data enable row level security;
create policy "own rows select" on public.user_data for select to authenticated using (user_id = auth.uid());
create policy "own rows insert" on public.user_data for insert to authenticated with check (user_id = auth.uid());
create policy "own rows update" on public.user_data for update to authenticated using (user_id = auth.uid()) with check (user_id = auth.uid());
create policy "own rows delete" on public.user_data for delete to authenticated using (user_id = auth.uid());
