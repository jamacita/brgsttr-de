from pathlib import Path

def read(path):
    return Path(path).read_text(encoding='utf-8')
def write(path, text):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')
def tag(name, attrs='', closing=False):
    if closing:
        return chr(60) + '/' + name + chr(62)
    return chr(60) + name + ((' ' + attrs) if attrs else '') + chr(62)

html_files = [p for p in Path('.').rglob('*.html') if '.git' not in p.parts]
path_replacements = {
    '/about.html':'/about/', '/discretion.html':'/discretion/', '/notes.html':'/notes/',
    '/access.html':'/access/', '/contact.html':'/contact/', '/privacy.html':'/privacy/',
    '/use.html':'/boundaries/', 'Use &amp; boundaries':'boundaries.', 'Privacy':'privacy.',
    'Contact':'contact.', 'About':'about.', 'Discretion':'discretion.', 'Notes':'notes.', 'Access':'access.'
}
for p in html_files:
    s = p.read_text(encoding='utf-8')
    for old, new in path_replacements.items():
        s = s.replace(old, new)
    p.write_text(s, encoding='utf-8')

p = Path('index.html')
s = read(p)
reps = {
    'A minimal contact and context endpoint for controlled exchange, discretion and governance-aware communication.':'A quiet contact point for selected professional and conceptual exchange with discretion, context and careful wording.',
    'Minimal contact endpoint — governance-first, low-friction.':'A quiet contact point for selected professional exchange.',
    'Discrete. Precise. Effective.':'Quiet contact. Clear context. Careful exchange.',
    'A reduced public surface for controlled exchange, careful framing and precise follow-up.':'brgsttr.de exists to make direct, discreet and context-aware contact possible without turning every matter into public content.',
    'Discrete, precise and governance-aware communication with a reduced public surface.':'Direct, discreet and context-aware contact without turning every matter into public content.',
    'What this is':'Purpose',
    'A minimal point of contact for precise, context-aware exchange.':'A reduced contact point for selected professional, conceptual and context-sensitive exchange.',
    'What this is not':'Useful when',
    'Contact may be useful where a matter benefits from careful framing, controlled circulation,\n          precise wording, structured assessment or discreet follow-up.':'Contact may be useful where context matters, public visibility is not helpful, or a topic should be framed carefully before wider circulation.',
    'Contact may be useful where a matter benefits from careful framing, controlled circulation, precise wording, structured assessment or discreet follow-up.':'Contact may be useful where context matters, public visibility is not helpful, or a topic should be framed carefully before wider circulation.',
    'Scope':'Boundaries',
    'Minimal public surface.':'This site is intentionally limited.',
    'No tracking, no analytics, no newsletter.':'Commercial use, redistribution or public reinterpretation of shared materials requires prior permission.',
    'No embedded third-party content.':'',
    'Content reuse is governed by the notice attached to the respective material.':'',
}
for old, new in reps.items():
    s = s.replace(old, new)
write(p, s)

p = Path('about/index.html')
if p.exists():
    s = read(p)
    reps = {
        'About BRGSTTR as a reduced contact point for selective professional exchange.':'About BRGSTTR as a quiet contact point for selected professional and conceptual exchange.',
        'brgsttr.de is a reduced public surface for selective professional exchange.':'brgsttr.de is a quiet contact point for selected professional, conceptual and context-sensitive exchange.',
        'It is not a public portfolio, media profile or open archive. Its purpose is to make contact possible without unnecessary public visibility.':'It is designed for matters where discretion, clarity and careful handling are more useful than public visibility.',
        'Precision':'Clarity',
        'Exchange should reduce ambiguity, not add performance.':'Exchange should reduce ambiguity and make the relevant context easier to understand.',
        'Governance':'Careful handling'
    }
    for old, new in reps.items():
        s = s.replace(old, new)
    write(p, s)

p = Path('access/index.html')
if p.exists():
    s = read(p)
    reps = {
        'Access information for selected materials that are not publicly listed on brgsttr.de.':'Access information for materials or references that may be shared directly when context and intended use are clear.',
        'Selected materials are not publicly listed.':'Some documents or references may be shared directly when context and intended use are clear.',
        'Access may be considered where the purpose, recipient context and intended use are clear.':'Access is considered where the purpose, recipient context and intended use are clear.'
    }
    for old, new in reps.items():
        s = s.replace(old, new)
    write(p, s)

p = Path('boundaries/index.html')
if p.exists():
    s = read(p)
    reps = {
        'It provides a stable contact and context point for selective exchange. It does not function as a public archive, portfolio, newsletter, social profile or general submission platform.':'It provides a stable contact and context point for matters that benefit from discretion, clarity and careful handling. It is not intended as a public portfolio, newsletter or open archive.',
        'Contact may be appropriate where a matter benefits from careful framing, controlled circulation, precise wording, structured assessment or discreet follow-up.':'Contact may be appropriate where a matter benefits from careful wording, structured assessment, discretion or precise follow-up.',
        'This site is not designed for unsolicited mass outreach, automated scraping, redistribution of materials, commercial reuse without permission or public reinterpretation of selectively shared content.':'This site is not intended for unsolicited mass outreach, automated scraping, redistribution of materials, commercial reuse without permission or public reinterpretation of selectively shared content.',
        'Selected materials may be shared directly and are not necessarily publicly listed. Commercial use, redistribution or derivative publication requires prior written permission.':'Some materials may be shared directly when context and intended use are clear. Commercial use, redistribution or derivative publication requires prior written permission.',
        'The limited public surface is intentional. Absence of a public listing does not imply absence of material, context or prior work.':'The limited public surface is intentional. A missing public listing does not imply absence of material, context or prior work.'
    }
    for old, new in reps.items():
        s = s.replace(old, new)
    write(p, s)

p = Path('contact/index.html')
if p.exists():
    s = read(p)
    s = s.replace('Contact BRGSTTR via welcome@brgsttr.de for precise, context-aware exchange.', 'Contact BRGSTTR via welcome@brgsttr.de for discreet, precise and context-aware exchange.')
    anchor = '      ' + tag('h2') + 'Commercial permissions' + tag('h2', closing=True) + '\n'
    if 'Discrete. Precise. Effective.' not in s and anchor in s:
        block = ''.join([
            '      ', tag('h2'), 'For collaboration or concept-related exchange', tag('h2', closing=True), '\n',
            '      ', tag('div', 'class="card"'), '\n',
            '        ', tag('p'), tag('strong'), 'Discrete. Precise. Effective.', tag('strong', closing=True), tag('p', closing=True), '\n',
            '        ', tag('p', 'class="muted"'), 'Where collaboration, review or concept-related exchange begins, the aim is careful handling, clear context and practical follow-up.', tag('p', closing=True), '\n',
            '      ', tag('div', closing=True), '\n\n'
        ])
        s = s.replace(anchor, block + anchor)
    write(p, s)

p = Path('discretion/index.html')
if p.exists():
    s = read(p)
    s = s.replace('Contact should start with a clear subject, purpose and relevant context.', 'Contact should start with a clear subject, purpose and relevant context, so that the exchange can remain concise and useful.')
    write(p, s)

p = Path('notes/index.html')
if p.exists():
    s = read(p)
    s = s.replace('Short, controlled notes on communication, governance, public systems and operational clarity.', 'Short notes on communication, public systems, service clarity and careful organisational thinking.')
    s = s.replace('Short notes on communication, governance, public systems and operational clarity.', 'Short notes on communication, public systems, service clarity and careful organisational thinking.')
    write(p, s)

old_privacy = Path('privacy.html')
if old_privacy.exists():
    s = old_privacy.read_text(encoding='utf-8')
    for old, new in path_replacements.items():
        s = s.replace(old, new)
    s = s.replace('href="assets/style.css"', 'href="/assets/style.css"')
    s = s.replace('https://www.brgsttr.de/privacy.html', 'https://www.brgsttr.de/privacy/')
    s = s.replace('Last update: 2026-05-14', 'Last update: 2026-05-22')
    write('privacy/index.html', s)

    redirect = ''.join([
        tag('!doctype html'), '\n', tag('html', 'lang="en"'), '\n', tag('head'), '\n',
        '  ', tag('meta', 'charset="utf-8"'), '\n',
        '  ', tag('meta', 'name="viewport" content="width=device-width, initial-scale=1"'), '\n',
        '  ', tag('title'), 'privacy. · BRGSTTR', tag('title', closing=True), '\n',
        '  ', tag('meta', 'name="robots" content="noindex"'), '\n',
        '  ', tag('meta', 'http-equiv="refresh" content="0; url=/privacy/"'), '\n',
        '  ', tag('link', 'rel="canonical" href="https://www.brgsttr.de/privacy/"'), '\n',
        '  ', tag('link', 'rel="stylesheet" href="/assets/style.css"'), '\n',
        tag('head', closing=True), '\n', tag('body'), '\n', '  ', tag('div', 'class="wrap"'), '\n', '    ', tag('main'), '\n',
        '      ', tag('h1'), 'privacy.', tag('h1', closing=True), '\n',
        '      ', tag('p', 'class="muted"'), 'This page has moved to ', tag('a', 'href="/privacy/"'), '/privacy/', tag('a', closing=True), '.', tag('p', closing=True), '\n',
        '    ', tag('main', closing=True), '\n', '  ', tag('div', closing=True), '\n', tag('body', closing=True), '\n', tag('html', closing=True), '\n'
    ])
    write('privacy.html', redirect)

usep = Path('use.html')
if usep.exists():
    s = read(usep)
    s = s.replace('href="assets/style.css"', 'href="/assets/style.css"')
    write(usep, s)

p = Path('404.html')
if p.exists():
    s = read(p)
    s = s.replace('href="assets/style.css"', 'href="/assets/style.css"')
    for old, new in path_replacements.items():
        s = s.replace(old, new)
    write(p, s)

workflow = Path('.github/workflows/apply-brgsttr-text-refactor-260522.yml')
if workflow.exists():
    workflow.unlink()
script = Path('.github/scripts/apply_brgsttr_refactor_260522.py')
if script.exists():
    script.unlink()
