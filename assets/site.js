
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


  // ---------- ambient particle network (the background from the original design) ----------
  (function(){
    var c = document.getElementById('net');
    if(!c || !c.getContext) return;
    if(matchMedia('(prefers-reduced-motion: reduce)').matches){ c.style.display='none'; return; }
    var ctx = c.getContext('2d'), w=0, h=0, dpr=1, pts=[], raf=null, running=true;
    var COUNT = window.innerWidth < 700 ? 24 : 52;
    var LINK = 19000; // squared distance limit

    function size(){
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      w = c.clientWidth || window.innerWidth;
      h = c.clientHeight || window.innerHeight;
      c.width = Math.round(w*dpr); c.height = Math.round(h*dpr);
      ctx.setTransform(dpr,0,0,dpr,0,0);
    }
    function seed(){
      pts = [];
      for(var i=0;i<COUNT;i++){
        pts.push({x:Math.random()*w, y:Math.random()*h,
                  vx:(Math.random()-.5)*.22, vy:(Math.random()-.5)*.22,
                  r:Math.random()*1.3+.7});
      }
    }
    function draw(){
      ctx.clearRect(0,0,w,h);
      for(var i=0;i<pts.length;i++){
        var p = pts[i];
        p.x += p.vx; p.y += p.vy;
        if(p.x < 0 || p.x > w) p.vx *= -1;
        if(p.y < 0 || p.y > h) p.vy *= -1;
        ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, 6.2832);
        ctx.fillStyle = 'rgba(14,165,233,.5)'; ctx.fill();
        for(var j=i+1;j<pts.length;j++){
          var q = pts[j], dx = p.x-q.x, dy = p.y-q.y, d2 = dx*dx + dy*dy;
          if(d2 < LINK){
            var a = (1 - d2/LINK) * 0.15;
            ctx.strokeStyle = 'rgba(14,165,233,' + a.toFixed(3) + ')';
            ctx.lineWidth = 1;
            ctx.beginPath(); ctx.moveTo(p.x,p.y); ctx.lineTo(q.x,q.y); ctx.stroke();
          }
        }
      }
      if(running) raf = requestAnimationFrame(draw);
    }
    size(); seed(); draw();
    addEventListener('resize', function(){ size(); seed(); }, {passive:true});
    document.addEventListener('visibilitychange', function(){
      if(document.hidden){ running = false; if(raf) cancelAnimationFrame(raf); }
      else if(!running){ running = true; draw(); }
    });
  })();

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

