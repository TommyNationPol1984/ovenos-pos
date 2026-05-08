// nexusOpenAI.js — NEXUS Chat for Base44 OvenOS
// Requires: OPENAI_API_KEY in Base44 App Settings > Secrets
const SYSTEM = `You are NEXUS, AI Chief of Staff for OvenOS restaurant POS.
Sharp, concise, data-driven. Max 150 words. $ for currency (2 decimals).
Use bullet points. Never invent data not provided to you.`;
function ctx(c={}) {
  const p=[], s=c.dailySummary||{}, f=c.floorStatus||{};
  if(s.revenue!=null) p.push(`TODAY: $${s.revenue.toFixed(2)} | ${s.covers||0} covers | avg $${(s.avgTicket||0).toFixed(2)}`);
  if(f.occupied!=null) p.push(`FLOOR: ${f.occupied}/${(f.occupied||0)+(f.available||0)} tables (${f.occupancyPct||0}%)`);
  if((c.openOrders||[]).length) p.push(`ORDERS: ${c.openOrders.length} open`);
  if((c.kitchenQueue||[]).length) {
    const avg=c.kitchenQueue.reduce((a,t)=>a+(t.waitMinutes||0),0)/c.kitchenQueue.length;
    p.push(`KITCHEN: ${c.kitchenQueue.length} tickets | avg ${avg.toFixed(1)}min`);
  }
  if((c.staff||[]).length) {
    const on=c.staff.filter(s=>s.status==='clocked_in').length;
    p.push(`STAFF: ${on}/${c.staff.length} on floor`);
  }
  if((c.inventory||[]).length) {
    const low=c.inventory.filter(i=>i.currentStock<=i.parLevel);
    if(low.length) p.push(`LOW STOCK: ${low.slice(0,4).map(i=>i.name).join(', ')}`);
  }
  return p.length ? '\n\nLIVE DATA:\n'+p.join('\n') : '';
}
export async function nexusChat({message, context={}, conversationHistory=[]}) {
  const key = process.env.OPENAI_API_KEY;
  if (!key) throw new Error('OPENAI_API_KEY not configured in Base44 Secrets');
  const res = await fetch('https://api.openai.com/v1/chat/completions', {
    method: 'POST',
    headers: {'Content-Type':'application/json','Authorization':`Bearer ${key}`},
    body: JSON.stringify({
      model: 'gpt-4o',
      messages: [
        {role:'system', content: SYSTEM+ctx(context)},
        ...conversationHistory.slice(-10),
        {role:'user', content: message}
      ],
      temperature: 0.4,
      max_tokens: 500
    })
  });
  if (!res.ok) throw new Error(`OpenAI ${res.status}: ${await res.text()}`);
  const d = await res.json();
  return {reply: d.choices?.[0]?.message?.content?.trim()||'No response', usage: d.usage||{}};
}
export async function nexusHealthCheck() {
  try {
    const r = await nexusChat({message:'Reply with exactly: NEXUS_ONLINE', context:{}, conversationHistory:[]});
    return {status: r.reply.includes('NEXUS_ONLINE') ? 'online' : 'degraded', reply: r.reply};
  } catch(e) { return {status:'offline', error: e.message}; }
}
