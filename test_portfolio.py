from portfolio import Portfolio

p = Portfolio()
p.load_portfolio()
print(p.query_links(["Python", "NLP"]))