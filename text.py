import re
import string


def remove_punctuation(s, all_but=['$', '\'', '@'], replace_with=' '):
    """Removes punctuation, except those in `all_but` (default: $, ', @), replacing with single
    space (default).
    """
    punc_chars = '[!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~]'
    rm_chars = punc_chars
    for char in all_but:
        rm_chars = rm_chars.replace(char, '')
    return re.sub(rm_chars, replace_with, s)


def separate_punctuation(s, all_but=['\''], sep=' '):
    """Separates, but does not remove punctuation, with whitespace (single space by default)."""
    punc_chars = '[!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~]'
    sep_chars = punc_chars
    for char in all_but:
        sep_chars = sep_chars.replace(char, '')
    remaining = s
    processed = []
    while remaining:
        groups = re.findall(re.compile('(.*?)(' + sep_chars + ')(.*)', re.DOTALL), remaining)
        if groups:
            groups = groups[0]
            processed.extend([groups[0].strip(), groups[1].strip()])
            remaining = groups[2].strip()
        else:
            processed.append(remaining.strip())
            remaining = ''
        
    return sep.join(processed)


def remove_numbers(s):
    """Removes numbers, including times."""
    return re.sub('\d+(:\d*)*(\.\d*)?', ' ', s)


def remove_tags(s):
    """Removes xml-style tags."""
    return re.sub('</*.*?>', '', s)


def separate_text_code(s, sep=' ', remove_tags=True):
    """Separate text blocks from code blocks. Does not remove inline code, but does remove <code>
    tags by default.
    """
    remaining = s
    text_groups = []
    code_groups = []
    while remaining:
        groups = re.findall(re.compile('(.*?)(<code>)(.*?)(</code>)(.*)', re.DOTALL), remaining)
        if groups:
            groups = groups[0]
            text = groups[0]
            code = groups[2]
            remaining = groups[4]
            if '\n' in code:
                text_groups.append(text)
                code_groups.append(code)
            else:
                if not remove_tags:
                    code = groups[1] + code + groups[3]
                text_groups.extend([text, code])
        else:
            text_groups.append(remaining)
            remaining = ''
    return sep.join(text_groups), sep.join(code_groups)


def clean_text(s, rm_tags=True, rm_numbers=False, rm_punc=False, sep_punc=True, lower=True):
    """Return cleaned and separated text terms and symbols. Tags, numbers, punctuation can be
    optionally removed.
    """
    if rm_tags:
        s = remove_tags(s)
    if rm_numbers:
        s = remove_numbers(s)
    if rm_punctuation:
        s = remove_punctuation(s)
    if sep_punctuation:
        s = separate_punctuation(s)
    s = re.sub('\s+', ' ', s.lower()).strip()
    return s


def get_code(s):
    """Returns code terms with compressed whitespace."""
    _, code = separate_text_code(s)
    return re.sub('\s+', ' ', code).strip()


def get_tags(s, unique=False):
    """Return list of xml-style tags (optionally unique), terms only (e.g., html from </html>)."""
    tags = [t[1] for t in re.findall('(</)(.*?)(>)', s)]
    if unique:
        return list(set(tags))
    else:
        return tags
