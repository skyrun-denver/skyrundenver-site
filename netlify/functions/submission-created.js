// Netlify event function: runs once for every verified (non spam) submission of the site form.
// Creates one HubSpot deal in the "New Inquiry" stage for each inquiry and links it to the contact.
//
// Dormant until Sebastien adds a HubSpot private app token to Netlify as HUBSPOT_TOKEN
// (Project configuration > Environment variables, scope Functions). Required private app scopes:
//   crm.objects.contacts.read, crm.objects.contacts.write, crm.objects.deals.read, crm.objects.deals.write
// Optional: HUBSPOT_DEAL_STAGE (a stage id) to skip the lookup of the "New Inquiry" stage.

const API = 'https://api.hubapi.com';
const DEDUPE_DAYS = 14; // one deal per owner inquiry; repeat submissions inside this window do not open another deal

exports.handler = async (event) => {
  const token = process.env.HUBSPOT_TOKEN;
  if (!token) return ok('HUBSPOT_TOKEN not set; deal creation is off');

  let payload;
  try { payload = JSON.parse(event.body).payload; } catch (e) { return ok('unreadable payload'); }
  if (!payload || payload.form_name !== 'property-evaluation') return ok('not the evaluation form');
  const d = payload.data || {};
  const email = (d.email || '').trim().toLowerCase();
  if (!email) return ok('no email');

  const hs = async (path, opts = {}) => {
    const r = await fetch(API + path, {
      ...opts,
      headers: { Authorization: 'Bearer ' + token, 'Content-Type': 'application/json', ...(opts.headers || {}) },
    });
    const text = await r.text();
    let body = null; try { body = text ? JSON.parse(text) : null; } catch (e) { body = text; }
    if (!r.ok) { const err = new Error(path + ' ' + r.status + ' ' + text.slice(0, 300)); err.status = r.status; throw err; }
    return body;
  };

  try {
    // 1. The HubSpot form submission usually creates the contact first. Wait briefly for it, then create it if missing.
    let contactId = null;
    for (let i = 0; i < 4 && !contactId; i++) {
      const found = await hs('/crm/v3/objects/contacts/search', {
        method: 'POST',
        body: JSON.stringify({ filterGroups: [{ filters: [{ propertyName: 'email', operator: 'EQ', value: email }] }], properties: ['email'], limit: 1 }),
      });
      contactId = found && found.results && found.results[0] && found.results[0].id;
      if (!contactId) await sleep(2500);
    }
    if (!contactId) {
      const props = pick(d, ['firstname', 'lastname', 'phone', 'message', 'skyrun_property_city', 'skyrun_property_type',
        'skyrun_rental_strategy', 'skyrun_start_window', 'skyrun_discovery_channel', 'skyrun_inquiry_landing_page']);
      props.email = email;
      const c = await hs('/crm/v3/objects/contacts', { method: 'POST', body: JSON.stringify({ properties: props }) });
      contactId = c.id;
    }

    // 2. One deal per inquiry: skip if this contact already has a deal created in the last DEDUPE_DAYS.
    const assoc = await hs(`/crm/v4/objects/contacts/${contactId}/associations/deals?limit=50`);
    const dealIds = (assoc && assoc.results || []).map((a) => a.toObjectId);
    if (dealIds.length) {
      const batch = await hs('/crm/v3/objects/deals/batch/read', {
        method: 'POST', body: JSON.stringify({ properties: ['createdate'], inputs: dealIds.map((id) => ({ id: String(id) })) }),
      });
      const cutoff = Date.now() - DEDUPE_DAYS * 864e5;
      if ((batch.results || []).some((x) => Date.parse(x.properties.createdate) > cutoff)) return ok('recent deal exists for ' + contactId);
    }

    // 3. Find the "New Inquiry" stage.
    let pipeline = null, stage = process.env.HUBSPOT_DEAL_STAGE || null;
    const pipes = await hs('/crm/v3/pipelines/deals');
    for (const p of pipes.results || []) {
      for (const s of p.stages || []) {
        if ((stage && s.id === stage) || (!stage && /new inquiry/i.test(s.label))) { pipeline = p.id; stage = s.id; }
      }
      if (pipeline) break;
    }
    if (!pipeline) throw new Error('No deal stage named New Inquiry found');

    // 4. Create the deal, linked to the contact. Property fields are best effort: if HubSpot rejects one, retry without them.
    const city = labelCity(d.skyrun_property_city);
    const name = [d.firstname, d.lastname].filter(Boolean).join(' ').trim() || email;
    const base = { dealname: `${name}, ${city || 'Denver Metro'} property`, pipeline, dealstage: stage };
    const extra = pick(d, ['skyrun_property_city', 'skyrun_property_type', 'skyrun_rental_strategy']);
    const assocs = [{ to: { id: contactId }, types: [{ associationCategory: 'HUBSPOT_DEFINED', associationTypeId: 3 }] }];
    let deal;
    try {
      deal = await hs('/crm/v3/objects/deals', { method: 'POST', body: JSON.stringify({ properties: { ...base, ...extra }, associations: assocs }) });
    } catch (e) {
      if (e.status !== 400) throw e;
      deal = await hs('/crm/v3/objects/deals', { method: 'POST', body: JSON.stringify({ properties: base, associations: assocs }) });
    }
    return ok('deal ' + deal.id + ' for contact ' + contactId);
  } catch (e) {
    console.error('HubSpot deal creation failed:', e.message); // visible in Netlify function logs; the submission itself is safe in Netlify Forms
    return ok('error logged');
  }
};

function ok(msg) { console.log(msg); return { statusCode: 200, body: msg }; }
function sleep(ms) { return new Promise((r) => setTimeout(r, ms)); }
function pick(src, keys) { const o = {}; keys.forEach((k) => { if (src[k]) o[k] = String(src[k]); }); return o; }
function labelCity(v) {
  const m = { denver: 'Denver', arvada: 'Arvada', wheat_ridge: 'Wheat Ridge', lakewood: 'Lakewood', englewood: 'Englewood',
    centennial: 'Centennial', other_needs_territory_approval: 'Denver Metro' };
  return m[v] || '';
}
