/* BRK Gestão Financeira — busca no glossário */
(function () {
    var input = document.getElementById('busca');
    if (!input) return;
    var terms = document.querySelectorAll('#terms .term'), none = document.getElementById('noterm');
    function norm(s) { return s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase(); }
    var idx = Array.prototype.map.call(terms, function (t) { return norm(t.dataset.term); });
    input.addEventListener('input', function () {
        var q = norm(input.value.trim()), shown = 0;
        terms.forEach(function (t, i) { var ok = !q || idx[i].indexOf(q) >= 0; t.style.display = ok ? '' : 'none'; if (ok) shown++; });
        none.style.display = shown ? 'none' : 'block';
    });
})();
