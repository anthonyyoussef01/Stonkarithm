
def generate_wordcloud(text, stopwords=None, mask=None):
    """Generate Word Cloud"""

    from PIL import Image
    import numpy as np
    from wordcloud import WordCloud

    mask_object = None
    if mask != None:
        mask_object = np.array(Image.open(mask))

    wordcloud = WordCloud(width=1200, height=600, stopwords=stopwords, max_font_size=200, mask=mask_object,
                          background_color='white', colormap='viridis')
    wordcloud = wordcloud.generate(' '.join(text))
    # Display the generated image:
    # the matplotlib way:
    import matplotlib.pyplot as plt
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()