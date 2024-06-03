# Emoji Enhancer

A simple CLI tool to enhance your text with emojis based on word2vec and emoji embeddings.

## Introduction

To help people find the best emoji and to some extent automatize the process, this tool was developed utilizing a combination of pre-trained text embeddings  [Word2Vec](https://code.google.com/archive/p/word2vec/) (2013) and emoji embeddings[Emoji2Vec](https://github.com/uclnlp/emoji2vec) (2016) to suggest the most relevant emojis.

In general, Emoji Enhancer aims to streamline the process of inserting emojis into text by analyzing the text's content and automatically suggesting relevant emojis which users can choose from. This tool is particularly useful for those who want make the text more engaging without interrupting their workflow to search for appropriate emojis.

## Installation

You can install Emoji Enhancer via [poetry](https://python-poetry.org/docs/#installation):

```bash
poetry install
```

Then download the en_core_web_lg model using spacy:

```bash
poetry run python -m spacy download en_core_web_lg
```

## Usage

Assuming you have a text that you want to add emojis to. To use the tool, simply run:

```bash
poetry run python emoji_enhancer/cli.py "YOUR TARGET TEXTS"
```

You can also decide which word class you want to add emoji to. The tool provides 4 options including nouns `-n`, verbs `-v`, adjectives `-adj` and adverbs `-adv`. If no word class is determined, the tool will try to annotate all nouns, verbs, adjectives and adverbs. You can use `--help` for specifics. For example you can run:

```bash
poetry run python emoji_enhancer/cli.py -n "My sister loves eating apple and drinking juice."
```

**Notice:** The first time you run this tool it'll take couple of minutes to download the pre-trained word2vec-google-news-300 embeddings, but after that it goes faster. You can find the gensim cache and delete the embeddings afterwards.

Then choose the emoji you want to insert or reject all the choices:

```bash
Options for apple:
1. 🍎 (0.14)
2. 🍅 (0.12)
3. 🍏 (0.10)
4. 🌰 (0.08)
5. 🥭 (0.06)
6. Reject all
Enter your choice (number): 1
```

After you finish all the choices it will return you a revised text with emojis:

```bash
Revised text: My sister👩‍👧 loves eating apple🍎 and drinking juice🧃
```

## Models

I obtained a brief understanding of the performance of the **4 methods (Word2Vec, SpaCy, FastText and GloVe)** and the **2 similarity metrix (cosine similarity and euclidean distance)** for assessing similarity on colab in script `models.ipynb` and `models.xlsx`. 

### Similarity metrix
**Cosine distance** is chosen here as similarity matrix, which is consistent with  principles and customs. 

For **euclidean distance**, we can know from the results in `model.xslx` that it have *no effect on emoji2vec*, and have *destructive effect on emojional*. And for the text-only embeddings it didn't show apparent contribution neither, and even showed negative impact on Word2Vec's performance. As a result, I didn't choose it when using emoji embeddings. 

### Text Embeddings
**Word2Vec** is apparently the best one among 4 models because its results contain the highest number of real words. 

**FastText** is based on n-gram, so the most similar tokens have overlapping letters with the original word. As we are looking into semantic similarity, it is not a good choice. 
**SpaCy** finds some pronouns frequently (something, it, I, you, what). Similar but less obvious case was found on **GloVe**.

### Emoji Embeddings

3 kind of emoji embeddings were tested here along with Word2Vec:

* emoji2vec `/model/emoji2vec.bin`
* emojional `/model/emojional.bin`
* self-generated embeddings `/model/emoji_embeddings.csv` average vectors of meanings in emoji dictionary 

### Combination

Integrating all the previous considerations, in total I tried 4 combinations:

* **cosine similarity + word2vec + emojional**
* cosine similarity + word2vec + emoji2vec
* cosine similarity + word2vec + self-generated embeddings from dictionary `emojional_dictionary.csv`
* cosine similarity + spacy + emoji dictionary `emoji2vec_dictionary.txt`

The final choice for my project is the first one, because it has the best accuracy and short running time. All other methods are saved in folder `emoji_enhancer/methods`.

## Data

* emoji dictionary from emoji2vec project `/data/emoji2vec_dictionary.txt`

* emoji dictionary from emojional project `/data/emojional_dictionary.csv`

## Test

For test, first install test:

```bash
poetry add --dev pytest
```

Run test:

```bash
poetry run pytest
```

## Discussion

In this small project I use pre-trained static embeddings. Further in the future, we can train one's own Word2Vec embeddings using cooking related data,  in conjunction with emoji embedding to produce a emoji tool specifically for recipes.

Of course, more complex contextual embeddings from LLM would be a better choice because they can find more appropriate emojis based on context and erase the polysemy problem like apple as fruit 🍎 and as a company . 

## References

Barry, E., Jameel, S., & Raza, H. (2022). Emojional: Emoji Embeddings. In T. Jansen, R. Jensen, N. Mac Parthaláin, & C. M. Lin (Eds.), *Advances in Computational Intelligence Systems. UKCI 2021. Advances in Intelligent Systems and Computing* (Vol. 1409). Springer, Cham. https://doi.org/10.1007/978-3-030-87094-2_27

Eisner, B., Rocktäschel, T., Augenstein, I., Bošnjak, M., & Riedel, S. (2016). Emoji2Vec: Learning Emoji Representations from their Description. In *Proceedings of the Fourth International Workshop on Natural Language Processing for Social Media* (pp. 48–54). Association for Computational Linguistics. https://aclanthology.org/W16-6208

GitHub-repo of emoji2vec: https://github.com/uclnlp/emoji2vec

Github-repo of emojional: https://github.com/elenabarry/emojional





