from wrapper import AmazonWrapper, CulturaWrapper, CompanhiaWrapper

if __name__ == '__main__':
    wrapper = CompanhiaWrapper('../data/crawled/companhiadasletras')
    wrapper.wrap()
