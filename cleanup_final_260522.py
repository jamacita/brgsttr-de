from pathlib import Path
p=Path('index.html')
lines=p.read_text(encoding='utf-8').splitlines()
out=[]
i=0
while i < len(lines):
    line=lines[i]
    if '<h2>Useful when</h2>' in line:
        out.append(line)
        out.append('          <p>A matter benefits from careful wording, structured assessment, discretion or precise follow-up.</p>')
        i += 1
        while i < len(lines) and '</article>' not in lines[i]:
            i += 1
        if i < len(lines):
            out.append(lines[i])
        i += 1
        continue
    if '<h2 id="scope-title">Boundaries</h2>' in line:
        out.append(line)
        out.append('        <p class="muted">This site is intentionally limited. Commercial use, redistribution or public reinterpretation of shared materials requires prior permission.</p>')
        i += 1
        while i < len(lines) and 'For details, see' not in lines[i]:
            i += 1
        continue
    out.append(line)
    i += 1
p.write_text('\n'.join(out)+'\n',encoding='utf-8')
