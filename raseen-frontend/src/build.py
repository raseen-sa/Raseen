# Run inside src/: python3 build.py  -> writes app.html (platform) and raseen.html (site + platform)
import base64
def R(s,a,b):
    assert s.count(a)==1,(a[:70],s.count(a)); return s.replace(a,b)
# the logo (new identity, Nov 24): vector files from the brand guidelines, white on navy and navy on light
logo=lambda f:'data:image/svg+xml;base64,'+base64.b64encode(open(f,'rb').read()).decode()
LW,LD=logo('../assets/logo-white.svg'),logo('../assets/logo-navy.svg')
FAV=logo('../assets/favicon.svg')

# ---------- platform: talk to the website when it runs inside it
a=open('app.src.html').read()
if 'raseen-exit' not in a:
    a=R(a,'<p class="hint">البيانات في هذا النموذج توضيحية، والشركة «نخلة للاتصالات» افتراضية.</p>',
        '<p class="hint">البيانات في هذا النموذج توضيحية، والشركة «نخلة للاتصالات» افتراضية.</p>\n      <a class="back-site" href="#" data-exit>الرجوع للموقع</a>')
    a=R(a,'/* toast + help */','.back-site{font-size:14px;color:var(--teal);font-weight:600;align-self:flex-start}\n.back-site:not(.in){display:none}\n\n/* toast + help */')
    a=R(a,'/* ---- routing */',"""/* ---- inside the website: logo, logout and back link return to the site */
var inSite=window.parent!==window;
if(inSite){$$('.back-site').forEach(function(x){x.classList.add('in')});$('#logout').setAttribute('data-exit','');$('.sbrand').setAttribute('data-exit','');}
document.addEventListener('click',function(e){var x=e.target.closest('[data-exit]');if(!x||!inSite)return;e.preventDefault();location.hash='#login';parent.postMessage('raseen-exit','*')});

/* ---- routing */""")
    open('app.src.html','w').write(a)
app=a.replace('{{LOGO_DARK}}',LD).replace('{{LOGO}}',LW).replace('{{FAVICON}}',FAV)
open('app.html','w').write(app)
doc='<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body>'+app+'</body></html>'

# ---------- website: one link, the platform opens from it
s=open('web.src.html').read()
if 'appLayer' not in s:
    s=R(s,'<a class="login" href="#cta">تسجيل الدخول</a>','<a class="login" href="#app" data-app>تسجيل الدخول</a>')
    s=R(s,'<a href="#faq">الأسئلة</a><a href="#cta">تسجيل الدخول</a></nav>','<a href="#faq">الأسئلة</a><a href="#app" data-app>تسجيل الدخول</a></nav>')
    s=R(s,'<a class="btn g" href="#cta">اطلب عرضًا</a></div>','<a class="btn g" href="#app" data-app>جرّب المنصة</a></div>')
    s=R(s,'<div class="acts"><a class="btn y" href="#cta">اطلب عرضًا</a><a class="btn g" href="#example">شاهد المثال</a></div>',
        '<div class="acts"><a class="btn y" href="#cta">اطلب عرضًا</a><a class="btn g" href="#app" data-app>جرّب المنصة</a></div>')
    s=R(s,'</style>','''#appLayer{position:fixed;inset:0;z-index:200;background:var(--navy);display:none;opacity:0;transition:opacity .45s var(--ease)}
#appLayer.on{display:block}
#appLayer.show{opacity:1}
#appLayer iframe{width:100%;height:100%;border:0;display:block}
</style>''')
    i=s.rindex('</div>')  # end of the RTL wrapper
    s=s[:i]+'''<div id="appLayer" aria-hidden="true"><iframe id="appFrame" title="منصة رسين"></iframe></div>
<script type="text/plain" id="appSrc">{{APP}}</script>
'''+s[i:]
    s=R(s,'  // marquee: duplicate the row so it loops without a gap','''  // the platform lives behind "تسجيل الدخول": it opens over the site and logout returns here
  (function(){
    var layer=$('#appLayer'), fr=$('#appFrame'), loaded=false;
    function open(e){if(e)e.preventDefault();
      if(!loaded){fr.srcdoc=$('#appSrc').textContent.replace(/<\\\\\\/script>/g,'<\\/script>');loaded=true;}
      layer.classList.add('on');requestAnimationFrame(function(){layer.classList.add('show')});layer.setAttribute('aria-hidden','false');
      document.documentElement.style.overflow='hidden'; if(window.__lenis) window.__lenis.stop();
      var sh=$('#sheet'); if(sh) sh.classList.remove('open');}
    function close(){layer.classList.remove('show');layer.setAttribute('aria-hidden','true');
      setTimeout(function(){layer.classList.remove('on')},450);
      document.documentElement.style.overflow=''; if(window.__lenis) window.__lenis.start();}
    document.addEventListener('click',function(e){var a=e.target.closest('[data-app]'); if(a) open(e);},true);
    addEventListener('message',function(e){if(e.data==='raseen-exit') close();});
    if(location.hash==='#app') setTimeout(open,300);
  })();

  // marquee: duplicate the row so it loops without a gap''')
    open('web.src.html','w').write(s)
out=s.replace('{{LOGO_DARK}}',LD).replace('{{LOGO}}',LW).replace('{{FAVICON}}',FAV).replace('{{APP}}',doc.replace('</script>','<\\/script>'))
open('raseen.html','w').write(out)
print('ok',len(out))
