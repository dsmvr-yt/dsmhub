// Protected AI endpoint (Supabase Edge Function). Provider key stays in Supabase secrets.
const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};
const json = (status: number, body: unknown) =>
  new Response(JSON.stringify(body), { status, headers: { ...cors, "Content-Type": "application/json" } });

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response(null, { headers: cors });
  if (req.method !== "POST") return json(405, { error: "POST only." });

  const key = Deno.env.get("AI_API_KEY");
  const model = Deno.env.get("AI_MODEL");
  const base = (Deno.env.get("AI_BASE_URL") || "https://api.openai.com/v1").replace(/\/$/, "");
  if (!key || !model) return json(501, { error: "AI is not configured. Set AI_API_KEY and AI_MODEL with `supabase secrets set`." });

  // The anon key also passes the gateway's JWT check, so confirm a real signed-in user.
  const token = (req.headers.get("authorization") || "").replace(/^Bearer /, "");
  const who = await fetch(`${Deno.env.get("SUPABASE_URL")}/auth/v1/user`, {
    headers: { apikey: Deno.env.get("SUPABASE_ANON_KEY") || "", Authorization: `Bearer ${token}` },
  });
  if (!who.ok) return json(401, { error: "Sign in required." });

  let body: { messages?: { role?: string; content?: unknown }[] };
  try { body = await req.json(); } catch { return json(400, { error: "Invalid JSON." }); }
  const messages = (Array.isArray(body.messages) ? body.messages : []).slice(-20).map((m) => ({
    role: m.role === "assistant" ? "assistant" : "user",
    content: String(m.content ?? "").slice(0, 4000),
  }));
  if (!messages.length) return json(400, { error: "No messages." });

  try {
    const r = await fetch(`${base}/chat/completions`, {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: `Bearer ${key}` },
      body: JSON.stringify({ model, max_tokens: 800, messages: [{ role: "system", content: "You are the DSMHub assistant. Be concise and helpful." }, ...messages] }),
    });
    if (!r.ok) return json(502, { error: `AI provider error (${r.status}).` });
    const d = await r.json();
    return json(200, { text: d.choices?.[0]?.message?.content ?? "" });
  } catch {
    return json(502, { error: "Could not reach the AI provider." });
  }
});
