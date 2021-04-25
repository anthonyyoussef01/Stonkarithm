from monkeylearn import MonkeyLearn

ml = MonkeyLearn('afa0bb36b07bdbdd058e1fb39f704f3ecb24f54a')
model_id = 'cl_Fxz8qaMc'

def sentiment_anal(data):
    result = ml.classifiers.classify(model_id, data)
    print(result.body)

    sen = 0
    for i in range(len(data)):
        print(result.body[i]['text']
              + "    " + result.body[i]['classifications'][0]['tag_name']
              + " " + str(result.body[i]['classifications'][0]['confidence']))
        if (result.body[i]['classifications'][0]['tag_name'] == "Positive"):
            sen += result.body[i]['classifications'][0]['confidence']
        elif (result.body[i]['classifications'][0]['tag_name'] == "Negative"):
            sen -= result.body[i]['classifications'][0]['confidence']
        else:
            sen /= 2
    sen /= len(data)

    print(sen)

#data = ["NIO 🚀🚀", "AMC diamond hands 💹💹", "$AAPL to the moon", "It's looking real good 👀 #GME"]
#sentiment_anal(data)