/* BRK Consultoria Financeira — interações do site */
(function () {
    var body = document.body;
    document.documentElement.classList.add('js');

    // ----- Revelação suave ao rolar -----
    if ('IntersectionObserver' in window) {
        var els = document.querySelectorAll('.section .section-head, .card, .tool-card, .post-card, .pain-card, .stat, .kpi, .cost, .outcomes, .commit > div, .step, .dash-card, .ebook, .track, .news-card, .faq, .quote, .mission, .statement');
        var ro = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); ro.unobserve(e.target); } }); }, { rootMargin: '0px 0px -8% 0px' });
        els.forEach(function (el) { el.classList.add('reveal'); ro.observe(el); });
    }

    // ----- Medição (ativa só se GA4/Pixel configurados) -----  brk-track
    document.addEventListener('click', function (e) {
        var a = e.target.closest && e.target.closest('a[href*="ig.me"], a[href*="wa.me"]');
        if (a) { try { if (window.gtag) gtag('event', 'whatsapp_click'); if (window.fbq) fbq('track', 'Contact'); } catch (x) {} }
    });
    document.addEventListener('submit', function (e) {
        try { if (window.gtag) gtag('event', 'generate_lead'); if (window.fbq) fbq('track', 'Lead'); } catch (x) {}
    });

    // ----- Menu do celular -----
    var toggle = document.querySelector('.menu-toggle');
    function setMenu(open) {
        body.classList.toggle('menu-open', open);
        if (toggle) {
            toggle.setAttribute('aria-expanded', open);
            toggle.setAttribute('aria-label', open ? 'Fechar menu' : 'Abrir menu');
        }
    }
    if (toggle) {
        toggle.addEventListener('click', function () { setMenu(!body.classList.contains('menu-open')); });
        document.querySelectorAll('.nav a').forEach(function (a) { a.addEventListener('click', function () { setMenu(false); }); });
    }

    // ----- Barra fixa de contato (celular): aparece depois do primeiro botão -----
    var bar = document.querySelector('.mobile-cta');
    var anchor = document.querySelector('.hero .btn, .page-hero .btn, .page-hero h1');
    if (bar && anchor && 'IntersectionObserver' in window) {
        new IntersectionObserver(function (entries) {
            var e = entries[0];
            bar.classList.toggle('visible', !e.isIntersecting && e.boundingClientRect.top < 0);
        }).observe(anchor);
    } else if (bar) {
        bar.classList.add('visible');
    }

    // ----- Guias: desbloqueio após seguir no Instagram -----
    var gate = document.getElementById('gate');
    if (gate) {
        var STORE_KEY = 'brk-guias-v1';
        var state = { instagram: false, linkedin: false };
        try {
            var saved = JSON.parse(localStorage.getItem(STORE_KEY) || '{}');
            state.instagram = !!saved.instagram; state.linkedin = !!saved.linkedin;
        } catch (e) {}
        var save = function () { try { localStorage.setItem(STORE_KEY, JSON.stringify(state)); } catch (e) {} };

        var steps = gate.querySelectorAll('.gate-step');
        var progress = gate.querySelector('.gate-progress span');
        var count = gate.querySelector('.js-count');
        var lastFocus = null, pending = null;

        var render = function () {
            var done = 0;
            steps.forEach(function (el) {
                var ok = state[el.getAttribute('data-step')];
                el.classList.toggle('done', ok);
                el.querySelector('.st').textContent = ok ? '✓ Feito' : 'Seguir';
                if (ok) done++;
            });
            count.textContent = done;
            progress.style.width = (done / steps.length * 100) + '%';
            var complete = done === steps.length;
            gate.classList.toggle('complete', complete);
            body.classList.toggle('guides-unlocked', complete);
        };
        var openGate = function () {
            lastFocus = document.activeElement;
            gate.classList.add('open'); gate.setAttribute('aria-hidden', 'false');
            body.classList.add('gate-open');
            setTimeout(function () { gate.querySelector('.gate-close').focus(); }, 50);
        };
        var closeGate = function () {
            gate.classList.remove('open'); gate.setAttribute('aria-hidden', 'true');
            body.classList.remove('gate-open');
            if (lastFocus) lastFocus.focus();
        };
        var confirmPending = function () {
            if (!pending) return;
            state[pending] = true; pending = null; save(); render();
        };

        document.querySelectorAll('.js-unlock').forEach(function (b) { b.addEventListener('click', openGate); });
        gate.querySelector('.js-gate-close').addEventListener('click', closeGate);
        gate.addEventListener('click', function (e) { if (e.target === gate) closeGate(); });
        document.addEventListener('keydown', function (e) {
            if (e.key !== 'Escape') return;
            if (gate.classList.contains('open')) closeGate(); else setMenu(false);
        });
        steps.forEach(function (el) {
            el.addEventListener('click', function () {
                if (state[el.getAttribute('data-step')]) return;
                pending = el.getAttribute('data-step');
                el.querySelector('.st').textContent = 'Abrindo…';
                setTimeout(confirmPending, 4000);
            });
        });
        document.addEventListener('visibilitychange', function () {
            if (document.visibilityState === 'visible' && pending) setTimeout(confirmPending, 600);
        });
        if (location.hash === '#guias-liberar') openGate();
        render();
    }
})();
