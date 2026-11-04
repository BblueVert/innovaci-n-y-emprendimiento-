/* Copiloto Kine — prototipo funcional.
 * Una sola app con dos versiones: V1 (alcance mínimo) y V2 (iterada).
 * Rutas por hash (#/hoy, #/tablero…). Estado en localStorage (si está disponible).
 * ?v=1|2 elige la versión · ?shot=1 muestra solo la pantalla (capturas).
 * Datos ficticios de ejemplo. Día de demostración: martes 24 de noviembre de 2026.
 */
(function () {
  'use strict';
  const Q = new URLSearchParams(location.search);
  const SHOT = Q.get('shot') === '1';
  const LS = {
    get(k) { try { return JSON.parse(localStorage.getItem(k)); } catch (e) { return null; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* sin almacenamiento */ } },
    del(k) { try { localStorage.removeItem(k); } catch (e) { /* nada */ } }
  };
  let V = Number(Q.get('v') || LS.get('ck-v') || 2) === 1 ? 1 : 2;
  const KEY = 'ck-state-v' + V;

  /* ---------------- Datos semilla ---------------- */
  function seed() {
    return {
      cfg: { share: 0.70, km: 180, ret: 0.1525, colchon: 0.05, meta: 1000000, cierre: '21:00',
        sectores: { Mar: 'Machalí', Jue: 'Rancagua oriente', Sáb: 'Rancagua centro' },
        agenda: { google: true, cal: false, excel: true } },
      kits: { lumbar: ['Kit lumbar', 1940], rodilla: ['Kit rodilla', 1500], neuro: ['Kit neurológico', 2300], resp: ['Kit respiratorio', 2600] },
      appts: [
        { id: 'a1', h: '09:00', p: 'María Soto', s: 'Rehabilitación de hombro', l: 'clin', v: 28000, st: 'done', pay: 'Convenio' },
        { id: 'a2', h: '10:00', p: 'Roberto Pérez', s: 'Kinesioterapia respiratoria', l: 'clin', v: 28000, st: 'done', pay: 'Boleta clínica' },
        { id: 'a3', h: '11:30', p: 'Luis Muñoz', s: 'Rehabilitación lumbar', l: 'dom', sector: 'Machalí', addr: 'Pje. Los Aromos 214', km: 12, kit: 'lumbar', v: 25000, st: 'pend', ses: '3 de 4' },
        { id: 'a4', h: '12:45', p: 'Ana Rojas', s: 'Rehabilitación de rodilla', l: 'dom', sector: 'Machalí', addr: 'Av. San Juan 1880', km: 3, kit: 'rodilla', v: 25000, st: 'pend', ses: '5 de 8' },
        { id: 'a5', h: '16:00', p: 'Pedro Lagos', s: 'Rehabilitación de tobillo', l: 'dom', sector: 'Rancagua centro', km: 8, kit: 'rodilla', v: 25000, st: 'cancel' },
        { id: 'a6', h: '17:30', p: 'Jorge Díaz', s: 'Kinesiología neurológica', l: 'dom', sector: 'Machalí', addr: 'Los Robles 77', km: 2.6, kit: 'neuro', v: 28000, st: 'pend', ses: '9 de 12' }
      ],
      mtd: 742600, colchonBase: 84000, renta: { apartado: 412000, estimado: 572000 }, horas: 11,
      hist: [['Jun', 742000], ['Jul', 690000], ['Ago', 815000], ['Sep', 870000], ['Oct', 905000]],
      proy: [['Dic', 940000], ['Ene', 820000], ['Feb', 410000], ['Mar', 860000], ['Abr', 900000], ['May', 880000]],
      acciones: false, cupo: 'none', cierre: { q1: false, q2: null, q3: null, done: false },
      pagoLuis: false, reserva: { day: 2, slot: '17:00', done: false }, pay: 'Transferencia'
    };
  }
  let S = LS.get(KEY) || seed();
  const save = () => LS.set(KEY, S);

  /* ---------------- Utilidades ---------------- */
  const $ = (n) => '$' + Math.round(n).toLocaleString('es-CL');
  const k$ = (n) => '$' + Math.round(n / 1000).toLocaleString('es-CL') + 'k';
  const byId = (id) => S.appts.find((a) => a.id === id);
  const bruto = (a) => a.l === 'clin' ? a.v * S.cfg.share : a.v * (a.cupo ? 0.85 : 1);
  const costoKm = (a) => a.l === 'dom' ? Math.round(a.km * S.cfg.km) : 0;
  const costoKit = (a) => a.l === 'dom' && a.kit ? S.kits[a.kit][1] : 0;
  const neto = (a) => Math.round(bruto(a) - costoKm(a) - costoKit(a));
  const split = (a) => {
    const n = neto(a), r = Math.round(bruto(a) * S.cfg.ret), c = Math.round(n * S.cfg.colchon);
    return { n, r, c, d: n - r - c };
  };
  const done = () => S.appts.filter((a) => a.st === 'done');
  const hoyNeto = () => done().reduce((s, a) => s + neto(a), 0);
  const mesNeto = () => S.mtd + hoyNeto();
  const hoyColchon = () => V === 2 ? done().reduce((s, a) => s + split(a).c, 0) : 0;
  const hoyRet = () => V === 2 ? done().reduce((s, a) => s + split(a).r, 0) : 0;
  const esc = (t) => String(t).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

  /* ---------------- Íconos ---------------- */
  const I = {
    hoy: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="17" rx="3"/><path d="M8 2v4M16 2v4M3 10h18"/></svg>',
    tablero: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 16a8 8 0 1 1 16 0"/><path d="M12 16l4-5"/><circle cx="12" cy="16" r="1.5" fill="currentColor"/></svg>',
    proy: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 17l5-5 4 3 8-8"/><path d="M15 7h5v5"/></svg>',
    cierre: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/></svg>',
    ajustes: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h10M18 7h2M4 17h4M12 17h8"/><circle cx="16" cy="7" r="2"/><circle cx="10" cy="17" r="2"/></svg>',
    back: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M15 18l-6-6 6-6"/></svg>',
    check: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>',
    car: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 17h14v-4l-2-5H7l-2 5z"/><circle cx="8" cy="17" r="2"/><circle cx="16" cy="17" r="2"/></svg>',
    bell: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 16V11a6 6 0 0 1 12 0v5l2 2H4z"/><path d="M10 20a2 2 0 0 0 4 0"/></svg>',
    spark: '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l2.2 6.3L20 10l-5.8 1.9L12 18l-2.2-6.1L4 10l5.8-1.7z"/></svg>',
    logo: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#FF6B35" stroke-width="2.6" stroke-linecap="round"><path d="M4 16a8 8 0 1 1 16 0"/><path d="M12 16l4.5-5"/></svg>',
    chev: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M9 6l6 6-6 6"/></svg>',
    lock: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/></svg>'
  };

  /* ---------------- Piezas comunes ---------------- */
  const status = (time, dark) => `<div class="status" style="${dark ? 'color:#fff' : ''}"><span>${time}</span><span class="sig"><i style="height:5px"></i><i style="height:8px"></i><i style="height:11px"></i><span class="bat"></span></span></div>`;
  const tabs = (on) => {
    const t = [['hoy', 'Hoy', I.hoy], ['tablero', 'Tablero', I.tablero], ['proyeccion', 'Proyección', I.proy], ['cierre', 'Cierre', I.cierre], ['ajustes', 'Ajustes', I.ajustes]];
    return `<nav class="tabs">${t.map(([r, n, ic]) => `<a href="#/${r}" class="${r === on ? 'on' : ''}">${ic}<span>${n}</span></a>`).join('')}</nav>`;
  };
  const top = (title, backTo, right) => `<div class="top"><a class="back" href="#/${backTo}">${I.back}</a><div class="ttl">${title}</div><div style="width:36px;text-align:right">${right || ''}</div></div>`;
  const pill = (a) => a.l === 'clin' ? '<span class="pill clin">Clínica 70/30</span>' : `<span class="pill dom">${V === 2 && a.sector ? esc(a.sector) : 'Domicilio'}</span>`;
  const semaforo = () => {
    const ratio = mesNeto() / (S.cfg.meta * 24 / 30);
    if (ratio >= 1) return ['#1F8A5B', 'Vas bien'];
    if (ratio >= 0.85) return ['#D99A12', 'Vas en camino'];
    return ['#D94B63', 'Vas atrasada'];
  };

  /* ---------------- Pantallas de Joselyn ---------------- */
  const screens = {};

  screens.inicio = () => ({ time: '9:41', html: `
    <div class="steps"><i class="on"></i><i></i><i></i></div>
    <div class="hero">
      <div class="brandmark" style="color:#fff"><span class="lg" style="background:#2A2547">${I.logo}</span>Copiloto Kine</div>
      <h2>Tú atiendes.<br>Tu copiloto lleva los números.</h2>
      <p>Se conecta a la agenda que ya usas y convierte cada atención en ganancia real, sin digitar.</p>
      <svg viewBox="0 0 320 120" style="width:100%;margin-top:14px">
        <path d="M30 110 A130 130 0 0 1 290 110" fill="none" stroke="#2F2A47" stroke-width="16" stroke-linecap="round"/>
        <path d="M30 110 A130 130 0 0 1 230 30" fill="none" stroke="#FF6B35" stroke-width="16" stroke-linecap="round"/>
        <path d="M160 110 L212 52" stroke="#fff" stroke-width="5" stroke-linecap="round"/><circle cx="160" cy="110" r="8" fill="#fff"/>
      </svg>
    </div>
    <div class="card tight row"><span>Cada cita se vuelve un ingreso proyectado</span>${I.check}</div>
    <div class="card tight row"><span>Ganancia neta por atención, con costos</span>${I.check}</div>
    <div class="card tight row"><span>${V === 2 ? 'Impuestos, colchón y rutas sin sorpresas' : 'Proyección de los próximos 3 meses'}</span>${I.check}</div>
    <div style="height:8px"></div>
    <a class="btn" href="#/conectar">Empezar · 10 minutos</a>` });

  screens.conectar = () => {
    const g = S.cfg.agenda;
    const it = (key, col, letter, name, desc) => `<button class="integ" data-act="toggle-agenda" data-k="${key}" style="width:100%;text-align:left">
      <span class="lg" style="background:${col}">${letter}</span><span class="mn"><b>${name}</b><span class="lbl">${desc}</span></span>
      ${g[key] ? '<span class="pill ok">✓ Conectado</span>' : '<span class="pill gray">Conectar</span>'}</button>`;
    return { time: '9:42', html: `
      <div class="steps"><i class="on"></i><i class="on"></i><i></i></div>
      <div class="hello"><div class="k">Paso 2 de 3</div><h2>Conecta tu agenda</h2><div class="muted tiny" style="margin-top:4px">Usa la que ya tienes. No la reemplazamos: la leemos.</div></div>
      ${it('google', '#4A3580', 'G', 'Google Calendar', 'joselyn.kine@gmail.com · 312 citas')}
      ${it('cal', '#12101E', 'C', 'Cal.com', 'Tu link de reservas en línea')}
      ${it('excel', '#1F8A5B', 'X', 'Importar mi Excel', 'Ingresos y gastos 2025–2026')}
      <div class="card purple" style="margin-top:6px"><div class="lbl up" style="color:var(--purple)">Lo que encontramos</div>
        <div style="margin-top:6px;font-size:14px">46 citas este mes: <b>18 en clínica</b> y <b>28 a domicilio</b>. Las vamos a etiquetar solas según el lugar.</div></div>
      <div class="card tight row" style="font-size:12.5px;color:var(--ink-2)"><span>${I.lock}&nbsp; Solo leemos fecha, lugar y valor. Nunca la ficha clínica.</span></div>
      <a class="btn" href="#/reglas">Continuar</a>` };
  };

  screens.reglas = () => ({ time: '9:45', html: `
    <div class="steps"><i class="on"></i><i class="on"></i><i class="on"></i></div>
    <div class="hello"><div class="k">Paso 3 de 3</div><h2>Tus reglas</h2><div class="muted tiny" style="margin-top:4px">Con esto calculamos tu ganancia real en cada atención.</div></div>
    <div class="card">
      <div class="field"><span>Tu parte en la clínica</span><span class="v">70 %</span></div>
      <div class="field"><span>Costo por km (auto)</span><span class="v">${$(S.cfg.km)}</span></div>
      <div class="field"><span>Kits de materiales</span><span class="v">4 kits</span></div>
      <div class="field"><span>Meta mensual</span><span class="v">${$(S.cfg.meta)}</span></div>
    </div>
    ${V === 2 ? `<div class="lbl up" style="margin:4px 0 8px">Nuevo en V2</div>
    <div class="card">
      <div class="field"><span>Retención de boleta (2026)</span><span class="v">15,25 %</span></div>
      <div class="field"><span>Colchón para meses bajos</span><span class="v">5 %</span></div>
      <div class="field"><span>Días por sector</span><span class="v tiny">Mar Machalí · Jue Oriente</span></div>
      <div class="field"><span>No trabajar después de</span><span class="v">21:00</span></div>
    </div>` : `<div class="card tight muted tiny">Puedes ajustar estas reglas cuando quieras en Ajustes.</div>`}
    <a class="btn" href="#/hoy" data-act="onboard-done">Listo, ver mi día</a>` });

  screens.hoy = () => {
    const list = S.appts.slice().sort((a, b) => a.h.localeCompare(b.h));
    const pend = list.filter((a) => a.st === 'pend').length;
    const proyHoy = list.filter((a) => a.st !== 'cancel').reduce((s, a) => s + neto(a), 0);
    const doms = list.filter((a) => a.l === 'dom' && a.st !== 'cancel');
    const row = (a) => {
      if (a.st === 'cancel' && V === 2 && S.cupo !== 'taken') {
        return `<a class="appt free" href="#/cupo"><div class="hr">${a.h}<small>45 min</small></div><div class="ln"></div>
          <div class="mn"><div class="nm">Hora libre</div><div class="sv">${esc(a.p)} canceló · ${esc(a.sector)}</div></div>
          <div class="rt">${S.cupo === 'offered' ? '<span class="pill ok">Ofrecida</span>' : '<span class="pill free">Ofrecer cupo</span>'}<span class="tiny muted">−15 %</span></div></a>`;
      }
      if (a.st === 'cancel') {
        return `<div class="appt cancel"><div class="hr">${a.h}<small>45 min</small></div><div class="ln"></div>
          <div class="mn"><div class="nm" style="text-decoration:line-through">${esc(a.p)}</div><div class="sv">Canceló · hora sin ocupar</div></div>
          <div class="rt"><span class="pill gray">Cancelada</span></div></div>`;
      }
      const href = a.st === 'pend' ? `#/atencion/${a.id}` : '#/hoy';
      return `<a class="appt ${a.l} ${a.st === 'done' ? 'done' : ''}" href="${href}"><div class="hr">${a.h}<small>${a.l === 'dom' ? a.km + ' km' : 'box 3'}</small></div><div class="ln"></div>
        <div class="mn"><div class="nm">${esc(a.p)}</div><div class="sv">${esc(a.s)}</div></div>
        <div class="rt">${pill(a)}<b class="${a.st === 'done' ? 'green' : ''}">${a.st === 'done' ? '✓ ' : ''}${$(neto(a))}</b></div></a>`;
    };
    return { tabs: 'hoy', time: '8:05', html: `
      <div class="row" style="margin:4px 0 2px"><div class="brandmark"><span class="lg">${I.logo}</span>Copiloto Kine</div><span class="avatar">JT</span></div>
      <div class="hello"><div class="k">Martes 24 de noviembre</div><h2>Hola, Joselyn</h2></div>
      <div class="grid2">
        <div class="card tight"><div class="lbl">Ganancia estimada hoy</div><div class="mid">${$(proyHoy)}</div></div>
        <div class="card tight"><div class="lbl">Atenciones</div><div class="mid">${list.filter((a) => a.st !== 'cancel').length} <span class="tiny muted" style="font-weight:500">· ${pend} por cerrar</span></div></div>
      </div>
      ${V === 2 ? `<a class="card ok row" href="#/ruta" style="display:flex">
          <span style="display:flex;gap:10px;align-items:center"><span class="green">${I.car}</span><span><b style="font-size:14px">Martes = Machalí</b><br><span class="tiny muted">${doms.length} domicilios agrupados · −9 km (≈ ${$(9 * S.cfg.km)})</span></span></span>${I.chev}</a>` : ''}
      <div class="sect row"><span>Tu agenda</span><span class="tiny muted" style="font-weight:500">Google Calendar · sincronizada</span></div>
      ${list.map(row).join('')}` };
  };

  screens.ruta = () => ({ tabs: 'hoy', time: '10:48', html: `
    ${top('Ruta del día', 'hoy')}
    <div class="map"><svg viewBox="0 0 354 230">
      <rect width="354" height="230" fill="#EAF1EA"/>
      <path d="M0 160 C80 150 120 190 200 170 S320 120 354 130" stroke="#fff" stroke-width="14" fill="none"/>
      <path d="M60 0 C70 60 40 120 70 230" stroke="#fff" stroke-width="10" fill="none"/>
      <path d="M210 0 C200 70 250 120 240 230" stroke="#fff" stroke-width="10" fill="none"/>
      <path d="M0 60 H354" stroke="#fff" stroke-width="6"/>
      <rect x="270" y="10" width="70" height="40" rx="6" fill="#DCE8F5"/><text x="305" y="34" font-size="10" text-anchor="middle" fill="#6A7FA0">Machalí</text>
      <path d="M52 178 C100 150 140 120 170 104 S250 80 286 70 S300 120 262 140" stroke="#FF6B35" stroke-width="4" fill="none" stroke-dasharray="2 0"/>
      <path d="M52 178 C120 200 210 210 300 190" stroke="#B6B3C9" stroke-width="3" fill="none" stroke-dasharray="6 6"/>
      <g font-size="11" font-weight="700" fill="#fff" text-anchor="middle">
        <circle cx="52" cy="178" r="13" fill="#7B3FA0"/><text x="52" y="182">C</text>
        <circle cx="170" cy="104" r="13" fill="#FF6B35"/><text x="170" y="108">1</text>
        <circle cx="286" cy="70" r="13" fill="#FF6B35"/><text x="286" y="74">2</text>
        <circle cx="262" cy="140" r="13" fill="#FF6B35"/><text x="262" y="144">3</text>
      </g>
      <text x="200" y="222" font-size="10" fill="#8C89A6">— sin agrupar: 24,6 km</text>
    </svg></div>
    <div class="grid2">
      <div class="card tight ok"><div class="lbl">Ruta agrupada</div><div class="mid green">15,6 km</div></div>
      <div class="card tight"><div class="lbl">Ahorro de hoy</div><div class="mid">−9 km · ${$(9 * S.cfg.km)}</div></div>
    </div>
    <div class="card">
      <div class="stop"><span class="n c">C</span><div class="col"><b>Clínica InMotion</b><span class="tiny muted">Salida 10:50</span></div></div>
      <div class="stop"><span class="n">1</span><div class="col"><b>11:30 · Luis Muñoz</b><span class="tiny muted">Pje. Los Aromos 214 · 12 km</span></div></div>
      <div class="stop"><span class="n">2</span><div class="col"><b>12:45 · Ana Rojas</b><span class="tiny muted">Av. San Juan 1880 · 3 km</span></div></div>
      <div class="stop"><span class="n">3</span><div class="col"><b>17:30 · Jorge Díaz</b><span class="tiny muted">Los Robles 77 · 2,6 km</span></div></div>
    </div>
    <div class="card tight tiny muted">Menos km = menos combustible y CO₂. Este mes llevas −38 km.</div>` });

  screens.atencion = (id) => {
    const a = byId(id) || byId('a3');
    const sp = split(a);
    const pays = ['Transferencia', 'Efectivo', 'Link de pago', 'Convenio'];
    return { time: '12:31', html: `
      <div class="notif"><span class="ic">${I.logo}</span><div><b>¿Atención realizada?</b><div class="tiny">${esc(a.p)} · ${a.l === 'dom' ? 'Domicilio' : 'Clínica'} · ${a.h} — terminó hace 1 min</div></div></div>
      <div class="hello" style="margin-top:0"><div class="k">${esc(a.s)}${a.ses ? ' · sesión ' + a.ses : ''}</div><h2>${esc(a.p)}</h2></div>
      <div class="card">
        <div class="lbl up">Ganancia de esta atención</div>
        <div class="kv"><span>Valor de la sesión</span><b>${$(a.v)}</b></div>
        ${a.l === 'clin' ? `<div class="kv"><span>Comisión clínica (30 %)</span><span>−${$(a.v * 0.3)}</span></div>` : `
        <div class="kv"><span>Traslado · ${String(a.km).replace('.', ',')} km</span><span>−${$(costoKm(a))}</span></div>
        <div class="kv"><span>${S.kits[a.kit][0]}</span><span>−${$(costoKit(a))}</span></div>`}
        <div class="kv total"><span>Ganancia neta</span><span class="green">${$(sp.n)}</span></div>
      </div>
      ${V === 2 ? `<div class="card brand">
        <div class="lbl up" style="color:#C24A1A">El pago se reparte solo</div>
        <div class="kv"><span>Para ti, disponible</span><b>${$(sp.d)}</b></div>
        <div class="kv"><span>Retención boleta (15,25 %)</span><span>${$(sp.r)}</span></div>
        <div class="kv"><span>Colchón meses bajos (5 %)</span><span>${$(sp.c)}</span></div>
      </div>
      <div class="lbl" style="margin:2px 0 8px">¿Cómo pagó?</div>
      <div class="chips" style="margin-bottom:14px">${pays.map((p) => `<button class="chip ${S.pay === p ? 'on' : ''}" data-act="pay" data-p="${p}">${p}</button>`).join('')}</div>` : ''}
      <div class="btns">
        <button class="btn ok" data-act="realizada" data-id="${a.id}">${I.check} Sí, realizada</button>
        <button class="btn ghost" data-act="noasistio" data-id="${a.id}">No asistió / reagendar</button>
      </div>` };
  };

  screens.cupo = () => {
    const a = byId('a5');
    const lista = [['Camila Fuentes', 'Machalí · alta hace 1 mes'], ['Sofía Vidal', 'Machalí · en lista de espera'], ['Diego Araya', 'Rancagua · pidió hora la semana pasada']];
    const taken = S.cupo === 'taken';
    return { tabs: 'hoy', time: '13:04', html: `
      ${top('Hora libre', 'hoy')}
      <div class="card bad"><b>${esc(a.p)} canceló la hora de las 16:00</b><div class="tiny muted" style="margin-top:2px">Esa hora vale ${$(neto(a))} de ganancia. Todavía puedes recuperarla.</div></div>
      <div class="card">
        <div class="row"><div><div class="lbl">Cupo de último minuto</div><div class="mid">Hoy 16:00 · Machalí</div></div><span class="pill dom">−15 %</span></div>
        <div class="divider"></div>
        <div class="kv"><span>Precio preferente</span><b>${$(25000 * 0.85)}</b></div>
        <div class="kv"><span>Ganancia estimada</span><b class="green">${$(25000 * 0.85 - 3 * S.cfg.km - 1500)}</b></div>
      </div>
      <div class="sect">Se lo ofreceremos a</div>
      <div class="card" style="padding:4px 16px">${lista.map(([n, d], i) => `<div class="field"><span><b style="font-size:14px">${n}</b><br><span class="tiny muted">${d}</span></span>${taken && i === 0 ? '<span class="pill ok">✓ La tomó</span>' : '<span class="toggle on"></span>'}</div>`).join('')}</div>
      <div class="card tight purple tiny">Mensaje con tu voz: “Hola, se liberó una hora hoy a las 16:00 en Machalí, con 15 % de descuento. ¿La quieres?”</div>
      ${taken ? `<div class="card ok"><b class="green">Camila Fuentes tomó la hora ✓</b><div class="tiny muted">Quedó en tu Google Calendar. Recuperaste ${$(25000 * 0.85 - 3 * S.cfg.km - 1500)}.</div></div><a class="btn dark" href="#/hoy">Volver a mi día</a>`
        : S.cupo === 'offered' ? `<div class="card tight row"><span class="tiny">Enviado a 3 pacientes por WhatsApp · esperando respuesta…</span></div><button class="btn ghost" data-act="cupo-take">Simular: Camila responde “Sí, la tomo”</button>`
          : `<button class="btn" data-act="cupo-offer">Ofrecer por WhatsApp</button>`}` };
  };

  screens.tablero = () => {
    const [col, txt] = semaforo();
    const m = mesNeto(), pct = Math.min(100, Math.round(m / S.cfg.meta * 100));
    const regSolas = 41 + done().length - 2;
    return { tabs: 'tablero', time: '20:38', html: `
      <div class="hello"><div class="k">Noviembre 2026 · día 24 de 30</div><h2>Mi tablero</h2></div>
      <div class="card">
        <div class="row"><span class="lbl"><span class="dot" style="background:${col}"></span>${txt}</span><span class="tiny muted">Meta ${$(S.cfg.meta)}</span></div>
        <div class="big" style="margin:6px 0 2px">${$(m)}</div>
        <div class="tiny muted" style="margin-bottom:10px">ganancia real del mes (ya descontados comisión, traslados y materiales)</div>
        <div class="bar"><i style="width:${pct}%"></i></div>
        <div class="row tiny muted" style="margin-top:6px"><span>${pct} % de la meta</span><span>Faltan ${$(Math.max(0, S.cfg.meta - m))}</span></div>
      </div>
      ${V === 2 ? `<div class="grid2">
        <div class="card tight"><div class="lbl">Colchón</div><div class="mid">${$(S.colchonBase + hoyColchon())}</div><div class="tiny muted">0,6 meses de costos</div></div>
        <div class="card tight"><div class="lbl">Horas recuperadas</div><div class="mid">${S.horas} h</div><div class="tiny muted">vs. el Excel de noche</div></div>
      </div>
      <div class="card">
        <div class="row"><div><div class="lbl">Operación Renta · abril 2027</div><div class="mid">${Math.round((S.renta.apartado + hoyRet()) / S.renta.estimado * 100)} % apartado</div></div>
        <svg viewBox="0 0 80 46" width="86" height="50"><path d="M8 42 A32 32 0 0 1 72 42" fill="none" stroke="#ECEAF4" stroke-width="9" stroke-linecap="round"/><path d="M8 42 A32 32 0 0 1 58 16" fill="none" stroke="#FF6B35" stroke-width="9" stroke-linecap="round"/><path d="M40 42 L56 24" stroke="#12101E" stroke-width="3" stroke-linecap="round"/><circle cx="40" cy="42" r="4" fill="#12101E"/></svg></div>
        <div class="tiny muted">Tienes ${$(S.renta.apartado + hoyRet())} de ~${$(S.renta.estimado)} estimados. Sin sorpresas en abril.</div>
      </div>` : ''}
      <div class="sect">¿Dónde gano más por hora?</div>
      <div class="grid2">
        <div class="card tight purple"><div class="lbl">Clínica 70/30</div><div class="mid purpletx">$14.700</div><div class="tiny muted">por hora · 18 atenciones</div></div>
        <div class="card tight brand"><div class="lbl">Domicilio</div><div class="mid orange">$16.100</div><div class="tiny muted">por hora, con traslado</div></div>
      </div>
      <div class="card tight row"><span>Atenciones registradas solas</span><b>${regSolas} / 46</b></div>
      <div class="card tight row"><span>Tiempo de cierre promedio</span><b>${V === 2 ? '4 min' : '6 min'}</b></div>` };
  };

  const lineChart = (pts, opts) => {
    const W = 354, H = 150, pad = 18, max = 1000000;
    const xs = (i) => pad + i * ((W - pad * 2) / (pts.length - 1));
    const ys = (v) => H - 26 - (v / max) * (H - 46);
    const path = pts.map((p, i) => (i ? 'L' : 'M') + xs(i).toFixed(1) + ' ' + ys(p[1]).toFixed(1)).join(' ');
    const low = pts.findIndex((p) => p[0] === 'Feb');
    let alt = '';
    if (opts.alt) alt = `<path d="M${xs(low - 1)} ${ys(pts[low - 1][1])} L${xs(low)} ${ys(opts.alt)} L${xs(low + 1)} ${ys(pts[low + 1][1])}" stroke="#FF6B35" stroke-width="3" fill="none" stroke-dasharray="6 5"/>`;
    return `<svg class="chart" viewBox="0 0 ${W} ${H}">
      <line x1="${pad}" x2="${W - pad}" y1="${ys(S.cfg.meta * 0.8)}" y2="${ys(S.cfg.meta * 0.8)}" stroke="#E7E5F0" stroke-dasharray="4 4"/>
      <path d="${path} L${xs(pts.length - 1)} ${H - 26} L${xs(0)} ${H - 26}Z" fill="rgba(123,63,160,.08)"/>
      <path d="${path}" stroke="#7B3FA0" stroke-width="3" fill="none" stroke-linejoin="round"/>${alt}
      ${pts.map((p, i) => `<circle cx="${xs(i)}" cy="${ys(p[1])}" r="${i === low ? 6 : 3.5}" fill="${i === low ? '#D94B63' : '#7B3FA0'}"/><text x="${xs(i)}" y="${H - 8}" font-size="11" text-anchor="middle" fill="#8C89A6">${p[0]}</text>`).join('')}
    </svg>`;
  };

  screens.proyeccion = () => {
    if (V === 1) {
      const p3 = S.proy.slice(0, 3);
      return { tabs: 'proyeccion', time: '20:40', html: `
        <div class="hello"><div class="k">Según tu agenda</div><h2>Próximos 3 meses</h2></div>
        <div class="card"><svg class="chart" viewBox="0 0 354 160">
          ${p3.map((p, i) => { const h = p[1] / 1000000 * 120; const x = 30 + i * 108; return `<rect x="${x}" y="${136 - h}" width="76" height="${h}" rx="8" fill="${p[0] === 'Feb' ? '#D94B63' : '#C9B3E3'}"/><text x="${x + 38}" y="${128 - h}" font-size="12" font-weight="700" text-anchor="middle" fill="#12101E">${k$(p[1])}</text><text x="${x + 38}" y="154" font-size="12" text-anchor="middle" fill="#8C89A6">${p[0]}</text>`; }).join('')}
        </svg></div>
        <div class="card">${p3.map((p) => `<div class="kv"><span>${({ Dic: 'Diciembre', Ene: 'Enero', Feb: 'Febrero' })[p[0]]}</span><b class="${p[0] === 'Feb' ? 'red' : ''}">${$(p[1])}</b></div>`).join('')}</div>
        <div class="card bad"><b class="red">Febrero viene bajo</b><div class="tiny muted" style="margin-top:2px">Tu agenda de febrero tiene la mitad de horas que un mes normal.</div></div>
        <div class="card tight tiny muted">La proyección usa solo las citas ya agendadas.</div>` };
    }
    const feb = S.proy.find((p) => p[0] === 'Feb')[1];
    return { tabs: 'proyeccion', time: '9:02', html: `
      <div class="hello"><div class="k">Con tu historial y la temporada</div><h2>Lo que viene</h2></div>
      <div class="card">${lineChart(S.proy, { alt: S.acciones ? feb + 275000 : 0 })}
        <div class="row tiny muted"><span><span class="dot" style="background:#7B3FA0"></span>Proyección</span>${S.acciones ? '<span><span class="dot" style="background:#FF6B35"></span>Con acciones</span>' : ''}<span>— meta 80 %</span></div></div>
      <div class="card bad">
        <div class="row" style="align-items:flex-start"><span class="red">${I.bell}</span><div style="flex:1"><b>En febrero vas a ganar ~${$(feb)}</b><div class="tiny muted" style="margin-top:2px">Es la mitad de un mes normal. Faltan 10 semanas: hay tiempo para actuar.</div></div></div>
      </div>
      <div class="sect">Acciones sugeridas</div>
      <div class="card" style="padding:4px 16px">
        <div class="field"><span><b style="font-size:14px">Pack de 4 sesiones</b><br><span class="tiny muted">Para 9 pacientes en tratamiento</span></span><b class="orange">+$180k</b></div>
        <div class="field"><span><b style="font-size:14px">Mensaje a pacientes de alta</b><br><span class="tiny muted">14 pacientes · seguimiento a 30 días</span></span><b class="orange">+$95k</b></div>
        <div class="field"><span><b style="font-size:14px">Colchón acumulado</b><br><span class="tiny muted">Cubre el resto de febrero</span></span><b>${$(S.colchonBase + hoyColchon())}</b></div>
      </div>
      ${S.acciones ? `<div class="card ok"><b class="green">Acciones activadas ✓</b><div class="tiny muted">Febrero sube a ~${$(feb + 275000)}. Te aviso cómo responden.</div></div>`
        : '<button class="btn" data-act="acciones">Activar acciones</button>'}` };
  };

  screens.cierre = () => {
    const c = S.cierre, night = V === 1;
    const pend = S.appts.filter((a) => a.st === 'pend');
    return { tabs: 'cierre', time: night ? '22:50' : '20:40', dark: false, html: `
      <div class="hello"><div class="k">Martes 24 de noviembre</div><h2>Cierre del día</h2></div>
      ${V === 2 ? `<div class="card dark row"><span style="display:flex;gap:10px;align-items:center">${I.cierre.replace('<svg', '<svg width="22" height="22"')}<span><b>Modo “no trabajo de noche”</b><br><span class="tiny" style="color:#B9B5D6">A las 21:00 el copiloto se silencia hasta mañana.</span></span></span></div>` : ''}
      ${c.done ? `<div class="card ok" style="text-align:center;padding:22px 16px">
          <div style="width:56px;height:56px;border-radius:50%;background:var(--ok);color:#fff;display:grid;place-items:center;margin:0 auto 10px">${I.check.replace('width="18" height="18"', 'width="28" height="28"')}</div>
          <div class="mid">Día cerrado en ${V === 2 ? '4' : '6'} min</div>
          <div class="tiny muted" style="margin-top:4px">Ganancia real de hoy: <b>${$(hoyNeto())}</b></div>
        </div>
        ${V === 2 ? `<div class="grid2"><div class="card tight"><div class="lbl">Horas recuperadas</div><div class="mid">${S.horas} h</div><div class="tiny muted">este mes</div></div><div class="card tight"><div class="lbl">Cerrado a las</div><div class="mid green">20:44</div><div class="tiny muted">antes de las 21:00 ✓</div></div></div>` : ''}
        <button class="btn ghost" data-act="cierre-reset">Volver a abrir</button>`
        : `
      <div class="q ${c.q1 ? 'done' : ''}"><span class="qn">1</span><div class="mn"><b>¿Se hicieron todas las atenciones?</b>
        ${pend.length ? `<div class="tiny muted" style="margin-bottom:8px">Faltan ${pend.length} por confirmar: ${pend.map((a) => esc(a.p.split(' ')[0])).join(', ')}</div>` : ''}
        <div class="chips"><button class="chip ${c.q1 ? 'on' : ''}" data-act="q1">${pend.length ? 'Sí, confirmar todas' : 'Sí, todas'}</button></div></div></div>
      <div class="q ${c.q2 !== null ? 'done' : ''}"><span class="qn">2</span><div class="mn"><b>¿Tuviste algún gasto extra?</b>
        <div class="chips"><button class="chip ${c.q2 === 0 ? 'on' : ''}" data-act="q2" data-v="0">No</button><button class="chip ${c.q2 === 4500 ? 'on' : ''}" data-act="q2" data-v="4500">Estacionamiento $4.500</button></div></div></div>
      <div class="q ${c.q3 !== null ? 'done' : ''}"><span class="qn">3</span><div class="mn"><b>¿Hiciste km fuera de la ruta?</b>
        <div class="chips"><button class="chip ${c.q3 === 0 ? 'on' : ''}" data-act="q3" data-v="0">No</button><button class="chip ${c.q3 === 6 ? 'on' : ''}" data-act="q3" data-v="6">Sí, ~6 km</button></div></div></div>
      <button class="btn ${c.q1 && c.q2 !== null && c.q3 !== null ? '' : 'ghost'}" data-act="cerrar">Cerrar el día</button>`}` };
  };

  screens.ajustes = () => ({ tabs: 'ajustes', time: '9:10', html: `
    <div class="hello"><div class="k">Copiloto Kine</div><h2>Ajustes</h2></div>
    <div class="card" style="padding:4px 16px">
      <div class="field"><span>Agenda conectada</span><span class="v">Google Calendar</span></div>
      <div class="field"><span>Tu parte en la clínica</span><span class="v">70 %</span></div>
      <div class="field"><span>Costo por km</span><span class="v">${$(S.cfg.km)}</span></div>
      <div class="field"><span>Meta mensual</span><span class="v">${$(S.cfg.meta)}</span></div>
      ${V === 2 ? `<div class="field"><span>Retención de boleta</span><span class="v">15,25 %</span></div>
      <div class="field"><span>Colchón</span><span class="v">5 %</span></div>
      <div class="field"><span>Avisos</span><span class="v tiny">1 diario + resumen lunes</span></div>
      <div class="field"><span>Silencio desde</span><span class="v">21:00</span></div>` : ''}
    </div>
    <div class="card tight row"><span>${I.lock}&nbsp; Solo datos de agenda y dinero</span><span class="pill ok">Ley 21.719</span></div>
    <div class="card"><div class="lbl up" style="margin-bottom:8px">Prototipo</div>
      <div class="chips"><a class="chip ${V === 1 ? 'on' : ''}" href="?v=1#/hoy">Versión 1</a><a class="chip ${V === 2 ? 'on' : ''}" href="?v=2#/hoy">Versión 2</a></div>
      <button class="btn ghost" style="margin-top:12px" data-act="reset">Reiniciar datos de ejemplo</button>
      <a class="btn ghost" style="margin-top:8px" href="#/exportar">Exportar mis datos (Excel)</a></div>` });

  screens.exportar = () => ({ tabs: 'ajustes', time: '9:11', html: `${top('Exportar', 'ajustes')}
    <div class="card"><b>Tus datos son tuyos</b><div class="tiny muted" style="margin-top:4px">Descarga el mes en Excel para tu contadora, cuando quieras.</div></div>
    <div class="card" style="padding:4px 16px"><div class="field"><span>Noviembre 2026</span><span class="pill gray">.xlsx</span></div><div class="field"><span>Octubre 2026</span><span class="pill gray">.xlsx</span></div></div>
    <button class="btn" data-act="toast" data-t="Archivo listo (demo)">Descargar noviembre</button>` });

  /* ---------------- Canal WhatsApp ---------------- */
  const wa = (name, sub, color, initials, msgs, time) => ({ kind: 'wa', time, html: `
    <div class="head"><a href="#/hoy" style="color:#0A7CFF">${I.back}</a><span class="av" style="background:${color}">${initials}</span><div class="col"><b>${name}</b><span class="tiny">${sub}</span></div></div>
    <div class="msgs">${msgs}</div>
    <div class="input"><div>Mensaje</div></div>` });
  const b = (dir, text, tm, extra) => `<div class="bub ${dir}">${text}${extra || ''}<span class="tm">${tm}${dir === 'out' ? ' ✓✓' : ''}</span></div>`;
  const day = (t) => `<div class="day">${t}</div>`;

  screens.resumen = () => wa('Copiloto Kine', 'tu asistente · cuenta verificada', '#12101E', 'CK',
    day('Lunes 23 de noviembre') +
    b('in', `<div class="from">Copiloto Kine</div>☀️ <b>Tu semana (16 al 22 nov)</b>
      <div class="card-in"><span class="dot" style="background:#1F8A5B"></span><b>Ganancia real: $236.500</b><br>13 atenciones · 8 clínica · 5 domicilio<br>Colchón: +$11.800 → $84.000<br>Renta abril: 72 % apartado<br>Km: 61 (−9 % vs. semana anterior)<br>Horas recuperadas: 3 h</div>
      Esta semana tienes 14 atenciones. El martes van 3 domicilios a Machalí.`, '09:00', '<a class="act" href="#/tablero">Ver mi tablero</a>') +
    b('in', '💡 <b>Febrero viene bajo.</b> ¿Preparo un mensaje con tu pack de 4 sesiones para 14 pacientes de alta?', '09:00', '<a class="act" href="#/proyeccion">Ver propuesta</a>') +
    b('out', 'Sí, muéstrame 👍', '09:14'), '9:14');

  /* ---------------- Paciente ---------------- */
  screens['p-reserva'] = () => {
    const r = S.reserva;
    const days = [['Lun', 23], ['Mar', 24], ['Mié', 25], ['Jue', 26], ['Vie', 27]];
    const slots = ['09:00', '10:00', '11:30', '15:00', '17:00', '18:30'];
    const off = { 1: ['09:00', '10:00', '11:30'], 2: ['11:30', '15:00'], 3: ['09:00'] };
    return { kind: 'pub', time: '21:12', html: `
      <div class="urlbar"><div>${I.lock} cal.com/joselyn-kine</div></div>
      <div class="body">
        ${r.done ? `<div style="text-align:center;padding:30px 6px">
          <div style="width:64px;height:64px;border-radius:50%;background:var(--ok);color:#fff;display:grid;place-items:center;margin:0 auto 14px">${I.check.replace('width="18" height="18"', 'width="32" height="32"')}</div>
          <div class="mid">¡Hora reservada!</div>
          <div class="muted" style="margin:6px 0 18px">${days[r.day][0]} ${days[r.day][1]} nov · ${r.slot} · Atención a domicilio</div>
          <div class="card" style="text-align:left"><div class="tiny muted">Te llegará la confirmación y un recordatorio por WhatsApp el día antes.</div></div>
          <button class="btn ghost" data-act="reserva-reset">Hacer otra reserva</button></div>` : `
        <div class="prof"><span class="ph">JT</span><div><b style="font-size:17px">Joselyn Toledo</b><div class="tiny muted">Kinesióloga · Centro Médico InMotion</div><div class="tiny" style="margin-top:2px">⭐ 4,9 · Atención 1:1 de 45–60 min</div></div></div>
        <div class="lbl" style="margin-bottom:8px">Servicio</div>
        <div class="chips" style="margin-bottom:14px"><span class="chip on">Rehabilitación</span><span class="chip">Respiratoria</span><span class="chip">Masoterapia</span></div>
        <div class="lbl" style="margin-bottom:8px">¿Dónde?</div>
        <div class="chips" style="margin-bottom:14px"><span class="chip">Clínica InMotion</span><span class="chip on">En mi casa</span></div>
        <div class="lbl" style="margin-bottom:8px">Noviembre</div>
        <div class="days" style="margin-bottom:14px">${days.map((d, i) => `<button class="${r.day === i ? 'on' : ''}" data-act="r-day" data-i="${i}">${d[0]}<b>${d[1]}</b></button>`).join('')}</div>
        <div class="slots" style="margin-bottom:16px">${slots.map((s) => (off[r.day] || []).includes(s) ? `<button class="off">${s}</button>` : `<button class="${r.slot === s ? 'on' : ''}" data-act="r-slot" data-s="${s}">${s}</button>`).join('')}</div>
        <button class="btn" data-act="reservar">Reservar ${days[r.day][0].toLowerCase()} ${days[r.day][1]} · ${r.slot}</button>
        <div class="tiny muted" style="text-align:center;margin-top:10px">Agenda en línea de Joselyn · conectada a su Copiloto</div>`}
      </div>` };
  };

  screens['p-luis'] = () => wa('Joselyn Kine', 'en línea', '#FF6B35', 'JT',
    day('Lunes 23 de noviembre') +
    b('in', 'Hola don Luis 👋 Le recuerdo su sesión de mañana <b>martes 24 a las 11:30</b> en su casa (Pje. Los Aromos 214). ¿Me confirma?', '11:30', '<span class="act">Confirmo</span><span class="act">Necesito cambiar la hora</span>') +
    b('out', 'Confirmo, gracias Joselyn', '11:42') +
    day('Hoy') +
    b('in', '🚗 Voy en camino. Llego a las 11:30 aprox.', '11:12') +
    b('in', `Gracias por la sesión de hoy, don Luis. Si le acomoda, puede pagar aquí 👇<div class="card-in"><b>Sesión de kinesiología · $25.000</b><br><span style="color:#667">pago.copilotokine.cl/js-0241</span></div>La boleta le llega al correo.`, '12:22', '<a class="act" href="#/p-pago">Pagar</a>') +
    (S.pagoLuis ? b('out', 'Listo, pagado 👍', '12:30') : '') +
    b('in', 'Recuerde sus ejercicios: 2 series de puente y gato-camello cada día 🙌', '12:31'), '12:31');

  screens['p-pago'] = () => ({ kind: 'pub', time: '12:28', html: `
    <div class="urlbar"><div>${I.lock} pago.copilotokine.cl/js-0241</div></div>
    <div class="body">
      ${S.pagoLuis ? `<div style="text-align:center;padding:36px 6px">
        <div style="width:64px;height:64px;border-radius:50%;background:var(--ok);color:#fff;display:grid;place-items:center;margin:0 auto 14px">${I.check.replace('width="18" height="18"', 'width="32" height="32"')}</div>
        <div class="mid">Pago recibido</div><div class="muted" style="margin:6px 0 18px">$25.000 · ${esc(S.pay)}</div>
        <div class="card" style="text-align:left"><div class="kv"><span>Comprobante</span><b>#0241</b></div><div class="kv"><span>Boleta de honorarios</span><span>enviada al correo</span></div></div>
        <a class="btn ghost" href="#/p-luis">Volver a WhatsApp</a></div>` : `
      <div class="prof"><span class="ph">JT</span><div><b style="font-size:17px">Joselyn Toledo</b><div class="tiny muted">Kinesióloga</div></div></div>
      <div class="card"><div class="lbl">Sesión a domicilio · martes 24 nov</div><div class="big" style="margin-top:4px">$25.000</div><div class="tiny muted">Rehabilitación lumbar · sesión 3 de 4</div></div>
      <div class="lbl" style="margin:4px 0 8px">Paga con</div>
      <div class="btns" style="margin-bottom:16px">${['Transferencia', 'Tarjeta de débito o crédito', 'Código QR'].map((p) => `<button class="integ" data-act="pay" data-p="${p}" style="width:100%;text-align:left;margin:0"><span class="mn"><b>${p}</b></span>${S.pay === p ? '<span class="pill ok">✓</span>' : ''}</button>`).join('')}</div>
      <button class="btn dark" data-act="pagar">Pagar $25.000</button>
      <div class="tiny muted" style="text-align:center;margin-top:10px">${I.lock} Pago seguro · el registro llega solo al Copiloto de Joselyn</div>`}
    </div>` });

  screens['p-camila'] = () => wa('Joselyn Kine', 'en línea', '#FF6B35', 'JT',
    day('Lunes 16 de noviembre') +
    b('in', 'Hola Camila 😊 Hace un mes terminamos tu tratamiento de tobillo. ¿Cómo has estado? Si quieres mantenerte, tengo un <b>pack de 4 sesiones de mantención</b>.', '10:00', '<span class="act">Ver el pack</span>') +
    b('out', '¡Bien! Lo pienso 🙂', '10:21') +
    day('Hoy') +
    b('in', 'Hola Camila, se liberó una hora <b>hoy a las 16:00</b> en Machalí, con 15 % de descuento ($21.250). ¿La quieres?', '13:05', S.cupo === 'taken' ? '' : '<button class="act" data-act="cupo-take" style="width:calc(100% + 20px)">Sí, la tomo</button><span class="act">Hoy no</span>') +
    (S.cupo === 'taken' ? b('out', '¡Sí, la tomo! 🙌', '13:07') + b('in', 'Listo ✅ Quedó agendada. Nos vemos a las 16:00.', '13:07') : ''), '13:07');

  /* ---------------- Render ---------------- */
  const V2ONLY = ['ruta', 'cupo', 'resumen', 'p-luis', 'p-pago', 'p-camila'];
  const NAV = [
    ['Joselyn · configurar', [['inicio', 'Bienvenida'], ['conectar', 'Conectar agenda'], ['reglas', 'Tus reglas']]],
    ['Joselyn · su día', [['hoy', 'Hoy'], ['ruta', 'Ruta por sector'], ['atencion/a3', 'Atención realizada'], ['cupo', 'Cupo de último minuto'], ['cierre', 'Cierre del día']]],
    ['Joselyn · sus números', [['tablero', 'Tablero'], ['proyeccion', 'Proyección'], ['resumen', 'Resumen semanal (WhatsApp)'], ['ajustes', 'Ajustes']]],
    ['Paciente', [['p-reserva', 'Reserva en línea'], ['p-luis', 'WhatsApp de don Luis'], ['p-pago', 'Pago con link'], ['p-camila', 'WhatsApp de Camila']]]
  ];
  let toastMsg = '';

  function route() {
    const h = (location.hash || '#/hoy').replace(/^#\//, '');
    const [name, arg] = h.split('/');
    return { name: screens[name] ? name : 'hoy', arg, full: h };
  }

  function render() {
    const r = route();
    let name = r.name;
    if (V === 1 && V2ONLY.includes(name)) name = 'hoy';
    const s = screens[name](r.arg);
    const nav = `<aside class="nav"><h1>Copiloto <span>Kine</span></h1><p>Prototipo funcional · datos ficticios de ejemplo · martes 24 nov 2026</p>
      <div class="vswitch"><a href="?v=1#/${r.full}" class="${V === 1 ? 'on' : ''}">V1 · alcance mínimo</a><a href="?v=2#/${r.full}" class="${V === 2 ? 'on' : ''}">V2 · iterada</a></div>
      ${NAV.map(([g, items]) => `<div class="grp">${g}</div>${items.map(([h, n]) => {
        const off = V === 1 && V2ONLY.includes(h.split('/')[0]);
        return `<a href="#/${h}" class="${r.full === h || (name === h.split('/')[0] && !off) ? 'on' : ''}" style="${off ? 'opacity:.35;pointer-events:none' : ''}">${n}${off ? '<small>V2</small>' : ''}</a>`;
      }).join('')}`).join('')}
      <button class="reset" data-act="reset">Reiniciar datos de ejemplo</button></aside>`;
    const inner = s.kind === 'wa' ? `<div class="wa">${status(s.time)}${s.html}</div>`
      : s.kind === 'pub' ? `<div class="pub">${status(s.time)}${s.html}</div>`
        : `<div class="app ${s.tabs ? 'has-tabs' : ''}">${status(s.time)}<div class="body">${s.html}</div>${s.tabs ? tabs(s.tabs) : ''}</div>`;
    document.getElementById('root').innerHTML = `<div class="stage">${nav}<div class="device"><div class="screen"><div class="island"></div>${inner}${toastMsg ? `<div class="toast">${toastMsg}</div>` : ''}</div></div></div>`;
    document.title = 'Copiloto Kine · ' + (V === 1 ? 'V1' : 'V2');
  }

  function toast(t) { toastMsg = t; render(); setTimeout(() => { toastMsg = ''; render(); }, 2200); }
  const go = (h) => { location.hash = '#/' + h; };

  document.addEventListener('click', (e) => {
    const el = e.target.closest('[data-act]');
    if (!el) return;
    const act = el.dataset.act;
    const A = {
      'toggle-agenda': () => { S.cfg.agenda[el.dataset.k] = !S.cfg.agenda[el.dataset.k]; },
      'onboard-done': () => {},
      pay: () => { S.pay = el.dataset.p; },
      realizada: () => { const a = byId(el.dataset.id); a.st = 'done'; a.pay = S.pay; save(); go('hoy'); toast('Atención registrada · +' + $(neto(a)) + ' de ganancia'); return 'skip'; },
      noasistio: () => { byId(el.dataset.id).st = 'cancel'; save(); go('hoy'); return 'skip'; },
      'cupo-offer': () => { S.cupo = 'offered'; toastMsg = ''; setTimeout(() => toast('Cupo enviado a 3 pacientes'), 0); },
      'cupo-take': () => {
        S.cupo = 'taken';
        const a = byId('a5');
        if (!S.appts.find((x) => x.id === 'a7')) S.appts.push({ id: 'a7', h: '16:00', p: 'Camila Fuentes', s: 'Mantención de tobillo', l: 'dom', sector: 'Machalí', addr: 'Villa Los Prados 45', km: 3, kit: 'rodilla', v: 25000, cupo: true, st: 'pend', ses: 'pack 1 de 4' });
        a.hidden = true;
      },
      acciones: () => { S.acciones = true; setTimeout(() => toast('Mensajes programados para mañana 10:00'), 0); },
      q1: () => { S.cierre.q1 = true; S.appts.forEach((a) => { if (a.st === 'pend') a.st = 'done'; }); },
      q2: () => { S.cierre.q2 = Number(el.dataset.v); },
      q3: () => { S.cierre.q3 = Number(el.dataset.v); },
      cerrar: () => { const c = S.cierre; if (c.q1 && c.q2 !== null && c.q3 !== null) c.done = true; else setTimeout(() => toast('Responde las 3 preguntas'), 0); },
      'cierre-reset': () => { S.cierre = { q1: false, q2: null, q3: null, done: false }; },
      'r-day': () => { S.reserva.day = Number(el.dataset.i); },
      'r-slot': () => { S.reserva.slot = el.dataset.s; },
      reservar: () => { S.reserva.done = true; },
      'reserva-reset': () => { S.reserva.done = false; },
      pagar: () => { S.pagoLuis = true; const a = byId('a3'); a.st = 'done'; a.pay = 'Link de pago'; },
      toast: () => { setTimeout(() => toast(el.dataset.t), 0); },
      reset: () => { S = seed(); LS.del(KEY); }
    };
    if (A[act]) { e.preventDefault(); if (A[act]() === 'skip') return; save(); render(); if (act === 'onboard-done') go('hoy'); }
  });

  // Las horas canceladas reemplazadas por un cupo tomado no se muestran.
  const baseHoy = screens.hoy;
  screens.hoy = () => { const keep = S.appts; S.appts = keep.filter((a) => !a.hidden); const out = baseHoy(); S.appts = keep; return out; };

  LS.set('ck-v', V);
  if (SHOT) document.body.classList.add('shot');
  window.addEventListener('hashchange', render);
  render();
})();
