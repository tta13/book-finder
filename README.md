# book-finder
Search engine and information retrieval tool for books

## Group
* [Amanda Soares de Castro Moraes](https://github.com/amandascm/)
* [Luís Eduardo Martins Alves](https://github.com/Luis-Alves2)
* [Tales Tomaz Alves](https://github.com/tta13)

## Milestones

- [Crawler](/crawler/)
- [Classifier](/classifier/)
- [Wrapper](/wrapper/)
- [Crawled data](/data/crawled/)
- [Extracted data](/data/wrapped/)
- [Slides I](https://docs.google.com/presentation/d/1oatbT9H2xB26mJvtc81HOb7a5bKktGGPeio9vy2M3P4/view?usp=sharing)
- [Video I](https://drive.google.com/file/d/1jE_3_5hpdxuBUR-ympyQzNhP1HXir0Gf/view?usp=sharing)
- [Inverted Index](/data/inverted-index/)
- [Query response composition](/search_engine/gui/)
- [Slides II](https://docs.google.com/presentation/d/1A99vLJuXnCeUq5nR6NCyVuH1trXh5y6sXhDMa_yERb4/view?usp=sharing)


## Dev environment and code execution

Commands to run the search engine code:

```bash
# Create Python venv
python -m venv .venv

# Activate venv
# Windows
.venv\Scripts\activate
# Linux
source .venv/bin/activate

# Install dependencies and local package
pip install -r requirements

pip install -e .
```

To run the Book Finder app and test it locally with your own queries do:

```bash
cd search_engine
cd gui
python index.py
```