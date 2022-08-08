from wrapper import AmazonWrapper, CulturaWrapper

if __name__ == '__main__':
    wrapper = CulturaWrapper('../data/crawled/livrariacultura')
    wrapper.wrap()