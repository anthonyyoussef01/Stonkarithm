from monkeylearn import MonkeyLearn

ml = MonkeyLearn('afa0bb36b07bdbdd058e1fb39f704f3ecb24f54a')
data = ['AMC to the moon!', 'Watch out for the dip!! $AAPL',
        "I'm selling a small position in $AMC", "Just bought 10,00 position in $GME"]
model_id = 'cl_Fxz8qaMc'
result = ml.classifiers.classify(model_id, data)

print(result.body)

for i in range(4):
    print(result.body[i]['text']
          + "    " + result.body[i]['classifications'][0]['tag_name']
          + " " + str(result.body[i]['classifications'][0]['confidence']))