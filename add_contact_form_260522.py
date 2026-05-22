from pathlib import Path

def t(name, attrs='', close=False):
    if close:
        return chr(60) + '/' + name + chr(62)
    return chr(60) + name + ((' ' + attrs) if attrs else '') + chr(62)

def ptag(text, cls=None):
    attrs = ('class="' + cls + '"') if cls else ''
    return t('p', attrs) + text + t('p', close=True)

# contact page
contact = Path('contact/index.html')
s = contact.read_text(encoding='utf-8')
if 'id="contact-form"' not in s:
    form = []
    form.append('      ' + t('h2') + 'Contact form' + t('h2', close=True))
    form.append('      ' + t('div', 'class="card"'))
    form.append('        ' + ptag('This form prepares an email locally in your browser. It does not send data through brgsttr.de.', 'muted'))
    form.append('        ' + t('form', 'id="contact-form" class="contact-form"'))
    form.append('          ' + t('label', 'for="cf-name"') + 'Name' + t('label', close=True))
    form.append('          ' + t('input', 'id="cf-name" name="name" type="text" autocomplete="name"'))
    form.append('          ' + t('label', 'for="cf-email"') + 'Email' + t('label', close=True))
    form.append('          ' + t('input', 'id="cf-email" name="email" type="email" autocomplete="email"'))
    form.append('          ' + t('label', 'for="cf-subject"') + 'Subject' + t('label', close=True))
    form.append('          ' + t('input', 'id="cf-subject" name="subject" type="text" value="Message via brgsttr.de" required'))
    form.append('          ' + t('label', 'for="cf-message"') + 'Message' + t('label', close=True))
    form.append('          ' + t('textarea', 'id="cf-message" name="message" rows="7" required') + t('textarea', close=True))
    form.append('          ' + t('button', 'class="btn" type="submit"') + 'Prepare email' + t('button', close=True))
    form.append('          ' + t('p', 'id="cf-status" class="muted" aria-live="polite"') + t('p', close=True))
    form.append('        ' + t('form', close=True))
    form.append('        ' + t('noscript') + ptag('JavaScript is disabled. Please use the direct email link above.', 'muted') + t('noscript', close=True))
    form.append('      ' + t('div', close=True))
    script = []
    script.append('      ' + t('script'))
    script.append("      (function () {")
    script.append("        var form = document.getElementById('contact-form');")
    script.append("        if (!form) return;")
    script.append("        form.addEventListener('submit', function (event) {")
    script.append("          event.preventDefault();")
    script.append("          var name = document.getElementById('cf-name').value.trim();")
    script.append("          var email = document.getElementById('cf-email').value.trim();")
    script.append("          var subject = document.getElementById('cf-subject').value.trim() || 'Message via brgsttr.de';")
    script.append("          var message = document.getElementById('cf-message').value.trim();")
    script.append("          var body = [];")
    script.append("          if (name) body.push('Name: ' + name);")
    script.append("          if (email) body.push('Email: ' + email);")
    script.append("          if (name || email) body.push('');")
    script.append("          body.push(message);")
    script.append("          var url = 'mailto:welcome@brgsttr.de?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body.join('\\n'));")
    script.append("          window.location.href = url;")
    script.append("          var status = document.getElementById('cf-status');")
    script.append("          if (status) status.textContent = 'Your email app should now open. Please review and send the message there.';")
    script.append("        });")
    script.append("      }());")
    script.append('      ' + t('script', close=True))
    block = '\n'.join(form + [''] + script) + '\n\n'
    marker = '      ' + t('h2') + 'For collaboration or concept-related exchange' + t('h2', close=True)
    s = s.replace(marker, block + marker)
    contact.write_text(s, encoding='utf-8')

# privacy page
privacy = Path('privacy/index.html')
s = privacy.read_text(encoding='utf-8')
s = s.replace('content="privacy. information for brgsttr.de: no cookies, no analytics, no embedded third-party content."', 'content="Privacy information for brgsttr.de: no cookies, no analytics, no embedded third-party content; local email helper on the contact page."')
s = s.replace('This website is intentionally minimal. It does not use analytics, tracking pixels, cookies, forms or embedded third-party content.', 'This website is intentionally minimal. It does not use analytics, tracking pixels, cookies or embedded third-party content. The contact page includes a local email helper form that runs in your browser and opens your email app; it does not submit data to brgsttr.de.')
s = s.replace('No newsletter, comments or public submission forms are provided.', 'No newsletter, comments or server-side public submission forms are provided.')
s = s.replace('<h2>contact. via email</h2>', '<h2>Contact via email and local helper form</h2>')
s = s.replace('If you send an email to welcome@brgsttr.de, the content of your message and your contact details are processed for handling the inquiry and any follow-up communication.\n        Processing occurs via the involved email providers.', 'If you send an email to welcome@brgsttr.de, the content of your message and your contact details are processed for handling the inquiry and any follow-up communication. The contact helper form on this site prepares such an email locally in your browser; data is only transmitted if you review and send the email through your own email application. Processing then occurs via the involved email providers.')
privacy.write_text(s, encoding='utf-8')

# stylesheet
css_path = Path('assets/style.css')
css = css_path.read_text(encoding='utf-8')
if '.contact-form' not in css:
    addition = '''\n.contact-form {\n  display: grid;\n  gap: 10px;\n  max-width: var(--measure);\n}\n\n.contact-form label {\n  color: var(--muted);\n  font-size: 13px;\n}\n\n.contact-form input,\n.contact-form textarea {\n  width: 100%;\n  padding: 10px 12px;\n  border-radius: 10px;\n  border: 1px solid var(--line);\n  background: var(--bg);\n  color: var(--fg);\n  font: inherit;\n}\n\n.contact-form textarea {\n  resize: vertical;\n  min-height: 140px;\n}\n\n.contact-form button {\n  justify-self: start;\n  background: transparent;\n  color: var(--fg);\n  cursor: pointer;\n}\n'''
    css = css.replace('\nfooter {', addition + '\nfooter {')
    css_path.write_text(css, encoding='utf-8')

# remove helper after run if present
for f in ['add_contact_form_260522.py', '.github/workflows/add-contact-form-260522.yml', 'trigger_contact_form_260522.txt']:
    q = Path(f)
    if q.exists():
        q.unlink()
