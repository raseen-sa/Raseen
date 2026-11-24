"""The Raseen logo as inline SVG with the radar sweep (Nov 24): the word stays still,
a sweep turns over the waves and lights each one as it passes.
Used by build.py: {{LOGO_SPRITE}} once per page, then {{RL:id:white|navy:loop|once[:extra-class]}}."""
import math, re
SRC = '../assets/logo-white.svg'
CX, CY, R = 710, 388, 126
VB = '366 264 472 158'

def _parts():
    s = open(SRC).read()
    glyphs = re.findall(r'<g id="(glyph-[^"]*)">(.*?)</g>', s)
    arcs = re.findall(r'<path fill="none"[^>]*/>', s)
    dot = re.search(r'<path fill-rule="nonzero" fill="#FFF"[^>]*/>', s).group(0)
    uses = re.findall(r'<use xlink:href="#(glyph-[^"]*)" x="([^"]*)" y="([^"]*)"/>', s)
    return glyphs, arcs, dot, uses

def _sector(a0, a1, r=R):
    P = lambda a: (CX + r * math.sin(math.radians(a)), CY - r * math.cos(math.radians(a)))
    x0, y0 = P(a0); x1, y1 = P(a1)
    return f'M{CX} {CY}L{x0:.1f} {y0:.1f}A{r} {r} 0 0 1 {x1:.1f} {y1:.1f}Z'

N, STEP = 40, 1.1
TRAIL = ''.join(f'<path d="{_sector(-(i+1)*STEP, -i*STEP+.15)}" fill-opacity="{(1-i/N)**2.2:.2f}"/>' for i in range(N))
EDGE = f'<path class="e" d="M{CX} {CY}L{CX} {CY-R}" fill="none"/>'

def sprite():
    glyphs, *_ = _parts()
    return ('<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>'
            + ''.join(f'<path id="rl{gid}" d="{re.search(r"d=\"([^\"]*)\"", body).group(1)}"/>' for gid, body in glyphs)
            + '</defs></svg>')

def logo(uid, variant='white', mode='once', extra=''):
    _, arcs, dot, uses = _parts()
    ink = '#FFFFFF' if variant == 'white' else '#0A2331'
    arcs = [re.sub(r' stroke="#FFF"', f' stroke="{ink}"', a) for a in arcs]
    arcs = [re.sub(r' (stroke-opacity|stroke-miterlimit|stroke-linejoin)="[^"]*"', '', a) for a in arcs]
    lit = ''.join(a.replace('stroke-width="8"', 'stroke-width="8.6"') for a in arcs)
    dot = dot.replace('fill="#FFF"', f'fill="{ink}"').replace(' fill-opacity="1"', '')
    word = ''.join(f'<use href="#rl{g}" x="{x}" y="{y}"/>' for g, x, y in uses)
    q, m = f'rlq{uid}', f'rlm{uid}'
    cls = f'rl rl-{mode} {extra}'.strip()
    return (f'<svg class="{cls}" viewBox="{VB}" role="img" aria-label="رسين" style="--ink:{ink}">'
            f'<defs><clipPath id="{q}"><path d="M{CX} {CY}L{CX} {CY-130}A130 130 0 0 1 {CX+130} {CY}Z"/></clipPath>'
            f'<mask id="{m}" maskUnits="userSpaceOnUse" x="560" y="240" width="320" height="200">'
            f'<g clip-path="url(#{q})"><g class="rl-sw" fill="#fff">{TRAIL}</g></g></mask></defs>'
            f'<g fill="{ink}">{word}</g>'
            f'<g clip-path="url(#{q})"><g class="rl-sw rl-beam">{TRAIL}{EDGE}</g></g>'
            f'<g class="rl-base">{"".join(arcs)}</g>{dot}'
            f'<g mask="url(#{m})">{lit}</g></svg>')

CSS = '''
/* logo radar (Nov 24): the word stays still; a sweep lights the waves. loop = repeats, once = on load and on hover */
.rl{display:block;overflow:visible;aspect-ratio:472/158}
.rl .rl-sw{transform-box:view-box;transform-origin:710px 388px;transform:rotate(-60deg)}
.rl .rl-beam{fill:#2FB3A3;fill-opacity:.15}
.rl .rl-beam path{fill-opacity:inherit}
.rl .rl-beam .e{stroke:var(--ink);stroke-width:1.4;stroke-linecap:round;opacity:.55}
.rl-loop .rl-sw{animation:rlSweep 3.2s cubic-bezier(.45,.05,.4,1) infinite}
.rl-loop .rl-beam{animation:rlSweep 3.2s cubic-bezier(.45,.05,.4,1) infinite,rlBeam 3.2s linear infinite}
.rl-loop .rl-base{animation:rlDim 3.2s ease infinite}
.rl-once.run .rl-sw{animation:rlSweep1 1.8s cubic-bezier(.45,.05,.4,1) both}
.rl-once.run .rl-beam{animation:rlSweep1 1.8s cubic-bezier(.45,.05,.4,1) both,rlBeam1 1.8s linear both}
.rl-once.run .rl-base{animation:rlDim1 1.8s ease both}
@keyframes rlSweep{0%{transform:rotate(-4deg)}62%,100%{transform:rotate(140deg)}}
@keyframes rlBeam{0%,50%{opacity:1}62%,100%{opacity:0}}
@keyframes rlDim{0%{opacity:1}8%,55%{opacity:.5}72%,100%{opacity:1}}
@keyframes rlSweep1{0%{transform:rotate(-4deg)}100%{transform:rotate(140deg)}}
@keyframes rlBeam1{0%,82%{opacity:1}100%{opacity:0}}
@keyframes rlDim1{0%{opacity:1}12%,82%{opacity:.5}100%{opacity:1}}
'''

JS = '''<script>
/* logo radar: "once" logos sweep after the page opens and again on hover */
(function(){var L=[].slice.call(document.querySelectorAll('.rl-once'));
function run(s){if(s.classList.contains('run'))return;s.classList.add('run');setTimeout(function(){s.classList.remove('run')},1900)}
L.forEach(function(s){var a=s.closest('a')||s;a.addEventListener('mouseenter',function(){run(s)});setTimeout(function(){run(s)},1600)});})();
</script>'''

def apply(html):
    html = html.replace('{{LOGO_SPRITE}}', sprite())
    def sub(m):
        p = m.group(1).split(':')
        return logo(p[0], p[1], p[2], p[3] if len(p) > 3 else '')
    return re.sub(r'\{\{RL:([^}]*)\}\}', sub, html)
