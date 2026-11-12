
(function(){
  document.documentElement.classList.add('js');
  // mobile nav
  var nav = document.querySelector('.nav');
  var t = document.querySelector('.nav__toggle');
  if(t && nav){ t.addEventListener('click', function(){
    nav.classList.toggle('open');
    t.setAttribute('aria-expanded', nav.classList.contains('open') ? 'true' : 'false');
  }); }

  // reveal
  var rv = document.querySelectorAll('.rv');
  if('IntersectionObserver' in window && rv.length){
    var io = new IntersectionObserver(function(es){
      es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); } });
    }, {rootMargin:'0px 0px -8% 0px', threshold:0.08});
    rv.forEach(function(el){ io.observe(el); });
    // safety net: nothing stays hidden for longer than a second
    setTimeout(function(){ rv.forEach(function(el){ el.classList.add('in'); }); }, 1200);
  } else { rv.forEach(function(el){ el.classList.add('in'); }); }

  // copy prompt buttons
  document.querySelectorAll('.copy').forEach(function(btn){
    btn.addEventListener('click', function(){
      var box = btn.closest('.prompt').querySelector('pre');
      var text = box.innerText;
      var done = function(){ btn.textContent='Copied'; btn.classList.add('done');
        setTimeout(function(){ btn.textContent='Copy'; btn.classList.remove('done'); }, 1600); };
      if(navigator.clipboard && navigator.clipboard.writeText){
        navigator.clipboard.writeText(text).then(done).catch(function(){ fallback(); });
      } else { fallback(); }
      function fallback(){
        var ta=document.createElement('textarea'); ta.value=text; document.body.appendChild(ta);
        ta.select(); try{ document.execCommand('copy'); }catch(e){} document.body.removeChild(ta); done();
      }
    });
  });

  // ---------- text to speech ----------
  (function(){
    if(!('speechSynthesis' in window)) return;
    var synth = window.speechSynthesis;
    var current = null;
    var ICON = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9v6h4l5 4V5L8 9H4zm12.5 3a4.5 4.5 0 0 0-2.5-4v8a4.5 4.5 0 0 0 2.5-4z"/></svg>';

    function makeBtn(){
      var b = document.createElement('button');
      b.className = 'speak'; b.type = 'button';
      b.innerHTML = ICON + '<span>Listen</span>';
      b.setAttribute('aria-label', 'Read this section aloud');
      return b;
    }
    function reset(btn){
      if(!btn) return;
      btn.classList.remove('on');
      var sp = btn.querySelector('span'); if(sp) sp.textContent = 'Listen';
    }
    function speak(el, btn){
      var wasOn = btn.classList.contains('on');
      synth.cancel();
      if(current) reset(current);
      current = null;
      if(wasOn) return;
      var clone = el.cloneNode(true);
      clone.querySelectorAll('.speak, script, style').forEach(function(n){ n.remove(); });
      var text = (clone.innerText || '').replace(/\s+/g, ' ').trim();
      if(!text) return;
      var u = new SpeechSynthesisUtterance(text);
      u.lang = 'en-IN'; u.rate = 0.98;
      u.onend = u.onerror = function(){ reset(btn); if(current === btn) current = null; };
      btn.classList.add('on');
      btn.querySelector('span').textContent = 'Stop';
      current = btn;
      synth.speak(u);
    }

    document.querySelectorAll('.prose[data-speak="sections"]').forEach(function(prose){
      var kids = Array.prototype.slice.call(prose.children);
      var group = null;
      kids.forEach(function(node){
        if(node.classList && node.classList.contains('pager')){ group = null; return; }
        if(node.tagName === 'H2'){
          group = document.createElement('div');
          group.className = 'sblock';
          prose.insertBefore(group, node);
          group.appendChild(node);
          var btn = makeBtn();
          group.insertBefore(btn, group.firstChild);
          btn.addEventListener('click', function(){ speak(group, btn); });
        } else if(group){
          group.appendChild(node);
        }
      });
    });

    document.querySelectorAll('.speakable').forEach(function(el){
      if(el.querySelector(':scope > .speak')) return;
      var btn = makeBtn();
      el.insertBefore(btn, el.firstChild);
      btn.addEventListener('click', function(){ speak(el, btn); });
    });

    addEventListener('beforeunload', function(){ synth.cancel(); });
  })();
})();

