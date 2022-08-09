from wrapper import AmazonWrapper, CulturaWrapper, CompanhiaWrapper, EstanteWrapper

if __name__ == '__main__':
    wrapper = EstanteWrapper('../data/crawled/estantevirtual')
    wrapper.wrap()
