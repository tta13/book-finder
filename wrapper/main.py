from wrapper import AmazonWrapper

if __name__ == '__main__':
    wrapper = AmazonWrapper('../data/crawled/amazon')
    wrapper.wrap()