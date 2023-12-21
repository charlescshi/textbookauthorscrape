from scholarly import scholarly
import pandas as pd

continuation = 0

def get_link_from_author(author_name):
    search_query = scholarly.search_author(author_name)
    author = ''
    lastresortauthor = ''
    for suggest_author in search_query:
        search_terms = ['econo', 'finance', 'asset', 'behavior', 'sociology', 'invest', 'economics',
                        'experimental economics', 'decision', 'pscyhology', 'charitable', 'charity',
                        'gender', 'artefactual', 'lab-in-the-field']
        if not suggest_author['interests']: ## author did not list interests on google scholar
            lastresortauthor = suggest_author
        if any(s in [x.lower() for x in suggest_author['interests']] for s in search_terms):
            author = scholarly.fill(suggest_author)
            break
    if author == '' and lastresortauthor != '':
        author = scholarly.fill(lastresortauthor)

    lastresort = ''
    if author != '':
        for pub in author['publications']:
            abstract = ''
            try:
                abstract = scholarly.fill(pub)['bib']['abstract']
            except:
                lastresort = str(pub['bib']['title'])
                continue
            if 'experiment' in abstract:
                if 'pub_url' in pub.keys():
                    return pub['pub_url']
                elif 'eprint_url' in pub.keys():
                    return pub['eprint_url']
                else:
                    lastresort = str(pub['bib']['title'])

    if lastresort != '':  ## if we found a paper with 'experiment' but can't find a link...
        return 'NO LINK FOUND, PAPER: ' + lastresort
    else:
        return 'NO PAPER FOUND'


df = pd.read_csv('authors.csv')
for ind in df.index:
    if ind < continuation:
        continue
    print(ind)
    link = get_link_from_author(df['Full Name'][ind])
    df['Link To Paper'][ind] = link
    if ind % 50 == 0:
        df.to_csv('authors_upd_partial.csv', encoding='utf-8')
df.to_csv('authors_upd.csv', encoding='utf-8')
