# Natural  Language Processing: N-Gram Model Project

## Abstract

No matter you are building Siri, Alexa or you are implementing a auto-translate or spell check program, a language model is 
necessary to be running at the back-end. In this project, we use **Python** makefile to read privacy policy across different domains
to construct a language model using an interpolated n-gram. The formula for computing each sequence of words (unigram, bigram and trigram) is
described as below. Notice that lambda is a parameter which requires tuning. We can almost think the formula as a linear model
where the probability terms are features like X1, X2, X3, whereas the lambda are their coefficients. 

<a href="https://imgbb.com/"><img src="https://image.ibb.co/dBBGiw/Screen_Shot_2017_09_30_at_3_31_50_PM.png" alt="Screen_Shot_2017_09_30_at_3_31_50_PM" border="0"></a>

We use Laplace Add-One Smoothing method to smooth our model so that we can handle un-seen and unknown words that are outside of our
language model. This is crucial to the development of language model because unseen words are frequent in real word setting. Knowing
how to handling these unseen words allow us to build a more robus and scalable model. Notice that the capitalized C indicates the occurrence
of a word in the training data. 

<a href="https://imgbb.com/"><img src="https://image.ibb.co/f65nqb/Screen_Shot_2017_09_30_at_3_32_34_PM.png" alt="Screen_Shot_2017_09_30_at_3_32_34_PM" border="0"></a>

## Command to Use
We can use the following command line to start the project. The `time` argument is to time how long the program runs. 
The txt files should be in the same directory as the project code with each file containing processed words. Ideally, we would 
want the input file to be exactly 50 lines long. The 0.25 0.25 0.25 0.25 are value assignments to lambda0 to lambda3. These values 
need to sum to $1$. However, they can range between $0$ to $1$. The output value is $perplexity$ which is the exponentiation of the entropy
of our language model. It is an important measurement to evaluate how good a model is. The lower the perplexity, the better the model.
Notice that in the command line below, the argument `shopping.txt` is test file whereas the other 3 files are training file. 

 `time ./languagemodeler 0.25 0.25 0.25 0.25 shopping.txt news.txt games.txt health.txt sports.txt`
